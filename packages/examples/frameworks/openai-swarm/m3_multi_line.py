"""Example: OpenAI Swarm + Hymoex M3 (MoE MultiLine).

Multiple teams with chained handoffs. An integrator agent routes
to team supervisors, which then route to domain experts.

Requires: pip install openai-swarm
"""

from swarm import Agent, Swarm

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


# --- Swarm Implementation: Chained handoffs for team routing ---

# Finance team experts
contracts_agent = Agent(name="contracts", instructions="You are a contracts expert.")
payments_agent = Agent(name="payments", instructions="You are a payments expert.")

def transfer_to_contracts():
    return contracts_agent

def transfer_to_payments():
    return payments_agent

# Finance team supervisor
finance_supervisor = Agent(
    name="finance_supervisor",
    instructions="You supervise the finance team. Route to contracts or payments.",
    functions=[transfer_to_contracts, transfer_to_payments],
)

# HR team experts
onboarding_agent = Agent(name="onboarding", instructions="You are an onboarding specialist.")
compliance_agent = Agent(name="compliance", instructions="You are a compliance officer.")

def transfer_to_onboarding():
    return onboarding_agent

def transfer_to_compliance():
    return compliance_agent

# HR team supervisor
hr_supervisor = Agent(
    name="hr_supervisor",
    instructions="You supervise the HR team. Route to onboarding or compliance.",
    functions=[transfer_to_onboarding, transfer_to_compliance],
)

# Integrator — routes to team supervisors
def transfer_to_finance():
    return finance_supervisor

def transfer_to_hr():
    return hr_supervisor

integrator = Agent(
    name="integrator",
    instructions="You are an integrator. Route to finance_supervisor or hr_supervisor based on the query.",
    functions=[transfer_to_finance, transfer_to_hr],
)

if __name__ == "__main__":
    print("\nSwarm + Hymoex M3: Chained handoffs for multi-team routing")
    print("Integrator -> Team Supervisor -> Expert (all via handoff functions)")
    # client = Swarm()
    # response = client.run(agent=integrator, messages=[{"role": "user", "content": "Set up payroll"}])
