"""Tests for Stage 2 — Translation (§5).

All tests are offline (no LLM calls) except TestTranslateSmokeAPI which is
gated on ANTHROPIC_API_KEY being set.
"""
from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from r2py.types import EntityKind, EffectClass, EditKind, Edit
from r2py.stage1.entities import Entity, EntityRef, SourceLocation
from r2py.stage1.script_map import ScriptMap


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_entity(
    eid: str,
    name: str = "x",
    kind: EntityKind = EntityKind.VARIABLE,
    deps: list[str] | None = None,
    flags: list[str] | None = None,
    package: str | None = None,
) -> Entity:
    return Entity(
        id=eid,
        kind=kind,
        name=name,
        source_span=SourceLocation(file="test.R", start_line=1, start_col=0,
                                   end_line=1, end_col=10),
        dependencies=[EntityRef(entity_id=d, kind=EntityKind.VARIABLE) for d in (deps or [])],
        r_semantic_flags=flags or [],
        package=package,
    )


def _make_script_map(entities: dict[str, Entity], source: str = "x <- 1") -> ScriptMap:
    return ScriptMap(source=source, entities=entities)


def _make_pattern(pid: str = "pkg.foo", pkg: str = "pkg", guidance: str = "Use bar() instead.") -> object:
    from r2py.library.pattern import Pattern, EvidenceEntry
    return Pattern(
        id=pid,
        package=pkg,
        confidence="confirmed",
        seed=False,
        guidance=guidance,
        evidence=[EvidenceEntry(script_id="s1", score=0.9,
                                verification_path="exact", variable="x")],
        contradictions=[],
        created="2026-01-01",
        last_review="2026-01-01",
    )


# ---------------------------------------------------------------------------
# T2: topological sort
# ---------------------------------------------------------------------------

class TestTopologicalOrder(unittest.TestCase):

    def test_no_entities(self):
        from r2py.stage2.walker import topological_order
        self.assertEqual(topological_order({}), [])

    def test_single_entity(self):
        from r2py.stage2.walker import topological_order
        entities = {"a": _make_entity("a")}
        self.assertEqual(topological_order(entities), ["a"])

    def test_linear_chain(self):
        from r2py.stage2.walker import topological_order
        a = _make_entity("a")
        b = _make_entity("b", deps=["a"])
        c = _make_entity("c", deps=["b"])
        entities = {"a": a, "b": b, "c": c}
        order = topological_order(entities)
        self.assertLess(order.index("a"), order.index("b"))
        self.assertLess(order.index("b"), order.index("c"))

    def test_diamond_dag(self):
        from r2py.stage2.walker import topological_order
        # a → b, c → d
        a = _make_entity("a")
        b = _make_entity("b", deps=["a"])
        c = _make_entity("c", deps=["a"])
        d = _make_entity("d", deps=["b", "c"])
        entities = {"a": a, "b": b, "c": c, "d": d}
        order = topological_order(entities)
        self.assertLess(order.index("a"), order.index("d"))
        self.assertLess(order.index("b"), order.index("d"))
        self.assertLess(order.index("c"), order.index("d"))

    def test_cycle_fallback_includes_all(self):
        from r2py.stage2.walker import topological_order
        # Mutual dependency: a → b → a
        a = _make_entity("a", deps=["b"])
        b = _make_entity("b", deps=["a"])
        entities = {"a": a, "b": b}
        order = topological_order(entities)
        self.assertEqual(sorted(order), ["a", "b"])

    def test_no_deps_come_first(self):
        from r2py.stage2.walker import topological_order
        a = _make_entity("a")
        b = _make_entity("b", deps=["a"])
        entities = {"b": b, "a": a}  # insertion order reversed
        order = topological_order(entities)
        self.assertLess(order.index("a"), order.index("b"))


# ---------------------------------------------------------------------------
# T3: prompt construction and response parsing
# ---------------------------------------------------------------------------

