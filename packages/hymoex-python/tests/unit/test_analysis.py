"""Tests for architecture analysis tools."""

from hymoex import (
    ExpertSpec,
    ExpertManagerSpec,
    IntegratorSpec,
    ManagerSpec,
    SupervisorSpec,
    OneLineMoE,
    OneLineSupervisor,
    MultiLine,
    Team,
    auto_select_modality,
    classify_topology,
    validate_topology,
)


class TestAutoSelectModality:
    def test_m1_for_1_or_2(self):
        for n in [1, 2]:
            experts = [ExpertSpec(domain=f"d{i}") for i in range(n)]
            assert auto_select_modality(experts) == "m1"

    def test_m2_for_3_to_5(self):
        for n in [3, 4, 5]:
            experts = [ExpertSpec(domain=f"d{i}") for i in range(n)]
            assert auto_select_modality(experts) == "m2"

    def test_m3_for_6_plus(self):
        for n in [6, 10, 20]:
            experts = [ExpertSpec(domain=f"d{i}") for i in range(n)]
            assert auto_select_modality(experts) == "m3"


class TestClassifyTopology:
    def test_flat_system(self):
        result = classify_topology(expert_count=2)
        assert result["current_modality"] == "m1"

    def test_supervised_system(self):
        result = classify_topology(has_supervisor=True, expert_count=4)
        assert result["current_modality"] == "m2"

    def test_multiline_system(self):
        result = classify_topology(has_integrator=True, has_expert_manager=True, expert_count=8)
        assert result["current_modality"] == "m3"

    def test_migration_recommendation(self):
        result = classify_topology(expert_count=5)
        assert result["current_modality"] == "m1"
        assert result["recommended_modality"] == "m2"
        assert result["should_migrate"] is True


class TestValidateTopology:
    def test_valid_m1(self):
        system = OneLineMoE(manager=ManagerSpec(), experts=[ExpertSpec()])
        result = validate_topology(system)
        assert result["valid"] is True

    def test_valid_m2(self):
        system = OneLineSupervisor(
            manager=ManagerSpec(),
            supervisor=SupervisorSpec(),
            experts=[ExpertSpec() for _ in range(3)],
        )
        result = validate_topology(system)
        assert result["valid"] is True

    def test_valid_m3(self):
        system = MultiLine(
            manager=ManagerSpec(),
            integrators=[IntegratorSpec()],
            expert_manager=ExpertManagerSpec(),
            teams=[Team(name="t", supervisor=SupervisorSpec(), experts=[ExpertSpec() for _ in range(3)])],
        )
        result = validate_topology(system)
        assert result["valid"] is True
