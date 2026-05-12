"""Architecture classifier — recommends the right modality for a given setup."""

from typing import Literal

from hymoex.taxonomy.specs import ExpertSpec

__all__ = ["auto_select_modality", "classify_topology"]


def auto_select_modality(experts: list[ExpertSpec]) -> Literal["m1", "m2", "m3"]:
    """Select the appropriate modality based on expert count.

    k ≤ 2  → M1 (One-Line MoE)
    3-5    → M2 (One-Line Supervisor)
    > 5    → M3 (MoE MultiLine)
    """
    k = len(experts)
    if k <= 2:
        return "m1"
    elif k <= 5:
        return "m2"
    else:
        return "m3"


def classify_topology(
    has_supervisor: bool = False,
    has_integrator: bool = False,
    has_expert_manager: bool = False,
    expert_count: int = 1,
) -> dict[str, str | int | bool]:
    """Classify an existing multi-agent system into a Hymoex modality.

    Useful for analyzing systems built with other frameworks and
    determining which Hymoex pattern they follow.
    """
    if has_integrator or has_expert_manager:
        modality = "m3"
        name = "MoE MultiLine"
    elif has_supervisor:
        modality = "m2"
        name = "One-Line Supervisor"
    else:
        modality = "m1"
        name = "One-Line MoE"

    recommended = auto_select_modality(
        [ExpertSpec(domain=f"d{i}") for i in range(expert_count)]
    )

    return {
        "current_modality": modality,
        "current_name": name,
        "expert_count": expert_count,
        "recommended_modality": recommended,
        "should_migrate": modality != recommended,
    }
