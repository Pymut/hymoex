# Hymoex

Type definitions for the **Hymoex** (Hybrid Modular Coordinated Experts) architectural paradigm — Pydantic models for designing scalable multi-agent systems.

## Installation

```bash
cd packages/hymoex-python
uv sync

# Or with pip
pip install -e .
```

## Usage

```python
from hymoex import (
    ExpertSpec, ManagerSpec, SupervisorSpec,
    OneLineSupervisor, auto_select_modality, validate_topology,
)

# Define agent specs
manager = ManagerSpec(objective="Customer support", strategy="route_by_domain")
supervisor = SupervisorSpec(routing="dependency_aware")
experts = [
    ExpertSpec(domain="legal", skills=["contracts"]),
    ExpertSpec(domain="tech", skills=["debugging"]),
    ExpertSpec(domain="billing", skills=["invoicing"]),
]

# Auto-select modality
modality = auto_select_modality(experts)  # -> "m2"

# Build and validate topology
system = OneLineSupervisor(manager=manager, supervisor=supervisor, experts=experts)
validation = validate_topology(system)
config = system.to_config()  # Export as JSON for your framework
```

## Three Modalities

| Modality | Experts | Class | Use Case |
|----------|---------|-------|----------|
| One-Line MoE | k ≤ 2 | `OneLineMoE` | Simple parallel tasks |
| One-Line Supervisor | 3-5 | `OneLineSupervisor` | Coordinated workflows |
| MoE MultiLine | 5+ | `MultiLine` | Enterprise-scale teams |

## Progressive Migration

```python
from hymoex import OneLineMoE, migrate_m1_to_m2, migrate_m2_to_m3

# Start simple (M1)
m1 = OneLineMoE(manager=manager, experts=[expert_a, expert_b])

# Scale up — 100% of existing agents preserved
m2 = migrate_m1_to_m2(m1, additional_experts=[expert_c])
m3 = migrate_m2_to_m3(m2)
```

## Development

```bash
# Run tests
uv run python -m pytest tests/unit/ --override-ini="addopts=" -v

# Lint
uv run ruff check src/

# Type check
uv run mypy src/
```

## Package Structure

```
src/hymoex/
  taxonomy/      # Role enum, agent specs (ManagerSpec, ExpertSpec, etc.)
  messaging/     # 7 HIP message types (Pydantic v2)
  modalities/    # OneLineMoE, OneLineSupervisor, MultiLine topologies
  moe/           # Gating algorithm, Rational-Raffle fusion
  migration/     # Progressive M1 -> M2 -> M3 transformations
  analysis/      # Topology classification and validation
  protocols/     # Base types (SignalVector, GatingResult)
```

## License

MIT
