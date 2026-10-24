"""Scoring epochs (2026-10-24): what the scorer regression check counts as a change."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from scoring_epoch import compare   # noqa: E402

from r2py import scoring             # noqa: E402


def run(agg, ents, exit_code=0):
    return {"aggregate": agg, "exit": exit_code, "entities": ents}


class TestCompare(unittest.TestCase):
    BASE = {
        "a": {"runs": [run(0.5, {"x": 0.5}), run(0.5, {"x": 0.5})], "flaky": False},
        "b": {"runs": [run(0.5, {"x": 0.5}), run(0.5, {"x": 0.5})], "flaky": False},
        "c": {"runs": [run(0.4, {"x": 0.4}), run(0.6, {"x": 0.6})], "flaky": True},
        "d": {"runs": [run(0.4, {"x": 0.4}), run(0.6, {"x": 0.6})], "flaky": True},
    }

    def test_unchanged_changed_and_flaky(self):
        new = {"a": dict(run(0.5, {"x": 0.5}), id="a"),
               "b": dict(run(0.5, {"x": 0.9, "y": 0.1}), id="b"),      # same aggregate, entities moved
               "c": dict(run(0.55, {"x": 0.55}), id="c"),               # flaky, inside its range
               "d": dict(run(0.9, {"x": 0.9}, exit_code=1), id="d")}    # flaky, outside its range
        out = compare(self.BASE, new)
        self.assertEqual(out["unchanged"], ["a"])
        self.assertEqual(out["flaky_in_range"], ["c"])
        self.assertEqual(sorted(c["id"] for c in out["changed"]), ["b", "d"])
        b = next(c for c in out["changed"] if c["id"] == "b")
        self.assertEqual(b["entities"], {"x": (0.5, 0.9), "y": (None, 0.1)})

    def test_a_move_within_verification_noise_is_small_not_changed(self):
        out = compare({"a": self.BASE["a"]}, {"a": dict(run(0.502, {"x": 0.51}), id="a")})
        self.assertEqual([c["id"] for c in out["small"]], ["a"])
        self.assertEqual(out["changed"], [])
        out = compare({"a": self.BASE["a"]}, {"a": dict(run(0.502, {"x": 0.6}), id="a")})   # one entity moved a lot
        self.assertEqual([c["id"] for c in out["changed"]], ["a"])

    def test_an_error_is_reported_not_counted_as_unchanged(self):
        out = compare({"a": self.BASE["a"]}, {"a": {"id": "a", "error": "boom"}})
        self.assertEqual(out["error"], [{"id": "a", "detail": "boom"}])


class TestScoringVersion(unittest.TestCase):
    def test_agent_code_is_outside_the_scorer(self):
        files = {p.relative_to(scoring.ROOT).as_posix() for p in scoring._files(scoring.SCORER_PATHS)}
        self.assertIn("r2py/stage4/verifier.py", files)
        self.assertIn("r2py/stage1/runner.py", files)
        self.assertNotIn("r2py/harness/agent.py", files)
        self.assertNotIn("r2py/harness/prompt.py", files)

    def test_line_endings_do_not_change_the_hash(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            a.mkdir(); b.mkdir()
            (a / "x.py").write_bytes(b"x = 1\ny = 2\n")
            (b / "x.py").write_bytes(b"x = 1\r\ny = 2\r\n")
            old = scoring.ROOT
            try:
                scoring.ROOT = a
                ha = scoring._hash([a / "x.py"])
                scoring.ROOT = b
                hb = scoring._hash([b / "x.py"])
            finally:
                scoring.ROOT = old
        self.assertEqual(ha, hb)


if __name__ == "__main__":
    unittest.main()
