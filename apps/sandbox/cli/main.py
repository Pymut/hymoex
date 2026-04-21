"""Hymoex Sandbox CLI — define a multi-agent topology from the command line.

Usage:
    uv run python apps/sandbox/cli/main.py --experts legal tech billing
    uv run python apps/sandbox/cli/main.py --experts writer editor
    uv run python apps/sandbox/cli/main.py --experts a b c d e f
"""

import argparse
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
    OneLineSupervisor,
    SupervisorSpec,
    Team,
    auto_select_modality,
    validate_topology,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hymoex Sandbox — define a multi-agent topology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--experts",
        nargs="+",
        default=["legal", "tech", "billing"],
        help="Domain names for experts (e.g., legal tech billing)",
    )
    parser.add_argument(
        "--objective",
        default="Process user request",
        help="Manager objective",
    )

    args = parser.parse_args()

    # Build expert specs
    experts = [ExpertSpec(domain=d, skills=[f"{d}_skill"]) for d in args.experts]
    manager = ManagerSpec(objective=args.objective)

    # Auto-select modality
    modality = auto_select_modality(experts)
    modality_names = {"m1": "One-Line MoE", "m2": "One-Line Supervisor", "m3": "MoE MultiLine"}

    # Build the appropriate topology
    if modality == "m1":
        system = OneLineMoE(manager=manager, experts=experts)
    elif modality == "m2":
        system = OneLineSupervisor(
            manager=manager,
            supervisor=SupervisorSpec(routing="dependency_aware"),
            experts=experts,
        )
    else:
        # M3: group experts into a single team
        system = MultiLine(
            manager=manager,
            integrators=[IntegratorSpec()],
            expert_manager=ExpertManagerSpec(),
            teams=[
                Team(
                    name="default",
                    supervisor=SupervisorSpec(),
                    experts=experts,
                )
            ],
        )

    # Validate
    validation = validate_topology(system)

    # Export config
    config = system.to_config()

    # Print results
    print()
    print("=" * 60)
    print("  HYMOEX SANDBOX")
    print("=" * 60)
    print(f"  Experts:    {', '.join(args.experts)} ({len(experts)})")
    print(f"  Modality:   {modality_names[modality]} ({modality.upper()})")
    print(f"  Agents:     {system.agent_count}")
    print(f"  Objective:  {args.objective}")
    print(f"  Valid:      {validation['valid']}")
    if validation["warnings"]:
        print(f"  Warnings:   {validation['warnings']}")
    print("=" * 60)
    print(f"\n  Config (JSON):")
    print(f"  {json.dumps(config, indent=2, default=str)}")
    print()


if __name__ == "__main__":
    main()
