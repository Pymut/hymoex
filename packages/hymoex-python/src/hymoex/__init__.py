"""Hymoex — Hybrid Modular Coordinated Experts.

An architectural paradigm for classifying, designing, and scaling
multi-agent systems. Hymoex defines the WHAT (taxonomy, modalities,
protocols) — frameworks like LangGraph, CrewAI, and Pydantic AI
provide the HOW (execution).
"""

__version__ = "0.1.0"

# Taxonomy — agent role classification
from hymoex.analysis.classifier import auto_select_modality, classify_topology
from hymoex.analysis.validator import validate_topology
from hymoex.messaging.types import (
    ContextEnvelope,
    DecisionRequest,
    ExecCommand,
    ExecReceipt,
    ExpertPayload,
    HIPMessage,
    MsgPacket,
    Telemetry,
)
from hymoex.migration.migrate import compute_preservation_ratio, migrate_m1_to_m2, migrate_m2_to_m3
from hymoex.modalities.topologies import MultiLine, OneLineMoE, OneLineSupervisor, Team
from hymoex.moe.fusioner import FusionConfig, compute_raffle_score
from hymoex.moe.gate import GatingConfig, softmax_gate, top_k_select
from hymoex.protocols.base import GatingResult, SignalVector
from hymoex.taxonomy.roles import Role
from hymoex.taxonomy.specs import (
    AgentSpec,
    ExecutorSpec,
    ExpertManagerSpec,
    ExpertSpec,
    IntegratorSpec,
    ManagerSpec,
    PerceiverSpec,
    SupervisorSpec,
)

__all__ = [
    "__version__",
    # Taxonomy
    "Role",
    "AgentSpec",
    "ManagerSpec",
    "IntegratorSpec",
    "ExpertManagerSpec",
    "SupervisorSpec",
    "ExpertSpec",
    "ExecutorSpec",
    "PerceiverSpec",
    # Modalities
    "OneLineMoE",
    "OneLineSupervisor",
    "MultiLine",
    "Team",
    # Protocols
    "SignalVector",
    "GatingResult",
    # HIP Messages
    "MsgPacket",
    "ContextEnvelope",
    "DecisionRequest",
    "ExpertPayload",
    "ExecCommand",
    "ExecReceipt",
    "Telemetry",
    "HIPMessage",
    # MoE algorithms
    "GatingConfig",
    "softmax_gate",
    "top_k_select",
    "FusionConfig",
    "compute_raffle_score",
    # Migration
    "migrate_m1_to_m2",
    "migrate_m2_to_m3",
    "compute_preservation_ratio",
    # Analysis
    "auto_select_modality",
    "classify_topology",
    "validate_topology",
]
