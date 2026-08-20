"""Tests for r2py/types.py — verifiable without any stage implementations."""
from r2py.types import (
    EffectClass,
    EntityKind,
    EditKind,
    CaptureSpec,
    EffectBundle,
    ComparatorResult,
    EntityScore,
    FeedbackItem,
    ScoreReport,
    TranslateResult,
    Candidate,
    Edit,
    ScriptMap,
)


# ---------------------------------------------------------------------------
# Enum counts (each count is load-bearing: the architecture fixes these)
# ---------------------------------------------------------------------------

def test_effect_class_count():
    assert len(list(EffectClass)) == 10


def test_effect_class_values():
    values = {e.value for e in EffectClass}
    assert values == {
        "stdout", "files", "graphics", "data", "html",
        "env", "warnings", "rng", "network", "syntax",
    }


def test_entity_kind_count():
    assert len(list(EntityKind)) == 10


def test_edit_kind_count():
    # Closed taxonomy from §8.3 — 9 variants (includes RetranslateScript).
    assert len(list(EditKind)) == 9


def test_edit_kind_members():
    names = {e.name for e in EditKind}
    assert "REPLACE_CALL" in names
    assert "WRAP_VALUE" in names
    assert "REPLACE_LIBRARY" in names


# ---------------------------------------------------------------------------
# CaptureSpec
# ---------------------------------------------------------------------------

def test_capture_spec_is_frozenset():
    spec: CaptureSpec = frozenset({EffectClass.STDOUT, EffectClass.FILES})
    assert isinstance(spec, frozenset)
    assert EffectClass.STDOUT in spec


# ---------------------------------------------------------------------------
# EffectBundle defaults — D2: uncapturable must never be silently absent
# ---------------------------------------------------------------------------

def test_effect_bundle_defaults():
    b = EffectBundle()
    assert b.stdout == ""
    assert b.stderr == ""
    assert b.uncapturable == []   # present and empty, never missing
    assert b.exit_code == 0
    assert b.run_time_s == 0.0


def test_effect_bundle_uncapturable_independent():
    b1 = EffectBundle()
    b2 = EffectBundle()
    b1.uncapturable.append("some_call")
    assert b2.uncapturable == []  # dataclass field isolation


# ---------------------------------------------------------------------------
# ComparatorResult
# ---------------------------------------------------------------------------

def test_comparator_result_verdict_pass_via_fallback():
    # §7.3.1: "pass_via_fallback" must be expressible as a verdict string.
    r = ComparatorResult(
        effect_class=EffectClass.DATA,
        score=0.85,
        verdict="pass_via_fallback",
        failure_tag="infra",
    )
    assert r.verdict == "pass_via_fallback"
    assert r.failure_tag == "infra"


def test_comparator_result_value_failure_not_rescuable():
    r = ComparatorResult(
        effect_class=EffectClass.DATA,
        score=0.0,
        verdict="fail",
        failure_tag="value",
    )
    assert r.failure_tag == "value"
    # "value"-tagged failures must NOT be rescued by the fallback — the test
    # documents the invariant; enforcement is in stage4/comparators/data.py.


# ---------------------------------------------------------------------------
# EntityScore
# ---------------------------------------------------------------------------

def test_entity_score_defaults():
    s = EntityScore(entity_id="var:x")
    assert s.executed_ok is False
    assert s.type_match == 0.0
    # D4: judge_pass is None when judge is disabled (the default).
    assert s.judge_pass is None


# ---------------------------------------------------------------------------
# ScoreReport
# ---------------------------------------------------------------------------

def test_score_report_defaults():
    r = ScoreReport(aggregate=0.5)
    assert r.by_entity == {}
    assert r.by_effect == {}
    assert r.uncomparable == []
    assert r.feedback == []


def test_score_report_independent_defaults():
    r1 = ScoreReport(aggregate=0.0)
    r2 = ScoreReport(aggregate=1.0)
    r1.uncomparable.append("var:x")
    assert r2.uncomparable == []


# ---------------------------------------------------------------------------
# TranslateResult
# ---------------------------------------------------------------------------

def test_translate_result_fields():
    r = TranslateResult(python_source="x = 1", final_score=0.9, iterations=3)
    assert r.score_history == []
    assert r.pattern_evidence_added == []
    assert r.pattern_contradictions_added == []


# ---------------------------------------------------------------------------
# Edit — attribution
# ---------------------------------------------------------------------------

def test_edit_defaults():
    e = Edit(kind=EditKind.REPLACE_CALL)
    assert e.entity_ids == []
    assert e.params == {}
    # pattern_id starts as None; must be set before an edit can be accepted (§8.5).
    assert e.pattern_id is None


def test_edit_with_attribution():
    e = Edit(kind=EditKind.WRAP_VALUE, entity_ids=["var:ui"], pattern_id="shiny.tag_as_str")
    assert e.pattern_id == "shiny.tag_as_str"


# ---------------------------------------------------------------------------
# Candidate
# ---------------------------------------------------------------------------

def test_candidate_fields():
    rep = ScoreReport(aggregate=0.7)
    c = Candidate(translation="x = 1", score=0.7, decomp=rep)
    assert c.score == 0.7
    assert c.translation == "x = 1"


# ---------------------------------------------------------------------------
# ScriptMap placeholder
# ---------------------------------------------------------------------------

def test_script_map_placeholder():
    sm = ScriptMap(source="x <- 1")
    assert sm.source == "x <- 1"
