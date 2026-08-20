"""Tests for per-entity bundle scoring in make_score_table (Option 2)."""
from __future__ import annotations

import pytest

from r2py.stage4.decompose import make_score_table, _compare_entity_bundles
from r2py.stage4.verifier import _inject_py_checkpoints, _collect_py_checkpoints
from r2py.types import (
    ComparatorResult,
    EffectBundle,
    EffectClass,
    EntityKind,
    EntityScore,
)


# ---------------------------------------------------------------------------
# Minimal fake entity
# ---------------------------------------------------------------------------

class _FakeEntity:
    def __init__(self, name: str, kind=EntityKind.FUNCTION_CALL):
        self.name = name
        self.kind = kind
        self.free_variable_refs: list = []
        self.actual_bundle = None


_WHOLE_SCRIPT_RESULTS = {
    EffectClass.DATA: ComparatorResult(
        effect_class=EffectClass.DATA, score=0.9, verdict="pass_via_fallback"
    ),
}


def _avg(es: EntityScore) -> float:
    return (es.type_match + es.control_flow_match + es.data_output
            + es.variable_output + es.callable_output + es.side_effects) / 6


# ---------------------------------------------------------------------------
# _inject_py_checkpoints
# ---------------------------------------------------------------------------

class TestInjectPyCheckpoints:
    def test_empty_line_map_returns_unchanged(self):
        src = "x = 1\n"
        modified, eids = _inject_py_checkpoints(src, {})
        assert modified == src
        assert eids == []

    def test_single_entity_injects_call(self):
        src = "x = 1\ny = 2\n"
        modified, eids = _inject_py_checkpoints(src, {"e1": (1, 1)})
        assert "_r2py_checkpoint('e1')" in modified
        assert eids == ["e1"]

    def test_two_entities_both_injected(self):
        src = "x = 1\ny = 2\nz = 3\n"
        modified, eids = _inject_py_checkpoints(src, {"e1": (1, 1), "e2": (2, 2)})
        assert modified.count("_r2py_checkpoint") == 2
        assert set(eids) == {"e1", "e2"}

    def test_ordering_ascending_end_line(self):
        src = "a = 1\nb = 2\nc = 3\n"
        modified, eids = _inject_py_checkpoints(src, {"e1": (1, 1), "e2": (2, 2), "e3": (3, 3)})
        # eids should be in ascending end_line order
        assert eids == ["e1", "e2", "e3"]

    def test_source_without_trailing_newline(self):
        src = "x = 1"
        modified, eids = _inject_py_checkpoints(src, {"e1": (1, 1)})
        assert "_r2py_checkpoint" in modified


# ---------------------------------------------------------------------------
# _compare_entity_bundles
# ---------------------------------------------------------------------------

class TestCompareEntityBundles:
    def test_both_empty_scores_one(self):
        r = EffectBundle()
        py = EffectBundle()
        results = _compare_entity_bundles(r, py)
        assert results[EffectClass.DATA].score == 1.0
        assert results[EffectClass.STDOUT].score == 1.0

    def test_matching_data_scores_one(self):
        r = EffectBundle(data={"x": 42})
        py = EffectBundle(data={"x": 42})
        results = _compare_entity_bundles(r, py)
        assert results[EffectClass.DATA].score == 1.0

    def test_r_has_data_py_has_none_scores_zero(self):
        r = EffectBundle(data={"x": 42})
        py = EffectBundle(data={})
        results = _compare_entity_bundles(r, py)
        assert results[EffectClass.DATA].score == 0.0

    def test_graphics_count_mismatch(self):
        r = EffectBundle(graphics=1)   # type: ignore[arg-type]
        py = EffectBundle(graphics=0)  # type: ignore[arg-type]
        results = _compare_entity_bundles(r, py)
        assert results[EffectClass.GRAPHICS].score == 0.0

    def test_graphics_count_match(self):
        r = EffectBundle(graphics=1)  # type: ignore[arg-type]
        py = EffectBundle(graphics=1)  # type: ignore[arg-type]
        results = _compare_entity_bundles(r, py)
        assert results[EffectClass.GRAPHICS].score == 1.0


# ---------------------------------------------------------------------------
# make_score_table with per-entity bundles
# ---------------------------------------------------------------------------

