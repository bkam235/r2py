"""Experiment registry (scripts/registry.py, 2026-10-25): register before data, complete when decided."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import registry  # noqa: E402

SPEC = dict(id="x-test", question="does it help?", track="harness", instrument="step_ab.py", pool="training",
            arms=["U", "X"], baseline="U", primary="P(step improves)", rule="free", est_cost=0.5,
            plan="X, registered 2026-10-25")


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.path = self.dir / "registry.jsonl"

    def test_register_stamps_and_refuses_duplicates_and_missing_fields(self):
        rec = registry.register(dict(SPEC), self.path)
        self.assertEqual(rec["status"], "registered")
        self.assertIn("scoring_version", rec)
        with self.assertRaises(ValueError):
            registry.register(dict(SPEC), self.path)
        with self.assertRaises(ValueError):
            registry.register({k: v for k, v in SPEC.items() if k != "rule"} | {"id": "y"}, self.path)
        self.assertEqual(len(registry.load(self.path)), 1)

    def test_tracks(self):
        registry.register(dict(SPEC, id="l", track="learning"), self.path)
        with self.assertRaises(ValueError):
            registry.register(dict(SPEC, id="o", track="other"), self.path)

    def test_result_takes_cost_only_from_invocations_after_registration(self):
        run = ROOT / "work" / f"_registry_test_{self.dir.name}"
        run.mkdir(parents=True)
        try:
            registry.register(dict(SPEC, run_dir=run.relative_to(ROOT).as_posix()), self.path)
            (run / "run_manifest.json").write_text(json.dumps([
                {"started": "2000-01-01 00:00:00", "cost": 9.0, "scoring_version": "old"},   # an earlier experiment
                {"started": "2999-01-01 00:00:00", "cost": 0.42, "scoring_version": "v"}]), encoding="utf-8")
            rec = registry.result("x-test", "+0.05 [0.00, +0.10]", "adopted", heldout="pending", path=self.path)
            self.assertEqual(rec["cost"], 0.42)
            self.assertEqual(rec["run_scoring_version"], "v")
            self.assertEqual(rec["status"], "decided")
        finally:
            for f in run.iterdir():
                f.unlink()
            run.rmdir()

    def test_result_rejects_unknown_id_and_decision(self):
        registry.register(dict(SPEC), self.path)
        with self.assertRaises(ValueError):
            registry.result("nope", "x", "adopted", path=self.path)
        with self.assertRaises(ValueError):
            registry.result("x-test", "x", "maybe", path=self.path)


if __name__ == "__main__":
    unittest.main()
