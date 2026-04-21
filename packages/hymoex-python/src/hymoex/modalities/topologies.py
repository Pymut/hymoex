"""Modality topology definitions — structural constraints on agent graphs.

Each modality defines WHICH roles appear and HOW they connect.
It does NOT define execution — that's the framework's job.
"""

from typing import Any

from pydantic import BaseModel, Field, model_validator

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

__all__ = ["OneLineMoE", "OneLineSupervisor", "Team", "MultiLine"]


class OneLineMoE(BaseModel):
    """Modality M1: Manager → Expert(s) → Executors/Perceivers.

    No Supervisor. Recommended for k ≤ 2 domain experts.
    Supports swarm-style autonomous operation.
    """

    manager: ManagerSpec
    experts: list[ExpertSpec] = Field(min_length=1, max_length=2)
    executors: list[ExecutorSpec] = Field(default_factory=list)
    perceivers: list[PerceiverSpec] = Field(default_factory=list)

    @property
    def agent_count(self) -> int:
        """Return the total number of agents in this topology."""
        return 1 + len(self.experts) + len(self.executors) + len(self.perceivers)

    @property
    def all_specs(self) -> list[AgentSpec]:
        """Return all agent specifications in this topology."""
        return [self.manager, *self.experts, *self.executors, *self.perceivers]

    def to_config(self) -> dict[str, Any]:
        """Export as a JSON-serializable architecture config."""
        return {
            "modality": "one_line_moe",
            "manager": self.manager.model_dump(),
            "experts": [e.model_dump() for e in self.experts],
            "executors": [e.model_dump() for e in self.executors],
            "perceivers": [p.model_dump() for p in self.perceivers],
        }


class OneLineSupervisor(BaseModel):
    """Modality M2: Manager → Supervisor → Expert(s).

    Adds tactical coordination. Recommended for 3-5 domain experts.
    """

    manager: ManagerSpec
    supervisor: SupervisorSpec
    experts: list[ExpertSpec] = Field(min_length=3, max_length=5)
    executors: list[ExecutorSpec] = Field(default_factory=list)
    perceivers: list[PerceiverSpec] = Field(default_factory=list)

    @property
    def agent_count(self) -> int:
        """Return the total number of agents in this topology."""
        return 2 + len(self.experts) + len(self.executors) + len(self.perceivers)

    @property
    def all_specs(self) -> list[AgentSpec]:
        """Return all agent specifications in this topology."""
        return [self.manager, self.supervisor, *self.experts, *self.executors, *self.perceivers]

    def to_config(self) -> dict[str, Any]:
        """Export as a JSON-serializable architecture config."""
        return {
            "modality": "one_line_supervisor",
            "manager": self.manager.model_dump(),
            "supervisor": self.supervisor.model_dump(),
            "experts": [e.model_dump() for e in self.experts],
            "executors": [e.model_dump() for e in self.executors],
            "perceivers": [p.model_dump() for p in self.perceivers],
        }


class Team(BaseModel):
    """A team within a MultiLine deployment."""

    name: str = "default"
    supervisor: SupervisorSpec
    experts: list[ExpertSpec] = Field(default_factory=list)
    executors: list[ExecutorSpec] = Field(default_factory=list)
    perceivers: list[PerceiverSpec] = Field(default_factory=list)


class MultiLine(BaseModel):
    """Modality M3: Manager → Integrators → Expert Manager → Teams.

    For complex systems with k > 5 experts organized into teams.
    Each team can independently adopt swarm or hierarchical coordination.
    """

    manager: ManagerSpec
    integrators: list[IntegratorSpec] = Field(min_length=1)
    expert_manager: ExpertManagerSpec
    teams: list[Team] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_expert_count(self) -> "MultiLine":
        total = sum(len(t.experts) for t in self.teams)
        if total < 1:
            raise ValueError(f"MultiLine requires experts across teams, got {total}")
        return self

    @property
    def agent_count(self) -> int:
        """Return the total number of agents across all teams."""
        team_count = sum(
            1 + len(t.experts) + len(t.executors) + len(t.perceivers)
            for t in self.teams
        )
        return 1 + len(self.integrators) + 1 + team_count

    def all_experts(self) -> list[ExpertSpec]:
        """Return all expert specs across all teams."""
        return [e for t in self.teams for e in t.experts]

    def to_config(self) -> dict[str, Any]:
        """Export as a JSON-serializable architecture config."""
        return {
            "modality": "multi_line",
            "manager": self.manager.model_dump(),
            "integrators": [i.model_dump() for i in self.integrators],
            "expert_manager": self.expert_manager.model_dump(),
            "teams": [
                {
                    "name": t.name,
                    "supervisor": t.supervisor.model_dump(),
                    "experts": [e.model_dump() for e in t.experts],
                }
                for t in self.teams
            ],
        }
