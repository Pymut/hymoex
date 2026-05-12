"""Benchmark: Scalability — coordination overhead at increasing agent counts.

Measures REAL token consumption and latency as agent count scales from 2 to 10+,
comparing flat vs hierarchical topologies.

Requires GEMINI_API_KEY environment variable.
"""

import os
import statistics

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set",
)

TASK = "Process a customer onboarding request: verify identity, generate contract, set up payment, and schedule orientation call"

SCALE_CONFIGS = [
    (2, ["legal", "tech"]),
    (5, ["legal", "tech", "billing", "hr", "compliance"]),
    (10, ["legal", "tech", "billing", "hr", "compliance",
          "contracts", "payments", "scheduling", "identity", "support"]),
]

RUNS_PER_CONFIG = 2


class TestScalability:
    """Measure how token overhead scales with agent count across topologies."""

    @pytest.fixture(scope="class")
    def provider(self):
        from llm_provider import GeminiBenchmarkProvider
        return GeminiBenchmarkProvider()

    def test_flat_scalability(self, provider):
        """Flat MAS token overhead at 2, 5, 10 agents."""
        results = {}

        for n_agents, domains in SCALE_CONFIGS:
            token_counts = []
            for _ in range(RUNS_PER_CONFIG):
                result = provider.coordinate_agents(TASK, domains, topology="flat")
                token_counts.append(result["total_tokens"])

            mean_tokens = statistics.mean(token_counts)
            results[n_agents] = mean_tokens
            print(f"\nFlat MAS @ {n_agents} agents: {mean_tokens:.0f} tokens/task")

        # Check degradation
        if 2 in results and 10 in results:
            degradation = ((results[10] - results[2]) / results[2]) * 100
            print(f"\nFlat MAS degradation (2->10 agents): {degradation:.1f}%")

    def test_hierarchical_scalability(self, provider):
        """Hymoex hierarchical token overhead at 2, 5, 10 agents."""
        results = {}

        for n_agents, domains in SCALE_CONFIGS:
            token_counts = []
            for _ in range(RUNS_PER_CONFIG):
                result = provider.coordinate_agents(TASK, domains, topology="hierarchical")
                token_counts.append(result["total_tokens"])

            mean_tokens = statistics.mean(token_counts)
            results[n_agents] = mean_tokens
            print(f"\nHymoex Hierarchical @ {n_agents} agents: {mean_tokens:.0f} tokens/task")

        if 2 in results and 10 in results:
            degradation = ((results[10] - results[2]) / results[2]) * 100
            print(f"\nHierarchical degradation (2->10 agents): {degradation:.1f}%")

    def test_scaling_comparison(self, provider):
        """Compare scaling behavior: flat should degrade much more than hierarchical."""
        # Use the largest config
        n_agents, domains = SCALE_CONFIGS[-1]

        flat = provider.coordinate_agents(TASK, domains, topology="flat")
        hierarchical = provider.coordinate_agents(TASK, domains, topology="hierarchical")

        print(f"\nAt {n_agents} agents:")
        print(f"  Flat:         {flat['total_tokens']} tokens, {flat['total_calls']} calls")
        print(f"  Hierarchical: {hierarchical['total_tokens']} tokens, {hierarchical['total_calls']} calls")
        print(f"  Token reduction: {(1 - hierarchical['total_tokens'] / flat['total_tokens']) * 100:.0f}%")
        print(f"  Call reduction:  {(1 - hierarchical['total_calls'] / flat['total_calls']) * 100:.0f}%")

        assert hierarchical["total_tokens"] < flat["total_tokens"], \
            "Hierarchical should use fewer tokens at scale"
