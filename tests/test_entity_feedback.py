"""Option entity_feedback: each losing entity is shown the comparison that scores it, shared items once (2026-10-31).

rvest html_children: the whole-script data comparison put the difference of the last ``html`` on ``html_1`` (1.0)
while ``html``, ``ul``, ``p`` (0.25) were shown nothing, and 8 of the 10 feedback lines were the same warnings item."""
from r2py.harness.prompt import format_score_report
from r2py.types import (ComparisonDetail, EffectBundle, EffectClass, EntityScore, FeedbackItem, ScoreReport)


def _es(eid, data):
    return EntityScore(entity_id=eid, executed_ok=True, type_match=data, control_flow_match=1.0, data_output=data,
                       variable_output=data, callable_output=1.0, side_effects=1.0,
                       active_dims=frozenset({"type_match", "data_output", "variable_output"}))


def _report():
    by_entity = {"html": _es("html", 0.0), "html_1": _es("html_1", 1.0)}
    return ScoreReport(
        aggregate=0.5, by_entity=by_entity,
        comparisons=[ComparisonDetail(EffectClass.DATA, "html_1", "'b'", "'c'", 0.0, "html: 'b' != 'c'")],
        feedback=[FeedbackItem("html_1", EffectClass.DATA, "html: 'b' != 'c'", 0.0)]
                 + [FeedbackItem(e, EffectClass.WARNINGS, "warnings similarity 0.000 < 0.95", 0.0) for e in by_entity],
        py_entity_bundles={"html": EffectBundle(data={"html": "x"}), "html_1": EffectBundle(data={"html": "c"})})


R_BUNDLES = {"html": EffectBundle(data={"html": "a"}), "html_1": EffectBundle(data={"html": "b"})}


def test_off_is_unchanged():
    text = format_score_report(_report())
    assert "[data] [html_1] score=0.000" in text and text.count("warnings similarity") == 2


def test_losing_entity_sees_its_own_comparison():
    text = format_score_report(_report(), R_BUNDLES)
    assert "[data] [html] score=0.000" in text and "R produced:      a\n" in text and "Python produced: x\n" in text
    assert "[html_1]" not in text.split("Per-entity scores:")[1].split("\n\n", 1)[1]


def test_shared_item_shown_once():
    text = format_score_report(_report(), R_BUNDLES)
    assert text.count("warnings similarity") == 1 and "[all entities] warnings" in text
