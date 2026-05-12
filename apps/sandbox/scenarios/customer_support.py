"""Scenario: Customer Support Triage (Modality M2)

Defines a customer support topology with 3 domain experts,
validates it, classifies it, and exports the architecture config.
"""

import json
import sys

sys.path.insert(0, "../../../packages/hymoex-python/src")

from hymoex import (
    ExpertSpec,
    ManagerSpec,
    OneLineSupervisor,
    SupervisorSpec,
    auto_select_modality,
    classify_topology,
    validate_topology,
)


def run() -> None:
    # --- Define the architecture ---
    manager = ManagerSpec(objective="Resolve customer issues fast", strategy="route_by_domain")
    supervisor = SupervisorSpec(routing="dependency_aware")

    experts = [
        ExpertSpec(domain="legal", skills=["contracts", "compliance"]),
        ExpertSpec(domain="tech", skills=["debugging", "infrastructure"]),
        ExpertSpec(domain="billing", skills=["invoicing", "refunds"]),
    ]

    # Auto-select modality based on expert count
    modality = auto_select_modality(experts)

    # Build the topology
    system = OneLineSupervisor(
        manager=manager,
        supervisor=supervisor,
        experts=experts,
    )

    # Validate
    validation = validate_topology(system)

    # Classify
    classification = classify_topology(
        has_supervisor=True,
        expert_count=len(experts),
    )

    # Export config
    config = system.to_config()

    # --- Print results ---
    print("=" * 60)
    print("  CUSTOMER SUPPORT TRIAGE (Modality M2)")
    print("=" * 60)
    print(f"\n  Auto-selected modality: {modality.upper()}")
    print(f"  Agent count: {system.agent_count}")
    print(f"  Experts: {[e.domain for e in experts]}")
    print(f"\n  Validation: {'PASSED' if validation['valid'] else 'FAILED'}")
    print(f"  Warnings: {validation['warnings'] or 'none'}")
    print(f"\n  Classification: {classification['current_name']}")
    print(f"  Should migrate: {classification['should_migrate']}")
    print(f"\n  Exported config:")
    print(f"  {json.dumps(config, indent=2, default=str)[:500]}")
    print("=" * 60)


if __name__ == "__main__":
    run()
