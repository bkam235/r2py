"""Learning-curve instrument: the statistics and the summary on synthetic rows."""
import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import learning_curve as LC  # noqa: E402


class TestStats(unittest.TestCase):
    def test_slope(self):
        self.assertAlmostEqual(LC.slope([0, 1, 2, 3], [1.0, 2.0, 3.0, 4.0]), 1.0)
        self.assertEqual(LC.slope([1, 1], [2, 5]), 0.0)

    def test_bootstrap_interval_contains_the_estimate_and_resamples_clusters(self):
        clusters = {f"s{i}": [float(i % 3)] for i in range(30)}
        est, lo, hi = LC.bootstrap(clusters, lambda cl: sum(c[0] for c in cl) / len(cl), n=500)
        self.assertLessEqual(lo, est)
        self.assertLessEqual(est, hi)
        self.assertGreater(hi - lo, 0)

    def test_bootstrap_of_a_constant_has_no_width(self):
        est, lo, hi = LC.bootstrap({"a": [1.0], "b": [1.0]}, lambda cl: sum(c[0] for c in cl) / len(cl), n=100)
        self.assertEqual((est, lo, hi), (1.0, 1.0, 1.0))


def _entity(eid, key, score=1.0):
    return {"id": eid, "name": eid, "key": key, "calls": [], "score": score, "executed_ok": True,
            "active_dims": ["data_output"], "dim_scores": {}, "uncomparable": False}


class TestSummary(unittest.TestCase):
    SNAPS = [{"name": "empty", "n_train": 0, "library": "e"}, {"name": "mid", "n_train": 100, "library": "m"},
             {"name": "full", "n_train": 200, "library": "f"}]

    def _rows(self, gain):
        rng = random.Random(1)
        rows = []
        for s in range(20):
            for snap in self.SNAPS:
                for idx in range(2):
                    # a targetable entity improves with the snapshot, an untargeted one does not
                    t = 0.3 + gain * snap["n_train"] / 200 + rng.uniform(-0.05, 0.05)
                    rows.append({"snapshot": snap["name"], "n_train": snap["n_train"], "script": f"s{s}", "idx": idx,
                                 "aggregate": round(t, 3), "exit_code": 0,
                                 "entities": [_entity("a", "P1", t), _entity("b", None, 0.5)]})
        return rows

    def _summary(self, gain):
        ids = {"e": set(), "m": {"P1"}, "f": {"P1"}}
        with patch("r2py.heldout.targetable_ids", side_effect=lambda lib: ids[lib]):
            return LC.summarise(self._rows(gain), {}, self.SNAPS)

    def test_a_real_effect_has_a_positive_slope_above_zero(self):
        text = self._summary(0.3)
        self.assertIn("slope +0.15", text)            # +0.3 over 200 training scripts = +0.15 per 100
        self.assertIn("entity level, 20 entities", text)
        self.assertIn("full=0.603", text)

    def test_no_effect_has_a_slope_interval_around_zero(self):
        text = self._summary(0.0)
        line = [l for l in text.splitlines() if l.startswith("script level")][0]
        lo, hi = [float(x) for x in line.split("[")[1].split("]")[0].split(",")]
        self.assertLess(lo, 0.0)
        self.assertGreater(hi, 0.0)

    def test_coverage_column_counts_only_what_a_snapshot_can_inform(self):
        text = self._summary(0.1)
        cov = {l.split()[0]: l.split()[-1] for l in text.splitlines() if l.startswith(("empty", "mid", "full"))}
        self.assertEqual(cov["empty"], "0.0%")
        self.assertEqual(cov["full"], "50.0%")        # one of the two entities has a pattern

    def test_no_rows(self):
        self.assertEqual(LC.summarise([], {}, self.SNAPS), "no finished seeds")


if __name__ == "__main__":
    unittest.main()
