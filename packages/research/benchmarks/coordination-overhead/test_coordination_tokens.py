"""Benchmark: Coordination token overhead across topologies.

Measures REAL token consumption via Gemini API across three coordination
topologies: Flat MAS (all-to-all), Single Supervisor (hub-spoke), and
Hymoex Hierarchical (MoE-gated top-k routing).

Requires GEMINI_API_KEY environment variable.
"""

import os
import statistics

import pytest

# Allow running without API key (skip gracefully)
pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set",
)


TASK_SUITE = [
    "I need help with my invoice, it doesn't match the contract terms we agreed on",
    "Our API is returning 500 errors and the SLA deadline is in 2 hours",
    "I want to dispute a charge on my last billing statement and need legal review",
    "The database migration failed and we need to roll back the payment system",
    "Can you review our service agreement and process the outstanding refund?",
]

EXPERT_DOMAINS = ["legal", "tech", "billing"]
RUNS_PER_TASK = 3  # Multiple runs for statistical validity


class TestCoordinationOverhead:
    """Compare real token consumption across topologies."""

    @pytest.fixture(scope="class")
    def provider(self):
        from llm_provider import GeminiBenchmarkProvider
        return GeminiBenchmarkProvider()

    def test_flat_mas_token_overhead(self, provider):
        """Flat MAS: every agent sees every message -> O(n^2) communication."""
        token_counts = []

        for task in TASK_SUITE:
            for _ in range(RUNS_PER_TASK):
                result = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="flat")
                token_counts.append(result["total_tokens"])

        mean_tokens = statistics.mean(token_counts)
        std_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0

        print(f"\nFlat MAS ({len(EXPERT_DOMAINS)} agents):")
        print(f"  Mean tokens/task: {mean_tokens:.0f} +/- {std_tokens:.0f}")
        print(f"  Total API calls per task: {result['total_calls']}")
        print(f"  Avg latency: {result['avg_latency_ms']:.0f}ms")
        assert mean_tokens > 0

    def test_single_supervisor_overhead(self, provider):
        """Single Supervisor: hub-and-spoke -> O(2n) communication."""
        token_counts = []

        for task in TASK_SUITE:
            for _ in range(RUNS_PER_TASK):
                result = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="supervisor")
                token_counts.append(result["total_tokens"])

        mean_tokens = statistics.mean(token_counts)
        std_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0

        print(f"\nSingle Supervisor ({len(EXPERT_DOMAINS)} experts + 1 supervisor):")
        print(f"  Mean tokens/task: {mean_tokens:.0f} +/- {std_tokens:.0f}")
        print(f"  Total API calls per task: {result['total_calls']}")
        print(f"  Avg latency: {result['avg_latency_ms']:.0f}ms")
        assert mean_tokens > 0

    def test_hymoex_hierarchical_overhead(self, provider):
        """Hymoex hierarchical: MoE gating routes to top-k experts only."""
        token_counts = []

        for task in TASK_SUITE:
            for _ in range(RUNS_PER_TASK):
                result = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="hierarchical")
                token_counts.append(result["total_tokens"])

        mean_tokens = statistics.mean(token_counts)
        std_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0

        print(f"\nHymoex Hierarchical (top-k gating):")
        print(f"  Mean tokens/task: {mean_tokens:.0f} +/- {std_tokens:.0f}")
        print(f"  Selected experts: {result.get('selected_experts', 'N/A')}")
        print(f"  Total API calls per task: {result['total_calls']}")
        print(f"  Avg latency: {result['avg_latency_ms']:.0f}ms")
        assert mean_tokens > 0

    def test_hierarchical_reduces_overhead(self, provider):
        """Key claim: hierarchical routing uses fewer tokens than flat."""
        # Run one task through each topology
        task = TASK_SUITE[0]

        flat = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="flat")
        supervisor = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="supervisor")
        hierarchical = provider.coordinate_agents(task, EXPERT_DOMAINS, topology="hierarchical")

        print(f"\nToken comparison (single task):")
        print(f"  Flat MAS:     {flat['total_tokens']} tokens ({flat['total_calls']} calls)")
        print(f"  Supervisor:   {supervisor['total_tokens']} tokens ({supervisor['total_calls']} calls)")
        print(f"  Hierarchical: {hierarchical['total_tokens']} tokens ({hierarchical['total_calls']} calls)")

        reduction_vs_flat = (1 - hierarchical["total_tokens"] / flat["total_tokens"]) * 100
        print(f"  Reduction vs flat: {reduction_vs_flat:.0f}%")

        assert hierarchical["total_tokens"] < flat["total_tokens"], \
            f"Hierarchical ({hierarchical['total_tokens']}) should use fewer tokens than flat ({flat['total_tokens']})"
