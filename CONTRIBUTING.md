# Contributing to Hymoex

Thank you for your interest in contributing to Hymoex! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [pnpm](https://pnpm.io/) (Node.js package manager)
- [Node.js](https://nodejs.org/) 18+

### Getting Started

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/hymoex.git
   cd hymoex
   ```

2. Install Node.js dependencies:

   ```bash
   pnpm install
   ```

3. Set up the Python core:

   ```bash
   cd packages/hymoex-python
   uv sync
   ```

4. Install pre-commit hooks:

   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Running Tests

```bash
cd packages/hymoex-python
uv run python -m pytest tests/unit/ --override-ini="addopts=" -v
```

## Running Linting

```bash
cd packages/hymoex-python
uv run ruff check src/
uv run ruff format --check src/
```

## Code Style

- **Formatter:** Black (line length 100)
- **Linter:** Ruff
- **Type checking:** mypy (optional, run manually)
- Line length: 100 characters
- Follow existing patterns in the codebase

## Pull Request Guidelines

1. Create a feature branch from `main`.
2. Keep PRs focused on a single change.
3. Write or update tests for your changes.
4. Ensure all CI checks pass before requesting review.
5. Write a clear PR description explaining the "why" behind your changes.
6. Reference any related issues (e.g., `Closes #42`).

## Reporting Issues

Use the [issue templates](https://github.com/pymut/hymoex/issues/new/choose) to report bugs or request features.

## License

By contributing, you agree that your contributions will be licensed under the project's existing license.
