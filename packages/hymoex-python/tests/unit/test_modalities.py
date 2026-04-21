"""Tests for modality topologies — validation, not execution."""

import pytest
from pydantic import ValidationError

from hymoex import (
    ManagerSpec,
    SupervisorSpec,
    ExpertSpec,
    ExpertManagerSpec,
    IntegratorSpec,
    OneLineMoE,
    OneLineSupervisor,
    MultiLine,
    Team,
)


class TestOneLineMoE:
    def test_rejects_more_than_2(self):
        with pytest.raises(ValidationError):
            OneLineMoE(
                manager=ManagerSpec(),
                experts=[ExpertSpec(domain=f"d{i}") for i in range(3)],
            )

    def test_accepts_1_or_2(self):
        for n in [1, 2]:
            system = OneLineMoE(
                manager=ManagerSpec(),
                experts=[ExpertSpec(domain=f"d{i}") for i in range(n)],
            )
            assert len(system.experts) == n

    def test_agent_count(self):
        system = OneLineMoE(
            manager=ManagerSpec(),
            experts=[ExpertSpec(), ExpertSpec()],
        )
        assert system.agent_count == 3

    def test_to_config(self):
        system = OneLineMoE(manager=ManagerSpec(), experts=[ExpertSpec()])
        config = system.to_config()
        assert config["modality"] == "one_line_moe"


class TestOneLineSupervisor:
    def test_accepts_3_to_5(self):
        for n in [3, 4, 5]:
            system = OneLineSupervisor(
                manager=ManagerSpec(),
                supervisor=SupervisorSpec(),
                experts=[ExpertSpec(domain=f"d{i}") for i in range(n)],
            )
            assert len(system.experts) == n

    def test_rejects_less_than_3(self):
        with pytest.raises(ValidationError):
            OneLineSupervisor(
                manager=ManagerSpec(),
                supervisor=SupervisorSpec(),
                experts=[ExpertSpec()],
            )

    def test_agent_count(self):
        system = OneLineSupervisor(
            manager=ManagerSpec(),
            supervisor=SupervisorSpec(),
            experts=[ExpertSpec() for _ in range(3)],
        )
        assert system.agent_count == 5  # manager + supervisor + 3 experts


class TestMultiLine:
    def test_creates_with_teams(self):
        teams = [
            Team(name="a", supervisor=SupervisorSpec(), experts=[ExpertSpec() for _ in range(3)]),
            Team(name="b", supervisor=SupervisorSpec(), experts=[ExpertSpec() for _ in range(3)]),
        ]
        system = MultiLine(
            manager=ManagerSpec(),
            integrators=[IntegratorSpec()],
            expert_manager=ExpertManagerSpec(),
            teams=teams,
        )
        assert len(system.all_experts()) == 6

    def test_to_config(self):
        system = MultiLine(
            manager=ManagerSpec(),
            integrators=[IntegratorSpec()],
            expert_manager=ExpertManagerSpec(),
            teams=[Team(name="t1", supervisor=SupervisorSpec(), experts=[ExpertSpec()])],
        )
        config = system.to_config()
        assert config["modality"] == "multi_line"
        assert len(config["teams"]) == 1
