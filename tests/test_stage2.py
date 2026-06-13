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

    def test_already_defined_names_in_prompt(self):
        entity = _make_entity("x1", name="v")
        sm = _make_script_map({"x1": entity})
        msgs = self.build(entity, sm, [], {}, already_defined={"_helper", "_MAP"})
        content = msgs[0]["content"]
        self.assertIn("_helper", content)
        self.assertIn("_MAP", content)
        self.assertIn("Already defined", content)

    def test_no_already_defined_section_when_empty(self):
        entity = _make_entity("x1", name="v")
        sm = _make_script_map({"x1": entity})
        msgs = self.build(entity, sm, [], {}, already_defined=set())
        self.assertNotIn("Already defined", msgs[0]["content"])


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

    def test_duplicate_def_removed_from_later_entity(self):
        """A top-level def present in entity e0 must not be re-emitted by e1."""
        sm = self._sm(2)
        helper = "def _helper(x):\n    return x + 1\n"
        per = {
            "e0": helper + "v0 = _helper(1)",
            "e1": helper + "v1 = _helper(2)",  # same helper — should be stripped
        }
        result, _ = self.compose(per, {}, ["e0", "e1"], sm, "model")
        self.assertEqual(result.count("def _helper"), 1, "Helper def must appear exactly once")
        self.assertIn("v0 = _helper(1)", result)
        self.assertIn("v1 = _helper(2)", result)

    def test_duplicate_underscore_constant_removed_from_later_entity(self):
        """A _-prefixed constant emitted by e0 must not be re-emitted by e1."""
        sm = self._sm(2)
        const = "_MAP = {'a': 1}\n"
        per = {
            "e0": const + "v0 = _MAP['a']",
            "e1": const + "v1 = _MAP['a']",  # same constant — should be stripped
        }
        result, _ = self.compose(per, {}, ["e0", "e1"], sm, "model")
        self.assertEqual(result.count("_MAP = "), 1, "_MAP must appear exactly once")

    def test_non_underscore_assignment_still_renamed(self):
        """Regular (non-_) variable assignments from different entities are still renamed."""
        sm = _make_script_map({
            "e0": _make_entity("e0", name="result"),
            "e1": _make_entity("e1", name="result2"),
        })
        per = {"e0": "result = 1", "e1": "result = 2"}
        result, _ = self.compose(per, {}, ["e0", "e1"], sm, "model")
        self.assertIn("result_1", result)


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

    def test_build_user_message_surfaces_shim_names(self):
        """Shim-bound names must appear in the coherence user message so the
        LLM knows to skip InsertPreamble/ReplaceCall edits that re-bind them."""
        from r2py.stage2.coherence import _build_user_message
        sm = self._sm()
        msg = _build_user_message("x = 1\n", sm, shim_names=["volcano", "iris"])
        self.assertIn("## Shim-loaded names", msg)
        self.assertIn("`iris`", msg)
        self.assertIn("`volcano`", msg)

    def test_build_user_message_omits_shim_section_when_empty(self):
        from r2py.stage2.coherence import _build_user_message
        sm = self._sm()
        msg = _build_user_message("x = 1\n", sm, shim_names=None)
        self.assertNotIn("## Shim-loaded names", msg)
        msg2 = _build_user_message("x = 1\n", sm, shim_names=[])
        self.assertNotIn("## Shim-loaded names", msg2)

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
# Data-loading shim (Option A — plans/i-go-with-option-melodic-dewdrop.md)
# ---------------------------------------------------------------------------


