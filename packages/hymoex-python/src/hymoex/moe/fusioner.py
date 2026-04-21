"""Rational-Raffle fusion mechanism for merging expert responses.

Implements the fusion strategy from Section 5.3 (Equation 5):
    score(r_i) = α_i · relevance(r_i, m) · confidence(r_i)
"""

import hashlib
import json

from pydantic import BaseModel, Field

from hymoex.messaging.types import DecisionRequest, ExpertPayload

__all__ = [
    "FusionConfig",
    "RationalRaffleResult",
    "compute_raffle_score",
    "rational_raffle",
]


class FusionConfig(BaseModel):
    """Configuration for Rational-Raffle fusion."""

    threshold: float = 0.3


class RationalRaffleResult(BaseModel):
    """Result of the Rational-Raffle fusion process."""

    base_response: ExpertPayload
    augmented_content: list[str] = Field(default_factory=list)
    reason_vector_hash: str = ""
    scores: dict[str, float] = Field(default_factory=dict)

    @property
    def fused_reply(self) -> str:
        """Return the combined reply from base response and augmented content."""
        parts = [self.base_response.reply_draft]
        parts.extend(self.augmented_content)
        return " ".join(parts)


def _jaccard_similarity(text_a: str, text_b: str) -> float:
    """Compute Jaccard similarity between two texts (MVP relevance proxy)."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


def compute_raffle_score(alpha: float, relevance: float, confidence: float) -> float:
    """Compute the Rational-Raffle score for an expert response.

    score(r_i) = α_i · relevance(r_i, m) · confidence(r_i)
    """
    return alpha * relevance * confidence


def rational_raffle(
    responses: list[tuple[ExpertPayload, float]],
    request: DecisionRequest,
    config: FusionConfig | None = None,
) -> RationalRaffleResult:
    """Fuse multiple expert responses using the Rational-Raffle mechanism.

    Args:
        responses: List of (expert_payload, gating_alpha) tuples.
        request: The original decision request (for relevance computation).
        config: Fusion configuration.

    Returns:
        RationalRaffleResult with the fused response and audit trail.
    """
    if config is None:
        config = FusionConfig()

    if not responses:
        return RationalRaffleResult(
            base_response=ExpertPayload(reply_draft="No expert responses available."),
        )

    query_text = ""
    if request.context and request.context.msg_packet:
        query_text = request.context.msg_packet.payload

    scored: list[tuple[ExpertPayload, float, float]] = []
    for payload, alpha in responses:
        relevance = _jaccard_similarity(payload.reply_draft, query_text) if query_text else 0.5
        score = compute_raffle_score(alpha, relevance, payload.confidence)
        scored.append((payload, score, alpha))

    scored.sort(key=lambda x: x[1], reverse=True)

    base = scored[0][0]
    scores_dict: dict[str, float] = {}
    augmented: list[str] = []

    for payload, score, _alpha in scored:
        expert_id = payload.expert_id or "unknown"
        scores_dict[expert_id] = score

        if payload != base and score >= config.threshold:
            augmented.append(payload.reply_draft)

    reason_data = json.dumps(scores_dict, sort_keys=True)
    reason_hash = hashlib.sha256(reason_data.encode()).hexdigest()

    return RationalRaffleResult(
        base_response=base.model_copy(update={"reason_vector": reason_hash}),
        augmented_content=augmented,
        reason_vector_hash=reason_hash,
        scores=scores_dict,
    )
