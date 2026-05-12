"""Scenario: Content Pipeline (Modality M1)

Two experts (Writer + Editor) working in parallel — no supervisor needed.
Defines an M1 topology, validates it, and exports the config.
"""

import json
import sys

sys.path.insert(0, "../../../packages/hymoex-python/src")

from hymoex import (
    ExpertSpec,
    ManagerSpec,
    OneLineMoE,
    auto_select_modality,
    validate_topology,
)


def run() -> None:
    # --- Define the architecture ---
    manager = ManagerSpec(objective="Create high-quality content", strategy="parallel_creation")

    writer = ExpertSpec(
        domain="writing",
        skills=["blog_posts", "copywriting", "storytelling"],
    )
    editor = ExpertSpec(
        domain="editing",
        skills=["grammar", "style", "tone"],
    )

    experts = [writer, editor]

    # Auto-select modality
    modality = auto_select_modality(experts)

    # Build the topology
    system = OneLineMoE(manager=manager, experts=experts)

    # Validate
    validation = validate_topology(system)

    # Export config
    config = system.to_config()

    # --- Print results ---
    print("=" * 60)
    print("  CONTENT PIPELINE (Modality M1 — No Supervisor)")
    print("=" * 60)
    print(f"\n  Auto-selected modality: {modality.upper()}")
    print(f"  Agent count: {system.agent_count}")
    print(f"  Experts: {[e.domain for e in experts]}")
    print(f"  Manager objective: {manager.objective}")
    print(f"\n  Validation: {'PASSED' if validation['valid'] else 'FAILED'}")
    print(f"  Warnings: {validation['warnings'] or 'none'}")
    print(f"\n  Exported config:")
    print(f"  {json.dumps(config, indent=2, default=str)}")
    print("=" * 60)


if __name__ == "__main__":
    run()
