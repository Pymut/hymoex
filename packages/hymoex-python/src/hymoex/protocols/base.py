"""Foundational protocol types for the Hymoex cognitive architecture."""

from pydantic import BaseModel, Field

__all__ = ["SignalVector", "GatingResult"]


class SignalVector(BaseModel):
    """Composite signal vector for MoE gating (Definition 3 in the paper).

    s = [e_intent, e_emotion, f_stage, s_score] in R^d

    Used by frameworks implementing Hymoex MoE gating to construct
    the input to the softmax gate function.
    """

    intent_embedding: list[float] = Field(default_factory=list)
    emotion_embedding: list[float] = Field(default_factory=list)
    stage_flag: list[float] = Field(default_factory=list)
    lead_score: float = 0.0

    def to_vector(self) -> list[float]:
        """Flatten all components into a single vector."""
        return self.intent_embedding + self.emotion_embedding + self.stage_flag + [self.lead_score]

    @property
    def dim(self) -> int:
        """Return the dimensionality of the flattened signal vector."""
        return len(self.to_vector())


class GatingResult(BaseModel):
    """Result of the MoE gating function."""

    selected_experts: list[str] = Field(default_factory=list)
    weights: dict[str, float] = Field(default_factory=dict)
