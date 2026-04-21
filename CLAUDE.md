# CLAUDE.md — Hymoex

## Project Overview

Hymoex (Hybrid Modular Coordinated Experts) is an architectural paradigm for scalable multi-agent systems. It is NOT a library or framework — it defines patterns (taxonomy, modalities, protocols) that you apply using your preferred execution framework (LangGraph, CrewAI, Pydantic AI, etc.).

## Repository Structure

- **Monorepo** managed with Turborepo + pnpm (Node) and uv (Python)
- `packages/hymoex-python/` — Type definitions and pattern library (Pydantic models for roles, topologies, messaging)
- `packages/examples/architecture/` — Pure Hymoex pattern definitions (M1, M2, M3)
- `packages/examples/frameworks/` — Implementations using each framework (LangGraph, CrewAI, Pydantic AI, AutoGen, Swarm, Vercel AI SDK, Mastra)
- `packages/examples/use-cases/` — Domain-specific examples
- `packages/research/benchmarks/` — Reproducible benchmark suites (Gemini API)
- `apps/docs/` — Next.js 15 documentation site (Fumadocs)
- `apps/sandbox/` — Interactive CLI, notebooks, scenarios
- `apps/skills/` — Claude Code skill installers

## Development Commands

```bash
# Python core — from packages/hymoex-python/
uv sync                                                          # Install dependencies
uv run python -m pytest tests/unit/ --override-ini="addopts=" -v # Unit tests
uv run ruff check src/                                           # Lint
uv run ruff format --check src/                                  # Format check

# Benchmarks — from packages/hymoex-python/
uv run python -m pytest ../../packages/research/benchmarks/ --override-ini="addopts=" -v -s

# Monorepo — from root
pnpm install          # Install Node dependencies
pnpm run build        # Build all packages (turbo)
pnpm run test         # Run all tests (turbo)
pnpm run lint         # Lint all packages (turbo)
```

## Key Conventions

- Python 3.10+ required, targets 3.12
- Pydantic v2 for all models and validation
- mypy strict mode enabled
- Ruff + Black for formatting (line length 100)
- All public API exported via `src/hymoex/__init__.py` with `__all__`
- Tests use pytest + pytest-asyncio (asyncio_mode = auto)
- No external LLM API keys needed for unit tests (benchmarks require GEMINI_API_KEY)

## Architecture Concepts

- **Roles:** Manager, Integrator, ExpertManager, Supervisor, Expert, Executor, Perceiver
- **Modalities:** M1 (OneLineMoE, k<=2), M2 (OneLineSupervisor, 3-5), M3 (MultiLine, 5+)
- **HIP Protocol:** 7 message types (MsgPacket, ContextEnvelope, DecisionRequest, ExpertPayload, ExecCommand, ExecReceipt, Telemetry)
- **Migration:** M1 -> M2 -> M3 with 100% agent preservation (additive changes only)
