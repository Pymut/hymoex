"""Example: Pydantic AI + Hymoex M2 (One-Line Supervisor).

A supervisor agent coordinates three expert agents.
The supervisor decides which expert to call based on the query.

Requires: pip install pydantic-ai
"""

from pydantic_ai import Agent

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


# --- Pydantic AI Implementation ---

legal_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a legal expert. Handle contracts and compliance.")
tech_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a tech expert. Debug and resolve technical issues.")
billing_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a billing expert. Handle invoices and payments.")

# Supervisor agent decides which expert to call
supervisor_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a supervisor. Analyze the query and respond with exactly one word: legal, tech, or billing.",
)


async def supervised_route(query: str) -> str:
    """Supervisor routes to the correct expert (Hymoex M2 pattern)."""
    # Supervisor decides
    routing = await supervisor_agent.run(query)
    domain = routing.data.strip().lower()

    # Route to expert
    agents = {"legal": legal_agent, "tech": tech_agent, "billing": billing_agent}
    expert = agents.get(domain, billing_agent)
    result = await expert.run(query)
    return result.data


if __name__ == "__main__":
    import asyncio
    print("\nPydantic AI + Hymoex M2: Supervisor routes to 3 experts")
    # Uncomment to run (requires OPENAI_API_KEY):
    # print(asyncio.run(supervised_route("My contract was breached")))
