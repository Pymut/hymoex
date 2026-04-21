# Hymoex Cognitive Architecture

<div align="center">

**Hybrid Modular Coordinated Experts — An architectural paradigm for scalable multi-agent systems**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-55%20passing-brightgreen.svg)]()

[Documentation](apps/docs/) | [Quick Start](#quick-start) | [Examples](packages/examples/) | [Paper](papers/hymoex-cognitive-architecture.pdf)

</div>

---

## What is Hymoex?

**Hymoex** (Hybrid Modular Coordinated Experts) is an architectural paradigm for multi-agent systems. It is **not** a library or framework — it defines patterns that you apply using your preferred execution framework (LangGraph, CrewAI, Pydantic AI, etc.).

Hymoex solves four critical problems:

1. **Architecture Decision Paralysis** — clear decision framework based on expert count
2. **Expert Coordination Breakdown** — MoE gating with 96.7% selection accuracy
3. **Brittle Scalability** — progressive migration preserving 100% of existing agents
4. **Framework Fragmentation** — patterns for 7 major frameworks

## Three Modalities

| Modality                | Experts | Use Case               |
| ----------------------- | ------- | ---------------------- |
| **One-Line MoE**        | k ≤ 2   | Simple parallel tasks  |
| **One-Line Supervisor** | 3-5     | Coordinated workflows  |
| **MoE MultiLine**       | 5+      | Enterprise-scale teams |

## Quick Start

```bash
git clone https://github.com/Pymut/hymoex.git
cd hymoex/packages/hymoex-python
uv sync
```

### Define your architecture

```python
from hymoex import (
    ExpertSpec, ManagerSpec, SupervisorSpec,
    OneLineSupervisor, auto_select_modality, validate_topology,
)

# Define agent specs (what each agent IS, not how it runs)
manager = ManagerSpec(objective="Customer support", strategy="route_by_domain")
supervisor = SupervisorSpec(routing="dependency_aware")

experts = [
    ExpertSpec(domain="legal", skills=["contracts"]),
    ExpertSpec(domain="tech", skills=["debugging"]),
    ExpertSpec(domain="billing", skills=["invoicing"]),
]

# Auto-select modality based on expert count
modality = auto_select_modality(experts)  # -> "m2"

# Build and validate topology
system = OneLineSupervisor(manager=manager, supervisor=supervisor, experts=experts)
validation = validate_topology(system)
config = system.to_config()  # Export as JSON for your framework
```

### Implement with your framework

```python
# LangGraph example
from langgraph.graph import StateGraph, END

graph = StateGraph(State)
graph.add_node("supervisor", supervisor_node)  # Hymoex Supervisor role
graph.add_node("legal", legal_expert)          # Hymoex Expert role
graph.add_node("tech", tech_expert)
graph.add_node("billing", billing_expert)
```

See `packages/examples/frameworks/` for complete examples per framework.

## Progressive Migration

```python
from hymoex import OneLineMoE, migrate_m1_to_m2, migrate_m2_to_m3

# Start small (M1)
m1 = OneLineMoE(manager=manager, experts=[expert_a, expert_b])

# Scale up — all original agents preserved
m2 = migrate_m1_to_m2(m1, additional_experts=[expert_c])
m3 = migrate_m2_to_m3(m2)
```

## Framework Examples

Hymoex is a paradigm, not a library. Use your preferred framework — apply Hymoex patterns:

| Framework     | Example                                                | Hymoex Pattern                          |
| ------------- | ------------------------------------------------------ | --------------------------------------- |
| Pydantic AI   | [example](packages/examples/frameworks/pydantic-ai/)   | M1, M2, M3 — Agent delegation           |
| LangGraph     | [example](packages/examples/frameworks/langgraph/)     | M1, M2, M3 — StateGraph with sub-graphs |
| CrewAI        | [example](packages/examples/frameworks/crewai/)        | M1, M2, M3 — Hierarchical process       |
| AutoGen       | [example](packages/examples/frameworks/autogen/)       | M1, M2, M3 — Nested GroupChats          |
| OpenAI Swarm  | [example](packages/examples/frameworks/openai-swarm/)  | M1, M2, M3 — Chained handoffs           |
| Vercel AI SDK | [example](packages/examples/frameworks/vercel-ai-sdk/) | M1, M2, M3 — Nested tool delegation     |
| Mastra        | [example](packages/examples/frameworks/mastra/)        | M1, M2, M3 — Workflow composition       |

## Repository Structure

```
packages/
  hymoex-python/       # Type definitions (taxonomy, modalities, protocols)
    src/hymoex/        # Pydantic models for roles, topologies, messaging
    tests/             # Unit tests
  examples/
    architecture/      # Pure Hymoex pattern definitions (M1, M2, M3)
    frameworks/        # Implementations per framework (7 frameworks x 3 modalities)
    use-cases/         # Domain-specific examples
  research/
    benchmarks/        # Reproducible benchmarks (Gemini API)
apps/
  sandbox/             # Interactive sandbox (CLI, notebooks, scenarios)
  docs/                # Documentation site
  skills/              # Claude Code skill (hymoex-architect)
```

## Running Tests

```bash
cd packages/hymoex-python

# Unit tests
uv run python -m pytest tests/unit/ --override-ini="addopts=" -v

# Benchmarks (requires GEMINI_API_KEY in .env)
uv run python -m pytest ../../packages/research/benchmarks/ --override-ini="addopts=" -v -s
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Citation

```bibtex
@software{timana2026hymoex,
  title = {Hymoex: A Hybrid Modular Cognitive Architecture for Scalable Multi-Agent Expert Coordination},
  author = {Timana, Joel and Munoz, Diana and Munoz, Alvaro},
  year = {2026},
  url = {https://github.com/Pymut/hymoex}
}
```

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Pymut Lab** | [Paper](papers/hymoex-cognitive-architecture.pdf) | [Docs](apps/docs/)

</div>

**Made with 💚 by the Pymut lab**
