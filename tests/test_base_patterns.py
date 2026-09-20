"""Tests for base-R patterns: verified statements attached to every base function they call."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import r2py
from r2py.library import PatternLibrary
from r2py.library.pattern import Pattern, TranslationExample, from_markdown, pattern_id, to_markdown
from r2py.library.retrieval import retrieve_base_patterns
from r2py.library.writer import _add_translation_example
from r2py.seed import _MAX_BASE_PATTERNS_IN_PROMPT, _build_prompt
from r2py.types import EntityKind


def _entity(name, line, kind, calls, *, package=None, rhs=None, rhs_pkg=None):
    return SimpleNamespace(name=name, package=package, kind=kind, base_r_calls=calls,
                           rhs_call_name=rhs, rhs_call_package=rhs_pkg,
                           source_span=SimpleNamespace(start_line=line, end_line=line))


R_SOURCE = "\n".join([
    'x <- paste("a")',                       # 0  paste, focused (1 base call)
    'print(paste("a", format(1)))',          # 1  print, paste, format (3 base calls)
    "v <- c(1, 2)",                          # 2  only c(): informative for nothing
    "y <- mutate(df, s = paste(a))",         # 3  paste inside a package call (1 base call)
])
PY_SOURCE = "\n".join([
    "# r2py:entity:e0", "x = 'a'",
    "# r2py:entity:e1", "print('a ' + fmt(1))",
    "# r2py:entity:e2", "v = [1, 2]",
    "# r2py:entity:e3", "y = df.assign(s=lambda d: d.a)",
]) + "\n"
ENTITIES = {
    "e0": _entity("x", 0, EntityKind.VARIABLE, ["base::paste"], rhs="paste", rhs_pkg="base"),
    "e1": _entity("print", 1, EntityKind.FUNCTION_CALL, ["base::print", "base::paste", "base::format"], package="base"),
    "e2": _entity("v", 2, EntityKind.VARIABLE, ["base::c"], rhs="c", rhs_pkg="base"),
    "e3": _entity("y", 3, EntityKind.VARIABLE, ["base::paste"], rhs="mutate", rhs_pkg=None),
}


class TestCapture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.lib = PatternLibrary(root / "lib")
        self.r_path, self.py_path = root / "s.R", root / "s.py"

    def tearDown(self):
        self._tmp.cleanup()

    def _seed(self, r_src=R_SOURCE, py_src=PY_SOURCE, entities=ENTITIES, script_id="s1"):
        self.r_path.write_text(r_src, encoding="utf-8")
        self.py_path.write_text(py_src, encoding="utf-8")
        with patch("r2py.stage1.analyze", return_value=SimpleNamespace(entities=entities, source=r_src)):
            return r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib, script_id=script_id)

    def test_every_informative_base_function_gets_a_pattern(self):
        touched = self._seed()
        self.assertEqual(sorted(touched), ["base.format", "base.paste", "base.print"])
        self.assertIsNone(self.lib.store.get("base.c"))  # c() and list() key nothing

    def test_one_example_per_function_per_script_from_the_most_focused_statement(self):
        self._seed()
        (ex,) = self.lib.store.get("base.paste").translation_examples
        self.assertEqual(ex.r_snippet, 'x <- paste("a")')   # 1 base call beats the 3-call statement
        self.assertEqual(ex.n_calls, 1)
        (fmt,) = self.lib.store.get("base.format").translation_examples
        self.assertEqual((fmt.r_snippet, fmt.n_calls), ('print(paste("a", format(1)))', 3))

    def test_a_pattern_made_only_from_nested_calls_says_so(self):
        self._seed()
        self.assertIn("inside a statement", self.lib.store.get("base.format").guidance)

    def test_the_focus_of_an_exact_example_is_recorded_too(self):
        self._seed()
        (ex,) = self.lib.store.get("base.print").translation_examples
        self.assertEqual(ex.n_calls, 3)

    def test_unverified_entities_teach_nothing(self):
        report = SimpleNamespace(by_entity={
            eid: SimpleNamespace(executed_ok=False, active_dims=frozenset()) for eid in ENTITIES})
        with patch("r2py.stage1.analyze", return_value=SimpleNamespace(entities=ENTITIES, source=R_SOURCE)):
            self.r_path.write_text(R_SOURCE, encoding="utf-8")
            self.py_path.write_text(PY_SOURCE, encoding="utf-8")
            touched = r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib,
                                                 score_report=report, entity_score_threshold=0.9)
        self.assertEqual(touched, [])

    def test_a_more_focused_example_from_a_later_script_is_shown_first(self):
        focus = lambda: [e.n_calls for e in self.lib.store.get("base.paste").translation_examples]
        self._seed(entities={"e1": ENTITIES["e1"]}, script_id="busy")      # paste inside a 3-call statement
        self.assertEqual(focus(), [3])
        self._seed(entities={"e0": ENTITIES["e0"]}, script_id="focused")   # paste in a 1-call statement
        self.assertEqual(focus(), [1, 3])                                   # the focused one now comes first


class TestFocusOrdering(unittest.TestCase):
    def _ex(self, r, n, score=1.0):
        return TranslationExample(r_hash=r, r_snippet=r, py_snippet="p", score=score, script_id="s", n_calls=n)

    def test_keeps_the_three_most_focused_then_highest_score(self):
        pat = Pattern(id="base.f", package="base", confidence="tentative", seed=True, guidance="g")
        for r, n, s in [("a", 5, 1.0), ("b", 1, 0.91), ("c", 3, 1.0), ("d", 1, 1.0), ("e", 2, 1.0)]:
            _add_translation_example(pat, self._ex(r, n, s))
        self.assertEqual([e.r_snippet for e in pat.translation_examples], ["d", "b", "e"])

    def test_round_trips_and_defaults_for_older_files(self):
        pat = Pattern(id="base.f", package="base", confidence="tentative", seed=True, guidance="g",
                      translation_examples=[self._ex("a", 4)])
        self.assertEqual(from_markdown(to_markdown(pat)).translation_examples[0].n_calls, 4)
        legacy = to_markdown(pat).replace(', "n_calls": 4', "")
        self.assertNotIn("n_calls", legacy)
        self.assertEqual(from_markdown(legacy).translation_examples[0].n_calls, 0)


class TestRetrieveBasePatterns(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.lib = PatternLibrary(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _store(self, qualified, *, n=1, example=True, confidence="tentative"):
        pkg, fn = qualified.split("::")
        pat = Pattern(id=pattern_id(pkg, fn), package=pkg, confidence=confidence, seed=True, guidance="g")
        if example:
            pat.translation_examples = [TranslationExample("h", f"r_{fn}", f"p_{fn}", 1.0, "s", n)]
        self.lib.store.save(pat)

    def _get(self, entity, **kw):
        return [p.id for p in self.lib.retrieve_base_patterns(entity, **kw)]

    def test_returns_the_patterns_of_the_functions_called_inside_the_entity(self):
        for q in ("base::paste", "base::format", "base::round"):
            self._store(q)
        e = _entity("res", 0, EntityKind.VARIABLE, ["base::paste", "base::format"])
        self.assertEqual(self._get(e), ["base.paste", "base.format"])

    def test_the_function_that_keys_the_entity_is_left_to_exact_retrieval(self):
        self._store("base::paste")
        self._store("base::format")
        e = _entity("x", 0, EntityKind.VARIABLE, ["base::paste", "base::format"], rhs="paste", rhs_pkg="base")
        self.assertEqual(self._get(e), ["base.format"])

    def test_needs_an_example_and_respects_the_usual_filters(self):
        self._store("base::paste", example=False)
        self._store("base::format", confidence="contradicted")
        self._store("base::round")
        e = _entity("x", 0, EntityKind.VARIABLE, ["base::paste", "base::format", "base::round"])
        self.assertEqual(self._get(e), ["base.round"])
        self.assertEqual(self._get(e, no_seeds=True), [])

    def test_ubiquitous_calls_and_unknown_entities_give_nothing(self):
        self._store("base::c")
        self.assertEqual(self._get(_entity("x", 0, EntityKind.VARIABLE, ["base::c", "base::list"])), [])
        self.assertEqual(self._get(SimpleNamespace()), [])


class TestPromptSection(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.lib = PatternLibrary(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _store(self, fn, n=1, r=None):
        pat = Pattern(id=pattern_id("base", fn), package="base", confidence="tentative", seed=True, guidance="g",
                      translation_examples=[TranslationExample("h", r or f"r_{fn}", f"p_{fn}", 1.0, "s", n)])
        self.lib.store.save(pat)

    def _prompt(self, *entities, show=True):
        self.lib.show_base_patterns = show
        script_map = SimpleNamespace(source="x <- 1\n", entity_bundles={},
                                     entities={f"e{i}": e for i, e in enumerate(entities)})
        return "\n".join(_build_prompt(script_map, self.lib))

    def test_a_focused_example_is_shown_under_its_own_heading(self):
        self._store("paste")
        text = self._prompt(_entity("x", 0, EntityKind.VARIABLE, ["base::paste"]))
        self.assertIn("## Base-R usage", text)
        self.assertIn("**base.paste**\n  R: `r_paste`\n  Python: `p_paste`", text)

    def test_can_be_switched_off(self):
        self._store("paste")
        self.assertNotIn("Base-R usage", self._prompt(_entity("x", 0, EntityKind.VARIABLE, ["base::paste"]), show=False))

    def test_library_imports_and_unmatched_functions_show_nothing(self):
        self._store("paste")
        self.assertNotIn("Base-R usage", self._prompt(_entity("p", 0, EntityKind.LIBRARY_IMPORT, ["base::paste"])))
        self.assertNotIn("Base-R usage", self._prompt(_entity("x", 0, EntityKind.VARIABLE, ["base::format"])))

    def test_the_cap_keeps_the_most_focused_examples(self):
        fns = [f"f{i:02d}" for i in range(_MAX_BASE_PATTERNS_IN_PROMPT + 3)]
        for i, fn in enumerate(fns):
            self._store(fn, n=i + 1)
        text = self._prompt(*[_entity(fn, 0, EntityKind.VARIABLE, [f"base::{fn}"]) for fn in fns])
        shown = [fn for fn in fns if f"**base.{fn}**" in text]
        self.assertEqual(shown, fns[:_MAX_BASE_PATTERNS_IN_PROMPT])

    def test_a_pattern_already_shown_as_an_exact_match_is_not_repeated(self):
        self._store("paste")
        call = _entity("paste", 0, EntityKind.FUNCTION_CALL, ["base::paste"], package="base")
        other = _entity("x", 1, EntityKind.VARIABLE, ["base::paste"])
        text = self._prompt(call, other)
        self.assertIn("## Translation patterns", text)
        self.assertEqual(text.count("**base.paste**"), 1)
        self.assertNotIn("## Base-R usage", text)


if __name__ == "__main__":
    unittest.main()
