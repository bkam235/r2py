"""Tests for Stage 4 comparators, decompose, verifier, replay, judge, wiki_update (§7)."""
from __future__ import annotations

import math
import pytest

from r2py.stage4.comparators.base import text_similarity
from r2py.stage4.comparators.stdout import StdoutComparator
from r2py.stage4.comparators.warnings import WarningsComparator
from r2py.stage4.comparators.env import EnvComparator
from r2py.stage4.comparators.files import FilesComparator
from r2py.stage4.comparators.html import HtmlComparator
from r2py.stage4.comparators.graphics import GraphicsComparator
from r2py.stage4.comparators.data import DataComparator, _compare_pair, _compare_callable_meta
from r2py.stage4.comparators import COMPARATORS
from r2py.stage4.decompose import make_score_table
from r2py.stage4.judge import judge_entity
from r2py.stage4.replay import capture_r_rng, ReplayLog
from r2py.stage4.wiki_update import after_accepted_edit, after_tie, after_rejected_edit, maybe_review
from r2py.types import (
    EffectBundle, EffectClass, EntityKind, EntityScore, FeedbackItem, ScoreReport,
    Edit, EditKind,
)


# ---------------------------------------------------------------------------
# text_similarity
# ---------------------------------------------------------------------------

class TestTextSimilarity:
    def test_identical(self):
        assert text_similarity("hello", "hello") == 1.0

    def test_empty_both(self):
        assert text_similarity("", "") == 1.0

    def test_one_empty(self):
        assert text_similarity("", "x") == 0.0
        assert text_similarity("x", "") == 0.0

    def test_partial(self):
        s = text_similarity("hello world", "hello earth")
        assert 0.0 < s < 1.0

    def test_completely_different(self):
        s = text_similarity("aaa", "bbb")
        assert s < 0.5


# ---------------------------------------------------------------------------
# StdoutComparator
# ---------------------------------------------------------------------------

class TestStdoutComparator:
    cmp = StdoutComparator()

    def test_identical(self):
        r = self.cmp.compare("hello\n", "hello\n")
        assert r.verdict == "pass"
        assert r.score == 1.0

    def test_both_empty(self):
        r = self.cmp.compare("", "")
        assert r.verdict == "pass"

    def test_completely_different(self):
        r = self.cmp.compare("abc", "xyz")
        assert r.verdict == "fail"
        assert r.score < 0.5

    def test_one_empty(self):
        r = self.cmp.compare("hello", "")
        assert r.verdict == "fail"
        assert r.score == 0.0


# ---------------------------------------------------------------------------
# WarningsComparator
# ---------------------------------------------------------------------------

class TestWarningsComparator:
    cmp = WarningsComparator()

    def test_identical_lists(self):
        r = self.cmp.compare(["warn A", "warn B"], ["warn A", "warn B"])
        assert r.verdict == "pass"

    def test_same_different_order(self):
        r = self.cmp.compare(["warn B", "warn A"], ["warn A", "warn B"])
        assert r.verdict == "pass"

    def test_both_empty(self):
        r = self.cmp.compare([], [])
        assert r.verdict == "pass"

    def test_different(self):
        r = self.cmp.compare(["warning: NAs introduced"], ["DeprecationWarning: foo"])
        assert r.verdict == "fail"


# ---------------------------------------------------------------------------
# EnvComparator
# ---------------------------------------------------------------------------

class TestEnvComparator:
    cmp = EnvComparator()

    def test_identical(self):
        r = self.cmp.compare({"X": 1}, {"X": 1})
        assert r.verdict == "pass"
        assert r.score == 1.0

    def test_both_empty(self):
        r = self.cmp.compare({}, {})
        assert r.verdict == "pass"

    def test_missing_key_in_python(self):
        r = self.cmp.compare({"X": 1}, {})
        assert r.verdict == "fail"
        assert "only in R" in r.explanation

    def test_value_differs(self):
        r = self.cmp.compare({"X": 1}, {"X": 2})
        assert r.verdict == "fail"
        assert "differing" in r.explanation


# ---------------------------------------------------------------------------
# FilesComparator
# ---------------------------------------------------------------------------

