"""Tests for Stage 3 — Editor (§8).

All tests are offline — no LLM calls are made. policy.py / editor.py tests
mock llm.call.
"""
from __future__ import annotations

import json
import unittest
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch

from r2py.types import (
    Candidate,
    Edit,
    EditKind,
    EntityId,
    EntityScore,
    FeedbackItem,
    EffectClass,
    ScoreReport,
)


# ---------------------------------------------------------------------------
# Helpers shared across test classes
# ---------------------------------------------------------------------------

def _make_edit(
    kind: EditKind = EditKind.INSERT_PREAMBLE,
    entity_ids: list[str] | None = None,
    params: dict | None = None,
    pattern_id: str | None = "test.pattern",
) -> Edit:
    return Edit(
        kind=kind,
        entity_ids=entity_ids or [],
        params=params or {},
        pattern_id=pattern_id,
    )


def _make_score_report(by_entity: dict | None = None) -> ScoreReport:
    return ScoreReport(
        aggregate=0.5,
        by_entity=by_entity or {},
        by_effect={},
        uncomparable=[],
        feedback=[],
    )


def _make_candidate(by_entity: dict | None = None, translation: str = "x = 1") -> Candidate:
    return Candidate(
        translation=translation,
        score=0.5,
        decomp=_make_score_report(by_entity),
    )


def _entity_score(eid: str, avg: float = 0.5) -> EntityScore:
    return EntityScore(
        entity_id=eid,
        executed_ok=True,
        type_match=avg,
        control_flow_match=avg,
        data_output=avg,
        variable_output=avg,
        callable_output=avg,
        side_effects=avg,
    )


# ---------------------------------------------------------------------------
# T1 — TestApplyEdit
# ---------------------------------------------------------------------------

class TestApplyEdit(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.edit_types import apply_edit
        self.apply = apply_edit

    def test_insert_preamble_before_first_code_line(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "import numpy as np"})
        result = self.apply(source, e)
        self.assertIn("import numpy as np\n", result)
        self.assertTrue(result.index("import numpy") < result.index("x = 1"))

    def test_insert_preamble_skips_comments(self):
        source = "# header\nx = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        result = self.apply(source, e)
        self.assertIn("import os", result)

    def test_insert_preamble_empty_code_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "   "})
        self.assertEqual(self.apply(source, e), source)

    def test_rename_variable(self):
        source = "foo = 1\nbar = foo + 2\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "foo", "new": "baz"})
        result = self.apply(source, e)
        self.assertNotIn("foo", result)
        self.assertIn("baz", result)

    def test_rename_variable_whole_word_only(self):
        source = "foobar = 1\nfoo = 2\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "foo", "new": "x"})
        result = self.apply(source, e)
        self.assertIn("foobar", result)  # not renamed
        self.assertIn("x = 2", result)

    def test_rename_variable_empty_params_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "", "new": "y"})
        self.assertEqual(self.apply(source, e), source)

    def test_change_import(self):
        source = "import pandas\nx = 1\n"
        e = Edit(kind=EditKind.CHANGE_IMPORT,
                 params={"old_import": "import pandas", "new_import": "import pandas as pd"})
        result = self.apply(source, e)
        self.assertIn("import pandas as pd", result)
        self.assertNotIn("import pandas\n", result)

    def test_change_import_no_match_noop(self):
        source = "import numpy\n"
        e = Edit(kind=EditKind.CHANGE_IMPORT,
                 params={"old_import": "import pandas", "new_import": "import polars"})
        self.assertEqual(self.apply(source, e), source)

    def test_wrap_value(self):
        source = "result = compute(x)\nprint(result)\n"
        e = Edit(kind=EditKind.WRAP_VALUE, params={"name": "result", "wrapper": "str"})
        result = self.apply(source, e)
        self.assertIn("str(result)", result)

    def test_wrap_value_empty_name_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.WRAP_VALUE, params={"name": "", "wrapper": "str"})
        self.assertEqual(self.apply(source, e), source)

    def test_replace_call(self):
        source = "y = old_fn(x)\n"
        e = Edit(kind=EditKind.REPLACE_CALL,
                 params={"old_call": "old_fn(x)", "new_call": "new_fn(x)"})
        result = self.apply(source, e)
        self.assertIn("new_fn(x)", result)
        self.assertNotIn("old_fn(x)", result)

    def test_replace_call_empty_old_noop(self):
        source = "y = old_fn(x)\n"
        e = Edit(kind=EditKind.REPLACE_CALL, params={"old_call": "", "new_call": "new_fn(x)"})
        self.assertEqual(self.apply(source, e), source)

    def test_restructure_control_flow(self):
        old = "if x > 0:\n    y = 1\nelse:\n    y = 0\n"
        new = "y = 1 if x > 0 else 0\n"
        source = old + "z = y\n"
        e = Edit(kind=EditKind.RESTRUCTURE_CONTROL_FLOW,
                 params={"old_code": old, "new_code": new})
        result = self.apply(source, e)
        self.assertIn("y = 1 if x > 0 else 0", result)

    def test_restructure_control_flow_empty_old_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.RESTRUCTURE_CONTROL_FLOW,
                 params={"old_code": "", "new_code": "y = 2\n"})
        self.assertEqual(self.apply(source, e), source)

    def test_replace_library_name_and_import(self):
        source = "import pandas as pd\ndf = pd.DataFrame({'a': [1]})\n"
        e = Edit(kind=EditKind.REPLACE_LIBRARY,
                 params={
                     "old_name": "pd",
                     "new_name": "pl",
                     "old_import": "import pandas as pd",
                     "new_import": "import polars as pl",
                 })
        result = self.apply(source, e)
        self.assertIn("import polars as pl", result)
        self.assertIn("pl.DataFrame", result)
        self.assertNotIn("pd.DataFrame", result)

    def test_replace_library_empty_names_noop(self):
        source = "import pandas as pd\n"
        e = Edit(kind=EditKind.REPLACE_LIBRARY, params={"old_name": "", "new_name": "pl"})
        self.assertEqual(self.apply(source, e), source)

    def test_bad_params_returns_source_unchanged(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={})  # no "code" key
        # Returns source unchanged (empty code → noop)
        self.assertEqual(self.apply(source, e), source)


