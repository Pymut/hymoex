"""Example: Customer Support with LangGraph following Hymoex M2 pattern.

Demonstrates how to build a One-Line Supervisor (M2) system
using LangGraph's StateGraph, following Hymoex architectural patterns.

Hymoex defines the architecture (roles, topology, routing).
LangGraph provides the execution (state management, graph orchestration).

Requires: pip install langgraph langchain-openai
"""

from typing import TypedDict

# LangGraph provides the execution engine
from langgraph.graph import END, StateGraph

# Hymoex defines the architecture — use it to validate your design
import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import ExpertSpec, ManagerSpec, OneLineSupervisor, SupervisorSpec, validate_topology


# --- Step 1: Define your Hymoex architecture ---

manager = ManagerSpec(objective="Resolve customer issues", strategy="route_by_domain")
supervisor = SupervisorSpec(routing="dependency_aware")
experts = [
    ExpertSpec(domain="legal", skills=["contracts", "compliance"]),
    ExpertSpec(domain="tech", skills=["debugging", "infrastructure"]),
    ExpertSpec(domain="billing", skills=["invoicing", "refunds"]),
]

# Validate the topology before building
topology = OneLineSupervisor(manager=manager, supervisor=supervisor, experts=experts)
validation = validate_topology(topology)
print(f"Hymoex topology valid: {validation['valid']}, agents: {topology.agent_count}")


# --- Step 2: Implement with LangGraph ---

class State(TypedDict):
    query: str
    domain: str
    response: str


def supervisor_node(state: State) -> State:
    """Supervisor routes to the correct expert (Hymoex Supervisor role)."""
    query = state["query"].lower()
    if any(w in query for w in ["contract", "legal", "compliance"]):
        return {**state, "domain": "legal"}
    elif any(w in query for w in ["error", "api", "bug", "system"]):
        return {**state, "domain": "tech"}
    else:
        return {**state, "domain": "billing"}


def legal_expert(state: State) -> State:
    """Legal expert agent (Hymoex Expert role)."""
    return {**state, "response": f"[Legal] Reviewing: {state['query']}"}


def tech_expert(state: State) -> State:
    """Tech expert agent (Hymoex Expert role)."""
    return {**state, "response": f"[Tech] Diagnosing: {state['query']}"}


def billing_expert(state: State) -> State:
    """Billing expert agent (Hymoex Expert role)."""
    return {**state, "response": f"[Billing] Processing: {state['query']}"}


def route_to_expert(state: State) -> str:
    """Conditional edge — routes based on supervisor decision."""
    return state["domain"]


# Build the LangGraph StateGraph following Hymoex M2 topology
graph = StateGraph(State)

# Manager is implicit (the entry point)
# Supervisor routes to experts
graph.add_node("supervisor", supervisor_node)
graph.add_node("legal", legal_expert)
graph.add_node("tech", tech_expert)
graph.add_node("billing", billing_expert)

graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", route_to_expert, {
    "legal": "legal",
    "tech": "tech",
    "billing": "billing",
})
graph.add_edge("legal", END)
graph.add_edge("tech", END)
graph.add_edge("billing", END)

app = graph.compile()

# --- Step 3: Run ---

if __name__ == "__main__":
    test_queries = [
        "My contract terms were violated",
        "API returning 500 errors",
        "Invoice amount is incorrect",
    ]
    for q in test_queries:
        result = app.invoke({"query": q, "domain": "", "response": ""})
        print(f"  '{q}' -> {result['response']}")
