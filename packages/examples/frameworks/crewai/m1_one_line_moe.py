"""Example: CrewAI + Hymoex M1 (One-Line MoE).

Two experts working sequentially with no supervisor.
CrewAI's process="sequential" maps to M1's flat expert execution (no routing).

Requires: pip install crewai
"""

from crewai import Agent, Crew, Task

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE, validate_topology


# --- Hymoex M1: Manager -> Experts (no Supervisor) ---

topology = OneLineMoE(
    manager=ManagerSpec(objective="Generate content"),
    experts=[
        ExpertSpec(domain="writer", skills=["copywriting"]),
        ExpertSpec(domain="editor", skills=["grammar"]),
    ],
)
print(f"Topology: M1, valid: {validate_topology(topology)['valid']}")


# --- CrewAI Implementation ---

writer = Agent(
    role="Writer",
    goal="Write compelling content",
    backstory="You are an experienced copywriter.",
)

editor = Agent(
    role="Editor",
    goal="Review and polish content",
    backstory="You are a meticulous editor.",
)

# M1 pattern: parallel execution, no supervisor coordination
crew = Crew(
    agents=[writer, editor],
    tasks=[
        Task(description="Write a blog post about AI agents", agent=writer),
        Task(description="Review and edit the blog post", agent=editor),
    ],
    process="sequential",  # Writer then editor
    verbose=True,
)

if __name__ == "__main__":
    print("\nCrewAI + Hymoex M1: Two experts, no supervisor")
    # result = crew.kickoff()  # Uncomment to run (requires API key)
