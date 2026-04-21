"""Example: LangGraph + Hymoex M1 (One-Line MoE).

Two experts working in parallel with no supervisor.
The Manager (entry point) routes directly to experts via MoE gating.

Requires: pip install langgraph
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE, validate_topology


# --- Hymoex M1: Manager -> Experts (no Supervisor) ---

topology = OneLineMoE(
    manager=ManagerSpec(objective="Generate and review content"),
    experts=[
        ExpertSpec(domain="writer", skills=["copywriting"]),
        ExpertSpec(domain="editor", skills=["grammar", "style"]),
    ],
)
print(f"Topology: M1, valid: {validate_topology(topology)['valid']}")


# --- LangGraph Implementation ---

class State(TypedDict):
    query: str
    writer_output: str
    editor_output: str
    final: str


def writer_node(state: State) -> State:
    """Writer expert — generates content."""
    return {**state, "writer_output": f"[Writer] Draft for: {state['query']}"}


def editor_node(state: State) -> State:
    """Editor expert — reviews content."""
    return {**state, "editor_output": f"[Editor] Reviewed: {state['writer_output']}"}


def merge_node(state: State) -> State:
    """Manager merges expert outputs (no supervisor needed in M1)."""
    return {**state, "final": f"{state['editor_output']} | Final version ready."}


graph = StateGraph(State)
graph.add_node("writer", writer_node)
graph.add_node("editor", editor_node)
graph.add_node("merge", merge_node)

# M1 pattern: Manager routes directly to experts, then merges
graph.set_entry_point("writer")
graph.add_edge("writer", "editor")
graph.add_edge("editor", "merge")
graph.add_edge("merge", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"query": "Write a blog post about AI agents", "writer_output": "", "editor_output": "", "final": ""})
    print(f"Result: {result['final']}")
