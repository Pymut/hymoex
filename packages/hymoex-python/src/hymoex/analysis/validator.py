"""Topology validator — checks if an architecture follows Hymoex constraints."""

from hymoex.modalities.topologies import MultiLine, OneLineMoE, OneLineSupervisor

__all__ = ["validate_topology"]


def validate_topology(
    system: OneLineMoE | OneLineSupervisor | MultiLine,
) -> dict[str, bool | str | int | list[str]]:
    """Validate that a system topology follows Hymoex architectural constraints.

    Returns validation results with hard errors (structural violations)
    and soft warnings (recommendation mismatches).
    """
    errors: list[str] = []
    warnings: list[str] = []

    if isinstance(system, OneLineMoE):
        modality = "m1"
        if len(system.experts) > 2:
            warnings.append(f"M1 recommends ≤2 experts, got {len(system.experts)}")

    elif isinstance(system, OneLineSupervisor):
        modality = "m2"
        if len(system.experts) > 5:
            warnings.append(f"M2 recommends ≤5 experts, got {len(system.experts)}. Consider M3.")

    elif isinstance(system, MultiLine):
        modality = "m3"
        total_experts = len(system.all_experts())
        if len(system.integrators) < 1:
            errors.append("M3 requires at least one Integrator")
        for team in system.teams:
            if not team.experts:
                errors.append(f"Team '{team.name}' has no experts")
        if total_experts <= 5:
            warnings.append(f"M3 recommends >5 experts, got {total_experts}. Consider M2.")
    else:
        modality = "unknown"
        errors.append(f"Unrecognized topology type: {type(system).__name__}")

    return {
        "valid": len(errors) == 0,
        "modality": modality,
        "agent_count": system.agent_count,
        "errors": errors,
        "warnings": warnings,
    }
