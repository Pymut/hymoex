"""Tests for progressive migration."""

from hymoex import (
    ExpertSpec,
    ManagerSpec,
    SupervisorSpec,
    OneLineMoE,
    OneLineSupervisor,
    MultiLine,
    migrate_m1_to_m2,
    migrate_m2_to_m3,
    compute_preservation_ratio,
)


class TestM1ToM2:
    def test_preserves_all_agents(self):
        m1 = OneLineMoE(
            manager=ManagerSpec(objective="test"),
            experts=[ExpertSpec(domain="legal"), ExpertSpec(domain="tech")],
        )
        m2 = migrate_m1_to_m2(m1, additional_experts=[ExpertSpec(domain="billing")])
        assert isinstance(m2, OneLineSupervisor)
        assert m2.manager.objective == "test"
        assert len(m2.experts) == 3

    def test_adds_supervisor(self):
        m1 = OneLineMoE(manager=ManagerSpec(), experts=[ExpertSpec(), ExpertSpec()])
        m2 = migrate_m1_to_m2(m1, additional_experts=[ExpertSpec()])
        assert m2.supervisor is not None


class TestM2ToM3:
    def test_preserves_all_agents(self):
        m2 = OneLineSupervisor(
            manager=ManagerSpec(objective="scale"),
            supervisor=SupervisorSpec(),
            experts=[ExpertSpec(domain=f"d{i}") for i in range(3)],
        )
        m3 = migrate_m2_to_m3(m2)
        assert isinstance(m3, MultiLine)
        assert m3.manager.objective == "scale"
        assert len(m3.teams[0].experts) == 3

    def test_supervisor_becomes_team_supervisor(self):
        sup = SupervisorSpec(routing="dependency_aware")
        m2 = OneLineSupervisor(
            manager=ManagerSpec(),
            supervisor=sup,
            experts=[ExpertSpec() for _ in range(3)],
        )
        m3 = migrate_m2_to_m3(m2)
        assert m3.teams[0].supervisor.routing == "dependency_aware"


class TestPreservationRatio:
    def test_full_preservation(self):
        assert compute_preservation_ratio(3, 3) == 1.0

    def test_above_threshold(self):
        assert compute_preservation_ratio(10, 9) >= 0.85