class TestMakeScoreTablePerEntity:
    def test_pass_entity_scores_low_when_r_produced_data_and_graphics(self):
        """Entity that produced data+graphics in R but nothing in Python → low score."""
        entities = {"e1": _FakeEntity("filled_contour")}
        r_eb = EffectBundle(data={"result": [1, 2, 3]}, graphics=1)  # type: ignore[arg-type]
        py_eb = EffectBundle(data={}, graphics=0)                     # type: ignore[arg-type]

        table = make_score_table(
            entities, _WHOLE_SCRIPT_RESULTS,
            r_entity_bundles={"e1": r_eb},
            py_entity_bundles={"e1": py_eb},
        )
        assert _avg(table["e1"]) < 0.3

    def test_good_entity_scores_high_when_data_matches(self):
        """Entity that faithfully translated a data-producing call → high score."""
        entities = {"e1": _FakeEntity("x")}
        r_eb = EffectBundle(data={"x": 5})
        py_eb = EffectBundle(data={"x": 5})

        table = make_score_table(
            entities, _WHOLE_SCRIPT_RESULTS,
            r_entity_bundles={"e1": r_eb},
            py_entity_bundles={"e1": py_eb},
        )
        assert _avg(table["e1"]) > 0.8

    def test_fallback_to_global_when_bundles_absent(self):
        """Without per-entity bundles, behaviour matches original global-score path."""
        entities = {"e1": _FakeEntity("foo")}
        table_global = make_score_table(entities, _WHOLE_SCRIPT_RESULTS)
        table_none = make_score_table(
            entities, _WHOLE_SCRIPT_RESULTS,
            r_entity_bundles=None,
            py_entity_bundles=None,
        )
        assert table_global["e1"].data_output == table_none["e1"].data_output

    def test_fallback_when_only_r_bundle_present(self):
        """If only the R-side bundle is available, fall back to global for that entity."""
        entities = {"e1": _FakeEntity("bar")}
        r_eb = EffectBundle(data={"bar": 1})
        table = make_score_table(
            entities, _WHOLE_SCRIPT_RESULTS,
            r_entity_bundles={"e1": r_eb},
            py_entity_bundles={},   # py side absent
        )
        # Falls back to global_data_score = 0.9
        assert abs(table["e1"].data_output - 0.9) < 1e-6

    def test_volcano_entity_still_scores_high(self):
        """The volcano VARIABLE entity should still score well when data matches."""
        entities = {"volcano": _FakeEntity("volcano", kind=EntityKind.VARIABLE)}
        # Simulate the text-fallback score for the matrix vs list-of-lists mismatch.
        whole = {
            EffectClass.DATA: ComparatorResult(
                effect_class=EffectClass.DATA, score=0.9,
                verdict="pass_via_fallback",
                per_variable={"volcano": 0.9},
            ),
        }
        # Per-entity: R has the volcano matrix, Python has the same (as list).
        # Use simple int proxies to avoid constructing real matrices.
        r_eb = EffectBundle(data={"volcano": [[1, 2], [3, 4]]})
        py_eb = EffectBundle(data={"volcano": [[1, 2], [3, 4]]})

        table = make_score_table(
            entities, whole,
            r_entity_bundles={"volcano": r_eb},
            py_entity_bundles={"volcano": py_eb},
        )
        assert _avg(table["volcano"]) > 0.8

    def test_per_entity_overrides_global_data_score_inflation(self):
        """Core regression: global score 0.9 must NOT bleed into unrelated entities."""
        entities = {
            "volcano": _FakeEntity("volcano", kind=EntityKind.VARIABLE),
            "filled_contour": _FakeEntity("filled_contour"),
        }
        r_bundles = {
            "volcano": EffectBundle(data={"volcano": [[1]]}),
            "filled_contour": EffectBundle(data={}, graphics=1),  # type: ignore[arg-type]
        }
        py_bundles = {
            "volcano": EffectBundle(data={"volcano": [[1]]}),
            "filled_contour": EffectBundle(data={}, graphics=0),  # type: ignore[arg-type]
        }
        table = make_score_table(
            entities, _WHOLE_SCRIPT_RESULTS,
            r_entity_bundles=r_bundles,
            py_entity_bundles=py_bundles,
        )
        # volcano should score well; filled_contour should score poorly
        assert _avg(table["volcano"]) > 0.8
        assert _avg(table["filled_contour"]) < 0.3
        # Overall must NOT be dominated by volcano's score
        avg_all = sum(_avg(v) for v in table.values()) / len(table)
        assert avg_all < 0.7
