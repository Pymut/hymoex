"""Example: AutoGen + Hymoex M1 (One-Line MoE).

Two agents in direct conversation with no supervisor.
AutoGen's two-agent chat maps to M1's flat expert pattern.

Requires: pip install pyautogen
"""

from autogen import AssistantAgent, UserProxyAgent

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE, validate_topology


# --- Hymoex M1: Manager -> Experts (no Supervisor) ---

topology = OneLineMoE(
    manager=ManagerSpec(objective="Code review"),
    experts=[
        ExpertSpec(domain="developer", skills=["python"]),
        ExpertSpec(domain="reviewer", skills=["code_quality"]),
    ],
)
print(f"Topology: M1, valid: {validate_topology(topology)['valid']}")


# --- AutoGen Implementation ---

llm_config = {"model": "gpt-4o-mini", "api_key": "your-key"}

# Two experts in direct conversation (M1 — no supervisor)
developer = AssistantAgent("developer", system_message="You are a Python developer.", llm_config=llm_config)
reviewer = AssistantAgent("reviewer", system_message="You are a code reviewer.", llm_config=llm_config)

if __name__ == "__main__":
    print("\nAutoGen + Hymoex M1: Two agents, direct conversation")
    # Uncomment to run:
    # developer.initiate_chat(reviewer, message="Review this function: def add(a, b): return a + b")
