"""Example: One-Line MoE (Modality M1) — Content Generation.

Two experts (Writer + Editor) working in parallel with no Supervisor.
Defines the topology, validates it, and exports the config.
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


def main() -> None:
    manager = ManagerSpec(
        objective="Generate and edit content",
        strategy="parallel_creation",
    )
    writer = ExpertSpec(domain="writing", skills=["blog_posts", "copywriting"])
    editor = ExpertSpec(domain="editing", skills=["grammar", "style"])

    experts = [writer, editor]

    # Auto-select confirms M1
    modality = auto_select_modality(experts)
    print(f"Auto-selected modality: {modality.upper()}")

    # Build topology
    system = OneLineMoE(manager=manager, experts=experts)

    # Validate
    validation = validate_topology(system)
    print(f"Agent count: {system.agent_count}")
    print(f"Valid: {validation['valid']}")
    print(f"Warnings: {validation['warnings'] or 'none'}")

    # Export config
    config = system.to_config()
    print(f"\nConfig:\n{json.dumps(config, indent=2, default=str)}")


if __name__ == "__main__":
    main()
