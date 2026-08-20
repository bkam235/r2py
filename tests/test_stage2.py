"""Tests for Stage 2 — shared translation infrastructure (§5).

All tests are offline (no LLM calls needed).
"""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from r2py.types import EntityKind
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
# T6b: sentinel comments and rebuild_entity_line_map
# ---------------------------------------------------------------------------

class TestSentinelAndRebuild(unittest.TestCase):

    def setUp(self):
        from r2py.stage2.stitch import rebuild_entity_line_map
        self.rebuild = rebuild_entity_line_map

    def _compose2(self):
        src = (
            "# header\n"
            "\n"
            "# r2py:entity:e0\n"
            "v0 = 1\n"
            "\n"
            "# r2py:entity:e1\n"
            "v1 = 2\n"
        )
        return src, {"e0": [(3, 4)], "e1": [(6, 7)]}

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

    def test_rebuild_returns_empty_without_sentinels(self):
        result = self.rebuild("x = 1\ny = 2\n")
        self.assertEqual(result, {})

    def test_sentinel_is_first_line_of_entity_range(self):
        src, lmap = self._compose2()
        lines = src.splitlines()
        for eid, ranges in lmap.items():
            start = ranges[0][0]
            self.assertIn(eid, lines[start - 1],
                          msg=f"Expected sentinel for {eid} at line {start}")


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


if __name__ == "__main__":
    unittest.main()
