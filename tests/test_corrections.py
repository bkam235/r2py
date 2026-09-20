"""Tests for corrections: base-R calls per entity, capture, retrieval, and the prompt section."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import r2py
from r2py.library import PatternLibrary
from r2py.library.pattern import EditExample, Pattern, correction_functions, pattern_id
from r2py.seed import _MAX_FIXES_IN_PROMPT, _build_prompt
from r2py.stage1.ast import parse
from r2py.stage1.script_map import ScriptMap, from_json, to_json
from r2py.stage1.walker import walk
from r2py.types import EntityKind, EntityScore, ScoreReport


# ---------------------------------------------------------------------------
# Stage 1: base-R calls inside an entity
# ---------------------------------------------------------------------------

class TestBaseRCalls(unittest.TestCase):
    def _calls(self, src: str) -> dict[str, list[str]]:
        entities, _ = walk(parse(src), "t.R")
        return {e.name: e.base_r_calls for e in entities.values()}

    def test_nested_calls_are_found_not_just_the_outermost(self):
        calls = self._calls("library(dplyr)\nprint(mutate(df, s = paste(a, format(b))))\n")
        self.assertEqual(calls["print"], ["base::print", "base::paste", "base::format"])

    def test_assignments_expose_the_functions_on_their_right_hand_side(self):
        calls = self._calls("res <- lapply(1:3, function(i) round(i / 3, 2))\n")
        self.assertEqual(calls["res"], ["base::lapply", "base::round"])

    def test_package_is_the_exporting_package(self):
        calls = self._calls("head(y)\nz <- sd(y)\n")
        self.assertEqual(calls["head"], ["utils::head"])
        self.assertEqual(calls["z"], ["stats::sd"])

    def test_qualified_calls_count_only_for_base_packages(self):
        calls = self._calls("z <- base::sprintf('%d', 1L)\ny <- dplyr::filter(df, a > 1)\n")
        self.assertEqual(calls["z"], ["base::sprintf"])
        self.assertEqual(calls["y"], [])  # filter is also a stats export, but this is dplyr's

    def test_functions_the_script_defines_are_not_base_calls(self):
        calls = self._calls("paste <- function(...) 1\nx <- paste('a')\ny <- format(2)\n")
        self.assertEqual(calls["x"], [])
        self.assertEqual(calls["y"], ["base::format"])

    def test_imports_and_return_are_not_behavioural(self):
        calls = self._calls("suppressPackageStartupMessages(library(dplyr))\n")
        self.assertEqual(calls["suppressPackageStartupMessages"], [])

    def test_survives_a_script_map_round_trip(self):
        src = "x <- paste('a', format(1))\n"
        root = parse(src)
        entities, _ = walk(root, "t.R")
        sm = ScriptMap(source=src, ast_root=root, entities=entities, effects=[])
        back = from_json(to_json(sm))
        self.assertEqual(back.entities["x"].base_r_calls, ["base::paste", "base::format"])

    def test_ubiquitous_calls_do_not_key_corrections(self):
        self.assertEqual(correction_functions(["base::c", "base::paste", "base::list"]), ["base::paste"])


# ---------------------------------------------------------------------------
# Capture: seed_from_translation with the pre-agent translation
# ---------------------------------------------------------------------------

R_SOURCE = "\n".join([
    'x <- paste("a", format(1.5))',   # 0  base::paste, base::format (fixed by the agent)
    "print(x)",                        # 1  base::print (right first time)
    "y <- c(1, 2)",                    # 2  base::c only (ubiquitous: never a key)
    "s <- sd(y)",                      # 3  stats::sd (seed crashed, then fixed)
])

FINAL_PY = "\n".join([
    "# r2py:entity:e_x", "x = ' '.join(['a', format_num(1.5)])",
    "# r2py:entity:e_print", "print(x)",
    "# r2py:entity:e_y", "y = [1, 2]",
    "# r2py:entity:e_sd", "s = statistics.stdev(y)",
]) + "\n"

SEED_PY = "\n".join([
    "# r2py:entity:e_x", "x = 'a' + str(1.5)",
    "# r2py:entity:e_print", "print(x)",
    "# r2py:entity:e_y", "y = [1, 2]",
    "# r2py:entity:e_sd", "s = np.std(y)",
]) + "\n"


def _entity(name, line, kind, calls, package=None):
    return SimpleNamespace(name=name, package=package, kind=kind, base_r_calls=calls,
                           source_span=SimpleNamespace(start_line=line, end_line=line))


ENTITIES = {
    "e_x": _entity("x", 0, EntityKind.VARIABLE, ["base::paste", "base::format"]),
    "e_print": _entity("print", 1, EntityKind.FUNCTION_CALL, ["base::print"], package="base"),
    "e_y": _entity("y", 2, EntityKind.VARIABLE, ["base::c"]),
    "e_sd": _entity("s", 3, EntityKind.VARIABLE, ["stats::sd"]),
}


def _es(eid, *, ok=True, **dims):
    return EntityScore(entity_id=eid, executed_ok=ok, **{
        d: dims.get(d, 1.0) for d in ("type_match", "control_flow_match", "data_output",
                                       "variable_output", "callable_output", "side_effects")})


FINAL_REPORT = ScoreReport(aggregate=1.0, by_entity={e: _es(e) for e in ENTITIES})
SEED_REPORT = ScoreReport(aggregate=0.6, by_entity={
    "e_x": _es("e_x", data_output=0.2),    # ran, wrong values
    "e_print": _es("e_print"),              # right first time
    "e_y": _es("e_y"),
    "e_sd": _es("e_sd", ok=False),          # crashed
})


class TestCaptureCorrections(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.libdir = root / "lib"
        self.lib = PatternLibrary(self.libdir)
        self.r_path, self.py_path = root / "s.R", root / "s.py"
        self.r_path.write_text(R_SOURCE, encoding="utf-8")
        self.py_path.write_text(FINAL_PY, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _seed(self, *, with_seed=True, seed_py=SEED_PY, script_id="s1"):
        script_map = SimpleNamespace(entities=ENTITIES, source=R_SOURCE)
        kwargs = dict(seed_source=seed_py, seed_score_report=SEED_REPORT) if with_seed else {}
        with patch("r2py.stage1.analyze", return_value=script_map):
            return r2py.seed_from_translation(
                self.r_path, self.py_path, library=self.lib, script_id=script_id,
                score_report=FINAL_REPORT, entity_score_threshold=0.9, **kwargs)

    def _edits(self, pid):
        pat = self.lib.store.get(pid)
        return pat.edit_examples if pat else []

    def test_the_correction_is_stored_on_each_base_function_the_entity_calls(self):
        self._seed()
        for pid in ("base.paste", "base.format"):
            (ex,) = self._edits(pid)
            self.assertEqual(ex.r_snippet, 'x <- paste("a", format(1.5))')
            self.assertEqual(ex.old_code.strip().splitlines()[-1], "x = 'a' + str(1.5)")
            self.assertIn("format_num", ex.new_code)
            self.assertEqual(ex.functions, ["base::paste", "base::format"])
            self.assertEqual(ex.script_id, "s1")
            self.assertGreater(ex.score_delta, 0)

    def test_failure_class_names_what_improved(self):
        self._seed()
        self.assertEqual(self._edits("base.paste")[0].failure_class, "data_output")
        self.assertEqual(self._edits("stats.sd")[0].failure_class, "crash")

    def test_only_entities_that_improved_produce_corrections(self):
        self._seed()
        self.assertEqual(self._edits("base.print"), [])  # right first time
        self.assertIsNone(self.lib.store.get("base.c"))   # ubiquitous: never a key

    def test_a_corrected_function_holds_both_the_verified_statement_and_the_fix(self):
        self._seed()
        pat = self.lib.store.get("base.format")
        self.assertEqual((pat.seed, pat.confidence), (True, "tentative"))
        self.assertEqual(len(pat.translation_examples), 1)  # the verified statement, from the nested pass
        self.assertEqual(len(pat.edit_examples), 1)         # and the correction

    def test_an_existing_translation_pattern_gains_the_correction_too(self):
        self._seed()
        # base.print got its usual example from the exact-function pass and nothing else
        self.assertEqual(len(self.lib.store.get("base.print").translation_examples), 1)

    def test_no_corrections_without_the_pre_agent_translation(self):
        self._seed(with_seed=False)
        self.assertTrue(all(not p.edit_examples for p in self.lib.store.load_all().values()))

    def test_an_unchanged_translation_is_not_a_correction(self):
        self._seed(seed_py=FINAL_PY)
        self.assertTrue(all(not p.edit_examples for p in self.lib.store.load_all().values()))

    def test_rerunning_does_not_duplicate_and_the_fields_persist(self):
        self._seed()
        self._seed()
        self.assertEqual(len(self._edits("base.paste")), 1)
        reloaded = PatternLibrary(self.libdir).store.get("base.paste").edit_examples[0]
        self.assertEqual((reloaded.functions, reloaded.r_snippet),
                         (["base::paste", "base::format"], 'x <- paste("a", format(1.5))'))


# ---------------------------------------------------------------------------
# Retrieval and the prompt
# ---------------------------------------------------------------------------

def _fix(functions, delta, script="s", r="x <- f()", new="new"):
    return EditExample(failure_class="data_output", old_code="old", new_code=new, score_delta=delta,
                       script_id=script, r_snippet=r, functions=functions)


class TestRetrieveCorrections(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.lib = PatternLibrary(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _store(self, qualified, *fixes, confidence="tentative", seed=True):
        package, fn = qualified.split("::")
        self.lib.store.save(Pattern(id=pattern_id(package, fn), package=package, confidence=confidence,
                                    seed=seed, guidance="g", edit_examples=list(fixes)))

    def _get(self, calls, **kw):
        return self.lib.retrieve_corrections(SimpleNamespace(base_r_calls=calls), **kw)

    def test_more_shared_functions_beat_a_bigger_gain(self):
        both = _fix(["base::paste", "base::format"], 0.3, script="a")
        one = _fix(["base::paste"], 0.9, script="b")
        self._store("base::paste", both, one)
        self._store("base::format", both)
        got = self._get(["base::paste", "base::format"], k=2)
        self.assertEqual([f.script_id for f in got], ["a", "b"])  # `both` appears once, not twice
        self.assertEqual([f.script_id for f in self._get(["base::paste", "base::format"], k=1)], ["a"])

    def test_the_key_is_the_functions_called_not_the_entity_name(self):
        self._store("base::format", _fix(["base::format"], 0.5))
        self.assertEqual(len(self._get(["base::paste", "base::format"])), 1)
        self.assertEqual(self._get(["base::paste"]), [])

    def test_ubiquitous_calls_never_match(self):
        self._store("base::c", _fix(["base::c"], 0.9))
        self.assertEqual(self._get(["base::c", "base::list"]), [])

    def test_contradicted_and_seed_filters_apply(self):
        self._store("base::paste", _fix(["base::paste"], 0.5), confidence="contradicted")
        self.assertEqual(self._get(["base::paste"]), [])
        self._store("base::format", _fix(["base::format"], 0.5))
        self.assertEqual(self._get(["base::format"], no_seeds=True), [])

    def test_an_entity_without_base_calls_gets_nothing(self):
        self.assertEqual(self.lib.retrieve_corrections(SimpleNamespace()), [])


class TestPromptFixes(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.lib = PatternLibrary(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _store(self, qualified, *fixes):
        package, fn = qualified.split("::")
        self.lib.store.save(Pattern(id=pattern_id(package, fn), package=package, confidence="tentative",
                                    seed=True, guidance="Verified fixes.", edit_examples=list(fixes)))

    def _prompt(self, *entities, show=True):
        self.lib.show_corrections = show
        script_map = SimpleNamespace(source="x <- 1\n", entity_bundles={},
                                     entities={f"e{i}": e for i, e in enumerate(entities)})
        return "\n".join(_build_prompt(script_map, self.lib))

    def _entity(self, calls, name="x", kind=EntityKind.VARIABLE, package=None):
        return SimpleNamespace(name=name, package=package, kind=kind, base_r_calls=calls, source_span=None)

    def test_a_relevant_fix_is_shown_with_both_attempts(self):
        self._store("base::paste", _fix(["base::paste"], 0.4, r='x <- paste("a")', new="x = 'a'"))
        text = self._prompt(self._entity(["base::paste"]))
        self.assertIn("## Verified fixes", text)
        self.assertIn('x <- paste("a")', text)
        self.assertIn("First attempt (wrong): `old`", text)
        self.assertIn("Corrected: `x = 'a'`", text)
        self.assertIn("calls base::paste", text)

    def test_switched_off_or_irrelevant_shows_nothing(self):
        self._store("base::paste", _fix(["base::paste"], 0.4))
        self.assertNotIn("Verified fixes", self._prompt(self._entity(["base::paste"]), show=False))
        self.assertNotIn("Verified fixes", self._prompt(self._entity(["base::format"])))

    def test_library_imports_are_skipped(self):
        self._store("base::paste", _fix(["base::paste"], 0.4))
        text = self._prompt(self._entity(["base::paste"], kind=EntityKind.LIBRARY_IMPORT))
        self.assertNotIn("Verified fixes", text)

    def test_at_most_a_handful_are_shown_best_gain_first(self):
        fns = [f"f{i}" for i in range(_MAX_FIXES_IN_PROMPT + 2)]
        for i, fn in enumerate(fns):
            self._store(f"base::{fn}", _fix([f"base::{fn}"], 0.1 * (i + 1), script=fn, r=f"r_{fn}"))
        text = self._prompt(*[self._entity([f"base::{fn}"], name=fn) for fn in fns])
        shown = [fn for fn in fns if f"`r_{fn}`" in text]
        self.assertEqual(len(shown), _MAX_FIXES_IN_PROMPT)
        self.assertEqual(shown, fns[-_MAX_FIXES_IN_PROMPT:])  # the highest gains

    def test_a_corrections_only_pattern_is_not_shown_as_a_translation_pattern(self):
        self._store("base::print", _fix(["base::print"], 0.4))
        text = self._prompt(self._entity(["base::print"], name="print",
                                         kind=EntityKind.FUNCTION_CALL, package="base"))
        self.assertNotIn("## Translation patterns", text)
        self.assertIn("## Verified fixes", text)


if __name__ == "__main__":
    unittest.main()
