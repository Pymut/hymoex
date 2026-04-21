"""Shared fixtures for Hymoex benchmarks."""

import sys
from pathlib import Path

# Add hymoex-python/src and benchmarks dir to path
_repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_repo_root / "packages" / "hymoex-python" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load .env before any test module checks GEMINI_API_KEY
from dotenv import load_dotenv
load_dotenv(_repo_root / ".env")

import pytest

from hymoex import (
    ExpertSpec,
    ManagerSpec,
    MsgPacket,
    SupervisorSpec,
)


@pytest.fixture
def sample_message():
    return MsgPacket(
        channel="web",
        customer_id="bench_user",
        payload="I need help with my invoice, it doesn't match the contract terms we agreed on",
    )


@pytest.fixture
def make_experts():
    """Factory for creating N expert specs with distinct domains."""
    def _make(n: int, domains: list[str] | None = None) -> list[ExpertSpec]:
        if domains is None:
            domains = [f"domain_{i}" for i in range(n)]
        return [
            ExpertSpec(domain=d, skills=[f"skill_{d}"])
            for d in domains[:n]
        ]
    return _make


@pytest.fixture
def manager():
    return ManagerSpec(objective="benchmark", strategy="route_by_domain")


@pytest.fixture
def supervisor():
    return SupervisorSpec(routing="dependency_aware")
