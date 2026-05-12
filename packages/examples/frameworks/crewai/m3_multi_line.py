"""Example: CrewAI + Hymoex M3 (MoE MultiLine).

Multiple teams as separate Crews, coordinated by a manager crew.
Each team has its own supervisor (Crew) and experts (Agents).

Requires: pip install crewai
"""

from crewai import Agent, Crew, Task

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import (
    ExpertManagerSpec, ExpertSpec, IntegratorSpec, ManagerSpec,
    MultiLine, SupervisorSpec, Team, validate_topology,
)


# --- Hymoex M3: Manager -> Integrators -> Expert Manager -> Teams ---

topology = MultiLine(
    manager=ManagerSpec(objective="Enterprise onboarding"),
    integrators=[IntegratorSpec()],
    expert_manager=ExpertManagerSpec(),
    teams=[
        Team(name="finance", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="contracts"),
            ExpertSpec(domain="payments"),
        ]),
        Team(name="hr", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="onboarding"),
            ExpertSpec(domain="compliance"),
        ]),
    ],
)
print(f"Topology: M3, valid: {validate_topology(topology)['valid']}, agents: {topology.agent_count}")


# --- CrewAI Implementation: One Crew per Hymoex Team ---

# Finance team (Hymoex Team with Supervisor)
contracts_agent = Agent(role="Contracts Expert", goal="Draft and review contracts", backstory="Legal specialist.")
payments_agent = Agent(role="Payments Expert", goal="Process payments", backstory="Financial specialist.")

finance_crew = Crew(
    agents=[contracts_agent, payments_agent],
    tasks=[
        Task(description="Review the employment contract", agent=contracts_agent),
        Task(description="Set up payroll", agent=payments_agent),
    ],
    verbose=True,
)

# HR team (Hymoex Team with Supervisor)
onboarding_agent = Agent(role="Onboarding Expert", goal="Onboard new hires", backstory="HR specialist.")
compliance_agent = Agent(role="Compliance Expert", goal="Ensure regulatory compliance", backstory="Compliance officer.")

hr_crew = Crew(
    agents=[onboarding_agent, compliance_agent],
    tasks=[
        Task(description="Complete onboarding checklist", agent=onboarding_agent),
        Task(description="Verify compliance requirements", agent=compliance_agent),
    ],
    verbose=True,
)


# Integrator: routes to the right team
def integrator_route(query: str) -> Crew:
    """Integrator routes to the appropriate team crew."""
    q = query.lower()
    if any(w in q for w in ["contract", "payment", "payroll"]):
        return finance_crew
    return hr_crew


if __name__ == "__main__":
    print("\nCrewAI + Hymoex M3: Multiple team crews with integrator routing")
    print("Each CrewAI Crew maps to a Hymoex Team (Supervisor + Experts)")
    # Uncomment to run:
    # team = integrator_route("Set up payroll for the new hire")
    # result = team.kickoff()
