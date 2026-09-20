"""Tests for keying assignments (`x <- f(...)`) by the function on their right-hand side."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import r2py
from r2py.library import PatternLibrary
from r2py.library.pattern import Pattern, TranslationExample, pattern_id, pattern_key
from r2py.seed import _build_prompt
from r2py.stage1 import _probe_function_metadata
from r2py.stage1.ast import parse
from r2py.stage1.entities import Entity, SourceLocation
from r2py.stage1.script_map import ScriptMap, from_json, to_json
from r2py.stage1.walker import walk
from r2py.types import EntityKind


# ---------------------------------------------------------------------------
# Stage 1: the walker records the right-hand call
# ---------------------------------------------------------------------------

class TestWalkerRecordsRightHandCall(unittest.TestCase):
    def _rhs(self, src: str) -> dict[str, tuple]:
        entities, _ = walk(parse(src), "t.R")
        return {e.name: (e.rhs_call_name, e.rhs_call_package)
                for e in entities.values() if e.kind == EntityKind.VARIABLE}

    def test_base_calls_are_resolved_statically(self):
        got = self._rhs('x <- paste("a")\ns = sd(x)\n')
        self.assertEqual(got["x"], ("paste", "base"))
        self.assertEqual(got["s"], ("sd", "stats"))

    def test_a_qualified_call_names_its_package(self):
        self.assertEqual(self._rhs("y <- dplyr::filter(df, a > 1)\n")["y"], ("filter", "dplyr"))

    def test_an_unqualified_package_call_is_left_for_the_r_probe(self):
        self.assertEqual(self._rhs("library(dplyr)\nz <- mutate(df, b = 1)\n")["z"], ("mutate", None))

    def test_forms_that_cannot_key_a_pattern_are_ignored(self):
        got = self._rhs("f <- function(a) a\nu <- f(1)\nw <- df |> mutate(b = 1)\nt <- obj$m(1)\nr <- 5\n")
        for name in ("u", "w", "t"):
            self.assertEqual(got[name], (None, None), name)  # script-defined, pipe, method call

    def test_survives_a_script_map_round_trip(self):
        src = "x <- paste('a')\n"
        root = parse(src)
        entities, _ = walk(root, "t.R")
        back = from_json(to_json(ScriptMap(source=src, ast_root=root, entities=entities, effects=[])))
        self.assertEqual((back.entities["x"].rhs_call_name, back.entities["x"].rhs_call_package),
                         ("paste", "base"))


# ---------------------------------------------------------------------------
# Stage 1: the R probe resolves the package of an unqualified call
# ---------------------------------------------------------------------------

def _entity(eid, kind, name, **kw):
    return Entity(id=eid, kind=kind, name=name, source_span=SourceLocation("t.R", 0, 0, 0, 10), **kw)


def _probe_output(eid, where):
    return "__R2PY_META__%s__%s\n" % (eid, json.dumps({"formals": {}, "methods": [], "where": where}))


class TestProbeResolvesAssignmentPackage(unittest.TestCase):
    def _probe(self, entities, stdout):
        with patch("r2py.stage1.run_slice", return_value=SimpleNamespace(stdout=stdout)):
            _probe_function_metadata("library(dplyr)\n", entities, 5)

    def test_package_comes_from_the_first_attached_package(self):
        entities = {"z": _entity("z", EntityKind.VARIABLE, "z", rhs_call_name="mutate")}
        self._probe(entities, _probe_output("z", ["package:dplyr", "namespace:dplyr"]))
        self.assertEqual(entities["z"].rhs_call_package, "dplyr")
        self.assertIsNone(entities["z"].function_metadata)  # a variable does not get the callee's formals

    def test_a_call_entity_of_the_same_function_shares_the_probe(self):
        entities = {
            "z": _entity("z", EntityKind.VARIABLE, "z", rhs_call_name="mutate"),
            "mutate": _entity("mutate", EntityKind.FUNCTION_CALL, "mutate"),
        }
        self._probe(entities, _probe_output("mutate", ["package:dplyr"]))
        self.assertEqual(entities["z"].rhs_call_package, "dplyr")
        self.assertEqual(entities["mutate"].function_metadata.where, ["package:dplyr"])

    def test_unresolved_stays_unresolved(self):
        entities = {"z": _entity("z", EntityKind.VARIABLE, "z", rhs_call_name="mystery")}
        self._probe(entities, _probe_output("z", [".GlobalEnv"]))
        self.assertIsNone(entities["z"].rhs_call_package)
        entities = {"z": _entity("z", EntityKind.VARIABLE, "z", rhs_call_name="mystery")}
        self._probe(entities, "")
        self.assertIsNone(entities["z"].rhs_call_package)

    def test_already_resolved_assignments_are_not_probed(self):
        entities = {"x": _entity("x", EntityKind.VARIABLE, "x", rhs_call_name="paste", rhs_call_package="base")}
        with patch("r2py.stage1.run_slice") as run_slice:
            _probe_function_metadata("x <- paste('a')\n", entities, 5)
        run_slice.assert_not_called()


# ---------------------------------------------------------------------------
# The library: key, retrieval, seeding, prompt
# ---------------------------------------------------------------------------

def _assign(name, rhs, pkg, line=0):
    return SimpleNamespace(name=name, package=None, kind=EntityKind.VARIABLE, rhs_call_name=rhs,
                           rhs_call_package=pkg, base_r_calls=[],
                           source_span=SimpleNamespace(start_line=line, end_line=line))


def _call(name, pkg, line=0):
    return SimpleNamespace(name=name, package=pkg, kind=EntityKind.FUNCTION_CALL, base_r_calls=[],
                           source_span=SimpleNamespace(start_line=line, end_line=line))


class TestPatternKey(unittest.TestCase):
    def test_a_call_is_keyed_by_itself(self):
        self.assertEqual(pattern_key(_call("mutate", "dplyr")), ("dplyr", "mutate"))

    def test_an_assignment_is_keyed_by_its_right_hand_call(self):
        self.assertEqual(pattern_key(_assign("z", "mutate", "dplyr")), ("dplyr", "mutate"))

    def test_no_key_without_a_package_or_for_ubiquitous_constructors(self):
        self.assertIsNone(pattern_key(_assign("z", "mutate", None)))
        self.assertIsNone(pattern_key(_assign("v", "c", "base")))
        self.assertIsNone(pattern_key(_assign("v", "list", "base")))
        self.assertIsNone(pattern_key(SimpleNamespace(name="x", package=None)))
        self.assertEqual(pattern_key(_assign("v", "matrix", "base")), ("base", "matrix"))


R_SOURCE = "\n".join(['y <- paste("a", "b")', 'paste("c")', "v <- c(1, 2)", "z <- mutate(df, b = 1)"])
PY_SOURCE = "\n".join([
    "# r2py:entity:e_assign", "y = 'a b'",
    "# r2py:entity:e_call", "print('c')",
    "# r2py:entity:e_c", "v = [1, 2]",
    "# r2py:entity:e_unresolved", "z = df.assign(b=1)",
]) + "\n"
ENTITIES = {
    "e_assign": _assign("y", "paste", "base", 0),
    "e_call": _call("paste", "base", 1),
    "e_c": _assign("v", "c", "base", 2),
    "e_unresolved": _assign("z", "mutate", None, 3),
}


class TestAssignmentPatterns(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.lib = PatternLibrary(root / "lib")
        self.r_path, self.py_path = root / "s.R", root / "s.py"
        self.r_path.write_text(R_SOURCE, encoding="utf-8")
        self.py_path.write_text(PY_SOURCE, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _seed(self, entities=ENTITIES):
        with patch("r2py.stage1.analyze", return_value=SimpleNamespace(entities=entities, source=R_SOURCE)):
            return r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib, script_id="s1")

    def test_an_assignment_teaches_the_function_on_its_right_hand_side(self):
        self._seed({"e_assign": ENTITIES["e_assign"]})
        pat = self.lib.store.get("base.paste")
        self.assertIsNotNone(pat)
        self.assertEqual(pat.translation_examples[0].r_snippet, 'y <- paste("a", "b")')
        self.assertEqual(pat.translation_examples[0].py_snippet, "y = 'a b'")
        self.assertIn("FunctionCall from base", pat.guidance)

    def test_a_bare_call_and_an_assignment_of_the_same_function_share_one_pattern(self):
        # One example per (package, function) per script, whichever statement form it takes.
        touched = self._seed()
        self.assertEqual(touched, ["base.paste"])
        self.assertEqual(len(self.lib.store.get("base.paste").translation_examples), 1)
        self.assertEqual(self.lib.store.list_ids(), ["base.paste"])

    def test_unresolved_and_ubiquitous_right_hand_calls_create_nothing(self):
        self._seed({k: ENTITIES[k] for k in ("e_c", "e_unresolved")})
        self.assertEqual(self.lib.store.list_ids(), [])

    def test_retrieval_finds_the_pattern_for_an_assignment(self):
        self._seed()
        self.assertEqual([p.id for p in self.lib.retrieve(_assign("q", "paste", "base"), k=2)], ["base.paste"])
        self.assertEqual(self.lib.retrieve(_assign("q", "paste0", "base"), k=2), [])

    def test_the_prompt_shows_the_pattern_for_an_assignment_entity(self):
        self._seed()
        script_map = SimpleNamespace(source="q <- paste('x')\n", entity_bundles={},
                                     entities={"e": _assign("q", "paste", "base")})
        text = "\n".join(_build_prompt(script_map, self.lib))
        self.assertIn("## Translation patterns", text)
        self.assertIn("base.paste", text)
        self.assertIn('y <- paste("a", "b")', text)


if __name__ == "__main__":
    unittest.main()
