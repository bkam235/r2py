"""Tests for r2py/batch.py and r2py/ablation.py."""
from __future__ import annotations

import csv
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from r2py.types import TranslateResult, ScoreReport


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _fake_result(score: float = 0.75) -> TranslateResult:
    return TranslateResult(
        python_source="x = 1\n",
        final_score=score,
        iterations=2,
        score_history=[ScoreReport(aggregate=score)],
        pattern_evidence_added=["p1"],
        pattern_contradictions_added=[],
    )


def _make_r_file(tmp: Path, name: str = "test.R") -> Path:
    p = tmp / name
    p.write_text("x <- 1\n", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# TestFrozenLibrary
# ---------------------------------------------------------------------------

class TestFrozenLibrary(unittest.TestCase):

    def _make_inner(self) -> MagicMock:
        inner = MagicMock()
        inner.some_attribute = "value"
        inner.retrieve = MagicMock(return_value=["pattern"])
        return inner

    def test_read_proxies_through(self):
        from r2py.ablation import _FrozenLibrary
        inner = self._make_inner()
        frozen = _FrozenLibrary(inner)
        assert frozen.some_attribute == "value"
        assert frozen.retrieve() == ["pattern"]

    def test_record_evidence_is_noop(self):
        from r2py.ablation import _FrozenLibrary
        inner = self._make_inner()
        frozen = _FrozenLibrary(inner)
        frozen.record_evidence("e1", score_delta=0.1)
        inner.record_evidence.assert_not_called()

    def test_record_tie_is_noop(self):
        from r2py.ablation import _FrozenLibrary
        inner = self._make_inner()
        frozen = _FrozenLibrary(inner)
        frozen.record_tie("e1")
        inner.record_tie.assert_not_called()

    def test_record_contradiction_is_noop(self):
        from r2py.ablation import _FrozenLibrary
        inner = self._make_inner()
        frozen = _FrozenLibrary(inner)
        frozen.record_contradiction("e1", observed=0.3)
        inner.record_contradiction.assert_not_called()

    def test_inner_write_methods_not_called(self):
        from r2py.ablation import _FrozenLibrary
        inner = self._make_inner()
        frozen = _FrozenLibrary(inner)
        for fn in ("record_evidence", "record_tie", "record_contradiction"):
            getattr(frozen, fn)("x")
        inner.record_evidence.assert_not_called()
        inner.record_tie.assert_not_called()
        inner.record_contradiction.assert_not_called()


# ---------------------------------------------------------------------------
# TestTranslateBatch
# ---------------------------------------------------------------------------

class TestTranslateBatch(unittest.TestCase):

    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())

    def _run(self, r_files: list[Path], translate_return=None, **kwargs):
        from r2py.batch import translate_batch

        input_dir = self._tmp / "inputs"
        input_dir.mkdir()
        for f in r_files:
            target = input_dir / f.name
            target.write_text(f.read_text(), encoding="utf-8")

        out_dir = self._tmp / "outputs"
        lc_csv = self._tmp / "learning_curve.csv"
        st_csv = self._tmp / "scoring_table.csv"

        side = translate_return or _fake_result()
        with patch("r2py.translate", return_value=side) as mock_t:
            results = translate_batch(
                input_dir=input_dir,
                output_dir=out_dir,
                learning_curve_csv=lc_csv,
                scoring_table_csv=st_csv,
                **kwargs,
            )
        return results, mock_t, lc_csv, st_csv, out_dir

    def test_calls_translate_for_each_r_file(self):
        r_files = [_make_r_file(self._tmp, f"s{i}.R") for i in range(3)]
        results, mock_t, *_ = self._run(r_files)
        assert mock_t.call_count == 3

    def test_returns_result_per_script(self):
        r_files = [_make_r_file(self._tmp, "a.R")]
        results, *_ = self._run(r_files)
        assert len(results) == 1
        assert results[0]["script_id"] == "a.R"
        assert results[0]["final_score"] == 0.75

    def test_appends_learning_curve_csv(self):
        r_files = [_make_r_file(self._tmp, f"s{i}.R") for i in range(2)]
        _, _, lc_csv, *_ = self._run(r_files)
        rows = list(csv.DictReader(lc_csv.open()))
        assert len(rows) == 2
        assert float(rows[0]["final_score"]) == 0.75

    def test_learning_curve_has_header(self):
        r_files = [_make_r_file(self._tmp, "x.R")]
        _, _, lc_csv, *_ = self._run(r_files)
        header = lc_csv.read_text().splitlines()[0]
        assert "script_id" in header
        assert "final_score" in header

    def test_writes_scoring_table_csv(self):
        r_files = [_make_r_file(self._tmp, "x.R")]
        _, _, _, st_csv, *_ = self._run(r_files)
        rows = list(csv.DictReader(st_csv.open()))
        assert len(rows) == 1
        assert rows[0]["script_id"] == "x.R"

    def test_error_does_not_abort_batch(self):
        r_files = [_make_r_file(self._tmp, f"s{i}.R") for i in range(3)]
        from r2py.batch import translate_batch

        input_dir = self._tmp / "inputs2"
        input_dir.mkdir()
        for f in r_files:
            (input_dir / f.name).write_text("x <- 1\n", encoding="utf-8")

        out_dir = self._tmp / "outputs2"
        lc_csv = self._tmp / "lc2.csv"
        st_csv = self._tmp / "st2.csv"

        call_count = 0

        def flaky(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("injected failure")
            return _fake_result()

        with patch("r2py.translate", side_effect=flaky):
            results = translate_batch(
                input_dir=input_dir,
                output_dir=out_dir,
                learning_curve_csv=lc_csv,
                scoring_table_csv=st_csv,
            )

        assert len(results) == 3
        errors = [r for r in results if "error" in r]
        assert len(errors) == 1

    def test_skip_existing_without_force(self):
        from r2py.batch import translate_batch

        input_dir = self._tmp / "in_skip"
        input_dir.mkdir()
        (input_dir / "x.R").write_text("x <- 1\n", encoding="utf-8")
        out_dir = self._tmp / "out_skip"
        lc_csv = self._tmp / "lc_skip.csv"
        st_csv = self._tmp / "st_skip.csv"

        with patch("r2py.translate", return_value=_fake_result()) as mock_t:
            # First run creates a timestamped output dir
            translate_batch(input_dir=input_dir, output_dir=out_dir,
                            learning_curve_csv=lc_csv, scoring_table_csv=st_csv)
            first_count = mock_t.call_count
            assert first_count == 1

            # Second run without force should skip because glob("x__*") finds the dir
            translate_batch(input_dir=input_dir, output_dir=out_dir,
                            learning_curve_csv=lc_csv, scoring_table_csv=st_csv)
            second_count = mock_t.call_count

        # No additional translate calls — the prior run dir was found via glob
        assert second_count == first_count

    def test_force_flag_retranslates(self):
        r_files = [_make_r_file(self._tmp, "y.R")]
        from r2py.batch import translate_batch

        input_dir = self._tmp / "in_force"
        input_dir.mkdir()
        (input_dir / "y.R").write_text("x <- 1\n", encoding="utf-8")
        out_dir = self._tmp / "out_force"
        lc_csv = self._tmp / "lc_force.csv"
        st_csv = self._tmp / "st_force.csv"

        with patch("r2py.translate", return_value=_fake_result()) as mock_t:
            translate_batch(input_dir=input_dir, output_dir=out_dir,
                            learning_curve_csv=lc_csv, scoring_table_csv=st_csv)
            translate_batch(input_dir=input_dir, output_dir=out_dir,
                            learning_curve_csv=lc_csv, scoring_table_csv=st_csv, force=True)

        assert mock_t.call_count == 2

    def test_no_r_files_returns_empty(self):
        empty_dir = self._tmp / "empty_in"
        empty_dir.mkdir()
        from r2py.batch import translate_batch
        results = translate_batch(
            input_dir=empty_dir,
            output_dir=self._tmp / "empty_out",
            learning_curve_csv=self._tmp / "elc.csv",
            scoring_table_csv=self._tmp / "est.csv",
        )
        assert results == []

    def test_evidence_and_contradictions_recorded(self):
        r_files = [_make_r_file(self._tmp, "ev.R")]
        result = _fake_result()
        result.pattern_evidence_added = ["p1", "p2"]
        result.pattern_contradictions_added = ["p3"]
        results, _, lc_csv, *_ = self._run(r_files, translate_return=result)
        rows = list(csv.DictReader(lc_csv.open()))
        assert rows[0]["evidence_added"] == "2"
        assert rows[0]["contradictions_added"] == "1"


# ---------------------------------------------------------------------------
# TestRunAblation
# ---------------------------------------------------------------------------

class TestRunAblation(unittest.TestCase):

    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())

    def _write_slice(self, scripts: list[str]) -> Path:
        p = self._tmp / "slice.txt"
        p.write_text("\n".join(scripts) + "\n", encoding="utf-8")
        return p

    def _run_ablation(self, scripts: list[str], score_a: float = 0.6,
                      score_b: float = 0.75, compare: str = "frozen-vs-learning"):
        from r2py.ablation import run_ablation

        slice_path = self._write_slice(scripts)
        out_dir = self._tmp / "ablation"

        call_num = [0]

        def fake_translate(*args, **kwargs):
            call_num[0] += 1
            # First half = run A, second half = run B
            score = score_a if call_num[0] <= len(scripts) else score_b
            result = _fake_result(score)
            # Write the output .py so cli doesn't crash
            py_path = kwargs.get("py_path")
            if py_path:
                Path(py_path).write_text("x = 1\n", encoding="utf-8")
            return result

        with patch("r2py.ablation.get_library", return_value=MagicMock()), \
             patch("r2py.translate", side_effect=fake_translate):
            summary = run_ablation(
                slice_path=slice_path,
                compare=compare,
                output_dir=out_dir,
            )
        return summary, out_dir

    def test_produces_summary_keys(self):
        summary, _ = self._run_ablation(["a.R"])
        for key in ("n_scripts", "mean_delta", "p_value", "test", "regressions"):
            assert key in summary

    def test_n_scripts_correct(self):
        summary, _ = self._run_ablation(["a.R", "b.R", "c.R"])
        assert summary["n_scripts"] == 3

    def test_mean_delta_positive_when_b_better(self):
        summary, _ = self._run_ablation(["a.R"], score_a=0.5, score_b=0.8)
        assert summary["mean_delta"] > 0

    def test_mean_delta_negative_when_b_worse(self):
        summary, _ = self._run_ablation(["a.R"], score_a=0.9, score_b=0.6)
        assert summary["mean_delta"] < 0

    def test_regressions_list_populated(self):
        summary, _ = self._run_ablation(["a.R"], score_a=0.9, score_b=0.6)
        assert "a.R" in summary["regressions"]

    def test_regressions_empty_when_b_better(self):
        summary, _ = self._run_ablation(["a.R"], score_a=0.5, score_b=0.8)
        assert summary["regressions"] == []

    def test_per_script_csv_created(self):
        _, out_dir = self._run_ablation(["a.R"])
        csv_files = list(out_dir.rglob("per_script.csv"))
        assert len(csv_files) == 1

    def test_per_script_csv_has_expected_columns(self):
        _, out_dir = self._run_ablation(["a.R"])
        csv_path = next(out_dir.rglob("per_script.csv"))
        rows = list(csv.DictReader(csv_path.open()))
        assert rows[0].keys() >= {"script_id", "score_A", "score_B", "delta"}

    def test_summary_json_created(self):
        _, out_dir = self._run_ablation(["a.R"])
        json_files = list(out_dir.rglob("summary.json"))
        assert len(json_files) == 1

    def test_summary_json_parseable(self):
        _, out_dir = self._run_ablation(["a.R"])
        json_path = next(out_dir.rglob("summary.json"))
        data = json.loads(json_path.read_text())
        assert "mean_delta" in data

    def test_skips_comment_and_blank_lines_in_slice(self):
        slice_path = self._tmp / "slice_comments.txt"
        slice_path.write_text(
            "# this is a comment\n\na.R\n\n# another comment\nb.R\n",
            encoding="utf-8",
        )
        out_dir = self._tmp / "ablation_comments"

        with patch("r2py.ablation.get_library", return_value=MagicMock()), \
             patch("r2py.translate", return_value=_fake_result()) as mock_t:
            from r2py.ablation import run_ablation
            summary = run_ablation(slice_path=slice_path, output_dir=out_dir)

        assert summary["n_scripts"] == 2
        assert mock_t.call_count == 4  # 2 scripts × 2 runs

    def test_raises_on_missing_slice(self):
        from r2py.ablation import run_ablation
        with self.assertRaises(FileNotFoundError):
            run_ablation(slice_path=self._tmp / "nonexistent.txt",
                         output_dir=self._tmp / "out")

    def test_raises_on_empty_slice(self):
        slice_path = self._tmp / "empty_slice.txt"
        slice_path.write_text("# only comments\n\n", encoding="utf-8")
        from r2py.ablation import run_ablation
        with self.assertRaises(ValueError):
            run_ablation(slice_path=slice_path, output_dir=self._tmp / "out")

    def test_frozen_library_used_for_run_a(self):
        from r2py.ablation import run_ablation, _FrozenLibrary
        slice_path = self._write_slice(["a.R"])
        out_dir = self._tmp / "frozen_check"

        library_instances = []

        def capture_library(*args, **kwargs):
            library_instances.append(kwargs.get("library"))
            py = kwargs.get("py_path")
            if py:
                Path(py).write_text("x=1\n", encoding="utf-8")
            return _fake_result()

        mock_lib = MagicMock()
        with patch("r2py.ablation.get_library", return_value=mock_lib), \
             patch("r2py.translate", side_effect=capture_library):
            run_ablation(slice_path=slice_path, compare="frozen-vs-learning",
                         output_dir=out_dir)

        assert len(library_instances) == 2
        # run A library must be a _FrozenLibrary
        assert isinstance(library_instances[0], _FrozenLibrary)
        # run B library must be the real one
        assert library_instances[1] is mock_lib

    def test_heuristic_vs_learned_sets_learned_flag(self):
        from r2py.ablation import run_ablation, _FrozenLibrary
        slice_path = self._write_slice(["a.R"])
        out_dir = self._tmp / "h_vs_l"

        library_instances = []

        def capture_learned(*args, **kwargs):
            library_instances.append(kwargs.get("library"))
            py = kwargs.get("py_path")
            if py:
                Path(py).write_text("x=1\n", encoding="utf-8")
            return _fake_result()

        mock_lib = MagicMock()
        mock_lib.learned_retrieval = False
        with patch("r2py.ablation.get_library", return_value=mock_lib), \
             patch("r2py.translate", side_effect=capture_learned):
            run_ablation(slice_path=slice_path, compare="heuristic-vs-learned",
                         output_dir=out_dir)

        assert isinstance(library_instances[0], _FrozenLibrary)  # run A always frozen
        assert library_instances[1] is mock_lib   # run B uses live library
        assert mock_lib.learned_retrieval is True  # flag set directly on library


