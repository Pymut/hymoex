"""Example: AutoGen + Hymoex M3 (MoE MultiLine).

Multiple teams using nested GroupChats. Each team is a GroupChat
with its own GroupChatManager (Supervisor). A top-level manager
coordinates across teams via an Integrator agent.

Requires: pip install pyautogen
"""

from autogen import AssistantAgent, GroupChat, GroupChatManager

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


# --- AutoGen Implementation: Nested GroupChats per team ---

llm_config = {"model": "gpt-4o-mini", "api_key": "your-key"}

# Finance team (Hymoex Team -> AutoGen GroupChat)
contracts = AssistantAgent("contracts", system_message="You are a contracts expert.", llm_config=llm_config)
payments = AssistantAgent("payments", system_message="You are a payments expert.", llm_config=llm_config)
finance_chat = GroupChat(agents=[contracts, payments], messages=[], max_round=3)
finance_supervisor = GroupChatManager(groupchat=finance_chat, llm_config=llm_config)

# HR team (Hymoex Team -> AutoGen GroupChat)
onboarding = AssistantAgent("onboarding", system_message="You are an onboarding specialist.", llm_config=llm_config)
compliance = AssistantAgent("compliance", system_message="You are a compliance officer.", llm_config=llm_config)
hr_chat = GroupChat(agents=[onboarding, compliance], messages=[], max_round=3)
hr_supervisor = GroupChatManager(groupchat=hr_chat, llm_config=llm_config)

# Integrator agent routes across teams
integrator = AssistantAgent(
    "integrator",
    system_message="You are an integrator. Route queries to the finance or HR team.",
    llm_config=llm_config,
)


if __name__ == "__main__":
    print("\nAutoGen + Hymoex M3: Nested GroupChats as teams")
    print("Each GroupChat maps to a Hymoex Team (Supervisor + Experts)")
    print("GroupChatManager maps to Hymoex Team Supervisor")
    print("Integrator agent routes across teams")
    # Uncomment to run:
    # integrator.initiate_chat(finance_supervisor, message="Process the new hire contract")
