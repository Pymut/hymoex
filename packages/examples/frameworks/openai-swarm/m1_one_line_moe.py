"""Example: Customer Support with OpenAI Swarm following Hymoex M1 pattern.

Demonstrates how to build a One-Line MoE (M1) system using
OpenAI Swarm's lightweight handoff pattern, following Hymoex patterns.

Swarm's flat agent handoff maps naturally to M1 (no supervisor).
Each Swarm Agent maps to a Hymoex Expert role.
Handoff functions implement the Manager's routing logic.

Requires: pip install openai-swarm
"""

from swarm import Agent, Swarm

# Hymoex validates your architecture
import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE, validate_topology


# --- Step 1: Define your Hymoex architecture ---

topology = OneLineMoE(
    manager=ManagerSpec(objective="Route customer queries"),
    experts=[
        ExpertSpec(domain="tech", skills=["debugging"]),
        ExpertSpec(domain="billing", skills=["invoicing"]),
    ],
)
validation = validate_topology(topology)
print(f"Hymoex topology valid: {validation['valid']}, agents: {topology.agent_count}")


# --- Step 2: Implement with OpenAI Swarm ---

# Each Hymoex Expert becomes a Swarm Agent
tech_agent = Agent(
    name="tech",
    instructions="You are a technical support expert. Resolve technical issues.",
)

billing_agent = Agent(
    name="billing",
    instructions="You are a billing specialist. Handle payment queries.",
)


# Handoff functions implement Hymoex Manager routing
def transfer_to_tech():
    """Route to tech expert."""
    return tech_agent


def transfer_to_billing():
    """Route to billing expert."""
    return billing_agent


# The triage agent acts as the Hymoex Manager — routing to experts
triage_agent = Agent(
    name="manager",
    instructions="You are a triage agent. Route to tech or billing based on the query.",
    functions=[transfer_to_tech, transfer_to_billing],
)


# --- Step 3: Run ---

if __name__ == "__main__":
    print("\nOpenAI Swarm implementation following Hymoex M1 (One-Line MoE) pattern")
    print("Each Swarm Agent maps to a Hymoex Expert role")
    print("Handoff functions implement Hymoex Manager routing")
    # Uncomment to run (requires OPENAI_API_KEY):
    # client = Swarm()
    # response = client.run(agent=triage_agent, messages=[{"role": "user", "content": "API error 500"}])
    # print(response.messages[-1]["content"])
