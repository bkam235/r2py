"""Stage 9a-b: trajectory log and verification cache."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import agent, tools, trajectory


class TestTrajectory(unittest.TestCase):
    def test_noop_without_begin_and_jsonl_with_it(self):
        trajectory.log("step", x=1)                      # no file: must not raise
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sub" / "r.jsonl"
            trajectory.begin(p, script="a.R")
            trajectory.log("seed", label="Bare 1", source="x = 1\n", aggregate=0.5)
            trajectory.end(final_score=0.7)
            recs = trajectory.read(p)
        self.assertEqual([r["kind"] for r in recs], ["run_start", "seed", "run_end"])
        self.assertEqual((recs[0]["script"], recs[1]["source"], recs[2]["final_score"]), ("a.R", "x = 1\n", 0.7))
        self.assertTrue(all("t" in r for r in recs))

    def test_agent_outcomes_carry_the_step_context(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.jsonl"
            trajectory.begin(p)
            agent._ctx.clear()
            agent._ctx.update(step=3, action="rewrite", source="y = 2\n", aggregate=0.0)
            agent._stat("outcome", "rewrite:catastrophic")
            agent._stat("action", "rewrite")             # not an outcome: not logged
            trajectory.end()
            recs = [r for r in trajectory.read(p) if r["kind"] == "step"]
        self.assertEqual(len(recs), 1)
        self.assertEqual((recs[0]["outcome"], recs[0]["step"], recs[0]["source"]),
                         ("rewrite:catastrophic", 3, "y = 2\n"))
        agent.drain_agent_stats()


class TestVerifyCache(unittest.TestCase):
    def test_identical_source_is_verified_once_and_restores_the_annotated_source(self):
        ht = tools.HarnessTools.__new__(tools.HarnessTools)
        ht._script_map, ht._model, ht._data_compare = NS(entities={}, source=""), "m", "auto"
        ht._sidecar_filename, ht._timeout_s, ht._verify_kwargs = "", 5, {}
        ht._verify_cache, ht.last_annotated_source, ht._mapped_eids = {}, "", set()
        tools.drain_cache_stats()
        from r2py.stage2 import sentinel_mapper as sm
        from r2py.stage4 import verifier
        with patch.object(sm, "map_entities_to_lines", return_value={}) as mapper, \
             patch.object(verifier, "verify", return_value="REPORT") as v:
            self.assertEqual(ht.verify("x = 1\n"), "REPORT")
            ht.last_annotated_source = "changed"
            self.assertEqual(ht.verify("# r2py:entity:e1\nx = 1\n"), "REPORT")   # same code, sentinels differ
            self.assertEqual(ht.last_annotated_source, "x = 1")
            ht.verify("x = 2\n")
        self.assertEqual((mapper.call_count, v.call_count), (2, 2))
        stats = tools.drain_cache_stats()
        self.assertEqual((stats["miss"], stats["hit"]), (2, 1))


if __name__ == "__main__":
    unittest.main()
