"""Tests for r2py/loop.py — cheap path + reasoning agent escalation."""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from r2py.loop import run_loop
from r2py.types import ScoreReport, ScriptMap


def _sr(aggregate: float) -> ScoreReport:
    return ScoreReport(aggregate=aggregate)


def _mock_lib() -> MagicMock:
    lib = MagicMock()
    lib.record_evidence = MagicMock()
    lib.record_tie = MagicMock()
    lib.record_contradiction = MagicMock()
    lib.store = MagicMock()
    lib.index = MagicMock()
    return lib


SM = ScriptMap(source="x <- 1")

_S2 = "r2py.seed.translate"
_S4 = "r2py.stage4.verify"
_EP = "r2py.library.epistemology.review"
_AGENT = "r2py.harness.agent.reason"

# The anti-hardcoding review now fails closed; without an API key it would reject every seed.
_review_patch = patch("r2py.harness.review.review_translation", return_value=(True, ""))


def setUpModule():
    _review_patch.start()


def tearDownModule():
    _review_patch.stop()


class TestCheapPathSuccess(unittest.TestCase):
    """Seed score >= threshold → agent not called."""

    def test_seed_meets_threshold(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("x = 1", {})), \
             patch(_S4, return_value=_sr(0.9)), \
             patch(_AGENT) as mock_agent, \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=5, score_threshold=0.85)
        assert result.final_score == 0.9
        mock_agent.assert_not_called()

    def test_returns_seed_translation(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("x = 1", {})), \
             patch(_S4, return_value=_sr(0.95)), \
             patch(_AGENT), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, score_threshold=0.9)
        assert result.python_source == "x = 1"


class TestAgentEscalation(unittest.TestCase):
    """Seed score < threshold → agent called."""

    def test_agent_called_on_low_score(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("seed", {})), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_AGENT, return_value=None) as mock_agent, \
             patch(_EP, return_value=[]):
            run_loop(SM, lib, score_threshold=0.85, agent_width=1)
        mock_agent.assert_called_once()

    def test_default_width_runs_independent_loops(self):
        from r2py.loop import DEFAULT_AGENT_WIDTH
        lib = _mock_lib()
        with patch(_S2, return_value=("seed", {})),              patch(_S4, return_value=_sr(0.4)),              patch(_AGENT, return_value=None) as mock_agent,              patch(_EP, return_value=[]):
            run_loop(SM, lib, score_threshold=0.85)
        self.assertEqual(mock_agent.call_count, DEFAULT_AGENT_WIDTH)
        harnesses = {id(c.kwargs["harness"]) for c in mock_agent.call_args_list}
        self.assertEqual(len(harnesses), DEFAULT_AGENT_WIDTH)   # each branch has its own harness

    def test_a_crashing_start_gets_the_crash_width_and_patience(self):
        from r2py.loop import DEFAULT_CRASH_STALLS, DEFAULT_CRASH_WIDTH
        lib = _mock_lib()
        crashing = ScoreReport(aggregate=0.0, py_exit_code=1)
        with patch(_S2, return_value=("seed", {})), patch(_S4, return_value=crashing),              patch(_AGENT, return_value=None) as mock_agent, patch(_EP, return_value=[]):
            run_loop(SM, lib, score_threshold=0.85, agent_budget_s=600)
        self.assertEqual(mock_agent.call_count, DEFAULT_CRASH_WIDTH)
        self.assertEqual(mock_agent.call_args.kwargs["crash_stalls"], DEFAULT_CRASH_STALLS)
        self.assertEqual(mock_agent.call_args.kwargs["budget_s"], 1200)    # twice the budget for twice the chains

    def test_a_running_start_keeps_its_budget(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("seed", {})), patch(_S4, return_value=_sr(0.4)),              patch(_AGENT, return_value=None) as mock_agent, patch(_EP, return_value=[]):
            run_loop(SM, lib, score_threshold=0.85, agent_budget_s=600)
        self.assertEqual(mock_agent.call_args.kwargs["budget_s"], 600)

    def test_agent_improvement_accepted(self):
        lib = _mock_lib()

        with patch(_S2, return_value=("seed", {})), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_AGENT, return_value=("improved", _sr(0.9))), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, score_threshold=0.85)
        assert result.python_source == "improved"
        assert result.final_score == 0.9

    def test_agent_no_improvement_keeps_seed(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("seed", {})), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_AGENT, return_value=None), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, score_threshold=0.85)
        assert result.python_source == "seed"
        assert result.final_score == 0.4


class TestZeroIters(unittest.TestCase):
    """max_iters=0: seed only, no agent."""

    def test_returns_seed_no_agent(self):
        lib = _mock_lib()
        with patch(_S2, return_value=("x = 1", {})), \
             patch(_S4, return_value=_sr(0.3)), \
             patch(_AGENT, return_value=None) as mock_agent, \
             patch(_EP, return_value=[]):
            result = run_loop(SM, lib, max_iters=0, score_threshold=0.85)
        assert result.python_source in ("x = 1",)


class TestSeedSourceKept(unittest.TestCase):
    """The result keeps the seed translation, so what the agent corrected can be compared."""

    def test_seed_kept_when_the_agent_improves_it(self):
        with patch(_S2, return_value=("seed", {})), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_AGENT, return_value=("improved", _sr(0.9))), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, _mock_lib(), score_threshold=0.85)
        assert (result.seed_source, result.python_source) == ("seed", "improved")
        assert result.score_history[0].aggregate == 0.4  # the seed's own report

    def test_seed_kept_when_the_agent_does_not_help(self):
        with patch(_S2, return_value=("seed", {})), \
             patch(_S4, return_value=_sr(0.4)), \
             patch(_AGENT, return_value=None), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, _mock_lib(), score_threshold=0.85)
        assert result.seed_source == result.python_source == "seed"

    def test_seed_is_the_final_translation_on_the_cheap_path(self):
        with patch(_S2, return_value=("x = 1", {})), \
             patch(_S4, return_value=_sr(0.95)), \
             patch(_AGENT), \
             patch(_EP, return_value=[]):
            result = run_loop(SM, _mock_lib(), score_threshold=0.9)
        assert result.seed_source == result.python_source == "x = 1"


class TestTranslatePyPathWritten(unittest.TestCase):
    """translate() writes the Python source to py_path."""

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
                 patch("r2py._append_run_record"), \
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
