"""Tests for r2py/loop.py — beam/strict-improvement loop (§4.1)."""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from r2py.loop import _state_hash, _top_k, run_loop
from r2py.types import (
    Candidate, Edit, EditKind, ScoreReport, ScriptMap,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sr(aggregate: float) -> ScoreReport:
    return ScoreReport(aggregate=aggregate)


def _edit(kind: EditKind = EditKind.INSERT_PREAMBLE,
          pattern_id: str | None = "p1",
          entity_ids: list | None = None) -> Edit:
    return Edit(kind=kind, entity_ids=entity_ids or [], params={}, pattern_id=pattern_id)


def _mock_lib() -> MagicMock:
    lib = MagicMock()
    lib.record_evidence = MagicMock()
    lib.record_tie = MagicMock()
    lib.record_contradiction = MagicMock()
    lib.store = MagicMock()
    lib.index = MagicMock()
    return lib


SM = ScriptMap(source="x <- 1")

# Patch targets inside loop.py — stage* are imported lazily inside run_loop().
_S2 = "r2py.stage2.translate"
_S3_PROPOSE = "r2py.stage3.propose_edit"
_S3_APPLY = "r2py.stage3.apply_edit"
_S4 = "r2py.stage4.verify"
_EP = "r2py.library.epistemology.review"


# ---------------------------------------------------------------------------
# _state_hash
# ---------------------------------------------------------------------------

class TestStateHash(unittest.TestCase):
    def test_deterministic(self):
        assert _state_hash("x = 1") == _state_hash("x = 1")

    def test_distinct_for_different_strings(self):
        assert _state_hash("x = 1") != _state_hash("y = 2")

    def test_returns_valid_hex(self):
        h = _state_hash("hello world")
        assert isinstance(h, str)
        int(h, 16)  # raises ValueError if not valid hex

    def test_empty_string(self):
        h = _state_hash("")
        assert len(h) == 64  # SHA-256 hex digest


# ---------------------------------------------------------------------------
# _top_k
# ---------------------------------------------------------------------------

class TestTopK(unittest.TestCase):
    def _cs(self, scores: list[float]) -> list[Candidate]:
        return [Candidate(f"t{s}", s, _sr(s)) for s in scores]

    def test_k1_returns_best(self):
        result = _top_k(self._cs([0.3, 0.9, 0.5]), 1)
        assert len(result) == 1
        assert result[0].score == 0.9

    def test_respects_beam_width(self):
        result = _top_k(self._cs([0.1, 0.5, 0.9, 0.7]), 2)
        assert len(result) == 2
        assert result[0].score == 0.9
        assert result[1].score == 0.7

    def test_k_larger_than_list(self):
        result = _top_k(self._cs([0.3, 0.7]), 10)
        assert len(result) == 2

    def test_incumbents_win_ties(self):
        # stable sort: incumbent (earlier in input) beats survivor at equal score
        incumbent = Candidate("incumbent", 0.5, _sr(0.5))
        survivor = Candidate("survivor", 0.5, _sr(0.5))
        result = _top_k([incumbent, survivor], 1)
        assert result[0].translation == "incumbent"

    def test_empty_list(self):
        assert _top_k([], 3) == []


# ---------------------------------------------------------------------------
# run_loop — seed / zero-iters
# ---------------------------------------------------------------------------

class TestRunLoopSeed(unittest.TestCase):
    """max_iters=0 returns seed translation immediately."""

    def test_returns_seed_translation(self):
        lib = _mock_lib()
        with patch(_S2, return_value="x = 1"), \
             patch(_S4, return_value=_sr(0.6)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=0, beam_width=1)
        assert result.python_source == "x = 1"
        assert result.final_score == 0.6

    def test_iterations_is_one(self):
        lib = _mock_lib()
        with patch(_S2, return_value="x = 1"), \
             patch(_S4, return_value=_sr(0.6)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=0)
        assert result.iterations == 1

    def test_score_history_contains_seed(self):
        lib = _mock_lib()
        with patch(_S2, return_value="x = 1"), \
             patch(_S4, return_value=_sr(0.6)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=0)
        assert len(result.score_history) == 1
        assert result.score_history[0].aggregate == 0.6

    def test_no_library_writes_on_seed_only(self):
        lib = _mock_lib()
        with patch(_S2, return_value="x = 1"), \
             patch(_S4, return_value=_sr(0.6)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            run_loop(SM, lib, max_iters=0)
        lib.record_evidence.assert_not_called()
        lib.record_tie.assert_not_called()
        lib.record_contradiction.assert_not_called()


# ---------------------------------------------------------------------------
# run_loop — halt on threshold
# ---------------------------------------------------------------------------

class TestHaltOnThreshold(unittest.TestCase):
    def test_seed_meets_threshold(self):
        lib = _mock_lib()
        with patch(_S2, return_value="x = 1"), \
             patch(_S4, return_value=_sr(0.9)), \
             patch(_S3_PROPOSE) as mock_s3, \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=5, score_threshold=0.85)
        assert result.final_score == 0.9
        mock_s3.assert_not_called()

    def test_iterations_is_one_when_seed_exceeds_threshold(self):
        lib = _mock_lib()
        with patch(_S2, return_value="seed"), \
             patch(_S4, return_value=_sr(1.0)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=8, score_threshold=0.85)
        assert result.iterations == 1


# ---------------------------------------------------------------------------
# run_loop — strict improvement
# ---------------------------------------------------------------------------

class TestStrictImprovement(unittest.TestCase):
    """new_score > parent_score → beam updated, record_evidence called."""

    def _run(self, seed_score: float = 0.5, new_score: float = 0.7):
        lib = _mock_lib()
        edit = _edit(pattern_id="good_pattern")
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(seed_score if verify_calls[0] == 1 else new_score)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, return_value="improved"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        return result, lib, edit

    def test_best_translation_updated(self):
        result, _, _ = self._run()
        assert result.python_source == "improved"
        assert result.final_score == 0.7

    def test_record_evidence_called_once(self):
        _, lib, _ = self._run(seed_score=0.5, new_score=0.7)
        lib.record_evidence.assert_called_once()

    def test_score_delta_is_correct(self):
        _, lib, _ = self._run(seed_score=0.5, new_score=0.7)
        kwargs = lib.record_evidence.call_args[1]
        assert abs(kwargs["score_delta"] - 0.2) < 1e-9

    def test_no_contradiction_on_improvement(self):
        _, lib, _ = self._run()
        lib.record_contradiction.assert_not_called()

    def test_pattern_id_in_evidence_added(self):
        result, _, _ = self._run()
        assert "good_pattern" in result.pattern_evidence_added

    def test_none_pattern_id_not_in_evidence_added(self):
        lib = _mock_lib()
        edit = _edit(pattern_id=None)
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5 if verify_calls[0] == 1 else 0.8)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, return_value="improved"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        assert result.pattern_evidence_added == []


