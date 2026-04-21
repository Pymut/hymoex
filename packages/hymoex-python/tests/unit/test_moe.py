"""Tests for MoE algorithms — gating and fusion."""

from hymoex import SignalVector, GatingConfig, softmax_gate, top_k_select, compute_raffle_score


class TestSoftmaxGate:
    def test_sums_to_one(self):
        signal = SignalVector(intent_embedding=[1.0, 0.5], lead_score=0.8)
        weights = {"a": [0.5, 0.3, 0.0, 0.0], "b": [0.2, 0.7, 0.0, 0.0]}
        result = softmax_gate(signal, weights)
        assert abs(sum(result.values()) - 1.0) < 1e-6

    def test_uniform_weights(self):
        signal = SignalVector(intent_embedding=[1.0], lead_score=0.5)
        weights = {"a": [0.0, 0.0], "b": [0.0, 0.0]}
        result = softmax_gate(signal, weights)
        assert abs(result["a"] - 0.5) < 1e-6

    def test_extreme_weights(self):
        signal = SignalVector(intent_embedding=[1.0], lead_score=0.5)
        weights = {"strong": [10.0, 10.0], "weak": [0.0, 0.0]}
        result = softmax_gate(signal, weights)
        assert result["strong"] > 0.99

    def test_temperature(self):
        signal = SignalVector(intent_embedding=[1.0], lead_score=0.5)
        weights = {"a": [1.0, 0.5], "b": [0.5, 0.3]}
        sharp = softmax_gate(signal, weights, config=GatingConfig(temperature=0.1))
        flat = softmax_gate(signal, weights, config=GatingConfig(temperature=10.0))
        assert max(sharp.values()) > max(flat.values())


class TestTopKSelect:
    def test_selects_top(self):
        scores = {"a": 0.5, "b": 0.3, "c": 0.15, "d": 0.05}
        result = top_k_select(scores, 2)
        assert len(result) == 2
        assert result[0][0] == "a"

    def test_k_larger_than_pool(self):
        scores = {"a": 0.7, "b": 0.3}
        result = top_k_select(scores, 5)
        assert len(result) == 2


class TestRaffleScore:
    def test_basic(self):
        assert compute_raffle_score(0.5, 0.8, 0.9) == 0.5 * 0.8 * 0.9

    def test_zero(self):
        assert compute_raffle_score(0.0, 1.0, 1.0) == 0.0
