"""Fixes the agent found become runtime candidates: mined from trajectory logs."""
import json
import pickle
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from r2py.runtime import mine_fixes


def _entity(name, start, end, rhs=None, pkg="base"):
    return SimpleNamespace(name=name, package=pkg, rhs_call_name=rhs, rhs_call_package=pkg if rhs else None,
                           source_span=SimpleNamespace(start_line=start, end_line=end))


SM = SimpleNamespace(source="x <- c(1, 2, 3)\nq <- quantile(x, 0.9)\ny <- 5\n",
                     entities={"e1": _entity("q", 1, 1, rhs="quantile", pkg="stats"), "e2": _entity("y", 2, 2, pkg="")})


def _traj(path: Path, states):
    recs = [{"kind": "run_start", "script": "s__x.R"}]
    for i, (src, per) in enumerate(states):
        recs.append({"kind": "accepted", "source": src, "per_entity": per, "aggregate": 0.5, "step": i})
    path.write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")


class TestMining(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "maps").mkdir()
        (self.d / "maps" / "s__x.pkl").write_bytes(pickle.dumps(SM))

    def tearDown(self):
        self.tmp.cleanup()

    def _fixes(self, states):
        _traj(self.d / "t.jsonl", states)
        return mine_fixes.fixes_from_trajectories([str(self.d / "t.jsonl")], self.d / "maps")

    BEFORE = "# r2py:entity:e1\nq = np.percentile(x, 90, method='nearest')\n# r2py:entity:e2\ny = 5\n"
    AFTER = "# r2py:entity:e1\nq = np.quantile(x, 0.9)\n# r2py:entity:e2\ny = 5\n"

    def test_an_entity_lifted_from_poor_to_good_is_a_fix_with_both_fragments(self):
        fixes = self._fixes([(self.BEFORE, {"e1": 0.2, "e2": 1.0}), (self.AFTER, {"e1": 1.0, "e2": 1.0})])
        self.assertEqual(len(fixes), 1)
        f = fixes[0]
        self.assertEqual((f.package, f.function, f.eid), ("stats", "quantile", "e1"))
        self.assertIn("np.quantile", f.after)
        self.assertIn("nearest", f.before)
        self.assertEqual(f.r_text, "q <- quantile(x, 0.9)")
        self.assertEqual((f.score_before, f.score_after), (0.2, 1.0))

    def test_small_gains_and_unkeyed_entities_are_not_fixes(self):
        self.assertEqual(self._fixes([(self.BEFORE, {"e1": 0.8, "e2": 0.5}), (self.AFTER, {"e1": 1.0, "e2": 1.0})]), [])   # e1 not poor; e2 has no key
        self.assertEqual(self._fixes([(self.BEFORE, {"e1": 0.2}), (self.AFTER, {"e1": 0.5})]), [])                          # not good after

    def test_candidates_skip_known_functions_and_long_fragments(self):
        fixes = self._fixes([(self.BEFORE, {"e1": 0.2}), (self.AFTER, {"e1": 1.0})])
        self.assertEqual(list(mine_fixes.candidates(fixes, set())), ["quantile"])
        self.assertEqual(mine_fixes.candidates(fixes, {"quantile"}), {})
        fixes[0].after = "\n".join(["x = 1"] * 60)
        self.assertEqual(mine_fixes.candidates(fixes, set()), {})

    def test_hint_is_evidence_not_a_specification(self):
        fixes = self._fixes([(self.BEFORE, {"e1": 0.2}), (self.AFTER, {"e1": 1.0})])
        text = mine_fixes.hint(fixes[0])
        self.assertIn("np.quantile(x, 0.9)", text)
        self.assertIn("scored 1.0", text)
        self.assertIn("not as the answer", text)

    def test_missing_script_map_is_skipped(self):
        (self.d / "maps" / "s__x.pkl").unlink()
        self.assertEqual(self._fixes([(self.BEFORE, {"e1": 0.2}), (self.AFTER, {"e1": 1.0})]), [])


if __name__ == "__main__":
    unittest.main()
