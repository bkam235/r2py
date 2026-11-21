"""r2py.translate() and `r2py translate` run the production default (2026-11-21: they ran claude-sonnet-4-6 for seeds
and agent, threshold 0.85, 3+3 seeds, no provider pin or reasoning cap)."""
from __future__ import annotations

import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import r2py
from r2py import loop


def _result():
    return SimpleNamespace(python_source="x = 1\n", final_score_report=None, final_exit_code=0, final_score=1.0,
                           iterations=0, score_history=[], seed_source=None)


class TestTranslateDefault(unittest.TestCase):
    def _run(self, **kw):
        seen = {}

        def run_loop(script_map, library, **kwargs):
            seen["loop"] = kwargs
            return _result()

        @contextmanager
        def pinned(model, settings):
            seen["pin"] = (model, settings)
            yield

        with tempfile.TemporaryDirectory() as d, \
                mock.patch("r2py.stage1.analyze", return_value=SimpleNamespace(entities={})), \
                mock.patch("r2py.loop.run_loop", side_effect=run_loop), \
                mock.patch("r2py.heldout.pinned_llm", side_effect=pinned), \
                mock.patch("r2py._write_translation_log"), mock.patch("r2py._append_run_record"):
            r2py.translate(Path(d) / "a.R", Path(d) / "a.py", library=object(), **kw)
        return seen

    def test_no_options_runs_the_production_default(self):
        seen = self._run()
        kw = seen["loop"]
        self.assertEqual(kw["model"], loop.DEFAULT_SEED_MODEL)
        self.assertEqual(kw["escalation_model"], loop.DEFAULT_AGENT_MODEL)
        self.assertEqual(kw["score_threshold"], loop.DEFAULT_SCORE_THRESHOLD)
        self.assertEqual((kw["n_bare_seeds"], kw["n_structured_seeds"]),
                         (loop.DEFAULT_BARE_SEEDS, loop.DEFAULT_STRUCTURED_SEEDS))
        self.assertEqual(kw["max_stalls"], loop.DEFAULT_MAX_STALLS)
        self.assertEqual(kw["agent_budget_s"], loop.DEFAULT_AGENT_BUDGET_S)
        self.assertEqual(kw["agent_max_tokens"], loop.DEFAULT_AGENT_MAX_TOKENS)
        # the agent's provider pin and reasoning cap, as in its replays; the seed model unpinned
        _, settings = seen["pin"]
        name = loop.DEFAULT_AGENT_MODEL.removeprefix("openrouter:")
        self.assertIsNone(settings["provider"])
        self.assertEqual(settings["provider_by_model"], {name: loop.DEFAULT_AGENT_PROVIDER})
        self.assertEqual(settings["extra_by_model"], {name: {"reasoning": loop.DEFAULT_AGENT_REASONING}})

    def test_another_agent_model_gets_no_pin_of_the_default_agent(self):
        seen = self._run(escalation_model="openrouter:other/model")
        self.assertNotIn("provider_by_model", seen["pin"][1])

    def test_no_openrouter_model_no_pin(self):
        seen = self._run(model="claude-sonnet-4-6", escalation_model="claude-sonnet-4-6")
        self.assertNotIn("pin", seen)

    def test_cli_defaults_leave_the_choice_to_translate(self):
        from r2py import cli
        with mock.patch("r2py.translate", return_value=_result()) as tr, \
                mock.patch("sys.argv", ["r2py", "translate", "a.R", "a.py"]):
            with self.assertRaises(SystemExit):
                cli.main()
        kw = tr.call_args.kwargs
        for key in ("model", "escalation_model", "score_threshold", "max_stalls"):
            self.assertIsNone(kw[key], key)
        self.assertEqual(kw["max_iters"], 20)


if __name__ == "__main__":
    unittest.main()
