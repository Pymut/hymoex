"""Progressive migration between Hymoex modalities.

Implements migration functions preserving >=85% of existing agents.
Migration only ADDS coordination agents -- never removes existing ones.
"""

from hymoex.modalities.topologies import MultiLine, OneLineMoE, OneLineSupervisor, Team
from hymoex.taxonomy.specs import ExpertManagerSpec, ExpertSpec, IntegratorSpec, SupervisorSpec

__all__ = ["migrate_m1_to_m2", "migrate_m2_to_m3", "compute_preservation_ratio"]


def migrate_m1_to_m2(
    system: OneLineMoE,
    supervisor: SupervisorSpec | None = None,
    additional_experts: list[ExpertSpec] | None = None,
) -> OneLineSupervisor:
    """Migrate from One-Line MoE (M1) to One-Line Supervisor (M2).

    Preserves all existing agents. Adds a Supervisor and optionally
    new experts to meet the M2 minimum (3 experts).
    """
    if supervisor is None:
        supervisor = SupervisorSpec(routing="dependency_aware")

    experts = list(system.experts)
    if additional_experts:
        experts.extend(additional_experts)

    return OneLineSupervisor(
        manager=system.manager,
        supervisor=supervisor,
        experts=experts,
        executors=system.executors,
        perceivers=system.perceivers,
    )


def migrate_m2_to_m3(
    system: OneLineSupervisor,
    integrators: list[IntegratorSpec] | None = None,
    expert_manager: ExpertManagerSpec | None = None,
    team_name: str = "team_1",
) -> MultiLine:
    """Migrate from One-Line Supervisor (M2) to MultiLine (M3).

    Preserves all existing agents. The existing Supervisor becomes a Team
    Supervisor. Adds Integrators and Expert Manager.
    """
    if integrators is None:
        integrators = [IntegratorSpec()]
    if expert_manager is None:
        expert_manager = ExpertManagerSpec()

    team = Team(
        name=team_name,
        supervisor=system.supervisor,
        experts=system.experts,
        executors=system.executors,
        perceivers=system.perceivers,
    )

    return MultiLine(
        manager=system.manager,
        integrators=integrators,
        expert_manager=expert_manager,
        teams=[team],
    )


def compute_preservation_ratio(original_agent_count: int, preserved_agent_count: int) -> float:
    """Compute the code preservation ratio (Property 2 from the paper)."""
    if original_agent_count == 0:
        return 1.0
    return preserved_agent_count / original_agent_count