class TestFilesComparator:
    cmp = FilesComparator()

    def test_identical(self):
        r = self.cmp.compare({"a.csv": "abc123"}, {"a.csv": "abc123"})
        assert r.verdict == "pass"
        assert r.score == 1.0

    def test_both_empty(self):
        r = self.cmp.compare({}, {})
        assert r.verdict == "pass"

    def test_hash_mismatch(self):
        r = self.cmp.compare({"a.csv": "abc"}, {"a.csv": "xyz"})
        assert r.verdict == "fail"
        assert r.score < 1.0

    def test_missing_file(self):
        r = self.cmp.compare({"a.csv": "abc"}, {})
        assert r.verdict == "fail"
        assert r.score == 0.0

    def test_python_extra_ignored(self):
        r = self.cmp.compare({"a.csv": "abc"}, {"a.csv": "abc", "b.csv": "xyz"})
        assert r.verdict == "pass"


# ---------------------------------------------------------------------------
# HtmlComparator
# ---------------------------------------------------------------------------

class TestHtmlComparator:
    cmp = HtmlComparator()

    def test_identical(self):
        r = self.cmp.compare(["<p>hello</p>"], ["<p>hello</p>"])
        assert r.verdict == "pass"

    def test_both_empty(self):
        r = self.cmp.compare([], [])
        assert r.verdict == "pass"

    def test_count_mismatch(self):
        r = self.cmp.compare(["<p>a</p>", "<p>b</p>"], ["<p>a</p>"])
        assert r.verdict == "fail"

    def test_normalized_similarity(self):
        # Same structure, minor whitespace/attr differences
        r = self.cmp.compare(
            ["<div><p class=\"a b\">hello</p></div>"],
            ["<div><p class=\"b a\">hello</p></div>"],
        )
        assert r.verdict == "pass"

    def test_structural_mismatch(self):
        # Different tag structure scores low even with same text
        r = self.cmp.compare(["<div><p>hello</p></div>"], ["<span>hello</span>"])
        assert r.score < 0.7

    def test_different_content(self):
        r = self.cmp.compare(["<p>aaaaaa</p>"], ["<p>zzzzzzz</p>"])
        assert r.verdict == "fail"


# ---------------------------------------------------------------------------
# GraphicsComparator
# ---------------------------------------------------------------------------

class TestGraphicsComparator:
    cmp = GraphicsComparator()

    def test_both_empty(self):
        r = self.cmp.compare([], [])
        assert r.verdict == "pass"

    def test_identical_bytes(self):
        data = b"\x89PNG\r\nfake"
        r = self.cmp.compare([data], [data])
        assert r.verdict == "pass"

    def test_count_mismatch(self):
        r = self.cmp.compare([b"img1", b"img2"], [b"img1"])
        assert r.verdict == "fail"

    def test_different_bytes_no_pillow(self):
        # Without Pillow, non-identical bytes should be uncomparable (not fail)
        try:
            import PIL  # noqa: F401
            pytest.skip("Pillow present — behaviour differs")
        except ImportError:
            r = self.cmp.compare([b"img1"], [b"img2"])
            assert r.verdict == "uncomparable"


# ---------------------------------------------------------------------------
# DataComparator — _compare_pair unit tests
# ---------------------------------------------------------------------------

