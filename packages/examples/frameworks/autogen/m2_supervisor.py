"""Example: Customer Support with AutoGen following Hymoex M2 pattern.

Demonstrates how to build a One-Line Supervisor (M2) system using
AutoGen's GroupChat, following Hymoex architectural patterns.

AutoGen's GroupChatManager maps to the Hymoex Supervisor role.
Each AssistantAgent maps to a Hymoex Expert role.

Requires: pip install pyautogen
"""

from autogen import AssistantAgent, GroupChat, GroupChatManager

# Hymoex validates your architecture
import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineSupervisor, SupervisorSpec, validate_topology


# --- Step 1: Define your Hymoex architecture ---

topology = OneLineSupervisor(
    manager=ManagerSpec(objective="Resolve customer issues"),
    supervisor=SupervisorSpec(routing="dependency_aware"),
    experts=[
        ExpertSpec(domain="legal", skills=["contracts", "compliance"]),
        ExpertSpec(domain="tech", skills=["debugging", "infrastructure"]),
        ExpertSpec(domain="billing", skills=["invoicing", "refunds"]),
    ],
)
validation = validate_topology(topology)
print(f"Hymoex topology valid: {validation['valid']}, agents: {topology.agent_count}")


# --- Step 2: Implement with AutoGen ---

llm_config = {"model": "gpt-4o-mini", "api_key": "your-key"}

# Each Hymoex Expert becomes an AutoGen AssistantAgent
legal = AssistantAgent("legal", system_message="You are a legal expert.", llm_config=llm_config)
tech = AssistantAgent("tech", system_message="You are a tech support expert.", llm_config=llm_config)
billing = AssistantAgent("billing", system_message="You are a billing specialist.", llm_config=llm_config)

# GroupChat + GroupChatManager maps to Hymoex Supervisor role
group_chat = GroupChat(agents=[legal, tech, billing], messages=[], max_round=3)
supervisor = GroupChatManager(groupchat=group_chat, llm_config=llm_config)


# --- Step 3: Run ---

if __name__ == "__main__":
    print("\nAutoGen implementation following Hymoex M2 (One-Line Supervisor) pattern")
    print("Each AssistantAgent maps to a Hymoex Expert role")
    print("GroupChatManager maps to the Hymoex Supervisor role")
    # Uncomment to run (requires API key):
    # legal.initiate_chat(supervisor, message="Contract breach reported by client")
