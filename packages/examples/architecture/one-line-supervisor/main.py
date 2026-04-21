"""Example: One-Line Supervisor (Modality M2) — B2B Customer Support.

Three experts (Legal, Tech, Billing) coordinated by a Supervisor.
This is the most common modality in production deployments.
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


def main() -> None:
    manager = ManagerSpec(
        objective="Resolve B2B customer issues",
        strategy="route_by_domain",
    )
    supervisor = SupervisorSpec(routing="dependency_aware")

    legal = ExpertSpec(domain="legal", skills=["contract_review", "compliance"])
    tech = ExpertSpec(domain="tech", skills=["diagnostics", "debugging"])
    billing = ExpertSpec(domain="billing", skills=["invoicing", "refunds"])

    experts = [legal, tech, billing]

    # Auto-select confirms M2
    modality = auto_select_modality(experts)
    print(f"Auto-selected modality: {modality.upper()}")

    # Build topology
    system = OneLineSupervisor(
        manager=manager,
        supervisor=supervisor,
        experts=experts,
    )

    # Validate
    validation = validate_topology(system)
    print(f"Agent count: {system.agent_count}")
    print(f"Valid: {validation['valid']}")

    # Classify
    classification = classify_topology(has_supervisor=True, expert_count=len(experts))
    print(f"Classification: {classification['current_name']}")
    print(f"Should migrate: {classification['should_migrate']}")

    # Export config
    config = system.to_config()
    print(f"\nConfig:\n{json.dumps(config, indent=2, default=str)}")


if __name__ == "__main__":
    main()
