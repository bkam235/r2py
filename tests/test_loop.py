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
            run_loop(SM, lib, score_threshold=0.85)
        mock_agent.assert_called_once()

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
