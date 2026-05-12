"""Agent specifications — architectural blueprints, not executors.

An AgentSpec describes WHAT an agent is (role, domain, skills, constraints)
without prescribing HOW it runs. Execution is the framework's responsibility.
"""

from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from hymoex.taxonomy.roles import Role

__all__ = [
    "AgentSpec",
    "ManagerSpec",
    "IntegratorSpec",
    "ExpertManagerSpec",
    "SupervisorSpec",
    "ExpertSpec",
    "ExecutorSpec",
    "PerceiverSpec",
]


class AgentSpec(BaseModel):
    """Base specification for any Hymoex agent.

    This is a blueprint — it defines the agent's identity and constraints
    within the architecture. It does NOT execute anything.
    """

    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    role: Role
    name: str = ""
    description: str = ""
    config: dict[str, Any] = Field(default_factory=dict)


class ManagerSpec(AgentSpec):
    """Strategic layer — defines objectives and selects coordination patterns."""

    role: Literal[Role.MANAGER] = Role.MANAGER
    objective: str = ""
    strategy: str = "default"


class IntegratorSpec(AgentSpec):
    """Bridging layer — routes context across domains, manages SLA budgets."""

    role: Literal[Role.INTEGRATOR] = Role.INTEGRATOR
    routing_overhead_ms: float = 50.0


class ExpertManagerSpec(AgentSpec):
    """Tactical layer — coordinates MoE gating across expert pools."""

    role: Literal[Role.EXPERT_MANAGER] = Role.EXPERT_MANAGER


class SupervisorSpec(AgentSpec):
    """Tactical layer — coordinates expert delegation and task dependencies."""

    role: Literal[Role.SUPERVISOR] = Role.SUPERVISOR
    routing: str = "dependency_aware"


class ExpertSpec(AgentSpec):
    """Specialist layer — domain-specific knowledge and query resolution."""

    role: Literal[Role.EXPERT] = Role.EXPERT
    domain: str = "general"
    skills: list[str] = Field(default_factory=list)
    system_prompt: str = ""


class ExecutorSpec(AgentSpec):
    """Operational layer — performs external actions (APIs, docs, payments)."""

    role: Literal[Role.EXECUTOR] = Role.EXECUTOR
    action_type: str = "generic"


class PerceiverSpec(AgentSpec):
    """Sensing layer — captures telemetry and feeds feedback loops."""

    role: Literal[Role.PERCEIVER] = Role.PERCEIVER
    sensor_type: str = "generic"