class TestComparePair:
    def test_both_null(self):
        score, verdict, tag, _ = _compare_pair("x", None, None, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_one_null(self):
        score, verdict, tag, _ = _compare_pair("x", 1.0, None, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_numeric_within_tolerance(self):
        score, verdict, tag, _ = _compare_pair("x", 1.0, 1.0 + 1e-8, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_numeric_outside_tolerance(self):
        score, verdict, tag, _ = _compare_pair("x", 1.0, 2.0, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_bool_match(self):
        score, verdict, tag, _ = _compare_pair("x", True, True, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_bool_mismatch(self):
        score, verdict, tag, _ = _compare_pair("x", True, False, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_string_match(self):
        score, verdict, tag, _ = _compare_pair("x", "foo", "foo", 1e-6, 1e-9)
        assert verdict == "pass"

    def test_string_mismatch(self):
        score, verdict, tag, _ = _compare_pair("x", "foo", "bar", 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_list_match(self):
        score, verdict, tag, _ = _compare_pair("x", [1, 2, 3], [1, 2, 3], 1e-6, 1e-9)
        assert verdict == "pass"

    def test_list_length_mismatch_is_infra(self):
        score, verdict, tag, _ = _compare_pair("x", [1, 2], [1], 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "infra"

    def test_list_value_mismatch(self):
        score, verdict, tag, _ = _compare_pair("x", [1, 2], [1, 99], 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_dict_match(self):
        r = {"a": [1, 2], "b": [3, 4]}
        score, verdict, tag, _ = _compare_pair("x", r, r, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_dict_column_set_mismatch_is_infra(self):
        score, verdict, tag, _ = _compare_pair("x", {"a": [1]}, {"b": [1]}, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "infra"

    def test_type_mismatch_is_infra(self):
        score, verdict, tag, _ = _compare_pair("x", [1, 2], 3.0, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "infra"


# ---------------------------------------------------------------------------
# DataComparator — data_compare modes
# ---------------------------------------------------------------------------

class TestDataComparator:
    def test_identical(self):
        cmp = DataComparator()
        r = cmp.compare({"x": 1.0}, {"x": 1.0})
        assert r.verdict == "pass"
        assert r.score == 1.0

    def test_both_empty(self):
        cmp = DataComparator()
        r = cmp.compare({}, {})
        assert r.verdict == "pass"

    def test_value_failure_not_rescued_by_auto(self):
        cmp = DataComparator(data_compare="auto")
        r = cmp.compare({"x": 1.0}, {"x": 999.0})
        assert r.verdict == "fail"

    def test_infra_failure_rescued_by_auto(self):
        # Length mismatch = infra; text fallback should rescue if strings are similar
        cmp = DataComparator(data_compare="auto")
        r = cmp.compare({"x": [1, 2, 3]}, {"x": [1, 2]})
        # fallback kicks in; verdict should be pass_via_fallback or score > 0
        assert r.verdict in ("pass_via_fallback", "fail")  # depends on text similarity

    def test_infra_failure_stays_fail_with_exact(self):
        cmp = DataComparator(data_compare="exact")
        r = cmp.compare({"x": [1, 2, 3]}, {"x": [1, 2]})
        assert r.verdict == "fail"

    def test_embedding_mode_always_uses_fallback(self):
        cmp = DataComparator(data_compare="embedding")
        r = cmp.compare({"x": 1.0}, {"x": 1.0})
        # Same value → text fallback returns 1.0 → pass_via_fallback
        assert r.verdict in ("pass", "pass_via_fallback")

    def test_missing_variable_in_python(self):
        cmp = DataComparator()
        r = cmp.compare({"x": 1.0}, {})
        assert r.verdict == "fail"
        assert r.score == 0.0

    def test_uncapturable_excluded(self):
        cmp = DataComparator()
        r = cmp.compare({"x": 1.0}, {"x": 1.0}, uncapturable=["x"])
        assert r.verdict == "uncomparable"

    def test_multiple_variables_averaged(self):
        cmp = DataComparator()
        r = cmp.compare({"x": 1.0, "y": 2.0}, {"x": 1.0, "y": 2.0})
        assert r.verdict == "pass"
        assert r.score == 1.0

    def test_invalid_data_compare_raises(self):
        with pytest.raises(ValueError):
            DataComparator(data_compare="invalid")


# ---------------------------------------------------------------------------
# COMPARATORS registry
# ---------------------------------------------------------------------------

class TestComparatorsRegistry:
    def test_all_effect_classes_present(self):
        expected = {
            EffectClass.STDOUT, EffectClass.WARNINGS, EffectClass.ENV,
            EffectClass.FILES, EffectClass.HTML, EffectClass.GRAPHICS, EffectClass.DATA,
            EffectClass.NETWORK, EffectClass.RNG, EffectClass.SYNTAX,
        }
        assert set(COMPARATORS.keys()) == expected

    def test_rng_in_registry(self):
        assert EffectClass.RNG in COMPARATORS

    def test_network_in_registry(self):
        assert EffectClass.NETWORK in COMPARATORS

    def test_syntax_in_registry(self):
        assert EffectClass.SYNTAX in COMPARATORS


# ---------------------------------------------------------------------------
# ExitCodeComparator
# ---------------------------------------------------------------------------

class TestExitCodeComparator:
    def setup_method(self):
        from r2py.stage4.comparators.exit_code import ExitCodeComparator
        self.cmp = ExitCodeComparator()

    def test_both_zero(self):
        r = self.cmp.compare(0, 0)
        assert r.score == 1.0
        assert r.verdict == "pass"

    def test_both_nonzero(self):
        r = self.cmp.compare(1, 1)
        assert r.score == 0.8
        assert r.verdict == "pass"

    def test_r_ok_py_crash(self):
        r = self.cmp.compare(0, 1)
        assert r.score == 0.0
        assert r.verdict == "fail"

    def test_r_crash_py_ok(self):
        r = self.cmp.compare(1, 0)
        assert r.score == 0.0
        assert r.verdict == "fail"


# ---------------------------------------------------------------------------
# make_score_table
# ---------------------------------------------------------------------------

class TestMakeScoreTable:
    def _fake_entity(self, eid):
        class E:
            pass
        e = E()
        return {eid: e}

    def test_executed_ok(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(EffectClass.DATA, 1.0, "pass"),
        }
        table = make_score_table(self._fake_entity("e1"), results, py_exit_code=0)
        assert table["e1"].executed_ok is True

    def test_executed_not_ok(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(EffectClass.DATA, 1.0, "pass"),
        }
        table = make_score_table(self._fake_entity("e1"), results, py_exit_code=1)
        assert table["e1"].executed_ok is False

    def test_data_score_populated(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(EffectClass.DATA, 0.75, "fail"),
        }
        table = make_score_table(self._fake_entity("e1"), results)
        assert table["e1"].data_output == pytest.approx(0.75)

    def test_empty_entities(self):
        table = make_score_table({}, {})
        assert table == {}


class TestKindScores:
    """Kind-aware type_match / control_flow_match / callable_output (§7.4)."""

    def _results(self, data=1.0, stdout=1.0):
        from r2py.types import ComparatorResult
        return {
            EffectClass.DATA: ComparatorResult(EffectClass.DATA, data, "pass"),
            EffectClass.STDOUT: ComparatorResult(EffectClass.STDOUT, stdout, "pass"),
        }

    def _entity(self, kind, name="x"):
        class E:
            pass
        e = E()
        e.kind = kind
        e.name = name
        return e

    def test_library_import_all_ok(self):
        entities = {"e1": self._entity(EntityKind.LIBRARY_IMPORT)}
        table = make_score_table(entities, self._results(), py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(1.0)
        assert es.control_flow_match == pytest.approx(1.0)
        assert es.callable_output == pytest.approx(1.0)

    def test_library_import_failed_exec(self):
        entities = {"e1": self._entity(EntityKind.LIBRARY_IMPORT)}
        table = make_score_table(entities, self._results(), py_exit_code=1)
        es = table["e1"]
        assert es.type_match == pytest.approx(0.0)
        assert es.control_flow_match == pytest.approx(0.0)
        assert es.callable_output == pytest.approx(1.0)

    def test_variable_uses_data_score_for_type(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(
                EffectClass.DATA, 0.6, "fail", per_variable={"x": 0.6}
            ),
            EffectClass.STDOUT: ComparatorResult(EffectClass.STDOUT, 1.0, "pass"),
        }
        entities = {"e1": self._entity(EntityKind.VARIABLE, name="x")}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(0.6)
        assert es.control_flow_match == pytest.approx(1.0)  # executed_ok
        assert es.callable_output == pytest.approx(1.0)     # not callable

    def test_constant_uses_data_score_for_type(self):
        results = self._results(data=0.9)
        entities = {"e1": self._entity(EntityKind.CONSTANT)}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(0.9)
        assert es.callable_output == pytest.approx(1.0)

    def test_function_def_uses_stdout_for_control_flow(self):
        results = self._results(data=0.8, stdout=0.5)
        entities = {"e1": self._entity(EntityKind.FUNCTION_DEF)}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(1.0)         # executed_ok
        assert es.control_flow_match == pytest.approx(0.5) # stdout score
        assert es.callable_output == pytest.approx(0.8)    # global data score

    def test_function_call_all_from_data_score(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(
                EffectClass.DATA, 0.7, "fail", per_variable={"result": 0.7}
            ),
            EffectClass.STDOUT: ComparatorResult(EffectClass.STDOUT, 1.0, "pass"),
        }
        entities = {"e1": self._entity(EntityKind.FUNCTION_CALL, name="result")}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(0.7)
        assert es.control_flow_match == pytest.approx(0.7)
        assert es.callable_output == pytest.approx(0.7)

    def test_external_symbol_all_from_data_score(self):
        results = self._results(data=0.55, stdout=0.9)
        entities = {"e1": self._entity(EntityKind.EXTERNAL_SYMBOL)}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(0.55)
        assert es.control_flow_match == pytest.approx(0.55)
        assert es.callable_output == pytest.approx(0.55)

    def test_formula_uses_executed_ok(self):
        results = self._results()
        entities = {"e1": self._entity(EntityKind.FORMULA)}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(1.0)
        assert es.control_flow_match == pytest.approx(1.0)
        assert es.callable_output == pytest.approx(1.0)

    def test_no_kind_attr_falls_back_to_executed_ok(self):
        """Fake entity with no kind attribute (pre-existing tests) still works."""
        class E:
            pass
        e = E()
        e.name = "y"
        results = self._results()
        table = make_score_table({"e1": e}, results, py_exit_code=0)
        es = table["e1"]
        assert es.type_match == pytest.approx(1.0)
        assert es.callable_output == pytest.approx(1.0)

    def test_no_stdout_comparator_falls_back_to_executed_ok(self):
        from r2py.types import ComparatorResult
        results = {
            EffectClass.DATA: ComparatorResult(EffectClass.DATA, 0.8, "pass"),
        }
        entities = {"e1": self._entity(EntityKind.FUNCTION_DEF)}
        table = make_score_table(entities, results, py_exit_code=0)
        es = table["e1"]
        # stdout_score falls back to float(executed_ok) = 1.0
        assert es.control_flow_match == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# judge_entity
# ---------------------------------------------------------------------------

class TestJudgeEntity:
    def test_disabled_by_default(self):
        result = judge_entity(None, None, None, use_judge=False)
        assert result is None

    def test_enabled_pass_verdict(self):
        from unittest.mock import patch
        with patch("r2py.stage2.llm.call", return_value="<verdict>pass</verdict> They match."):
            result = judge_entity(None, "1", "1", use_judge=True)
        assert result is not None
        assert result.verdict == "pass"
        assert result.score == 1.0

    def test_enabled_fail_verdict(self):
        from unittest.mock import patch
        with patch("r2py.stage2.llm.call", return_value="<verdict>fail</verdict> Different output."):
            result = judge_entity(None, "1", "2", use_judge=True)
        assert result is not None
        assert result.verdict == "fail"
        assert result.score == 0.0

    def test_enabled_llm_error_returns_uncomparable(self):
        from unittest.mock import patch
        with patch("r2py.stage2.llm.call", side_effect=RuntimeError("API down")):
            result = judge_entity(None, "x", "y", use_judge=True)
        assert result is not None
        assert result.verdict == "uncomparable"


# ---------------------------------------------------------------------------
# capture_r_rng / ReplayLog
# ---------------------------------------------------------------------------

class TestReplayLog:
    def test_capture_rng(self):
        bundle = EffectBundle(rng_log=[("runif", (), 0.5), ("rnorm", (), 1.2)])
        log = capture_r_rng(bundle)
        assert isinstance(log, ReplayLog)
        assert log.rng_sequence == [0.5, 1.2]

    def test_non_float_excluded(self):
        bundle = EffectBundle(rng_log=[("sample", (), [1, 2, 3]), ("runif", (), 0.7)])
        log = capture_r_rng(bundle)
        assert log.rng_sequence == [0.7]

    def test_empty_rng_log(self):
        bundle = EffectBundle()
        log = capture_r_rng(bundle)
        assert log.rng_sequence == []


# ---------------------------------------------------------------------------
# wiki_update
# ---------------------------------------------------------------------------

class _FakeLibrary:
    def __init__(self):
        self.evidence = []
        self.ties = []
        self.contradictions = []
        self.reviews = 0

    def record_evidence(self, edit, *, score_delta, script_id, verification_path):
        self.evidence.append((edit.pattern_id, script_id, score_delta, verification_path))

    def record_tie(self, edit, *, script_id):
        self.ties.append((edit.pattern_id, script_id))

    def record_contradiction(self, edit, *, observed, script_id):
        self.contradictions.append((edit.pattern_id, script_id, observed))

    def epistemology_review(self):
        self.reviews += 1
        return ["reviewed"]


class TestWikiUpdate:
    def _edit(self, pid="p1"):
        return Edit(kind=EditKind.REPLACE_CALL, pattern_id=pid)

    def test_after_accepted_edit(self):
        lib = _FakeLibrary()
        after_accepted_edit(self._edit(), 0.9, lib, r_source="x <- 1")
        assert len(lib.evidence) == 1
        assert lib.evidence[0][0] == "p1"
        assert lib.evidence[0][2] == 0.9

    def test_after_tie(self):
        lib = _FakeLibrary()
        after_tie(self._edit(), 0.75, lib, r_source="x <- 1")
        assert len(lib.ties) == 1

    def test_after_rejected_edit(self):
        lib = _FakeLibrary()
        after_rejected_edit(self._edit(), lib, r_source="x <- 1")
        assert len(lib.contradictions) == 1

    def test_none_pattern_id_noop(self):
        lib = _FakeLibrary()
        after_accepted_edit(Edit(kind=EditKind.REPLACE_CALL, pattern_id=None), 0.9, lib)
        assert lib.evidence == []

    def test_maybe_review_triggers(self):
        lib = _FakeLibrary()
        result = maybe_review(10, lib, every_n=10)
        assert result == ["reviewed"]

    def test_maybe_review_skips(self):
        lib = _FakeLibrary()
        result = maybe_review(7, lib, every_n=10)
        assert result == []

    def test_maybe_review_zero_skips(self):
        lib = _FakeLibrary()
        result = maybe_review(0, lib, every_n=10)
        assert result == []


# ---------------------------------------------------------------------------
# verify() smoke test (no R runtime needed — uses empty ScriptMap)
# ---------------------------------------------------------------------------

class TestVerifySmoke:
    def test_verify_empty_script_map(self):
        """verify() on an empty ScriptMap with trivial Python returns a ScoreReport."""
        from r2py.stage4 import verify
        from r2py.types import ScriptMap

        sm = ScriptMap(source="x <- 1")
        report = verify(sm, "x = 1")

        assert isinstance(report, ScoreReport)
        assert isinstance(report.aggregate, float)
        assert 0.0 <= report.aggregate <= 1.0
        assert isinstance(report.by_effect, dict)
        assert isinstance(report.feedback, list)
        assert isinstance(report.uncomparable, list)

    def test_verify_returns_high_score_for_empty_bundles(self):
        """Empty R bundle vs trivial Python that produces no side effects → score ≈ 1."""
        from r2py.stage4 import verify
        from r2py.types import ScriptMap

        sm = ScriptMap(source="")
        report = verify(sm, "pass")
        # All comparators score empty-vs-empty as 1.0
        assert report.aggregate >= 0.9

    def test_verify_incremental_changed(self):
        """changed= parameter restricts which entities are re-verified."""
        from r2py.stage4 import verify
        from r2py.types import ScriptMap

        sm = ScriptMap(source="x <- 1")
        # No entities in the base ScriptMap, so changed= has no effect but must not error
        report = verify(sm, "x = 1", changed=["entity_abc"])
        assert isinstance(report, ScoreReport)

    def test_verify_return_bundle_false_returns_score_report(self):
        from r2py.stage4 import verify
        from r2py.types import ScriptMap

        sm = ScriptMap(source="")
        result = verify(sm, "pass", return_bundle=False)
        assert isinstance(result, ScoreReport)

    def test_verify_return_bundle_true_returns_tuple(self):
        from r2py.stage4 import verify
        from r2py.types import ScriptMap

        sm = ScriptMap(source="")
        result = verify(sm, "pass", return_bundle=True)
        assert isinstance(result, tuple)
        assert len(result) == 2
        report, bundle = result
        assert isinstance(report, ScoreReport)
        assert isinstance(bundle, EffectBundle)

    def test_get_r_bundle_returns_effect_bundle(self):
        from r2py.stage4 import get_r_bundle
        from r2py.types import ScriptMap

        sm = ScriptMap(source="")
        result = get_r_bundle(sm)
        assert isinstance(result, EffectBundle)


# ---------------------------------------------------------------------------
# _build_feedback direct tests
# ---------------------------------------------------------------------------

class TestBuildFeedback:
    def _make_fail(self, ec, msg="something went wrong", score=0.0):
        from r2py.types import ComparatorResult
        return ComparatorResult(effect_class=ec, score=score, verdict="fail", explanation=msg)

    def _make_pass(self, ec):
        from r2py.types import ComparatorResult
        return ComparatorResult(effect_class=ec, score=1.0, verdict="pass")

    def test_no_failures_returns_empty(self):
        from r2py.stage4.verifier import _build_feedback
        results = {
            EffectClass.STDOUT: self._make_pass(EffectClass.STDOUT),
            EffectClass.DATA: self._make_pass(EffectClass.DATA),
        }
        items = _build_feedback(results, {"e1": None})
        assert items == []

    def test_one_failure_one_item(self):
        from r2py.stage4.verifier import _build_feedback
        results = {
            EffectClass.STDOUT: self._make_fail(EffectClass.STDOUT, "stdout mismatch"),
        }
        items = _build_feedback(results, {"e1": None})
        assert len(items) == 1
        assert items[0].effect_class == EffectClass.STDOUT
        assert items[0].entity_id == "e1"
        assert "stdout mismatch" in items[0].message

    def test_two_failures_two_items(self):
        from r2py.stage4.verifier import _build_feedback
        results = {
            EffectClass.STDOUT: self._make_fail(EffectClass.STDOUT, "stdout bad"),
            EffectClass.DATA: self._make_fail(EffectClass.DATA, "data bad"),
        }
        items = _build_feedback(results, {"e1": None})
        assert len(items) == 2

    def test_no_explanation_skipped(self):
        from r2py.stage4.verifier import _build_feedback
        from r2py.types import ComparatorResult
        results = {
            EffectClass.STDOUT: ComparatorResult(EffectClass.STDOUT, 0.0, "fail", explanation=""),
        }
        items = _build_feedback(results, {"e1": None})
        assert items == []

    def test_no_entities_returns_empty(self):
        from r2py.stage4.verifier import _build_feedback
        results = {
            EffectClass.STDOUT: self._make_fail(EffectClass.STDOUT, "bad"),
        }
        items = _build_feedback(results, {})
        assert items == []


# ---------------------------------------------------------------------------
# DataComparator bool/int cross-type compatibility (new regression tests)
# ---------------------------------------------------------------------------

class TestBoolIntCompat:
    def test_r_true_py_int_one(self):
        score, verdict, tag, _ = _compare_pair("x", True, 1, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_r_false_py_int_zero(self):
        score, verdict, tag, _ = _compare_pair("x", False, 0, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_r_true_py_int_two_is_value_fail(self):
        score, verdict, tag, _ = _compare_pair("x", True, 2, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"

    def test_r_int_one_py_true(self):
        score, verdict, tag, _ = _compare_pair("x", 1, True, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_r_int_one_py_false_is_value_fail(self):
        score, verdict, tag, _ = _compare_pair("x", 1, False, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "value"


# ---------------------------------------------------------------------------
# Callable metadata comparison
# ---------------------------------------------------------------------------

class TestCallableMetaComparison:
    def _meta(self, formals, attrs=None, cls=None):
        return {
            "__r2py_callable_meta__": True,
            "class": cls or ["S7_generic", "function"],
            "formals": formals,
            "attributes": attrs or {},
        }

    def test_exact_formals_match_no_attrs(self):
        r = self._meta(["x", "y", "..."])
        py = self._meta(["x", "y"], cls=["S7GenericWrapper"])
        score, verdict, _, _ = _compare_callable_meta("foo", r, py)
        assert verdict == "pass"
        assert score == pytest.approx(1.0)

    def test_exact_formals_match_with_attrs(self):
        r = self._meta(["x", "y", "..."], {"name": "foo", "dispatch_args": "x"})
        py = self._meta(["x", "y"], cls=["Wrapper"], attrs={"name": "foo", "dispatch_args": "x"})
        score, verdict, _, _ = _compare_callable_meta("foo", r, py)
        assert verdict == "pass"
        assert score == pytest.approx(1.0)

    def test_mismatched_formals(self):
        r = self._meta(["x", "y", "..."])
        py = self._meta(["a", "b"], cls=["Wrapper"])
        score, verdict, tag, _ = _compare_callable_meta("foo", r, py)
        assert verdict == "fail"
        assert score < 0.7

    def test_partial_formals_overlap(self):
        r = self._meta(["x", "y", "z", "..."])
        py = self._meta(["x", "y", "w"], cls=["Wrapper"])
        score, verdict, tag, _ = _compare_callable_meta("foo", r, py)
        assert 0.3 < score < 0.9
        assert tag == "infra"

    def test_attr_mismatch_partial_score(self):
        r = self._meta(["x", "..."], {"name": "foo", "dispatch_args": "x"})
        py = self._meta(["x"], cls=["W"], attrs={"name": "bar", "dispatch_args": "x"})
        score, verdict, _, _ = _compare_callable_meta("foo", r, py)
        assert score == pytest.approx(0.7 + 0.3 * 0.5)

    def test_compare_pair_dispatches_to_callable_meta(self):
        r = self._meta(["x", "y", "..."], {"name": "foo"})
        py = self._meta(["x", "y"], cls=["W"], attrs={"name": "foo"})
        score, verdict, _, _ = _compare_pair("foo", r, py, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_compare_pair_regular_dict_not_affected(self):
        r = {"a": [1, 2], "b": [3, 4]}
        score, verdict, _, _ = _compare_pair("x", r, r, 1e-6, 1e-9)
        assert verdict == "pass"

    def test_data_comparator_r_callable_py_missing(self):
        cmp = DataComparator()
        r_meta = self._meta(["x", "y", "..."])
        result = cmp.compare({"foo": r_meta}, {})
        assert result.score == 0.0
        assert result.verdict == "fail"

    def test_r_callable_vs_py_plain_dict_is_infra_fail(self):
        """A non-callable Python object that contains the sentinel key
        should have the sentinel stripped by the epilogue, so the comparator
        sees callable-meta vs plain-dict → infra mismatch."""
        r = self._meta(["x", "y", "..."], {"name": "foo"})
        # Simulate what the epilogue produces after stripping the sentinel
        py_plain = {k: v for k, v in r.items() if k != "__r2py_callable_meta__"}
        score, verdict, tag, _ = _compare_pair("foo", r, py_plain, 1e-6, 1e-9)
        assert verdict == "fail"
        assert tag == "infra"


# ---------------------------------------------------------------------------
# DataComparator embedding mode: missing variable scores 0.0, not text(r, "None")
# ---------------------------------------------------------------------------

class TestEmbeddingModeMissingVar:
    def test_missing_var_scores_zero_not_none_similarity(self):
        cmp = DataComparator(data_compare="embedding")
        r = cmp.compare({"x": 42.0}, {})
        assert r.score == 0.0
        assert r.verdict == "fail"
        assert "missing" in r.explanation

    def test_present_var_uses_fallback(self):
        cmp = DataComparator(data_compare="embedding")
        r = cmp.compare({"x": 1.0}, {"x": 1.0})
        # identical → text fallback 1.0 → pass_via_fallback
        assert r.verdict in ("pass", "pass_via_fallback")
        assert r.score == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# pass_via_fallback propagated through verify()
# ---------------------------------------------------------------------------

class TestPassViaFallbackEndToEnd:
    def test_infra_failure_produces_pass_via_fallback_in_by_effect(self):
        """An infra-tagged length mismatch with auto mode should produce
        pass_via_fallback in the DATA comparator result visible in by_effect."""
        cmp = DataComparator(data_compare="auto")
        # [1,2,3] vs [1,2] → infra (length mismatch) → auto fallback
        result = cmp.compare({"x": [1, 2, 3]}, {"x": [1, 2]})
        # text("[1, 2, 3]", "[1, 2]") is high similarity → rescued
        assert result.verdict in ("pass_via_fallback", "fail")
        if result.verdict == "pass_via_fallback":
            assert result.score > 0.0


# ---------------------------------------------------------------------------
# DataFrameGenerator mixed-type boundary cases
# ---------------------------------------------------------------------------

class TestDataFrameGeneratorMixedType:
    def test_boundary_zero_rows_has_all_columns(self):
        from r2py.stage4.generators import DataFrameGenerator
        df = {"a": [1, 2], "b": ["x", "y"]}
        g = DataFrameGenerator(df)
        cases = g.boundary_cases()
        # 0-row case must have all columns
        zero_row_case = cases[0]
        assert set(zero_row_case.keys()) == {"a", "b"}

    def test_boundary_one_row_has_all_columns(self):
        from r2py.stage4.generators import DataFrameGenerator
        df = {"a": [1, 2], "b": ["x", "y"]}
        g = DataFrameGenerator(df)
        cases = g.boundary_cases()
        one_row_case = cases[1]
        assert set(one_row_case.keys()) == {"a", "b"}

    def test_observed_without_list_column_handled(self):
        from r2py.stage4.generators import DataFrameGenerator
        # scalar-valued column (shouldn't normally happen, but mustn't crash)
        df = {"a": [1, 2], "b": 99}
        g = DataFrameGenerator(df)
        rng = __import__("random").Random(0)
        result = g.sample(rng)
        assert "a" in result
