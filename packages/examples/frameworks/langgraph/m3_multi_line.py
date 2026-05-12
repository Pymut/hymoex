"""Example: LangGraph + Hymoex M3 (MoE MultiLine).

Uses LangGraph's sub-graph composition: each Hymoex Team is a
compiled sub-graph with its own internal nodes. The top-level graph
routes across teams via an Integrator node.

This is the key differentiator from M2 — M2 uses conditional edges
on a flat graph; M3 uses nested sub-graphs for team encapsulation.

Requires: pip install langgraph
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph

import sys
sys.path.insert(0, "../../../../packages/hymoex-python/src")
from hymoex import (
    ExpertManagerSpec, ExpertSpec, IntegratorSpec, ManagerSpec,
    MultiLine, SupervisorSpec, Team, validate_topology,
)


# --- Hymoex M3: Manager -> Integrators -> Expert Manager -> Teams ---

topology = MultiLine(
    manager=ManagerSpec(objective="Enterprise customer onboarding"),
    integrators=[IntegratorSpec()],
    expert_manager=ExpertManagerSpec(),
    teams=[
        Team(name="finance", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="contracts", skills=["drafting"]),
            ExpertSpec(domain="payments", skills=["processing"]),
        ]),
        Team(name="hr", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="onboarding", skills=["new_hires"]),
            ExpertSpec(domain="compliance", skills=["regulations"]),
        ]),
    ],
)
print(f"Topology: M3, valid: {validate_topology(topology)['valid']}, agents: {topology.agent_count}")


# --- LangGraph Implementation: Sub-graphs per team ---

class TeamState(TypedDict):
    query: str
    expert: str
    response: str


class TopState(TypedDict):
    query: str
    team: str
    response: str


# ---- Finance Team Sub-graph (Hymoex Team = LangGraph Sub-graph) ----

def finance_supervisor(state: TeamState) -> TeamState:
    """Finance team supervisor routes to contracts or payments expert."""
    q = state["query"].lower()
    if any(w in q for w in ["contract", "agreement", "terms"]):
        return {**state, "expert": "contracts"}
    return {**state, "expert": "payments"}


def contracts_expert(state: TeamState) -> TeamState:
    return {**state, "response": f"[Finance/Contracts] Drafting for: {state['query']}"}


def payments_expert(state: TeamState) -> TeamState:
    return {**state, "response": f"[Finance/Payments] Processing: {state['query']}"}


def route_finance_expert(state: TeamState) -> str:
    return state["expert"]


finance_graph = StateGraph(TeamState)
finance_graph.add_node("supervisor", finance_supervisor)
finance_graph.add_node("contracts", contracts_expert)
finance_graph.add_node("payments", payments_expert)
finance_graph.set_entry_point("supervisor")
finance_graph.add_conditional_edges("supervisor", route_finance_expert, {
    "contracts": "contracts",
    "payments": "payments",
})
finance_graph.add_edge("contracts", END)
finance_graph.add_edge("payments", END)
finance_team = finance_graph.compile()  # Compiled sub-graph


# ---- HR Team Sub-graph ----

def hr_supervisor(state: TeamState) -> TeamState:
    q = state["query"].lower()
    if any(w in q for w in ["onboard", "new hire", "welcome"]):
        return {**state, "expert": "onboarding"}
    return {**state, "expert": "compliance"}


def onboarding_expert(state: TeamState) -> TeamState:
    return {**state, "response": f"[HR/Onboarding] Processing: {state['query']}"}


def compliance_expert(state: TeamState) -> TeamState:
    return {**state, "response": f"[HR/Compliance] Checking: {state['query']}"}


def route_hr_expert(state: TeamState) -> str:
    return state["expert"]


hr_graph = StateGraph(TeamState)
hr_graph.add_node("supervisor", hr_supervisor)
hr_graph.add_node("onboarding", onboarding_expert)
hr_graph.add_node("compliance", compliance_expert)
hr_graph.set_entry_point("supervisor")
hr_graph.add_conditional_edges("supervisor", route_hr_expert, {
    "onboarding": "onboarding",
    "compliance": "compliance",
})
hr_graph.add_edge("onboarding", END)
hr_graph.add_edge("compliance", END)
hr_team = hr_graph.compile()  # Compiled sub-graph


# ---- Top-level Graph: Integrator routes to team sub-graphs ----

def integrator_node(state: TopState) -> TopState:
    """Integrator routes to the correct team (cross-team coordination)."""
    q = state["query"].lower()
    if any(w in q for w in ["contract", "payment", "invoice", "payroll"]):
        return {**state, "team": "finance"}
    return {**state, "team": "hr"}


def run_finance_team(state: TopState) -> TopState:
    """Execute the finance sub-graph."""
    result = finance_team.invoke({"query": state["query"], "expert": "", "response": ""})
    return {**state, "response": result["response"]}


def run_hr_team(state: TopState) -> TopState:
    """Execute the HR sub-graph."""
    result = hr_team.invoke({"query": state["query"], "expert": "", "response": ""})
    return {**state, "response": result["response"]}


def route_to_team(state: TopState) -> str:
    return state["team"]


top_graph = StateGraph(TopState)
top_graph.add_node("integrator", integrator_node)
top_graph.add_node("finance", run_finance_team)
top_graph.add_node("hr", run_hr_team)
top_graph.set_entry_point("integrator")
top_graph.add_conditional_edges("integrator", route_to_team, {
    "finance": "finance",
    "hr": "hr",
})
top_graph.add_edge("finance", END)
top_graph.add_edge("hr", END)

app = top_graph.compile()

if __name__ == "__main__":
    queries = [
        "Draft the employment contract for John",
        "Set up payroll for the new employee",
        "Complete onboarding checklist for Maria",
        "Check compliance for international hiring",
    ]
    for q in queries:
        result = app.invoke({"query": q, "team": "", "response": ""})
        print(f"  '{q}' -> {result['response']}")