class TestBuildEntityPrompt(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.prompt import build_entity_prompt, SYSTEM_PROMPT
        self.build = build_entity_prompt
        self.system = SYSTEM_PROMPT

    def test_returns_list_with_user_role(self):
        entity = _make_entity("x1", name="my_var", flags=["na_semantics"])
        sm = _make_script_map({"x1": entity}, source="my_var <- NA")
        msgs = self.build(entity, sm, [], {})
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["role"], "user")

    def test_entity_name_in_prompt(self):
        entity = _make_entity("x1", name="my_var")
        sm = _make_script_map({"x1": entity})
        msgs = self.build(entity, sm, [], {})
        self.assertIn("my_var", msgs[0]["content"])

    def test_semantic_flags_in_prompt(self):
        entity = _make_entity("x1", name="v", flags=["nse", "vector_recycling"])
        sm = _make_script_map({"x1": entity})
        msgs = self.build(entity, sm, [], {})
        content = msgs[0]["content"]
        self.assertIn("nse", content)
        self.assertIn("vector_recycling", content)

    def test_pattern_guidance_in_prompt(self):
        entity = _make_entity("x1", name="v")
        sm = _make_script_map({"x1": entity})
        pat = _make_pattern(guidance="Use pd.DataFrame() here.")
        msgs = self.build(entity, sm, [pat], {})
        self.assertIn("pd.DataFrame()", msgs[0]["content"])

    def test_prior_translation_in_prompt(self):
        entity = _make_entity("x1", name="v", deps=["dep1"])
        sm = _make_script_map({"x1": entity})
        msgs = self.build(entity, sm, [], {"dep1": "dep1 = 42"})
        self.assertIn("dep1 = 42", msgs[0]["content"])

    def test_system_prompt_has_xml_tag_instruction(self):
        self.assertIn("<python>", self.system)
        self.assertIn("</python>", self.system)
        self.assertIn("<imports>", self.system)
        self.assertIn("<effects>", self.system)


