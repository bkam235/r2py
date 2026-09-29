"""scripts/analyze_train_log.py: the baseline metrics are recomputed, not typed in."""
import importlib.util
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "atl", Path(__file__).resolve().parents[1] / "scripts" / "analyze_train_log.py")
atl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(atl)


class TestMetrics(unittest.TestCase):
    def test_progress(self):
        rows = [{"score": 1.0, "patterns": 3, "seconds": 3600},
                {"score": 0.3, "patterns": 3, "seconds": 3600},
                {"score": 0.95, "patterns": 5, "seconds": 3600}]
        m = atl.progress_metrics(rows)
        self.assertAlmostEqual(m["patterns_per_compute_hour"], 5 / 3)
        self.assertAlmostEqual(m["share_scripts_contributing"], 2 / 3)
        self.assertAlmostEqual(m["share_compute_on_scripts_teaching_nothing"], 1 / 3)
        self.assertAlmostEqual(m["share_reaching_threshold"], 2 / 3)

    def test_stdout(self):
        text = ("[Agent]   Step 1: rewrite\n[Agent]   Rewrite scored: 0.500 (was 0.400), exit_code=0\n"
                "[Agent]   Step 2: rewrite\n[Agent]   Rewrite scored: 0.000 (was 0.500), exit_code=1\n"
                "[Agent]   Step 3: probe_r\n[Agent]   Syntax error: line 3\n"
                "[Agent]   Rewrite scored: 0.500 (was 0.500), exit_code=0\n")
        m = atl.stdout_metrics(text)
        self.assertAlmostEqual(m["share_rewrites_improving"], 1 / 3)
        self.assertAlmostEqual(m["share_rewrites_worsening"], 1 / 3)
        self.assertAlmostEqual(m["share_rewrites_catastrophic"], 1 / 3)
        self.assertAlmostEqual(m["share_non_rewrite_actions"], 1 / 3)
        self.assertEqual(m["syntax_rejections"], 1)


if __name__ == "__main__":
    unittest.main()
