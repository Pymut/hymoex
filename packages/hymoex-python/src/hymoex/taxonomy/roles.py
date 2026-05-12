"""The seven agent roles in the Hymoex cognitive architecture."""

from enum import StrEnum

__all__ = ["Role"]


class Role(StrEnum):
    """Agent roles define WHAT an agent is in the architecture, not HOW it runs.

    Each role has specific responsibilities, allowed message types, and
    position in the hierarchy. Frameworks (LangGraph, CrewAI, etc.)
    map these roles to their own abstractions.
    """

    MANAGER = "manager"
    INTEGRATOR = "integrator"
    EXPERT_MANAGER = "expert_manager"
    SUPERVISOR = "supervisor"
    EXPERT = "expert"
    EXECUTOR = "executor"
    PERCEIVER = "perceiver"
