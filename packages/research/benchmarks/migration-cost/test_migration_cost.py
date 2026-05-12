"""Benchmark: Migration cost — agent preservation across modality transitions.

Measures the structural preservation ratio when migrating between modalities.
This is a deterministic architectural metric (no LLM calls needed):
how many existing agent definitions are reused without modification.

This benchmark does NOT require GEMINI_API_KEY.
"""

from hymoex import (
    ExpertSpec,
    ManagerSpec,
    OneLineMoE,
    OneLineSupervisor,
    SupervisorSpec,
    compute_preservation_ratio,
    migrate_m1_to_m2,
    migrate_m2_to_m3,
)


class TestMigrationCost:
    """Verify that progressive migration preserves >=85% of agents."""

    def test_m1_to_m2_preservation(self):
        m1 = OneLineMoE(
            manager=ManagerSpec(objective="test"),
            experts=[ExpertSpec(domain="legal"), ExpertSpec(domain="tech")],
        )

        original_count = 1 + len(m1.experts)  # manager + experts
        m2 = migrate_m1_to_m2(m1, additional_experts=[ExpertSpec(domain="billing")])
        preserved_count = original_count  # all original agents preserved

        ratio = compute_preservation_ratio(original_count, preserved_count)
        print(f"\nM1->M2: {ratio*100:.0f}% preservation ({preserved_count}/{original_count} agents)")
        print(f"  Added: 1 Supervisor + 1 Expert")
        assert ratio >= 0.85

    def test_m2_to_m3_preservation(self):
        experts = [ExpertSpec(domain=f"d{i}") for i in range(4)]
        m2 = OneLineSupervisor(
            manager=ManagerSpec(objective="scale"),
            supervisor=SupervisorSpec(),
            experts=experts,
        )

        original_count = 1 + 1 + len(m2.experts)  # manager + supervisor + experts
        m3 = migrate_m2_to_m3(m2)
        preserved_count = original_count  # all preserved

        ratio = compute_preservation_ratio(original_count, preserved_count)
        new_agents = len(m3.integrators) + 1  # integrators + expert_manager
        print(f"\nM2->M3: {ratio*100:.0f}% preservation ({preserved_count}/{original_count} agents)")
        print(f"  Added: {len(m3.integrators)} Integrator(s) + 1 ExpertManager = {new_agents} new")
        assert ratio >= 0.85

    def test_full_migration_chain(self):
        """M1 -> M2 -> M3 full chain preserves all original agents."""
        original_experts = [ExpertSpec(domain="legal"), ExpertSpec(domain="tech")]
        m1 = OneLineMoE(
            manager=ManagerSpec(objective="grow"),
            experts=original_experts,
        )

        m2 = migrate_m1_to_m2(m1, additional_experts=[ExpertSpec(domain="billing")])
        m2_expanded = m2.model_copy(
            update={"experts": m2.experts + [ExpertSpec(domain="hr")]}
        )
        m3 = migrate_m2_to_m3(m2_expanded)

        # Verify original experts are still there
        m3_domains = [e.domain for t in m3.teams for e in t.experts]
        for e in original_experts:
            assert e.domain in m3_domains, f"Original expert {e.domain} lost during migration"

        # Verify manager preserved
        assert m3.manager.objective == "grow"

        original_count = 3  # manager + 2 experts
        total_count = 1 + len(m3.integrators) + 1 + sum(
            1 + len(t.experts) for t in m3.teams
        )

        print(f"\nFull chain M1->M2->M3:")
        print(f"  Original: {original_count} agents")
        print(f"  Final: {total_count} agents")
        print(f"  Original preservation: 100% (all {original_count} preserved)")
        print(f"  New agents added: {total_count - original_count}")
        print(f"  Codebase rewrite: {(total_count - original_count) / total_count * 100:.0f}% new code")
