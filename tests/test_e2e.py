"""End-to-end pipeline tests — NOT run in per-merge CI (§12.4).

These tests require:
  R2PY_E2E=1          — opt-in gate so CI never picks them up
  ANTHROPIC_API_KEY   — live LLM calls
  Rscript             — sandbox execution

Run manually:
  R2PY_E2E=1 ANTHROPIC_API_KEY=sk-... python -m pytest tests/test_e2e.py -v
"""
from __future__ import annotations

import ast
import os
import pathlib
import tempfile
import unittest

_E2E = bool(os.environ.get("R2PY_E2E"))
_HAS_KEY = bool(os.environ.get("ANTHROPIC_API_KEY"))
_SKIP_REASON = "set R2PY_E2E=1 and ANTHROPIC_API_KEY to run end-to-end tests"

FIXTURE_R = pathlib.Path("tests/fixtures/simple.R")


@unittest.skipUnless(_E2E and _HAS_KEY, _SKIP_REASON)
class TestEndToEndTranslate(unittest.TestCase):
    """Full pipeline: analyze → translate → verify loop on the fixture script."""

    def test_translate_simple_fixture(self):
        from r2py import translate

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            py_path = pathlib.Path(f.name)

        try:
            result = translate(
                r_path=FIXTURE_R,
                py_path=py_path,
                max_iters=2,
            )

            # Basic invariants
            assert result.final_score >= 0.0, "score must be non-negative"
            assert result.final_score <= 1.0, "score must be at most 1"
            assert result.iterations >= 0, "iterations must be non-negative"
            assert isinstance(result.python_source, str), "python_source must be str"
            assert len(result.python_source) > 0, "output must be non-empty"

            # Output file must exist and contain valid Python
            assert py_path.exists(), "output .py file must be written"
            src = py_path.read_text(encoding="utf-8")
            ast.parse(src)  # raises SyntaxError if not valid Python

        finally:
            py_path.unlink(missing_ok=True)

    def test_translate_produces_score_history(self):
        from r2py import translate

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            py_path = pathlib.Path(f.name)

        try:
            result = translate(
                r_path=FIXTURE_R,
                py_path=py_path,
                max_iters=2,
            )
            assert isinstance(result.score_history, list)
            # At least the initial seed score should be recorded
            assert len(result.score_history) >= 1

        finally:
            py_path.unlink(missing_ok=True)

    def test_translate_with_no_seeds(self):
        from r2py import translate

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            py_path = pathlib.Path(f.name)

        try:
            result = translate(
                r_path=FIXTURE_R,
                py_path=py_path,
                max_iters=1,
                no_seeds=True,
            )
            assert result.final_score >= 0.0
            src = py_path.read_text(encoding="utf-8")
            ast.parse(src)

        finally:
            py_path.unlink(missing_ok=True)


@unittest.skipUnless(_E2E and _HAS_KEY, _SKIP_REASON)
class TestEndToEndAnalyze(unittest.TestCase):
    """Stage 1 analysis on the fixture script."""

    def test_analyze_returns_script_map(self):
        from r2py import analyze

        sm = analyze(FIXTURE_R)
        assert hasattr(sm, "entities"), "ScriptMap must have entities"
        assert hasattr(sm, "source"), "ScriptMap must have source"
        assert len(sm.source) > 0, "source must be non-empty"


@unittest.skipUnless(_E2E and _HAS_KEY, _SKIP_REASON)
class TestEndToEndBatch(unittest.TestCase):
    """Batch runner on the fixture script."""

    def test_batch_runs_and_writes_csv(self):
        import csv
        import tempfile
        from pathlib import Path
        from r2py.batch import translate_batch

        tmp = Path(tempfile.mkdtemp())
        input_dir = tmp / "inputs"
        input_dir.mkdir()
        # Symlink or copy fixture
        dest = input_dir / "simple.R"
        dest.write_text(FIXTURE_R.read_text(encoding="utf-8"), encoding="utf-8")

        lc_csv = tmp / "lc.csv"
        st_csv = tmp / "st.csv"

        results = translate_batch(
            input_dir=input_dir,
            output_dir=tmp / "outputs",
            learning_curve_csv=lc_csv,
            scoring_table_csv=st_csv,
            max_iters=1,
        )

        assert len(results) == 1
        assert "error" not in results[0]

        lc_rows = list(csv.DictReader(lc_csv.open()))
        assert len(lc_rows) == 1
        assert float(lc_rows[0]["final_score"]) >= 0.0

        st_rows = list(csv.DictReader(st_csv.open()))
        assert len(st_rows) == 1


if __name__ == "__main__":
    unittest.main()