class TestParseEntityResponse(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.prompt import parse_entity_response
        self.parse = parse_entity_response

    def test_parses_xml_tags(self):
        raw = "<python>\nx = 1\n</python>\n<imports>import os</imports>\n<effects>DATA</effects>"
        python, imports, effects = self.parse(raw)
        self.assertEqual(python, "x = 1")
        self.assertIn("import os", imports)
        self.assertIn("DATA", effects)

    def test_multiple_imports(self):
        raw = "<python>x=1</python><imports>import os, import sys</imports><effects></effects>"
        _py, imports, _eff = self.parse(raw)
        self.assertEqual(len(imports), 2)

    def test_fallback_on_no_python_tag(self):
        raw = "```python\nx = 42\n```"
        python, _imp, _eff = self.parse(raw)
        self.assertIn("x = 42", python)

    def test_empty_imports_and_effects(self):
        raw = "<python>pass</python><imports></imports><effects></effects>"
        _py, imports, effects = self.parse(raw)
        self.assertEqual(imports, [])
        self.assertEqual(effects, [])

    def test_fallback_treats_whole_response_as_python(self):
        raw = "x = 1\ny = 2\n"
        python, _imp, _eff = self.parse(raw)
        self.assertIn("x = 1", python)


# ---------------------------------------------------------------------------
# T6: stitch / compose
# ---------------------------------------------------------------------------

class TestCompose(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.stitch import compose
        self.compose = compose

    def _sm(self, n_entities: int = 2) -> ScriptMap:
        entities = {f"e{i}": _make_entity(f"e{i}", name=f"v{i}") for i in range(n_entities)}
        return _make_script_map(entities)

    def test_header_comment_present(self):
        sm = self._sm(1)
        result, _ = self.compose({"e0": "v0 = 1"}, {}, ["e0"], sm, "claude-sonnet-4-6", "test.R")
        self.assertIn("# Translated from", result)
        self.assertIn("r2py", result)

    def test_import_hoisted(self):
        sm = self._sm(1)
        result, _ = self.compose(
            {"e0": "import numpy as np\nv0 = np.array([1])"},
            {},
            ["e0"],
            sm,
            "model",
        )
        lines = result.splitlines()
        import_idx = next(i for i, l in enumerate(lines) if "import numpy" in l)
        code_idx = next(i for i, l in enumerate(lines) if "v0 = " in l)
        self.assertLess(import_idx, code_idx)

    def test_import_deduplication(self):
        sm = self._sm(2)
        per = {"e0": "import os\nv0 = 1", "e1": "import os\nv1 = 2"}
        result, _ = self.compose(per, {}, ["e0", "e1"], sm, "model")
        self.assertEqual(result.count("import os"), 1)

    def test_explicit_imports_included(self):
        sm = self._sm(1)
        result, _ = self.compose(
            {"e0": "v0 = 1"},
            {"e0": ["import pandas as pd"]},
            ["e0"],
            sm,
            "model",
        )
        self.assertIn("import pandas as pd", result)

    def test_name_collision_suffixed(self):
        sm = _make_script_map({
            "e0": _make_entity("e0", name="result"),
            "e1": _make_entity("e1", name="result2"),
        })
        per = {"e0": "result = 1", "e1": "result = 2"}
        result, _ = self.compose(per, {}, ["e0", "e1"], sm, "model")
        self.assertIn("result_1", result)

    def test_bare_import_before_from_import(self):
        sm = self._sm(1)
        result, _ = self.compose(
            {"e0": "from os import path\nimport sys\nv0 = 1"},
            {},
            ["e0"],
            sm,
            "model",
        )
        lines = [l for l in result.splitlines() if l.startswith("import") or l.startswith("from")]
        self.assertTrue(lines[0].startswith("import"), msg=f"Got: {lines}")


# ---------------------------------------------------------------------------
# T6b: sentinel comments and rebuild_entity_line_map
# ---------------------------------------------------------------------------

class TestSentinelAndRebuild(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.stitch import compose, rebuild_entity_line_map
        self.compose = compose
        self.rebuild = rebuild_entity_line_map

    def _sm(self, n: int = 2) -> ScriptMap:
        entities = {f"e{i}": _make_entity(f"e{i}", name=f"v{i}") for i in range(n)}
        return _make_script_map(entities)

    def _compose2(self):
        sm = self._sm(2)
        return self.compose({"e0": "v0 = 1", "e1": "v1 = 2"}, {}, ["e0", "e1"], sm, "m")

    def test_sentinel_comments_present(self):
        src, _ = self._compose2()
        self.assertIn("# r2py:entity:e0", src)
        self.assertIn("# r2py:entity:e1", src)

    def test_rebuild_entity_line_map_roundtrip(self):
        src, original_map = self._compose2()
        rebuilt = self.rebuild(src)
        self.assertEqual(set(rebuilt.keys()), set(original_map.keys()))
        for eid in original_map:
            self.assertEqual(rebuilt[eid], original_map[eid],
                             msg=f"Range mismatch for {eid}: {rebuilt[eid]} vs {original_map[eid]}")

    def test_rebuild_after_insert_preamble(self):
        from r2py.types import Edit, EditKind
        from r2py.stage3.edit_types import apply_edit
        src, original_map = self._compose2()
        e = Edit(kind=EditKind.INSERT_PREAMBLE, entity_ids=[], params={"code": "import os"})
        src2 = apply_edit(src, e)
        rebuilt = self.rebuild(src2)
        # Both entities must still be found after the edit.
        self.assertEqual(set(rebuilt.keys()), {"e0", "e1"})
        # INSERT_PREAMBLE inserts inside e0's body, shifting e1's sentinel.
        self.assertGreater(rebuilt["e1"][0], original_map["e1"][0],
                           "e1's sentinel should shift down after INSERT_PREAMBLE adds a line to e0")
        # e0's sentinel line itself is unchanged (the insert goes inside e0's body, after the sentinel).
        self.assertEqual(rebuilt["e0"][0], original_map["e0"][0])

    def test_rebuild_returns_empty_without_sentinels(self):
        result = self.rebuild("x = 1\ny = 2\n")
        self.assertEqual(result, {})

    def test_sentinel_is_first_line_of_entity_range(self):
        src, lmap = self._compose2()
        lines = src.splitlines()
        for eid, (start, _end) in lmap.items():
            self.assertIn(eid, lines[start - 1],
                          msg=f"Expected sentinel for {eid} at line {start}")


# ---------------------------------------------------------------------------
# T7: coherence review
# ---------------------------------------------------------------------------

class TestCoherenceReview(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.coherence import review, _parse_response
        self.review = review
        self.parse = _parse_response

    def _sm(self) -> ScriptMap:
        return _make_script_map({"e0": _make_entity("e0", name="x")})

    def test_parse_insert_preamble_edit_applied(self):
        # Applier should prepend the code; <python> block is ignored
        raw = (
            '{"kind": "InsertPreamble", "entity_ids": [], "params": {"code": "import os"}}\n'
            "<python>\nimport os\nx = 1\n</python>"
        )
        revised, edits = self.parse(raw, "x = 1\n")
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0].kind, EditKind.INSERT_PREAMBLE)
        # Programmatic applier prepends "import os" before "x = 1"
        self.assertIn("import os", revised)
        self.assertLess(revised.index("import os"), revised.index("x = 1"))

    def test_parse_rename_variable_edit_applied(self):
        raw = (
            '{"kind": "RenameVariable", "entity_ids": ["e0"], "params": {"old": "foo", "new": "bar"}}\n'
            "<python>\nbar = 1\n</python>"
        )
        revised, edits = self.parse(raw, "foo = 1\n")
        self.assertEqual(edits[0].kind, EditKind.RENAME_VARIABLE)
        self.assertEqual(edits[0].params["old"], "foo")
        # Programmatic rename: foo → bar
        self.assertIn("bar = 1", revised)
        self.assertNotIn("foo", revised)

    def test_parse_change_import_applied(self):
        raw = (
            '{"kind": "ChangeImport", "entity_ids": [], '
            '"params": {"old_import": "import pandas", "new_import": "import pandas as pd"}}\n'
            "<python>\nimport pandas as pd\nx = 1\n</python>"
        )
        revised, edits = self.parse(raw, "import pandas\nx = 1\n")
        self.assertEqual(edits[0].kind, EditKind.CHANGE_IMPORT)
        self.assertIn("import pandas as pd", revised)
        self.assertNotIn("import pandas\n", revised)

    def test_parse_wrap_value_applied(self):
        raw = (
            '{"kind": "WrapValue", "entity_ids": ["e0"], '
            '"params": {"name": "result", "wrapper": "str"}}\n'
            "<python>\nresult = 42\n</python>"
        )
        revised, edits = self.parse(raw, "result = 42\n")
        self.assertEqual(edits[0].kind, EditKind.WRAP_VALUE)
        self.assertIn("str(result)", revised)

    def test_parse_no_edits_returns_original_unchanged(self):
        # No edit lines + <python> block → original returned (applier has nothing to do)
        raw = "<python>\nx = 1\n</python>"
        revised, edits = self.parse(raw, "x = 1\n")
        self.assertEqual(edits, [])
        self.assertEqual(revised, "x = 1\n")

    def test_parse_failure_returns_original(self):
        bad_raw = "not valid json or python"
        revised, edits = self.parse(bad_raw, "original = 42")
        # No JSON edit lines, no <python> tag → no edits, original unchanged
        self.assertEqual(revised, "original = 42")
        self.assertEqual(edits, [])

    def test_review_llm_error_returns_original(self):
        sm = self._sm()
        lib = MagicMock()
        with patch("r2py.stage2.coherence._llm.call", side_effect=RuntimeError("API down")):
            revised, edits = self.review("x = 1\n", sm, lib)
        self.assertEqual(revised, "x = 1\n")
        self.assertEqual(edits, [])

    def test_review_empty_source_returns_unchanged(self):
        sm = self._sm()
        lib = MagicMock()
        revised, edits = self.review("", sm, lib)
        self.assertEqual(revised, "")
        self.assertEqual(edits, [])

    def test_parse_unknown_kind_ignored(self):
        raw = (
            '{"kind": "UnknownEditKind", "entity_ids": [], "params": {}}\n'
            "<python>\nx = 1\n</python>"
        )
        _revised, edits = self.parse(raw, "x = 1")
        self.assertEqual(edits, [])


# ---------------------------------------------------------------------------
# Package translator
# ---------------------------------------------------------------------------

class TestPackageTranslator(unittest.TestCase):

    def setUp(self):
        # Reset module-level recursion guard between tests
        import r2py.stage2.package_translator as _pt
        _pt._in_progress.clear()

    def _make_ext_entity(self, pkg: str = "mypkg") -> object:
        return _make_entity("ext1", name="myfunc", kind=EntityKind.EXTERNAL_SYMBOL, package=pkg)

    def test_no_package_returns_none(self):
        from r2py.stage2.package_translator import translate_external_symbol
        entity = _make_entity("ext1", name="myfunc", kind=EntityKind.EXTERNAL_SYMBOL, package=None)
        sm = _make_script_map({})
        lib = MagicMock()
        result = translate_external_symbol(entity, sm, lib)
        self.assertIsNone(result)

    def test_no_source_loc_returns_none(self):
        from r2py.stage2.package_translator import translate_external_symbol
        entity = self._make_ext_entity("mypkg")
        sm = _make_script_map({})  # external_sources is empty
        lib = MagicMock()
        result = translate_external_symbol(entity, sm, lib)
        self.assertIsNone(result)

    def test_recursion_guard_returns_none(self):
        from r2py.stage2.package_translator import translate_external_symbol, _in_progress
        entity = self._make_ext_entity("mypkg")
        sm = _make_script_map({})
        lib = MagicMock()
        _in_progress.add("mypkg")
        result = translate_external_symbol(entity, sm, lib)
        self.assertIsNone(result)

    def test_cache_hit_returns_cached_content(self):
        from r2py.stage2.package_translator import translate_external_symbol
        from r2py.stage1.entities import SourceLocation
        import tempfile, os

        entity = self._make_ext_entity("mypkg")
        sm = _make_script_map({})

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir)
            # Write a fake cache file
            cache_path = cache_dir / "mypkg__myfunc.py"
            cache_path.write_text("myfunc_cached = True\n", encoding="utf-8")

            # Give it a source_loc so we pass the None check, but cache should short-circuit
            src_loc = SourceLocation(file="fake.R", start_line=1, start_col=0,
                                     end_line=2, end_col=0)
            sm = ScriptMap(source="", entities={},
                           external_sources={"ext1": src_loc})

            lib = MagicMock()
            result = translate_external_symbol(entity, sm, lib, cache_dir=cache_dir)

        self.assertEqual(result, "myfunc_cached = True\n")


# ---------------------------------------------------------------------------
# Retrieval wrapper
# ---------------------------------------------------------------------------

class TestRetrievePatterns(unittest.TestCase):

    def test_delegates_to_library(self):
        from r2py.stage2.retrieval import retrieve_patterns
        entity = _make_entity("x1")
        pat = _make_pattern()
        lib = MagicMock()
        lib.retrieve.return_value = [pat]
        result = retrieve_patterns(entity, lib, no_seeds=False)
        lib.retrieve.assert_called_once_with(entity, k=3, no_seeds=False)
        self.assertEqual(result, [pat])

    def test_no_seeds_propagated(self):
        from r2py.stage2.retrieval import retrieve_patterns
        entity = _make_entity("x1")
        lib = MagicMock()
        lib.retrieve.return_value = []
        retrieve_patterns(entity, lib, no_seeds=True)
        lib.retrieve.assert_called_once_with(entity, k=3, no_seeds=True)


# ---------------------------------------------------------------------------
# T8: orchestration (mock LLM)
# ---------------------------------------------------------------------------

class TestTranslateOrchestration(unittest.TestCase):

    def _mock_llm_response(self, entity_name: str = "x") -> str:
        return f"<python>\n{entity_name} = 1\n</python>\n<imports></imports>\n<effects>DATA</effects>"

    def test_returns_string(self):
        from r2py.stage2.translator import translate
        entities = {"e0": _make_entity("e0", name="x")}
        sm = _make_script_map(entities, source="x <- 1")
        lib = MagicMock()
        lib.retrieve.return_value = []
        with patch("r2py.stage2.translator._llm.call", return_value=self._mock_llm_response("x")):
            result, _ = translate(sm, lib, run_coherence=False)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_all_entities_visited(self):
        from r2py.stage2.translator import translate
        entities = {
            "a": _make_entity("a", name="a"),
            "b": _make_entity("b", name="b", deps=["a"]),
        }
        sm = _make_script_map(entities, source="a <- 1\nb <- a + 1")
        lib = MagicMock()
        lib.retrieve.return_value = []
        called_with: list[str] = []

        def fake_llm(messages, system, **kwargs):
            content = messages[0]["content"]
            called_with.append(content)
            return "<python>\npass\n</python><imports></imports><effects></effects>"

        with patch("r2py.stage2.translator._llm.call", side_effect=fake_llm):
            translate(sm, lib, run_coherence=False)

        self.assertEqual(len(called_with), 2)

    def test_llm_failure_per_entity_is_stubbed(self):
        from r2py.stage2.translator import translate
        entities = {"e0": _make_entity("e0", name="x")}
        sm = _make_script_map(entities, source="x <- 1")
        lib = MagicMock()
        lib.retrieve.return_value = []
        with patch("r2py.stage2.translator._llm.call", side_effect=RuntimeError("down")):
            result, _ = translate(sm, lib, run_coherence=False)
        # Should contain a stub comment, not raise
        self.assertIn("translation failed", result)

    def test_coherence_called_once(self):
        from r2py.stage2.translator import translate
        entities = {"e0": _make_entity("e0", name="x")}
        sm = _make_script_map(entities, source="x <- 1")
        lib = MagicMock()
        lib.retrieve.return_value = []

        with patch("r2py.stage2.translator._llm.call",
                   return_value=self._mock_llm_response()):
            with patch("r2py.stage2.translator._coherence.review",
                       return_value=("x = 1\n", [])) as mock_coh:
                translate(sm, lib, run_coherence=True)
        mock_coh.assert_called_once()

    def test_coherence_skipped_when_disabled(self):
        from r2py.stage2.translator import translate
        entities = {"e0": _make_entity("e0", name="x")}
        sm = _make_script_map(entities, source="x <- 1")
        lib = MagicMock()
        lib.retrieve.return_value = []

        with patch("r2py.stage2.translator._llm.call",
                   return_value=self._mock_llm_response()):
            with patch("r2py.stage2.translator._coherence.review",
                       return_value=("x = 1\n", [])) as mock_coh:
                translate(sm, lib, run_coherence=False)
        mock_coh.assert_not_called()

    def test_empty_script_map(self):
        from r2py.stage2.translator import translate
        sm = _make_script_map({}, source="")
        lib = MagicMock()
        lib.retrieve.return_value = []
        result, _ = translate(sm, lib, run_coherence=False)
        self.assertIsInstance(result, str)


# ---------------------------------------------------------------------------
# T1: LLM client (import-only — no API key needed for basic checks)
# ---------------------------------------------------------------------------

class TestLLMModule(unittest.TestCase):

    def test_importable(self):
        from r2py.stage2 import llm
        self.assertTrue(hasattr(llm, "call"))
        self.assertTrue(hasattr(llm, "_DEFAULT_MODEL"))

    def test_missing_api_key_raises(self):
        from r2py.stage2.llm import call
        with patch.dict(os.environ, {}, clear=True):
            # Remove ANTHROPIC_API_KEY if present
            env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            with patch.dict(os.environ, env, clear=True):
                with self.assertRaises(RuntimeError):
                    call([{"role": "user", "content": "hi"}], "sys")


# ---------------------------------------------------------------------------
# Live API smoke test (requires ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

@unittest.skipUnless(os.environ.get("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not set")
class TestTranslateSmokeAPI(unittest.TestCase):

    def test_translate_simple_r_returns_python(self):
        from r2py.stage2.translator import translate
        from r2py.library import get_library

        entities = {"x1": _make_entity("x1", name="x")}
        sm = _make_script_map(entities, source="x <- 42")
        lib = get_library()

        result = translate(sm, lib, run_coherence=False)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 0)
        # Should contain some Python (header + something)
        self.assertIn("r2py", result)


if __name__ == "__main__":
    unittest.main()
