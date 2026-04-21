# Advanced Examples: MoE MultiLine (M3)

**Purpose:** Patterns for enterprise-scale multi-team systems with integrators and progressive migration.

---

## Example 1: Enterprise Onboarding System (M3)

**Use Case:** Multi-team system for employee onboarding across finance, HR, and IT domains.

**Architecture:**
```
Manager
├── Integrator (cross-team routing)
├── Expert Manager (MoE gating across all experts)
│
├── Finance Team
│   ├── Team Supervisor
│   ├── Contracts Expert
│   └── Payments Expert
│
├── HR Team
│   ├── Team Supervisor
│   ├── Onboarding Expert
│   └── Compliance Expert
│
└── IT Team
    ├── Team Supervisor
    ├── Access Expert
    └── Equipment Expert
```

**Hymoex Topology:**
```python
from hymoex import (
    ExpertManagerSpec, ExpertSpec, IntegratorSpec,
    ManagerSpec, SupervisorSpec, MultiLine, Team, validate_topology,
)

system = MultiLine(
    manager=ManagerSpec(objective="Employee onboarding"),
    integrators=[IntegratorSpec()],
    expert_manager=ExpertManagerSpec(),
    teams=[
        Team(name="finance", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="contracts", skills=["drafting", "review"]),
            ExpertSpec(domain="payments", skills=["payroll", "benefits"]),
        ]),
        Team(name="hr", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="onboarding", skills=["new_hires", "orientation"]),
            ExpertSpec(domain="compliance", skills=["regulations", "audit"]),
        ]),
        Team(name="it", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="access", skills=["accounts", "permissions"]),
            ExpertSpec(domain="equipment", skills=["laptop", "software"]),
        ]),
    ],
)

validation = validate_topology(system)
print(f"Agents: {system.agent_count}, Valid: {validation['valid']}")
```

**LangGraph Implementation (Sub-graphs):**
```python
# Each team is a compiled sub-graph
finance_graph = StateGraph(TeamState)
finance_graph.add_node("supervisor", finance_supervisor)
finance_graph.add_node("contracts", contracts_expert)
finance_graph.add_node("payments", payments_expert)
finance_team = finance_graph.compile()

# Top-level graph routes to team sub-graphs
top_graph = StateGraph(TopState)
top_graph.add_node("integrator", integrator_node)
top_graph.add_node("finance", lambda s: finance_team.invoke(s))
top_graph.add_node("hr", lambda s: hr_team.invoke(s))
top_graph.add_node("it", lambda s: it_team.invoke(s))
```

---

## Example 2: Progressive Migration (M1 → M2 → M3)

**Use Case:** Start with 2 experts, grow to enterprise scale without rewriting.

### Step 1: Start with M1 (2 experts)

```python
from hymoex import ExpertSpec, ManagerSpec, OneLineMoE

m1 = OneLineMoE(
    manager=ManagerSpec(objective="Customer support"),
    experts=[
        ExpertSpec(domain="tech", skills=["debugging"]),
        ExpertSpec(domain="billing", skills=["invoicing"]),
    ],
)
# 3 agents total (Manager + 2 Experts)
```

### Step 2: Migrate to M2 (add 3rd expert → needs Supervisor)

```python
from hymoex import migrate_m1_to_m2

m2 = migrate_m1_to_m2(m1, additional_experts=[
    ExpertSpec(domain="legal", skills=["contracts"]),
])
# Original tech + billing experts preserved
# Added: 1 Supervisor + 1 Legal Expert
# 5 agents total
```

### Step 3: Migrate to M3 (add teams)

```python
from hymoex import migrate_m2_to_m3, Team, MultiLine

m3 = migrate_m2_to_m3(m2, team_name="support")

# Add a second team
m3_expanded = MultiLine(
    manager=m3.manager,
    integrators=m3.integrators,
    expert_manager=m3.expert_manager,
    teams=[
        *m3.teams,
        Team(name="sales", supervisor=SupervisorSpec(), experts=[
            ExpertSpec(domain="pricing"),
            ExpertSpec(domain="crm"),
        ]),
    ],
)
# All original agents preserved (100%)
# Added: Integrator, Expert Manager, new team
```

**Key Guarantee:** Every migration preserves 100% of existing agent definitions. Only new coordination agents are added.

---

## Example 3: Real Estate Platform (Rehof Case Study)

**Use Case:** 36 agents across 3 domains handling 10,000+ concurrent conversations.

**Architecture:**
```
Manager
├── Channel Integrators (WhatsApp, Web, Voice)
├── Cross-Domain Integrator (routes by customer stage)
│
├── Marketing Domain
│   ├── Expert Manager MKT
│   ├── Team Attraction (lead generation)
│   ├── Team Cultivation (nurturing)
│   └── Team Discovery (property matching)
│
├── Sales Domain
│   ├── Expert Manager SALES
│   ├── Team CoCreation (3D floor plans, simulators)
│   ├── Team Validation (document verification)
│   └── Team Closing (contracts, payments)
│
└── Customer Service Domain
    ├── Expert Manager CS
    ├── Team Activation (onboarding)
    ├── Team Assistance (support)
    ├── Team Loyalty (NPS, retention)
    └── Team Expansion (upsell)
```

**Key M3 Patterns Used:**
- **Multiple Integrators:** Channel Integrators normalize multimodal input; Cross-Domain Integrator routes by customer lifecycle stage
- **Domain-level Expert Managers:** Each domain runs independent MoE gating
- **PDCA Feedback:** Perceivers in each team feed telemetry back to Supervisors
- **SLA Budgets:** Integrators manage <500ms routing latency

---

## Example 4: Text-to-SQL Platform (Ontop Case Study)

**Use Case:** Natural language queries against 75+ country-specific database schemas.

**Architecture:**
```
Manager
├── Integrator (query understanding)
├── Expert Manager (schema routing)
│
├── Contracts Team
│   ├── Team Supervisor
│   ├── Schema Expert (contracts tables)
│   └── SQL Expert (query generation)
│
├── Payments Team
│   ├── Team Supervisor
│   ├── Schema Expert (payroll tables)
│   └── SQL Expert (query generation)
│
├── Legal Team
│   ├── Team Supervisor
│   ├── Schema Expert (compliance tables)
│   └── Jurisdiction Expert (country-specific rules)
│
└── HR Team
    ├── Team Supervisor
    ├── Schema Expert (employee tables)
    └── SQL Expert (query generation)
```

**Key M3 Patterns Used:**
- **Expert Manager as MoE gate:** Routes queries to the team whose schema matches the query intent
- **Country-specific routing:** Jurisdiction Expert handles 75+ country variations
- **Progressive migration:** Started as M2 with 4 experts, grew to M3 with 15+ experts, modifying only 8% of existing code

---

## When to Choose M3

| Signal | Action |
|--------|--------|
| More than 5 domain experts | Consider M3 |
| Multiple distinct business domains | Use teams per domain |
| Cross-domain queries are common | Add Integrators |
| Need global expert pool optimization | Add Expert Manager |
| Teams need independent scaling | M3 teams scale independently |
| Latency budgets differ per domain | Integrators manage SLA budgets |

---

**Document Version:** 1.0.0
**Last Updated:** 2026-04-21
