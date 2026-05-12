"""Example: CrewAI + Hymoex M2 (One-Line Supervisor).

Uses CrewAI's hierarchical process mode where a manager LLM
acts as the Hymoex Supervisor — automatically routing tasks
to the right expert agent.

Key difference from M1: M1 uses process="sequential" (fixed order).
M2 uses process="hierarchical" with manager_llm (dynamic routing).

Requires: pip install crewai
"""

from crewai import Agent, Crew, Task

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineSupervisor, SupervisorSpec, validate_topology


# --- Hymoex M2: Manager -> Supervisor -> Experts ---

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


# --- CrewAI Implementation: Hierarchical process = Hymoex Supervisor ---

# Each Hymoex Expert becomes a CrewAI Agent
legal_agent = Agent(
    role="Legal Expert",
    goal="Review contracts and ensure compliance",
    backstory="You are a legal expert specializing in contracts and regulatory compliance.",
    allow_delegation=False,
)

tech_agent = Agent(
    role="Tech Expert",
    goal="Diagnose and resolve technical issues",
    backstory="You are a senior engineer specializing in debugging and infrastructure.",
    allow_delegation=False,
)

billing_agent = Agent(
    role="Billing Expert",
    goal="Handle invoicing, refunds, and payment issues",
    backstory="You are a billing specialist with deep knowledge of payment systems.",
    allow_delegation=False,
)

# Tasks — the Supervisor (manager_llm) decides which agent handles each
tasks = [
    Task(
        description="Analyze the following customer issue and provide a resolution: {query}",
        expected_output="A clear resolution addressing the customer's concern",
    ),
]

# The Crew in hierarchical mode uses manager_llm as the Hymoex Supervisor
# It automatically routes tasks to the right expert based on the query
crew = Crew(
    agents=[legal_agent, tech_agent, billing_agent],
    tasks=tasks,
    process="hierarchical",  # KEY: This enables supervisor-style routing
    manager_llm="gpt-4o-mini",  # The Supervisor LLM that decides routing
    verbose=True,
)


if __name__ == "__main__":
    print("\nCrewAI + Hymoex M2: Hierarchical process with manager_llm as Supervisor")
    print("process='hierarchical' = Hymoex Supervisor pattern")
    print("process='sequential' = Hymoex M1 pattern (no supervisor)")
    # Uncomment to run (requires API key):
    # result = crew.kickoff(inputs={"query": "My contract terms were violated"})
    # print(result)
