# Intermediate Examples: One-Line Supervisor (M2)

**Purpose:** Patterns for coordinated multi-expert systems with supervisor routing.

---

## Example 1: Customer Support Triage (M2)

**Use Case:** 3 domain experts coordinated by a supervisor that routes based on query intent.

**Architecture:**
```
Manager → Supervisor → [Legal Expert, Tech Expert, Billing Expert]
                    ↑                                    |
                    └──── Perceiver (feedback) ──────────┘
```

**Hymoex Topology:**
```python
from hymoex import ExpertSpec, ManagerSpec, SupervisorSpec, OneLineSupervisor

system = OneLineSupervisor(
    manager=ManagerSpec(objective="Resolve customer issues", strategy="route_by_domain"),
    supervisor=SupervisorSpec(routing="dependency_aware"),
    experts=[
        ExpertSpec(domain="legal", skills=["contracts", "compliance", "disputes"]),
        ExpertSpec(domain="tech", skills=["debugging", "infrastructure", "API"]),
        ExpertSpec(domain="billing", skills=["invoicing", "refunds", "payments"]),
    ],
)
```

**LangGraph Implementation:**
```python
from langgraph.graph import StateGraph, END

graph = StateGraph(State)

# Supervisor analyzes query and routes
graph.add_node("supervisor", supervisor_route)
graph.add_node("legal", legal_expert)
graph.add_node("tech", tech_expert)
graph.add_node("billing", billing_expert)

graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", route_to_expert, {
    "legal": "legal", "tech": "tech", "billing": "billing",
})
graph.add_edge("legal", END)
graph.add_edge("tech", END)
graph.add_edge("billing", END)
```

**CrewAI Implementation:**
```python
from crewai import Agent, Crew

crew = Crew(
    agents=[legal_agent, tech_agent, billing_agent],
    tasks=[support_task],
    process="hierarchical",    # Supervisor pattern
    manager_llm="gpt-4o-mini", # LLM acts as supervisor
)
```

---

## Example 2: Content Pipeline with Dependencies (M2)

**Use Case:** Sequential content creation where each expert depends on the previous output.

**Architecture:**
```
Manager → Supervisor → Research Expert → Writer Expert → Editor Expert
                       (step 1)          (step 2)        (step 3)
```

**Key Pattern:** Supervisor manages **dependency ordering** — the Editor can't run until the Writer finishes, which can't run until Research finishes.

**Hymoex Topology:**
```python
system = OneLineSupervisor(
    manager=ManagerSpec(objective="Create published content"),
    supervisor=SupervisorSpec(routing="dependency_aware"),
    experts=[
        ExpertSpec(domain="research", skills=["web_search", "summarization"]),
        ExpertSpec(domain="writing", skills=["copywriting", "SEO"]),
        ExpertSpec(domain="editing", skills=["grammar", "style", "fact_check"]),
    ],
)
```

**When to use M2 over M1:** When experts have **dependencies** between them. M1 is for parallel/independent experts. M2 adds a Supervisor to manage execution order.

---

## Example 3: Multi-Domain Query (M2)

**Use Case:** A query that needs input from multiple experts, with the supervisor merging responses.

**Architecture:**
```
Manager → Supervisor ──→ Expert A ──→ Response A ─┐
                    └──→ Expert B ──→ Response B ──┤→ Supervisor merges → Final Response
                    └──→ Expert C ──→ Response C ─┘
```

**Key Pattern:** The Supervisor runs multiple experts in parallel, then **fuses** their responses using the Rational-Raffle algorithm (highest confidence + relevance wins).

**Hymoex MoE Gating:**
```python
from hymoex.moe.gate import gate_experts, GatingConfig
from hymoex.messaging.types import DecisionRequest

# Signal vector represents query intent
request = DecisionRequest(intent_embedding=[0.4, 0.5, 0.1], lead_score=0.7)

# Gate selects top-k experts
result = gate_experts(request, expert_weights, config=GatingConfig(top_k=2))
# result.selected_experts = ["tech", "billing"]  (top 2 by score)
```

---

## Example 4: Supervisor with Perceiver Feedback (M2)

**Use Case:** Real-time feedback loop where the Perceiver monitors execution quality.

**Architecture:**
```
Manager → Supervisor → Expert → Executor → Perceiver
              ↑                                |
              └──── telemetry feedback ────────┘
```

**Key Pattern:** The Perceiver captures telemetry (sentiment, latency, success rate) and feeds it back to the Supervisor, which adjusts routing for future queries.

```python
from hymoex import PerceiverSpec, ExecutorSpec

system = OneLineSupervisor(
    manager=ManagerSpec(objective="Customer support with feedback"),
    supervisor=SupervisorSpec(routing="dependency_aware"),
    experts=[
        ExpertSpec(domain="legal", skills=["contracts"]),
        ExpertSpec(domain="tech", skills=["debugging"]),
        ExpertSpec(domain="billing", skills=["invoicing"]),
    ],
    executors=[ExecutorSpec(action_type="crm_update")],
    perceivers=[PerceiverSpec(sensor_type="sentiment")],
)
```

---

**Document Version:** 1.0.0
**Last Updated:** 2026-04-21
