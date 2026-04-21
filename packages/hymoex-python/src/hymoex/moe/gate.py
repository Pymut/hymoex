"""MoE gating mechanism — softmax gate, top-k selection, dynamic temperature.

Implements Algorithm 1 from the paper (Section 5.3).
Pure Python, no numpy dependency.
"""

import math
from typing import Any

from pydantic import BaseModel

from hymoex.messaging.types import DecisionRequest
from hymoex.protocols.base import GatingResult, SignalVector

__all__ = [
    "GatingConfig",
    "compute_signal_vector",
    "compute_signal_vector_with_llm",
    "softmax_gate",
    "top_k_select",
    "apply_dynamic_temperature",
    "gate_experts",
]


class GatingConfig(BaseModel):
    """Configuration for the MoE gating mechanism."""

    temperature: float = 1.0
    top_k: int = 2
    low_temperature: float = 0.5
    sla_threshold_ms: float = 500.0


def compute_signal_vector(request: DecisionRequest) -> SignalVector:
    """Extract signal vector from a DecisionRequest (stage 1 of pipeline)."""
    return SignalVector(
        intent_embedding=request.intent_embedding,
        emotion_embedding=request.emotion_vector,
        stage_flag=request.stage_flag,
        lead_score=request.lead_score,
    )


async def compute_signal_vector_with_llm(
    request: DecisionRequest,
    llm: Any,
) -> SignalVector:
    """Extract signal vector using LLM embeddings for intent detection.

    Uses the provider's embed() method to generate real intent embeddings
    from the message payload, replacing hardcoded vectors.
    """
    payload = ""
    if request.context and request.context.msg_packet:
        payload = request.context.msg_packet.payload

    intent_embedding = await llm.embed(payload) if payload else []

    return SignalVector(
        intent_embedding=intent_embedding or request.intent_embedding,
        emotion_embedding=request.emotion_vector,
        stage_flag=request.stage_flag,
        lead_score=request.lead_score,
    )


def _dot_product(a: list[float], b: list[float]) -> float:
    """Compute dot product of two vectors."""
    return sum(x * y for x, y in zip(a, b, strict=False))


def softmax_gate(
    signal: SignalVector,
    expert_weights: dict[str, list[float]],
    expert_biases: dict[str, float] | None = None,
    config: GatingConfig | None = None,
) -> dict[str, float]:
    """Compute gating probabilities via softmax (stage 2 of pipeline).

    g(s) = softmax(Ws + b) ∈ Δ^{K-1}

    Args:
        signal: The composite signal vector.
        expert_weights: Dict mapping expert_id to weight vector w_i.
        expert_biases: Optional dict mapping expert_id to bias b_i.
        config: Gating configuration (temperature).

    Returns:
        Dict mapping expert_id to selection probability α_i.
    """
    if config is None:
        config = GatingConfig()
    if expert_biases is None:
        expert_biases = {}

    s = signal.to_vector()
    temperature = config.temperature

    logits: dict[str, float] = {}
    for expert_id, w in expert_weights.items():
        if len(w) != len(s):
            padded_w = w[:len(s)] if len(w) > len(s) else w + [0.0] * (len(s) - len(w))
        else:
            padded_w = w
        bias = expert_biases.get(expert_id, 0.0)
        logits[expert_id] = _dot_product(padded_w, s) + bias

    # Apply temperature scaling
    if temperature != 1.0 and temperature > 0:
        logits = {k: v / temperature for k, v in logits.items()}

    # Softmax with numerical stability
    max_logit = max(logits.values()) if logits else 0.0
    exp_logits = {k: math.exp(v - max_logit) for k, v in logits.items()}
    total = sum(exp_logits.values())

    if total < 1e-300:
        n = len(exp_logits)
        return {k: 1.0 / n for k in exp_logits} if n > 0 else {}

    return {k: v / total for k, v in exp_logits.items()}


def top_k_select(scores: dict[str, float], k: int) -> list[tuple[str, float]]:
    """Select top-k experts by gating score (stage 3 of pipeline).

    Returns:
        List of (expert_id, weight) tuples, sorted descending.
    """
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:k]


def apply_dynamic_temperature(config: GatingConfig, sla_budget_remaining: float) -> float:
    """Compute effective temperature based on SLA budget (Section 5.3).

    T_eff = T_base if budget >= threshold, else T_low
    """
    if sla_budget_remaining < config.sla_threshold_ms:
        return config.low_temperature
    return config.temperature


def gate_experts(
    request: DecisionRequest,
    expert_weights: dict[str, list[float]],
    expert_biases: dict[str, float] | None = None,
    config: GatingConfig | None = None,
    sla_budget: float | None = None,
) -> GatingResult:
    """Full gating pipeline: signal extraction → scoring → top-k selection.

    This is the convenience function combining stages 1-3 of Algorithm 1.
    """
    if config is None:
        config = GatingConfig()

    # Dynamic temperature adjustment
    if sla_budget is not None:
        config = config.model_copy(
            update={"temperature": apply_dynamic_temperature(config, sla_budget)}
        )

    signal = compute_signal_vector(request)
    scores = softmax_gate(signal, expert_weights, expert_biases, config)
    selected = top_k_select(scores, config.top_k)

    return GatingResult(
        selected_experts=[eid for eid, _ in selected],
        weights={eid: w for eid, w in selected},
    )