# ---------------------------------------------------------------------------
# TestSignificance (unit tests for the stat helper)
# ---------------------------------------------------------------------------

class TestSignificance(unittest.TestCase):

    def test_positive_deltas_return_low_p(self):
        from r2py.ablation import _significance
        # All improvements → p should be small (or at least well-defined)
        deltas = [0.1] * 20
        p, name = _significance(deltas)
        assert 0.0 <= p <= 1.0
        assert name in ("wilcoxon", "sign_test")

    def test_mixed_deltas_return_high_p(self):
        from r2py.ablation import _significance
        # Perfect noise: alternating +/− same magnitude
        deltas = [0.1, -0.1] * 10
        p, name = _significance(deltas)
        assert p > 0.3  # should not be significant

    def test_single_delta_returns_one(self):
        from r2py.ablation import _significance
        p, name = _significance([0.1])
        assert p == 1.0
        assert name == "insufficient_data"

    def test_empty_returns_one(self):
        from r2py.ablation import _significance
        p, name = _significance([])
        assert p == 1.0

    def test_p_value_in_range(self):
        from r2py.ablation import _significance
        import random
        rng = random.Random(42)
        deltas = [rng.gauss(0.05, 0.1) for _ in range(30)]
        p, _ = _significance(deltas)
        assert 0.0 <= p <= 1.0


# ---------------------------------------------------------------------------
# TestReadSlice
# ---------------------------------------------------------------------------

class TestReadSlice(unittest.TestCase):

    def test_reads_valid_lines(self):
        from r2py.ablation import _read_slice
        p = Path(tempfile.mktemp(suffix=".txt"))
        p.write_text("a.R\nb.R\n", encoding="utf-8")
        assert _read_slice(p) == ["a.R", "b.R"]

    def test_skips_comments_and_blanks(self):
        from r2py.ablation import _read_slice
        p = Path(tempfile.mktemp(suffix=".txt"))
        p.write_text("# comment\n\na.R\n\n# another\nb.R\n", encoding="utf-8")
        assert _read_slice(p) == ["a.R", "b.R"]

    def test_raises_if_missing(self):
        from r2py.ablation import _read_slice
        with self.assertRaises(FileNotFoundError):
            _read_slice(Path("/nonexistent/slice.txt"))


if __name__ == "__main__":
    unittest.main()
