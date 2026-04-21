"""Example: OpenAI Swarm + Hymoex M2 (One-Line Supervisor).

A triage agent acts as Supervisor, routing to domain experts.
Swarm's handoff functions implement the routing logic.

Requires: pip install openai-swarm
"""

from swarm import Agent, Swarm

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineSupervisor, SupervisorSpec, validate_topology


# --- Hymoex M2: Manager -> Supervisor -> Experts ---

topology = OneLineSupervisor(
    manager=ManagerSpec(objective="Customer support"),
    supervisor=SupervisorSpec(routing="dependency_aware"),
    experts=[
        ExpertSpec(domain="legal", skills=["contracts"]),
        ExpertSpec(domain="tech", skills=["debugging"]),
        ExpertSpec(domain="billing", skills=["invoicing"]),
    ],
)
print(f"Topology: M2, valid: {validate_topology(topology)['valid']}")


# --- Swarm Implementation ---

legal_agent = Agent(name="legal", instructions="You are a legal expert. Handle contracts and compliance.")
tech_agent = Agent(name="tech", instructions="You are a tech expert. Debug and resolve issues.")
billing_agent = Agent(name="billing", instructions="You are a billing expert. Handle payments.")


def transfer_to_legal():
    return legal_agent

def transfer_to_tech():
    return tech_agent

def transfer_to_billing():
    return billing_agent


# Supervisor agent — routes to the correct expert via handoffs
supervisor_agent = Agent(
    name="supervisor",
    instructions="You are a customer support supervisor. Route queries to the right expert.",
    functions=[transfer_to_legal, transfer_to_tech, transfer_to_billing],
)

if __name__ == "__main__":
    print("\nSwarm + Hymoex M2: Supervisor routes via handoff functions")
    # client = Swarm()
    # response = client.run(agent=supervisor_agent, messages=[{"role": "user", "content": "Contract breach"}])