# ---------------------------------------------------------------------------
# run_loop — tie not accepted
# ---------------------------------------------------------------------------

class TestTieNotAccepted(unittest.TestCase):
    """new_score == parent_score → beam unchanged, record_tie called."""

    def _run_tie(self, score: float = 0.5):
        lib = _mock_lib()
        edit = _edit(pattern_id="tie_pattern")

        with patch(_S2, return_value="seed"), \
             patch(_S4, return_value=_sr(score)), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, return_value="tie_translation"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        return result, lib

    def test_best_stays_on_seed(self):
        result, _ = self._run_tie()
        assert result.python_source == "seed"

    def test_record_tie_called(self):
        _, lib = self._run_tie()
        lib.record_tie.assert_called_once()

    def test_record_evidence_not_called(self):
        _, lib = self._run_tie()
        lib.record_evidence.assert_not_called()

    def test_record_contradiction_not_called(self):
        _, lib = self._run_tie()
        lib.record_contradiction.assert_not_called()


# ---------------------------------------------------------------------------
# run_loop — regression not accepted
# ---------------------------------------------------------------------------

class TestRegressionNotAccepted(unittest.TestCase):
    """new_score < parent_score → beam unchanged, record_contradiction called."""

    def _run_regression(self):
        lib = _mock_lib()
        edit = _edit(pattern_id="bad_pattern")
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.6 if verify_calls[0] == 1 else 0.3)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, return_value="regressed"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        return result, lib

    def test_best_stays_on_seed(self):
        result, _ = self._run_regression()
        assert result.python_source == "seed"

    def test_record_contradiction_called(self):
        _, lib = self._run_regression()
        lib.record_contradiction.assert_called_once()

    def test_record_evidence_not_called(self):
        _, lib = self._run_regression()
        lib.record_evidence.assert_not_called()

    def test_pattern_id_in_contradictions_added(self):
        result, _ = self._run_regression()
        assert "bad_pattern" in result.pattern_contradictions_added


# ---------------------------------------------------------------------------
# run_loop — tabu set
# ---------------------------------------------------------------------------

class TestTabuSet(unittest.TestCase):
    """apply_edit producing a visited translation is skipped without verifying."""

    def test_same_translation_as_seed_is_tabu(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, return_value="seed"), \
             patch(_EP, return_value=[]):
            run_loop(SM, lib, max_iters=2, beam_width=1)

        # Only the seed verify call; proposals skipped (all tabu)
        assert verify_calls[0] == 1

    def test_new_translation_not_tabu(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5 if verify_calls[0] == 1 else 0.8)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, return_value="new_translation"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        assert verify_calls[0] == 2  # seed + proposal


# ---------------------------------------------------------------------------
# run_loop — no proposals → break early
# ---------------------------------------------------------------------------