# ---------------------------------------------------------------------------
# T2 — TestEditHistory
# ---------------------------------------------------------------------------

class TestEditHistory(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.history import EditHistory
        self.EditHistory = EditHistory

    def test_empty_history_was_tried_false(self):
        h = self.EditHistory()
        e = _make_edit(EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        self.assertFalse(h.was_tried(e))

    def test_add_and_was_tried(self):
        h = self.EditHistory()
        e = _make_edit(EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        h.add(e)
        self.assertTrue(h.was_tried(e))

    def test_different_params_not_tried(self):
        h = self.EditHistory()
        e1 = _make_edit(EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        e2 = _make_edit(EditKind.INSERT_PREAMBLE, params={"code": "import sys"})
        h.add(e1)
        self.assertFalse(h.was_tried(e2))

    def test_different_kind_not_tried(self):
        h = self.EditHistory()
        e1 = _make_edit(EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        e2 = _make_edit(EditKind.RENAME_VARIABLE, params={"old": "x", "new": "y"})
        h.add(e1)
        self.assertFalse(h.was_tried(e2))

    def test_pattern_id_ignored_in_equality(self):
        h = self.EditHistory()
        e1 = _make_edit(EditKind.RENAME_VARIABLE, params={"old": "x", "new": "y"}, pattern_id="p1")
        e2 = _make_edit(EditKind.RENAME_VARIABLE, params={"old": "x", "new": "y"}, pattern_id="p2")
        h.add(e1)
        self.assertTrue(h.was_tried(e2))

    def test_clear_resets_history(self):
        h = self.EditHistory()
        e = _make_edit()
        h.add(e)
        h.clear()
        self.assertFalse(h.was_tried(e))
        self.assertEqual(h.tried, [])


# ---------------------------------------------------------------------------
# T3 — TestBuildEditPrompt
# ---------------------------------------------------------------------------

class TestBuildEditPrompt(unittest.TestCase):

    def _make_entity(self, name: str = "x", package: str | None = None):
        from r2py.stage1.entities import Entity, SourceLocation
        from r2py.types import EntityKind
        return Entity(
            id="e1",
            kind=EntityKind.VARIABLE,
            name=name,
            source_span=SourceLocation("test.R", 1, 0, 1, 10),
            dependencies=[],
            r_semantic_flags=["na_semantics"],
            package=package,
        )

    def setUp(self):
        from r2py.stage3.prompt import build_edit_prompt
        from r2py.stage3.history import EditHistory
        self.build = build_edit_prompt
        self.EditHistory = EditHistory

    def test_entity_name_in_prompt(self):
        entity = self._make_entity("my_var")
        es = _entity_score("e1")
        messages = self.build(entity, es, [], "x = 1", [], self.EditHistory(), exploit=False)
        content = messages[0]["content"]
        self.assertIn("my_var", content)

    def test_exploit_mode_includes_pattern_guidance(self):
        from r2py.library.pattern import Pattern, EvidenceEntry
        pat = Pattern(
            id="my.pattern", package="dplyr", confidence="confirmed", seed=False,
            guidance="Use polars.filter instead of pandas boolean mask.",
            evidence=[EvidenceEntry("s1", 0.9, "exact", "x")],
            contradictions=[],
            created="2026-01-01", last_review="2026-01-01",
        )
        entity = self._make_entity("x", package="dplyr")
        es = _entity_score("e1")
        messages = self.build(entity, es, [], "x = 1", [pat], self.EditHistory(), exploit=True)
        content = messages[0]["content"]
        self.assertIn("my.pattern", content)
        self.assertIn("polars.filter", content)

    def test_explore_mode_no_pattern_guidance(self):
        entity = self._make_entity()
        es = _entity_score("e1")
        messages = self.build(entity, es, [], "x = 1", [], self.EditHistory(), exploit=False)
        content = messages[0]["content"]
        self.assertIn("explore", content.lower())
        self.assertNotIn("Pattern Library guidance", content)

    def test_feedback_included_in_prompt(self):
        entity = self._make_entity()
        es = _entity_score("e1", avg=0.1)
        feedback = [FeedbackItem("e1", EffectClass.DATA, "value mismatch at row 0", 0.1)]
        messages = self.build(entity, es, feedback, "x = 1", [], self.EditHistory(), exploit=False)
        content = messages[0]["content"]
        self.assertIn("value mismatch", content)

    def test_history_shown_in_prompt(self):
        from r2py.stage3.history import EditHistory
        entity = self._make_entity()
        es = _entity_score("e1")
        h = EditHistory()
        h.add(_make_edit(EditKind.RENAME_VARIABLE, params={"old": "a", "new": "b"}))
        messages = self.build(entity, es, [], "x = 1", [], h, exploit=False)
        content = messages[0]["content"]
        self.assertIn("RenameVariable", content)

    def test_score_breakdown_in_prompt(self):
        entity = self._make_entity()
        es = EntityScore(entity_id="e1", data_output=0.123)
        messages = self.build(entity, es, [], "x = 1", [], self.EditHistory(), exploit=False)
        content = messages[0]["content"]
        self.assertIn("data_output", content)


# ---------------------------------------------------------------------------
# T4 — TestParseEditResponse
# ---------------------------------------------------------------------------

class TestParseEditResponse(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.prompt import parse_edit_response
        self.parse = parse_edit_response

    def test_valid_json_line(self):
        raw = '{"kind": "InsertPreamble", "entity_ids": [], "params": {"code": "import os"}, "pattern_id": "my.pat"}'
        result = self.parse(raw)
        self.assertIsNotNone(result)
        self.assertEqual(result["kind"], "InsertPreamble")

    def test_json_line_with_surrounding_prose(self):
        raw = (
            "Here is my proposed edit:\n"
            '{"kind": "RenameVariable", "entity_ids": ["e1"], "params": {"old": "foo", "new": "bar"}, "pattern_id": "x"}\n'
            "This renames foo to bar."
        )
        result = self.parse(raw)
        self.assertIsNotNone(result)
        self.assertEqual(result["kind"], "RenameVariable")

    def test_no_json_returns_none(self):
        raw = "I cannot propose an edit right now."
        self.assertIsNone(self.parse(raw))

    def test_invalid_json_returns_none(self):
        raw = "{invalid json here}"
        self.assertIsNone(self.parse(raw))

    def test_json_without_kind_returns_none(self):
        raw = '{"entity_ids": [], "params": {}}'
        self.assertIsNone(self.parse(raw))

    def test_first_json_wins(self):
        raw = (
            '{"kind": "InsertPreamble", "entity_ids": [], "params": {"code": "a"}, "pattern_id": "p1"}\n'
            '{"kind": "RenameVariable", "entity_ids": [], "params": {}, "pattern_id": "p2"}\n'
        )
        result = self.parse(raw)
        self.assertEqual(result["kind"], "InsertPreamble")


# ---------------------------------------------------------------------------
# T5 — TestAttributor
# ---------------------------------------------------------------------------

class TestAttributor(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.attributor import attribute, AttributionError
        self.attribute = attribute
        self.AttributionError = AttributionError

    def test_valid_attribution(self):
        e = _make_edit(pattern_id=None)
        attributed = self.attribute(e, "my.pattern")
        self.assertEqual(attributed.pattern_id, "my.pattern")

    def test_strips_whitespace_from_pattern_id(self):
        e = _make_edit(pattern_id=None)
        attributed = self.attribute(e, "  my.slug  ")
        self.assertEqual(attributed.pattern_id, "my.slug")

    def test_preserves_other_fields(self):
        e = Edit(kind=EditKind.RENAME_VARIABLE, entity_ids=["e1"],
                 params={"old": "x", "new": "y"}, pattern_id=None)
        attributed = self.attribute(e, "slug")
        self.assertEqual(attributed.kind, EditKind.RENAME_VARIABLE)
        self.assertEqual(attributed.entity_ids, ["e1"])
        self.assertEqual(attributed.params, {"old": "x", "new": "y"})

    def test_none_pattern_id_raises(self):
        e = _make_edit(pattern_id=None)
        with self.assertRaises(self.AttributionError):
            self.attribute(e, None)

    def test_empty_string_raises(self):
        e = _make_edit(pattern_id=None)
        with self.assertRaises(self.AttributionError):
            self.attribute(e, "")

    def test_whitespace_only_raises(self):
        e = _make_edit(pattern_id=None)
        with self.assertRaises(self.AttributionError):
            self.attribute(e, "   ")

    def test_attribution_error_is_value_error(self):
        from r2py.stage3.attributor import AttributionError
        self.assertTrue(issubclass(AttributionError, ValueError))


# ---------------------------------------------------------------------------
# T6 — TestEditTypesHelpers
# ---------------------------------------------------------------------------

class TestEditTypesHelpers(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.edit_types import edit_to_dict, dict_to_edit
        self.to_dict = edit_to_dict
        self.from_dict = dict_to_edit

    def test_round_trip(self):
        e = Edit(kind=EditKind.REPLACE_CALL, entity_ids=["e1"],
                 params={"old_call": "foo()", "new_call": "bar()"},
                 pattern_id="my.pat")
        d = self.to_dict(e)
        e2 = self.from_dict(d)
        self.assertEqual(e.kind, e2.kind)
        self.assertEqual(e.entity_ids, e2.entity_ids)
        self.assertEqual(e.params, e2.params)
        self.assertEqual(e.pattern_id, e2.pattern_id)

    def test_invalid_kind_raises(self):
        with self.assertRaises(ValueError):
            self.from_dict({"kind": "NotAKind", "entity_ids": [], "params": {}})

    def test_missing_kind_raises(self):
        with self.assertRaises(KeyError):
            self.from_dict({"entity_ids": [], "params": {}})


# ---------------------------------------------------------------------------
# T7 — TestPolicy (mocked LLM)
# ---------------------------------------------------------------------------

class TestPolicy(unittest.TestCase):

    def _make_script_map(self, entity_id: str = "e1"):
        from r2py.stage1.entities import Entity, SourceLocation
        from r2py.stage1.script_map import ScriptMap
        from r2py.types import EntityKind
        entity = Entity(
            id=entity_id,
            kind=EntityKind.VARIABLE,
            name="x",
            source_span=SourceLocation("test.R", 1, 0, 1, 5),
            dependencies=[],
            r_semantic_flags=[],
            package=None,
        )
        return ScriptMap(source="x <- 1", entities={entity_id: entity})

    def _make_library(self):
        lib = MagicMock()
        lib.retrieve.return_value = []
        return lib

    def _llm_response(self, kind="InsertPreamble", params=None, pid="test.pat"):
        d = {
            "kind": kind,
            "entity_ids": ["e1"],
            "params": params or {"code": "import os"},
            "pattern_id": pid,
        }
        return json.dumps(d)

    def test_exploit_path_uses_pattern_id(self):
        from r2py.library.pattern import Pattern, EvidenceEntry
        from r2py.stage3.history import EditHistory
        from r2py.stage3.policy import propose

        pat = Pattern(
            id="existing.pat", package=None, confidence="confirmed", seed=False,
            guidance="test guidance", evidence=[EvidenceEntry("s1", 0.9, "exact", "x")],
            contradictions=[], created="2026-01-01", last_review="2026-01-01",
        )
        lib = self._make_library()
        lib.retrieve.return_value = [pat]
        sm = self._make_script_map()
        candidate = _make_candidate({"e1": _entity_score("e1", 0.3)})
        history = EditHistory()

        response = self._llm_response(pid="existing.pat")
        with patch("r2py.stage3.policy._llm.call", return_value=response):
            with patch("r2py.stage3.policy.random.random", return_value=0.99):  # > epsilon → exploit
                edit = propose(candidate, sm, lib, history, epsilon=0.2)

        self.assertEqual(edit.pattern_id, "existing.pat")
        self.assertEqual(edit.kind, EditKind.INSERT_PREAMBLE)

    def test_explore_path_uses_llm_pattern_id(self):
        from r2py.stage3.history import EditHistory
        from r2py.stage3.policy import propose

        lib = self._make_library()
        lib.retrieve.return_value = []  # no patterns → always explore
        sm = self._make_script_map()
        candidate = _make_candidate({"e1": _entity_score("e1", 0.3)})
        history = EditHistory()

        response = self._llm_response(pid="new.slug")
        with patch("r2py.stage3.policy._llm.call", return_value=response):
            edit = propose(candidate, sm, lib, history, epsilon=0.2)

        self.assertEqual(edit.pattern_id, "new.slug")

    def test_already_tried_edit_skipped(self):
        from r2py.stage3.history import EditHistory
        from r2py.stage3.policy import propose

        lib = self._make_library()
        sm = self._make_script_map()
        candidate = _make_candidate({"e1": _entity_score("e1", 0.3)})
        history = EditHistory()
        # Pre-add the edit that the LLM would propose
        tried = Edit(kind=EditKind.INSERT_PREAMBLE, entity_ids=["e1"],
                     params={"code": "import os"}, pattern_id="test.pat")
        history.add(tried)

        # LLM proposes the same edit → should be skipped.
        response = self._llm_response()
        with patch("r2py.stage3.policy._llm.call", return_value=response):
            with self.assertRaises(RuntimeError):
                propose(candidate, sm, lib, history, epsilon=0.2)

    def test_no_entities_raises(self):
        from r2py.stage3.history import EditHistory
        from r2py.stage3.policy import propose
        from r2py.stage1.script_map import ScriptMap

        lib = self._make_library()
        sm = ScriptMap(source="", entities={})
        candidate = _make_candidate({})
        history = EditHistory()

        with self.assertRaises(RuntimeError):
            propose(candidate, sm, lib, history)

    def test_parse_failure_tries_next_entity(self):
        from r2py.stage3.history import EditHistory
        from r2py.stage3.policy import propose
        from r2py.stage1.entities import Entity, SourceLocation
        from r2py.stage1.script_map import ScriptMap
        from r2py.types import EntityKind

        e1 = Entity(id="e1", kind=EntityKind.VARIABLE, name="a",
                    source_span=SourceLocation("t.R", 1, 0, 1, 5),
                    dependencies=[], r_semantic_flags=[], package=None)
        e2 = Entity(id="e2", kind=EntityKind.VARIABLE, name="b",
                    source_span=SourceLocation("t.R", 2, 0, 2, 5),
                    dependencies=[], r_semantic_flags=[], package=None)
        sm = ScriptMap(source="", entities={"e1": e1, "e2": e2})

        by_entity = {
            "e1": _entity_score("e1", 0.1),  # weakest
            "e2": _entity_score("e2", 0.9),
        }
        candidate = _make_candidate(by_entity)
        history = EditHistory()
        lib = self._make_library()

        # First call (e1) returns unparseable; second (e2) returns valid JSON
        valid_resp = self._llm_response(pid="good.pat")
        with patch("r2py.stage3.policy._llm.call",
                   side_effect=["not valid json", valid_resp]):
            edit = propose(candidate, sm, lib, history, epsilon=1.0)  # epsilon=1 → always explore

        self.assertEqual(edit.pattern_id, "good.pat")


# ---------------------------------------------------------------------------
# T8 — TestEditor
# ---------------------------------------------------------------------------

class TestEditor(unittest.TestCase):

    def test_epsilon_decay(self):
        from r2py.stage3.editor import _epsilon
        self.assertAlmostEqual(_epsilon(0), 0.30)
        self.assertAlmostEqual(_epsilon(10), 0.05)
        self.assertAlmostEqual(_epsilon(20), 0.05)  # floor

    def test_epsilon_midpoint(self):
        from r2py.stage3.editor import _epsilon
        self.assertAlmostEqual(_epsilon(5), 0.175)

    def test_apply_edit_re_exported(self):
        from r2py.stage3.editor import apply_edit
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        result = apply_edit("x = 1\n", e)
        self.assertIn("import os", result)

    def test_propose_edit_delegates_to_policy(self):
        from r2py.stage3.editor import propose_edit
        from r2py.stage3.history import EditHistory
        from r2py.stage1.script_map import ScriptMap

        sm = ScriptMap(source="", entities={})
        candidate = _make_candidate({})
        lib = MagicMock()
        history = EditHistory()

        with patch("r2py.stage3.policy.propose", side_effect=RuntimeError("no entities")):
            with self.assertRaises(RuntimeError):
                propose_edit(candidate, lib, sm, history, iteration=3)


# ---------------------------------------------------------------------------
# T9 — TestStage3Init (public interface)
# ---------------------------------------------------------------------------

class TestStage3Init(unittest.TestCase):

    def test_apply_edit_callable(self):
        from r2py.stage3 import apply_edit
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "foo", "new": "bar"},
                 pattern_id="p1")
        result = apply_edit("foo = 1\n", e)
        self.assertIn("bar = 1", result)

    def test_propose_edit_importable(self):
        from r2py.stage3 import propose_edit
        self.assertTrue(callable(propose_edit))

    def test_propose_edit_raises_runtime_on_empty_map(self):
        from r2py.stage3 import propose_edit
        from r2py.stage1.script_map import ScriptMap

        sm = ScriptMap(source="", entities={})
        candidate = _make_candidate({})
        lib = MagicMock()
        lib.retrieve.return_value = []

        with patch("r2py.stage3.policy._llm.call", return_value="no json"):
            with self.assertRaises(RuntimeError):
                propose_edit(candidate, lib, sm)

    def test_edit_history_importable_from_stage3(self):
        from r2py.stage3.history import EditHistory
        h = EditHistory()
        self.assertIsNotNone(h)


if __name__ == "__main__":
    unittest.main()
