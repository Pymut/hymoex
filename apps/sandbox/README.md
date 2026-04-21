# Hymoex Sandbox

An interactive environment for experimenting with the Hymoex cognitive architecture. Try different modalities, swap experts, and see results — without writing a full application.

## Quick Start

```bash
# From the repo root — install the library first
cd packages/hymoex-python
uv sync

# Run a pre-built scenario
uv run python apps/sandbox/scenarios/customer_support.py

# Launch the CLI
uv run python apps/sandbox/cli/main.py

# Open Jupyter notebooks
cd apps/sandbox/notebooks
jupyter lab
```

## What's Inside

```
sandbox/
  cli/            # Command-line interface to spin up systems
  notebooks/      # Jupyter notebooks for interactive experimentation
  scenarios/      # Pre-built scenarios to run and modify
```

## Scenarios

| Scenario | Modality | Experts | What it does |
|----------|----------|---------|-------------|
| `customer_support.py` | M2 | Legal, Tech, Billing | Routes customer queries to the right expert |
| `content_pipeline.py` | M1 | Writer, Editor | Parallel content generation |
| `enterprise.py` | M3 | Multi-team | Progressive migration M1 → M2 → M3 |


**Made with ❤️ by the Pymut lab**