class TestNoProposals(unittest.TestCase):
    def test_runtime_error_causes_early_break(self):
        lib = _mock_lib()
        with patch(_S2, return_value="seed"), \
             patch(_S4, return_value=_sr(0.5)), \
             patch(_S3_PROPOSE, side_effect=RuntimeError("exhausted")), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=5, beam_width=1)
        assert result.python_source == "seed"
        # Entered iteration 0, then broke — iterations = 1
        assert result.iterations == 1

    def test_all_proposals_tabu_causes_break(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, return_value="seed"),  \
             patch(_EP, return_value=[]):
            run_loop(SM, lib, max_iters=5, beam_width=1)

        assert verify_calls[0] == 1  # only seed; loop breaks on empty proposals


# ---------------------------------------------------------------------------
# run_loop — beam width
# ---------------------------------------------------------------------------

class TestBeamWidth(unittest.TestCase):
    """W=2 beam holds multiple distinct candidates."""

    def test_improvement_accepted_with_w2(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5 if verify_calls[0] == 1 else 0.7)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, return_value="improved"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=2)

        assert result.final_score == 0.7


# ---------------------------------------------------------------------------
# run_loop — max_iters halt
# ---------------------------------------------------------------------------

class TestMaxItersHalt(unittest.TestCase):
    def test_iterations_matches_max_iters(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(verify_calls[0] * 0.05)

        def fake_apply(translation, e):
            return f"v{verify_calls[0]}"

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, side_effect=fake_apply), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=3, beam_width=1, score_threshold=0.99)

        assert result.iterations == 3


# ---------------------------------------------------------------------------
# run_loop — pattern tracking
# ---------------------------------------------------------------------------

class TestPatternTracking(unittest.TestCase):
    def test_evidence_added_deduplicated(self):
        lib = _mock_lib()
        edit = _edit(pattern_id="dup_pattern")
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(verify_calls[0] * 0.1)

        def fake_apply(t, e):
            return f"v{verify_calls[0]}"

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, side_effect=fake_apply), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=2, beam_width=1, score_threshold=0.99)

        assert result.pattern_evidence_added.count("dup_pattern") == 1

    def test_contradictions_added_deduplicated(self):
        lib = _mock_lib()
        edit = _edit(pattern_id="bad")
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            # seed high, proposals low
            return _sr(0.8 if verify_calls[0] == 1 else 0.1)

        def fake_apply(t, e):
            return f"v{verify_calls[0]}"

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=edit), \
             patch(_S3_APPLY, side_effect=fake_apply), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        assert result.pattern_contradictions_added.count("bad") == 1


# ---------------------------------------------------------------------------
# run_loop — score history
# ---------------------------------------------------------------------------

class TestScoreHistory(unittest.TestCase):
    def test_history_length_seed_plus_proposals(self):
        lib = _mock_lib()
        verify_calls = [0]

        def fake_verify(sm, src, **kw):
            verify_calls[0] += 1
            return _sr(0.5)

        with patch(_S2, return_value="seed"), \
             patch(_S4, side_effect=fake_verify), \
             patch(_S3_PROPOSE, return_value=_edit()), \
             patch(_S3_APPLY, return_value="new_v"), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1, beam_width=1)

        # 1 seed + 1 proposal
        assert len(result.score_history) == 2

    def test_history_entries_are_score_reports(self):
        lib = _mock_lib()
        with patch(_S2, return_value="seed"), \
             patch(_S4, return_value=_sr(0.5)), \
             patch(_S3_PROPOSE, side_effect=RuntimeError), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=1)

        assert all(isinstance(r, ScoreReport) for r in result.score_history)

    def test_history_not_collected_when_zero_iters(self):
        lib = _mock_lib()
        with patch(_S2, return_value="seed"), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_S3_PROPOSE), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=0)

        assert len(result.score_history) == 1  # only seed


# ---------------------------------------------------------------------------
# translate() — top-level API writes py_path to disk
# ---------------------------------------------------------------------------

class TestTranslatePyPathWritten(unittest.TestCase):
    """translate() in r2py/__init__.py must write the Python source to py_path."""

    def test_py_path_written(self):
        import tempfile
        import os
        from r2py import translate
        from r2py.types import TranslateResult

        fake_result = TranslateResult(python_source="x = 1", final_score=0.9, iterations=1)

        with tempfile.NamedTemporaryFile(suffix=".R", delete=False, mode="w") as rf:
            rf.write("x <- 1\n")
            r_path = rf.name
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as pf:
            py_path = pf.name

        try:
            with patch("r2py.stage1.analyze") as mock_analyze, \
                 patch("r2py.library.get_library"), \
                 patch("r2py.loop.run_loop", return_value=fake_result):
                mock_analyze.return_value = ScriptMap(source="x <- 1")
                result = translate(r_path, py_path)

            assert result.python_source == "x = 1"
            with open(py_path, encoding="utf-8") as f:
                assert f.read() == "x = 1"
        finally:
            os.unlink(r_path)
            os.unlink(py_path)


if __name__ == "__main__":
    unittest.main()