class TestDataLoadingShim(unittest.TestCase):
    """Phase 3 + 4: shim emission, saved-form is no-op, activated form executes."""

    def test_classifier_detects_rng_and_read_sources(self):
        from r2py.stage2.stitch import is_non_translatable_source_entity as cls
        self.assertTrue(cls("x <- rnorm(10)"))
        self.assertTrue(cls("df <- read.csv('a.csv')"))
        self.assertTrue(cls("env <- Sys.getenv('HOME')"))
        self.assertFalse(cls("y <- mean(x)"))
        self.assertFalse(cls("x <- c(1, 2, 3)"))
        self.assertFalse(cls(""))

    def test_classifier_ignores_call_names_in_r_comments(self):
        """Regression: an R comment that mentions an allowlist call name must
        not flip the classifier — only the actual RHS call matters."""
        from r2py.stage2.stitch import is_non_translatable_source_entity as cls
        self.assertFalse(cls("# uses rnorm() internally\nx <- some_other(1)"))
        self.assertFalse(cls("y <- mean(x)  # not read.csv()"))
        # Sanity: comment plus real RNG call still classifies as RNG.
        self.assertTrue(cls("# generate samples\nx <- rnorm(10)"))

    def test_build_shim_returns_empty_when_no_names(self):
        from r2py.stage2.stitch import build_data_shim
        self.assertEqual(build_data_shim([], "foo.json"), "")
        self.assertEqual(build_data_shim(["x"], ""), "")

    def test_shim_defines_file_fallback_when_relpath_given(self):
        """The shim must define ``__file__`` as a fallback when given a
        script_relpath, so users can paste-execute the .py in a REPL where
        Python doesn't bind __file__ automatically."""
        from r2py.stage2.stitch import build_data_shim
        shim = build_data_shim(
            ["volcano"],
            "foo.r2py_data.json",
            script_relpath=r"work\outputs\foo.py",
        )
        # Forward-slash normalized (avoids \n / \t escape pitfalls).
        self.assertIn("'work/outputs/foo.py'", shim)
        # Guarded so a normal `python foo.py` invocation still gets the
        # real __file__ (which uses an absolute path).
        self.assertIn("if '__file__' not in globals():", shim)

    def test_shim_omits_file_fallback_when_relpath_absent(self):
        from r2py.stage2.stitch import build_data_shim
        shim = build_data_shim(["volcano"], "foo.r2py_data.json")
        self.assertNotIn("__file__ =", shim)

    def test_shim_file_fallback_works_in_interactive_subprocess(self):
        """End-to-end: activate the shim, drop the sidecar file in the cwd,
        and run a Python -c snippet that simulates a REPL (no __file__).
        The shim must define __file__ and load the data."""
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        from r2py.stage2.stitch import build_data_shim
        from r2py.stage4.verifier import _activate_data_shim

        with tempfile.TemporaryDirectory() as wd:
            wd = Path(wd)
            (wd / "data.r2py_data.json").write_text(
                json.dumps({"v": [1, 2, 3]}), encoding="utf-8"
            )
            shim = build_data_shim(
                ["v"], "data.r2py_data.json",
                script_relpath="ignored.py",   # next to sidecar
            )
            activated, _ = _activate_data_shim(shim)
            # Simulate a REPL: ``python -c`` does not bind __file__.
            program = activated + "\nimport json as _j; print(_j.dumps(v))\n"
            r = subprocess.run(
                [sys.executable, "-c", program],
                cwd=str(wd),
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(r.returncode, 0, f"stderr: {r.stderr}")
            self.assertEqual(json.loads(r.stdout.strip()), [1, 2, 3])

    def test_shim_saved_form_is_fully_commented(self):
        from r2py.stage2.stitch import build_data_shim, DATA_SHIM_BEGIN, DATA_SHIM_END
        shim = build_data_shim(["iris"], "test.r2py_data.json")
        self.assertIn(DATA_SHIM_BEGIN, shim)
        self.assertIn(DATA_SHIM_END, shim)
        for line in shim.splitlines():
            if line in (DATA_SHIM_BEGIN, DATA_SHIM_END):
                continue
            self.assertTrue(line.startswith("# "), f"uncommented body line: {line!r}")

    def test_shim_activation_round_trip_produces_valid_python(self):
        import ast
        from r2py.stage2.stitch import build_data_shim
        from r2py.stage4.verifier import _activate_data_shim

        shim = build_data_shim(["iris", "mtcars"], "x.r2py_data.json")
        src = "import json\n\n" + shim + "\n\nresult = iris\n"
        activated, has_shim = _activate_data_shim(src)
        self.assertTrue(has_shim)
        # Activated form must be valid Python
        ast.parse(activated)
        # Saved form must also be valid Python (it's a no-op)
        ast.parse(src)
        # And source without a shim block returns has_shim=False unchanged
        plain = "x = 1\nprint(x)\n"
        unchanged, has_shim2 = _activate_data_shim(plain)
        self.assertEqual(unchanged, plain)
        self.assertFalse(has_shim2)

    def test_shim_loads_data_into_globals_in_subprocess(self):
        """The activated shim, given a sidecar JSON, binds names into globals."""
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        from r2py.stage2.stitch import build_data_shim
        from r2py.stage4.verifier import _activate_data_shim

        shim = build_data_shim(["iris"], "data.r2py_data.json")
        src = (
            shim
            + "\nimport json as _j\nprint(_j.dumps({'iris_loaded': iris}))\n"
        )
        activated, _ = _activate_data_shim(src)
        with tempfile.TemporaryDirectory() as wd:
            wd = Path(wd)
            (wd / "data.r2py_data.json").write_text(
                json.dumps({"iris": [[1, 2], [3, 4]]}),
                encoding="utf-8",
            )
            (wd / "script.py").write_text(activated, encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(wd / "script.py")],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(r.returncode, 0, f"stderr: {r.stderr}")
            out = json.loads(r.stdout.strip())
            self.assertEqual(out, {"iris_loaded": [[1, 2], [3, 4]]})

    def test_compose_skips_shim_when_no_free_vars_or_sources(self):
        """No free-var ∩ captured-data intersection + no RNG/read entities → no shim."""
        from r2py.stage2.stitch import compose, DATA_SHIM_BEGIN
        entities = {"x1": _make_entity("x1", name="x")}
        sm = _make_script_map(entities, source="x <- 1")
        source, _ = compose(
            per_entity={"x1": "x = 1"},
            per_entity_imports={"x1": []},
            order=["x1"],
            script_map=sm,
            model="test",
            sidecar_filename="t.r2py_data.json",
        )
        self.assertNotIn(DATA_SHIM_BEGIN, source)

    def test_collect_shim_needed_names_handles_rng_entity_at_row_zero(self):
        """Regression: collect_shim_needed_names must use 0-based SourceLocation
        rows (matching prompt._entity_source). The previous 1-based slice
        returned [] for any entity whose start_line==0, silently dropping
        RNG/read-source entities at the top of the R script."""
        from r2py.stage0.effects.bundle import EffectBundle
        from r2py.stage2.stitch import collect_shim_needed_names

        ent = _make_entity("e1", name="x")
        ent.source_span = SourceLocation(
            file="t.R", start_line=0, start_col=0, end_line=0, end_col=15,
        )
        ent.actual_bundle = EffectBundle(data={"x": [0.1, 0.2, 0.3]})

        sm = _make_script_map({"e1": ent}, source="x <- rnorm(3)")
        needed = collect_shim_needed_names(sm)
        self.assertIn("x", needed,
                      "RNG entity at row 0 must be classified as non-translatable source")

    def test_collect_shim_needed_names_handles_multiline_entity(self):
        """A multi-line entity (start_line=2, end_line=5) must slice exactly
        rows 2..5 inclusive, not 1..4."""
        from r2py.stage0.effects.bundle import EffectBundle
        from r2py.stage2.stitch import collect_shim_needed_names

        ent = _make_entity("e1", name="df")
        ent.source_span = SourceLocation(
            file="t.R", start_line=2, start_col=0, end_line=2, end_col=30,
        )
        ent.actual_bundle = EffectBundle(data={"df": {"col": [1, 2]}})
        r_src = "# line 0\n# line 1\ndf <- read.csv('x.csv')\n"
        sm = _make_script_map({"e1": ent}, source=r_src)
        needed = collect_shim_needed_names(sm)
        self.assertIn("df", needed)

    def test_remove_shim_overrides_strips_volcano_stub(self):
        """Regression for shape__rd_example__greycol_Rd.py: an LLM-emitted
        ``volcano = np.array([...])`` stub appearing after the shim must be
        stripped at compose time so the shim's authoritative R value survives
        into the body."""
        from r2py.stage2.stitch import remove_shim_overrides

        body = (
            "volcano = np.array([[94, 94, 94],\n"
            "                    [97, 97, 97]], dtype=int)\n"
            "# filled.contour creates a filled contour plot\n"
            "plt.contourf(volcano)\n"
        )
        cleaned = remove_shim_overrides(body, {"volcano"})
        self.assertNotIn("np.array", cleaned)
        self.assertIn("plt.contourf(volcano)", cleaned)
        # Comments and downstream code preserved
        self.assertIn("# filled.contour creates", cleaned)

    def test_remove_shim_overrides_preserves_unrelated_assignments(self):
        from r2py.stage2.stitch import remove_shim_overrides
        body = "x = 1\ny = 2\nresult = x + y\n"
        # Empty shim set → no-op
        self.assertEqual(remove_shim_overrides(body, set()), body)
        # Only matching target removed
        cleaned = remove_shim_overrides(body, {"x"})
        self.assertNotIn("x = 1", cleaned)
        self.assertIn("y = 2", cleaned)
        self.assertIn("result = x + y", cleaned)

    def test_translator_post_strip_removes_coherence_injected_literal(self):
        """Regression for shape__rd_example__greycol_Rd.py round 2: the
        coherence pass injects ``volcano = [[...full matrix...]]`` via an
        InsertPreamble edit after compose, undoing compose's strip.  The
        post-coherence strip in translator.translate must remove it again
        so the shim's value survives."""
        from r2py.stage0.effects.bundle import EffectBundle
        from r2py.stage2 import stitch as _stitch
        from r2py.stage2.translator import _strip_shim_overrides_global

        # Simulate the post-compose / post-coherence state: shim block followed
        # by a body that re-defines volcano (as coherence does).
        source = (
            "import numpy as np\n"
            "\n"
            "# r2py:data_shim:begin\n"
            "# import json as _r2py_shim_json\n"
            "# r2py:data_shim:end\n"
            "\n"
            "# r2py:entity:filled.contour\n"
            "volcano = [[100, 100], [101, 101]]\n"
            "import matplotlib.pyplot as plt\n"
            "plt.contourf(volcano)\n"
        )
        cleaned = _strip_shim_overrides_global(source, {"volcano"}, _stitch)
        self.assertNotIn("volcano = [[", cleaned)
        # Other code in the entity body and the shim block both preserved.
        self.assertIn("plt.contourf(volcano)", cleaned)
        self.assertIn("# r2py:data_shim:begin", cleaned)
        self.assertIn("# r2py:entity:filled.contour", cleaned)

    def test_post_strip_leaves_non_shim_assignments_alone(self):
        """The post-strip must not touch assignments to names the shim
        does not bind."""
        from r2py.stage2 import stitch as _stitch
        from r2py.stage2.translator import _strip_shim_overrides_global

        source = (
            "# r2py:entity:e1\n"
            "x = 42\n"
            "y = x + 1\n"
        )
        cleaned = _strip_shim_overrides_global(source, {"volcano"}, _stitch)
        self.assertEqual(cleaned, source)

    def test_compose_strips_volcano_stub_when_shim_loads_it(self):
        """End-to-end through compose(): a body containing a volcano stub
        appearing AFTER the shim block must have the stub removed so the shim's
        binding survives into the body block."""
        from r2py.stage0.effects.bundle import EffectBundle
        from r2py.stage2.stitch import compose, DATA_SHIM_BEGIN

        ent = _make_entity("e1", name="plot")
        ent.free_variable_refs = ["volcano"]
        ent.actual_bundle = EffectBundle(data={"volcano": [[100, 101], [102, 103]]})

        sm = _make_script_map({"e1": ent}, source="filled.contour(volcano)")
        snippet = (
            "volcano = np.array([[94, 94],\n"
            "                    [97, 97]], dtype=int)\n"
            "plt.contourf(volcano)\n"
        )
        source, _ = compose(
            per_entity={"e1": snippet},
            per_entity_imports={"e1": []},
            order=["e1"],
            script_map=sm,
            model="test",
            sidecar_filename="t.r2py_data.json",
        )
        self.assertIn(DATA_SHIM_BEGIN, source)
        # The hallucinated stub is gone; the actual call survives.
        self.assertNotIn("np.array", source)
        self.assertIn("plt.contourf(volcano)", source)

    def test_compose_emits_shim_for_free_variable_with_captured_data(self):
        from r2py.stage0.effects.bundle import EffectBundle
        from r2py.stage2.stitch import compose, DATA_SHIM_BEGIN, DATA_SHIM_END

        ent = _make_entity("e1", name="result")
        ent.free_variable_refs = ["iris"]
        bundle = EffectBundle(data={"iris": [[1, 2], [3, 4]]})
        ent.actual_bundle = bundle

        sm = _make_script_map({"e1": ent}, source="result <- head(iris)")
        source, _ = compose(
            per_entity={"e1": "result = iris[:5]"},
            per_entity_imports={"e1": []},
            order=["e1"],
            script_map=sm,
            model="test",
            sidecar_filename="t.r2py_data.json",
        )
        self.assertIn(DATA_SHIM_BEGIN, source)
        self.assertIn(DATA_SHIM_END, source)
        # The shim must reference the iris name we provided
        self.assertIn("'iris'", source)


# ---------------------------------------------------------------------------
# Pipeline-level shim tests (Stage 1 → Stage 2 stitch → Stage 4 activation)
# LLM-free: we hand-assemble per-entity snippets and call stitch.compose
# directly, then exercise the verifier's shim activation in-subprocess.
# ---------------------------------------------------------------------------


class TestShimPipelineIris(unittest.TestCase):
    """End-to-end: R script using `iris` → Stage 1 capture → stitch with shim
    → verifier activation → subprocess subprocess binds iris from sidecar JSON."""

    def test_iris_inherited_var_flows_through_shim(self):
        import shutil
        from pathlib import Path as _P
        if not shutil.which("Rscript") and not (_P(__file__).resolve().parent.parent
                                                / "r2py" / "stage0" / "r_env" / "runtime"
                                                / "bin" / "Rscript.exe").exists():
            self.skipTest("R not available")

        import json
        import subprocess
        import sys
        import tempfile
        from r2py import stage1
        from r2py.stage2.stitch import compose, DATA_SHIM_BEGIN
        from r2py.stage4.verifier import _activate_data_shim, _build_sidecar_payload

        # ── Stage 1: run on a script that touches a built-in dataset ──
        r_src = "n <- nrow(iris)\nm <- mean(iris$Sepal.Length)\n"
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False,
                                         encoding="utf-8") as _rf:
            _rf.write(r_src)
            _r_path = _P(_rf.name)
        try:
            sm = stage1.analyze(_r_path)
        finally:
            _r_path.unlink(missing_ok=True)

        # Pull main bundle via the verifier helper.
        from r2py.stage4.verifier import get_r_bundle
        bundle = get_r_bundle(sm)
        self.assertIn("iris", bundle.data,
                      "Stage 1's inherited-var probe should capture iris")

        # ── Stage 2 (LLM-free): hand-assembled per-entity snippets ──
        # Build a minimal per_entity map covering the entity ids Stage 1 produced.
        eids = list(sm.entities.keys())
        per_entity = {eid: "" for eid in eids}
        # Put a single use-iris snippet in the first entity so its free_variable_refs
        # populate the shim.  The other entities stay no-ops.
        per_entity[eids[0]] = (
            "import json as _j\n"
            "print(_j.dumps({'n_cols': len(iris), "
            "'n_rows': len(next(iter(iris.values()))), "
            "'has_sepal_length': 'Sepal.Length' in iris}))"
        )
        per_entity_imports = {eid: [] for eid in eids}

        source, _ = compose(
            per_entity, per_entity_imports, eids, sm,
            model="test", sidecar_filename="iris_test.r2py_data.json",
        )
        self.assertIn(DATA_SHIM_BEGIN, source,
                      "shim should be emitted when iris is a free-variable ref")

        # ── Stage 4 activation: un-comment shim, write sidecar, run ──
        activated, has_shim = _activate_data_shim(source)
        self.assertTrue(has_shim)
        payload = _build_sidecar_payload(sm)

        with tempfile.TemporaryDirectory() as wd:
            wd = _P(wd)
            (wd / "iris_test.r2py_data.json").write_text(payload, encoding="utf-8")
            (wd / "script.py").write_text(activated, encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(wd / "script.py")],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(r.returncode, 0, f"stderr: {r.stderr}")
            # iris in R is a 150-row data.frame; serialized via the column-dict
            # adapter, it becomes a dict whose values are 150-element lists.
            out = json.loads(r.stdout.strip().splitlines()[-1])
            self.assertEqual(out.get("n_rows"), 150)
            self.assertEqual(out.get("n_cols"), 5)
            self.assertTrue(out.get("has_sepal_length"))


