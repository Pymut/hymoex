"""Example: Pydantic AI + Hymoex M3 (MoE MultiLine).

Multiple teams with an integrator routing across them.
Each team has a supervisor agent that coordinates domain experts.

Requires: pip install pydantic-ai
"""

from pydantic_ai import Agent

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


# --- Pydantic AI Implementation ---

# Finance team experts
contracts_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a contracts expert.")
payments_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a payments expert.")

# HR team experts
onboarding_agent = Agent("openai:gpt-4o-mini", system_prompt="You are an onboarding specialist.")
compliance_agent = Agent("openai:gpt-4o-mini", system_prompt="You are a compliance officer.")

# Team supervisors
finance_supervisor = Agent("openai:gpt-4o-mini", system_prompt="You are a finance supervisor. Route to: contracts or payments.")
hr_supervisor = Agent("openai:gpt-4o-mini", system_prompt="You are an HR supervisor. Route to: onboarding or compliance.")

# Integrator — routes to the right team
integrator = Agent("openai:gpt-4o-mini", system_prompt="You are an integrator. Route to: finance or hr. Respond with one word.")


async def multi_line_route(query: str) -> str:
    """M3 pattern: Integrator -> Team Supervisor -> Expert."""
    # Integrator routes to team
    team_decision = await integrator.run(query)
    team = team_decision.data.strip().lower()

    # Team supervisor routes to expert within team
    if team == "finance":
        routing = await finance_supervisor.run(query)
        domain = routing.data.strip().lower()
        expert = contracts_agent if "contract" in domain else payments_agent
    else:
        routing = await hr_supervisor.run(query)
        domain = routing.data.strip().lower()
        expert = onboarding_agent if "onboard" in domain else compliance_agent

    result = await expert.run(query)
    return result.data


if __name__ == "__main__":
    import asyncio
    print("\nPydantic AI + Hymoex M3: Integrator -> Team Supervisors -> Experts")
    # Uncomment to run (requires OPENAI_API_KEY):
    # print(asyncio.run(multi_line_route("Set up payroll for new hire")))
