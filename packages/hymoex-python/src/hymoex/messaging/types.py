"""HIP (Hymoex Interchange Protocol) typed message definitions.

All seven message types used for inter-agent communication, implemented as
pydantic v2 models with strict validation.
"""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

__all__ = [
    "MsgPacket",
    "ContextEnvelope",
    "DecisionRequest",
    "ExpertPayload",
    "ExecCommand",
    "ExecReceipt",
    "Telemetry",
    "HIPMessage",
]


class MsgPacket(BaseModel):
    """Raw user input with channel metadata."""

    channel: Literal["whatsapp", "web", "voice"]
    customer_id: str
    payload: str
    lang: str = "en"
    latency: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)


class ContextEnvelope(BaseModel):
    """Enriched packet with routing state, produced by Integrators."""

    msg_packet: MsgPacket
    lead_stage: str = "unknown"
    sla_budget: float = 5000.0
    interaction_id: UUID = Field(default_factory=uuid4)
    trace_context: str = ""


class DecisionRequest(BaseModel):
    """Signal vector plus context for MoE gating."""

    intent_embedding: list[float] = Field(default_factory=list)
    emotion_vector: list[float] = Field(default_factory=list)
    stage_flag: list[float] = Field(default_factory=list)
    lead_score: float = 0.0
    context: ContextEnvelope | None = None


class ExpertPayload(BaseModel):
    """Expert response with confidence and audit trail."""

    reply_draft: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    reason_vector: str = ""
    expert_id: str = ""
    tokens_used: int = 0


class ExecCommand(BaseModel):
    """Typed action command for Executors."""

    type: Literal["crm_update", "doc_generate", "payment", "calendar"]
    params: dict[str, Any] = Field(default_factory=dict)
    callback_url: str = ""
    idempotency_key: UUID = Field(default_factory=uuid4)


class ExecReceipt(BaseModel):
    """Execution result from Executors."""

    status: Literal["success", "failure", "pending"] = "pending"
    latency: float = 0.0
    error_code: str | None = None
    next_action: str | None = None


class Telemetry(BaseModel):
    """Real-time feedback from Perceivers."""

    sentiment: float = Field(default=0.0, ge=-1.0, le=1.0)
    delivery_status: str = "unknown"
    action_outcome: str = ""
    team_id: str = ""
    stage: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


type HIPMessage = (
    MsgPacket
    | ContextEnvelope
    | DecisionRequest
    | ExpertPayload
    | ExecCommand
    | ExecReceipt
    | Telemetry
)