class TestShimPipelineWithLocaleNestedDate(unittest.TestCase):
    """Regression for the v0.1 JSON-opacity trap: a DataFrame column of
    datetime.date objects must serialize correctly through the full pipeline
    (Phase 1c parity verified end-to-end via the shim)."""

    def test_with_locale_dataframe_date_column_round_trip(self):
        import shutil
        from pathlib import Path as _P
        repo = _P(__file__).resolve().parent.parent
        if not shutil.which("Rscript") and not (
            repo / "r2py" / "stage0" / "r_env" / "runtime" / "bin" / "Rscript.exe"
        ).exists():
            self.skipTest("R not available")

        fixture = repo / "work" / "inputs" / "harvested" / "withr__rd_example__with_locale_Rd.R"
        if not fixture.exists():
            self.skipTest("withr fixture not present")

        import json
        import subprocess
        import sys
        import tempfile
        from r2py import stage1
        from r2py.stage4.verifier import _build_sidecar_payload

        # Stage 1: run the fixture; df with a Date column should be captured.
        sm = stage1.analyze(fixture)

        from r2py.stage4.verifier import get_r_bundle
        bundle = get_r_bundle(sm)
        # Stage 1's R sandbox may fail to run the full with_locale calls
        # (en_GB / es_ES locales may be unavailable on the test host), but
        # the data.frame assignment must always succeed.
        self.assertIn("df", bundle.data, f"df not captured; keys={list(bundle.data)}")
        df = bundle.data["df"]
        self.assertIsInstance(df, dict)
        self.assertIn("date", df)
        # The nested-date case: column values must be ISO date strings, NOT
        # opaque jsonlite-flattened ints or empty lists.
        self.assertEqual(df["date"], ["2019-01-01", "2019-02-01"])
        self.assertEqual(df["value"], [1, 2])

        # Round-trip through the sidecar / shim and confirm Python sees the
        # same structure (no information lost across the JSON boundary).
        payload = _build_sidecar_payload(sm)
        loaded = json.loads(payload)
        self.assertEqual(loaded["df"]["date"], ["2019-01-01", "2019-02-01"])

        # And the activated shim binds df with the same shape.
        from r2py.stage2.stitch import build_data_shim
        from r2py.stage4.verifier import _activate_data_shim
        shim = build_data_shim(["df"], "with_locale.r2py_data.json")
        check = (
            shim
            + "\nimport json as _j\nprint(_j.dumps(df))\n"
        )
        activated, _ = _activate_data_shim(check)
        with tempfile.TemporaryDirectory() as wd:
            wd = _P(wd)
            (wd / "with_locale.r2py_data.json").write_text(payload, encoding="utf-8")
            (wd / "script.py").write_text(activated, encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(wd / "script.py")],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(r.returncode, 0, f"stderr: {r.stderr}")
            out = json.loads(r.stdout.strip().splitlines()[-1])
            self.assertEqual(out["date"], ["2019-01-01", "2019-02-01"])


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
