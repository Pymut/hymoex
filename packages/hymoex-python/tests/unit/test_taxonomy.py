"""Tests for agent taxonomy — role classification and specs."""

import hymoex
from hymoex import (
    Role,
    AgentSpec,
    ManagerSpec,
    SupervisorSpec,
    ExpertSpec,
    ExecutorSpec,
    PerceiverSpec,
    IntegratorSpec,
    ExpertManagerSpec,
)


class TestVersion:
    def test_version_exists(self):
        assert hasattr(hymoex, "__version__")
        assert isinstance(hymoex.__version__, str)
        assert len(hymoex.__version__) > 0


class TestRole:
    def test_seven_roles(self):
        assert len(Role) == 7

    def test_role_values(self):
        assert Role.MANAGER == "manager"
        assert Role.EXPERT == "expert"
        assert Role.PERCEIVER == "perceiver"


class TestSpecs:
    def test_manager_spec(self):
        m = ManagerSpec(objective="test", strategy="default")
        assert m.role == Role.MANAGER
        assert m.objective == "test"

    def test_expert_spec(self):
        e = ExpertSpec(domain="legal", skills=["contracts", "compliance"])
        assert e.role == Role.EXPERT
        assert e.domain == "legal"
        assert len(e.skills) == 2

    def test_supervisor_spec(self):
        s = SupervisorSpec(routing="round_robin")
        assert s.role == Role.SUPERVISOR
        assert s.routing == "round_robin"

    def test_executor_spec(self):
        ex = ExecutorSpec(action_type="crm_update")
        assert ex.role == Role.EXECUTOR

    def test_perceiver_spec(self):
        p = PerceiverSpec(sensor_type="sentiment")
        assert p.role == Role.PERCEIVER

    def test_integrator_spec(self):
        i = IntegratorSpec(routing_overhead_ms=100.0)
        assert i.role == Role.INTEGRATOR

    def test_expert_manager_spec(self):
        em = ExpertManagerSpec()
        assert em.role == Role.EXPERT_MANAGER

    def test_unique_ids(self):
        a = ManagerSpec()
        b = ManagerSpec()
        assert a.id != b.id

    def test_serialization(self):
        e = ExpertSpec(domain="tech", skills=["debug"])
        data = e.model_dump()
        restored = ExpertSpec(**data)
        assert restored.domain == "tech"
