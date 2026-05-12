"""Example: Customer Support with Pydantic AI following Hymoex M1 pattern.

Demonstrates how to build a One-Line MoE (M1) system using
Pydantic AI's Agent abstraction, following Hymoex patterns.

Pydantic AI's single-agent model maps naturally to Hymoex Expert role.
For M1, the Manager delegates directly to experts with no supervisor.

Requires: pip install pydantic-ai
"""

from pydantic_ai import Agent

# Hymoex validates your architecture
import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE, validate_topology


# --- Step 1: Define your Hymoex architecture ---

topology = OneLineMoE(
    manager=ManagerSpec(objective="Handle customer queries"),
    experts=[
        ExpertSpec(domain="tech", skills=["debugging", "troubleshooting"]),
        ExpertSpec(domain="billing", skills=["invoicing", "payments"]),
    ],
)
validation = validate_topology(topology)
print(f"Hymoex topology valid: {validation['valid']}, agents: {topology.agent_count}")


# --- Step 2: Implement with Pydantic AI ---

# Each Hymoex Expert becomes a Pydantic AI Agent
tech_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a technical support expert. Diagnose and resolve technical issues concisely.",
)

billing_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a billing specialist. Handle invoice and payment queries concisely.",
)

# The Manager role is your application code — it decides which agent to call
async def manager_route(query: str) -> str:
    """Manager routes to the appropriate expert (Hymoex Manager role)."""
    q = query.lower()
    if any(w in q for w in ["error", "bug", "api", "system", "crash"]):
        result = await tech_agent.run(query)
    else:
        result = await billing_agent.run(query)
    return result.data


# --- Step 3: Run ---

if __name__ == "__main__":
    import asyncio

    async def main():
        print("\nPydantic AI implementation following Hymoex M1 (One-Line MoE) pattern")
        print("Each Pydantic AI Agent maps to a Hymoex Expert role")
        print("Your application code acts as the Hymoex Manager role")
        # Uncomment to run (requires OPENAI_API_KEY):
        # result = await manager_route("My API is returning 500 errors")
        # print(f"Response: {result}")

    asyncio.run(main())
