# Hymoex Benchmarks

Reproducibility scripts for the benchmark results presented in the Hymoex paper.

## Prerequisites

```bash
cd packages/hymoex-python
uv sync
```

## Running All Benchmarks

From the repository root:

```bash
uv run python packages/research/benchmarks/run_all.py
```

This runs all 4 benchmark categories and prints a formatted summary table matching the paper's Table 3.

## Individual Benchmarks

Run a single category with pytest:

```bash
cd packages/hymoex-python

# Coordination overhead (Table 3a)
uv run pytest ../../packages/research/benchmarks/coordination-overhead/ -v -s

# Expert selection accuracy (Table 3b)
uv run pytest ../../packages/research/benchmarks/expert-selection/ -v -s

# Scalability (Table 3c)
uv run pytest ../../packages/research/benchmarks/scalability/ -v -s

# Migration cost (Table 3d)
uv run pytest ../../packages/research/benchmarks/migration-cost/ -v -s
```

Use `-s` to see printed metric output from each test.

## Benchmark Categories

| Category                 | What it measures                                    | Paper reference |
| ------------------------ | --------------------------------------------------- | --------------- |
| `coordination-overhead/` | Token cost across topologies (flat vs hierarchical) | Table 3, Q1     |
| `expert-selection/`      | MoE gating accuracy vs baselines                    | Table 3, Q3     |
| `scalability/`           | Latency degradation at 2-15 agents                  | Table 3, Q1     |
| `migration-cost/`        | Agent preservation across M1->M2->M3                | Table 3, Q2     |

## Notes

- All benchmarks use `MockLLMProvider` for deterministic, reproducible results
- No API keys or external services required
- The `conftest.py` in this directory provides shared fixtures (sample messages, expert factories)
- The `run_all.py` script parses pytest output to extract key metrics and format them into Table 3

**Made with ❤️ by the Pymut lab**
