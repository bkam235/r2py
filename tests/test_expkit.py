"""Experiment kit (2026-10-24): run guard, common result format, generic comparison."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import expkit   # noqa: E402


class TestRunGuard(unittest.TestCase):
    def guard(self, balances, **kw):
        it = iter(balances)
        return expkit.RunGuard(tempfile.mkdtemp(), read_credits=lambda: next(it), poll_s=0, tick_s=3600, **kw)

    def test_budget_and_reserve_stop_the_run(self):
        g = self.guard([(10.0, 2.0), (10.0, 4.5)], budget=2.0)
        g.balance_start = (10.0, 2.0)
        g._credits = lambda: (10.0, 4.5)          # spent 2.5 of a 2.0 budget
        g._check_money()
        self.assertTrue(g.should_stop())
        self.assertIn("budget", g.stop_reason)
        g = self.guard([], reserve=0.5)
        g.balance_start, g._credits = (10.0, 2.0), (lambda: (10.0, 9.7))   # 0.3 left
        g._check_money()
        self.assertIn("reserve", g.stop_reason)

    def test_a_row_that_overlapped_a_wall_clock_gap_is_invalid(self):
        g = self.guard([])
        g.version = "v"
        now = time.time()
        g.gaps = [(now - 3600, now - 1800)]
        self.assertEqual(g.annotate({"seconds": 7200})["invalid"], "sleep")   # started before the gap
        self.assertNotIn("invalid", g.annotate({"seconds": 60}))              # started after it

    def test_the_manifest_records_cost_and_stop_reason(self):
        d = tempfile.mkdtemp()
        balances = iter([(10.0, 2.0), (10.0, 3.25)])
        with expkit.RunGuard(d, read_credits=lambda: next(balances), poll_s=3600, tick_s=3600) as g:
            g.annotate({"seconds": 1})
        m = json.loads((Path(d) / "run_manifest.json").read_text())[-1]
        self.assertEqual((m["cost"], m["rows"], m["stop_reason"]), (1.25, 1, "finished"))


class TestLoad(unittest.TestCase):
    def write(self, rows):
        f = Path(tempfile.mkdtemp()) / "results.jsonl"
        f.write_text("".join(json.dumps(r) + "\n" for r in rows))
        return f

    def test_two_step_rows_become_two_arms(self):
        f = self.write([{"script": "s", "sample": 0, "start_exit": 0, "best1": 0.5, "fresh": 0.5, "conv": 0.7,
                         "fresh_improved": False, "conv_improved": True, "step2_ran": True}])
        rows = {r["arm"]: r for r in expkit.load(f)}
        self.assertEqual((rows["fresh"]["improved"], rows["conv"]["improved"]), (False, True))
        self.assertAlmostEqual(rows["conv"]["gain"], 0.2)

    def test_a_state_has_one_stratum_and_errors_are_invalid(self):
        f = self.write([{"script": "s", "arm": "U", "sample": 0, "exit_before": 1, "improved": True, "gain": 0.1},
                        {"script": "s", "arm": "U", "sample": 1, "exit_before": 0, "improved": False, "gain": 0.0},
                        {"script": "s", "arm": "U", "sample": 2, "outcome": "error: boom"}])
        rows = expkit.load(f)
        self.assertEqual({r["stratum"] for r in rows}, {"crashing"})          # a tie counts as crashing
        self.assertEqual([r["invalid"] for r in rows], [None, None, "error"])


class TestCompare(unittest.TestCase):
    def test_paired_difference_and_best_of_k(self):
        rows = []
        for s in range(10):
            rows += [{"state": s, "arm": "A", "improved": True}, {"state": s, "arm": "B", "improved": False},
                     {"state": s, "arm": "B", "improved": s % 2 == 0}]
        c = expkit.compare_arms(rows, "A", "B", "improved")
        self.assertAlmostEqual(c["mean"], 0.75)
        self.assertGreater(c["p_gt0"], 0.99)
        c = expkit.compare_arms(rows, "A", "B", "improved", best_of=2)
        self.assertAlmostEqual(c["mean"], 0.5)


if __name__ == "__main__":
    unittest.main()
