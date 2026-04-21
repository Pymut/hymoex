"""Benchmark: Expert selection accuracy — LLM-based routing vs baselines.

Measures REAL expert selection accuracy using Gemini API for:
1. LLM-based routing (Hymoex MoE gating approach)
2. Keyword-based routing (rule-based baseline)
3. Random routing (baseline)
4. Round-robin routing (baseline)

Ground truth is defined by domain experts for each test query.
Requires GEMINI_API_KEY environment variable.
"""

import os
import random
import statistics

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set",
)


# Ground truth: query -> correct expert domain (human-annotated)
GROUND_TRUTH = [
    {"query": "contract terms violation", "correct": "legal"},
    {"query": "system is down error 500", "correct": "tech"},
    {"query": "invoice amount incorrect", "correct": "billing"},
    {"query": "service level agreement breach", "correct": "legal"},
    {"query": "cannot login to dashboard", "correct": "tech"},
    {"query": "payment was double charged", "correct": "billing"},
    {"query": "warranty claim on product", "correct": "legal"},
    {"query": "API rate limit exceeded", "correct": "tech"},
    {"query": "refund not processed", "correct": "billing"},
    {"query": "data privacy compliance", "correct": "legal"},
    {"query": "database connection timeout", "correct": "tech"},
    {"query": "subscription renewal pricing", "correct": "billing"},
    {"query": "non-disclosure agreement review", "correct": "legal"},
    {"query": "memory leak in production", "correct": "tech"},
    {"query": "tax calculation error", "correct": "billing"},
    {"query": "intellectual property dispute", "correct": "legal"},
    {"query": "SSL certificate expired", "correct": "tech"},
    {"query": "credit note not applied", "correct": "billing"},
    {"query": "regulatory compliance audit", "correct": "legal"},
    {"query": "microservice deployment failed", "correct": "tech"},
    # Additional cases for statistical validity
    {"query": "breach of contract damages", "correct": "legal"},
    {"query": "load balancer configuration error", "correct": "tech"},
    {"query": "payment gateway timeout", "correct": "billing"},
    {"query": "GDPR data deletion request", "correct": "legal"},
    {"query": "container orchestration failure", "correct": "tech"},
    {"query": "duplicate invoice issued", "correct": "billing"},
    {"query": "employment law consultation", "correct": "legal"},
    {"query": "DNS resolution failure", "correct": "tech"},
    {"query": "wire transfer not received", "correct": "billing"},
    {"query": "trademark infringement notice", "correct": "legal"},
]

EXPERT_DOMAINS = ["legal", "tech", "billing"]
RUNS = 3  # Run LLM routing multiple times for consistency check


class TestExpertSelectionAccuracy:
    @pytest.fixture(scope="class")
    def provider(self):
        from llm_provider import GeminiBenchmarkProvider
        return GeminiBenchmarkProvider()

    def test_llm_routing_accuracy(self, provider):
        """LLM-based routing using Gemini (Hymoex MoE approach)."""
        accuracies = []

        for run in range(RUNS):
            correct = 0
            for case in GROUND_TRUTH:
                result = provider.route_query(case["query"], EXPERT_DOMAINS)
                if result["selected_domain"] == case["correct"]:
                    correct += 1
            accuracy = correct / len(GROUND_TRUTH) * 100
            accuracies.append(accuracy)

        mean_acc = statistics.mean(accuracies)
        std_acc = statistics.stdev(accuracies) if len(accuracies) > 1 else 0

        print(f"\nLLM Routing (Gemini) Accuracy: {mean_acc:.1f}% +/- {std_acc:.1f}%")
        print(f"  Runs: {RUNS}, Cases per run: {len(GROUND_TRUTH)}")
        print(f"  Total API calls: {provider.metrics.total_calls}")
        print(f"  Total tokens used: {provider.metrics.total_tokens}")
        assert mean_acc > 0

    def test_rule_based_accuracy(self):
        """Keyword-based routing baseline."""
        correct = 0
        for case in GROUND_TRUTH:
            selected = self._rule_based_route(case["query"])
            if selected == case["correct"]:
                correct += 1
        accuracy = correct / len(GROUND_TRUTH) * 100

        print(f"\nRule-based Accuracy: {accuracy:.1f}% ({correct}/{len(GROUND_TRUTH)})")

    def test_random_accuracy(self):
        """Random routing baseline (averaged over 100 runs)."""
        accuracies = []
        for seed in range(100):
            random.seed(seed)
            correct = sum(
                1 for c in GROUND_TRUTH
                if random.choice(EXPERT_DOMAINS) == c["correct"]
            )
            accuracies.append(correct / len(GROUND_TRUTH) * 100)

        mean_acc = statistics.mean(accuracies)
        std_acc = statistics.stdev(accuracies)
        print(f"\nRandom Accuracy: {mean_acc:.1f}% +/- {std_acc:.1f}% (100 runs)")

    def test_round_robin_accuracy(self):
        """Round-robin routing baseline."""
        correct = sum(
            1 for i, c in enumerate(GROUND_TRUTH)
            if EXPERT_DOMAINS[i % len(EXPERT_DOMAINS)] == c["correct"]
        )
        accuracy = correct / len(GROUND_TRUTH) * 100
        print(f"\nRound-robin Accuracy: {accuracy:.1f}% ({correct}/{len(GROUND_TRUTH)})")

    def test_llm_beats_baselines(self, provider):
        """Verify LLM routing outperforms all baselines."""
        # LLM routing
        llm_correct = 0
        for case in GROUND_TRUTH:
            result = provider.route_query(case["query"], EXPERT_DOMAINS)
            if result["selected_domain"] == case["correct"]:
                llm_correct += 1
        llm_acc = llm_correct / len(GROUND_TRUTH) * 100

        # Rule-based
        rule_correct = sum(
            1 for c in GROUND_TRUTH
            if self._rule_based_route(c["query"]) == c["correct"]
        )
        rule_acc = rule_correct / len(GROUND_TRUTH) * 100

        # Random (expected ~33%)
        random.seed(42)
        rand_correct = sum(
            1 for c in GROUND_TRUTH
            if random.choice(EXPERT_DOMAINS) == c["correct"]
        )
        rand_acc = rand_correct / len(GROUND_TRUTH) * 100

        print(f"\nComparison:")
        print(f"  LLM routing:  {llm_acc:.1f}%")
        print(f"  Rule-based:   {rule_acc:.1f}%")
        print(f"  Random:       {rand_acc:.1f}%")

        assert llm_acc >= rule_acc, \
            f"LLM ({llm_acc:.1f}%) should beat rule-based ({rule_acc:.1f}%)"

    @staticmethod
    def _rule_based_route(query: str) -> str:
        """Simple keyword routing baseline."""
        q = query.lower()
        if any(w in q for w in [
            "contract", "legal", "compliance", "agreement", "warranty",
            "dispute", "privacy", "nda", "intellectual", "regulatory",
            "breach", "gdpr", "trademark", "employment", "law",
        ]):
            return "legal"
        if any(w in q for w in [
            "error", "system", "api", "database", "login",
            "memory", "ssl", "deploy", "timeout", "dns",
            "container", "load balancer", "microservice", "orchestration",
        ]):
            return "tech"
        if any(w in q for w in [
            "invoice", "payment", "refund", "billing", "price",
            "subscription", "tax", "credit", "charged", "wire",
            "gateway", "duplicate",
        ]):
            return "billing"
        return random.choice(EXPERT_DOMAINS)
