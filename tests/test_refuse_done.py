"""refuse_done (2026-11-06): below the threshold a "done" counts as a failed step; every "done" is logged."""
import json
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import agent, trajectory
from tests import test_entity_repair as _er


class TestRefuseDone(unittest.TestCase):

    def run_loop(self, tmp, **kw):
        T = _er.TestCrashFirst
        rep = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        sent = []

        def call(messages, system, **kw):
            sent.append(messages[-1]["content"])
            if len(sent) == 1:
                return 'The score is fine.\n{"action": "done"}'
            return f"ACTION: rewrite\n```python\n# r2py:entity:e1\nb = {len(sent) + 1}\n```"
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        sm = NS(source="b <- 1\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles={})
        path = f"{tmp}/t.jsonl"
        trajectory.begin(path)
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason("# r2py:entity:e1\nb = 1\n", rep, harness, sm, model="openrouter:m", max_steps=10,
                         max_stalls=3, entity_repair=False, converse=True, **kw)
        trajectory.end()
        recs = [json.loads(l) for l in open(path, encoding="utf-8")]
        return agent.drain_agent_stats(), sent, [r for r in recs if r["kind"] == "done"]

    def test_done_below_the_threshold_is_refused_and_counts_as_a_stall(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            stats, sent, dones = self.run_loop(tmp, refuse_done=True)
        self.assertEqual(stats["outcome"].get("done_refused"), 1)
        self.assertNotIn("done", stats["stop"])
        self.assertEqual(len(sent), 3)                       # the refusal and two failed rewrites: 3 stalls
        self.assertIn("done refused", sent[1])               # the next turn says why the chain goes on
        self.assertEqual(len(dones), 1)
        self.assertTrue(dones[0]["refused"])
        self.assertIn("The score is fine.", dones[0]["raw"])

    def test_off_by_default_the_chain_stops_and_the_reason_is_logged(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            stats, sent, dones = self.run_loop(tmp)
        self.assertEqual(stats["stop"].get("done"), 1)
        self.assertEqual(len(sent), 1)
        self.assertEqual(len(dones), 1)
        self.assertFalse(dones[0]["refused"])
        self.assertIn("The score is fine.", dones[0]["raw"])


if __name__ == "__main__":
    unittest.main()
