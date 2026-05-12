"""Example: MoE MultiLine (Modality M3) — Enterprise Workflow.

Multiple teams across domains with Integrators and Expert Manager.
Demonstrates progressive migration from M1 -> M2 -> M3.
"""

import json
import sys

sys.path.insert(0, "../../../packages/hymoex-python/src")

from hymoex import (
    ExpertManagerSpec,
    ExpertSpec,
    IntegratorSpec,
    ManagerSpec,
    MultiLine,
    OneLineMoE,
    SupervisorSpec,
    Team,
    compute_preservation_ratio,
    migrate_m1_to_m2,
    migrate_m2_to_m3,
    validate_topology,
)


def main() -> None:
    # --- Step 1: Start with M1 (2 experts) ---
    print("=== Step 1: One-Line MoE (M1) ===")
    manager = ManagerSpec(objective="Global workforce management")
    contracts = ExpertSpec(domain="contracts", skills=["drafting", "review"])
    payments = ExpertSpec(domain="payments", skills=["payroll", "invoicing"])

    m1 = OneLineMoE(manager=manager, experts=[contracts, payments])
    v1 = validate_topology(m1)
    print(f"  Agents: {m1.agent_count}, Valid: {v1['valid']}")

    # --- Step 2: Migrate to M2 (add compliance) ---
    print("\n=== Step 2: Migrate to One-Line Supervisor (M2) ===")
    compliance = ExpertSpec(domain="compliance", skills=["regulations", "audit"])
    m2 = migrate_m1_to_m2(m1, additional_experts=[compliance])

    ratio = compute_preservation_ratio(m1.agent_count, m1.agent_count)
    v2 = validate_topology(m2)
    print(f"  Agents: {m2.agent_count}, Experts: {len(m2.experts)}")
    print(f"  Preservation: {ratio*100:.0f}%, Valid: {v2['valid']}")

    # --- Step 3: Migrate to M3 (add HR team) ---
    print("\n=== Step 3: Migrate to MoE MultiLine (M3) ===")
    m3 = migrate_m2_to_m3(m2, team_name="finance_team")

    # Add a second team
    hr_team = Team(
        name="hr_team",
        supervisor=SupervisorSpec(routing="dependency_aware"),
        experts=[
            ExpertSpec(domain="onboarding", skills=["new_hires"]),
            ExpertSpec(domain="benefits", skills=["insurance", "401k"]),
        ],
    )
    m3_expanded = MultiLine(
        manager=m3.manager,
        integrators=m3.integrators,
        expert_manager=m3.expert_manager,
        teams=[*m3.teams, hr_team],
    )

    ratio_m3 = compute_preservation_ratio(m2.agent_count, m2.agent_count)
    v3 = validate_topology(m3_expanded)
    print(f"  Teams: {[t.name for t in m3_expanded.teams]}")
    print(f"  Total experts: {len(m3_expanded.all_experts())}")
    print(f"  Total agents: {m3_expanded.agent_count}")
    print(f"  Preservation: {ratio_m3*100:.0f}%, Valid: {v3['valid']}")

    # Export final config
    config = m3_expanded.to_config()
    print(f"\nFinal M3 config:\n{json.dumps(config, indent=2, default=str)}")


if __name__ == "__main__":
    main()
