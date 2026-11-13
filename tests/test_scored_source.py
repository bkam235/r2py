"""scored_source (2026-11-13): an `accepted` record logs the program as it was scored (the harness's annotated
source, which the chain continues from), next to the raw candidate. Continuations started from the raw candidate
re-verified differently in patience-dsflash (15 of 66 chains)."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import agent, trajectory
from tests import test_entity_repair as _er


class TestScoredSource(unittest.TestCase):

    def test_accepted_record_carries_the_scored_program(self):
        T = _er.TestCrashFirst
        start = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                   aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        better = NS(by_entity={"e1": T.full("e1", True, 1.0)}, crash_entities=[], py_exit_code=0,
                    aggregate=1.0, feedback=[], comparisons=[], uncomparable=[])
        harness = NS(_probe_count=0, last_annotated_source="", _sidecar_filename="", note_reference=lambda s: None)

        def verify(src):   # the harness rewrites the sentinels it attributed, as HarnessTools.verify does
            harness.last_annotated_source = "# r2py:entity:e1\nb = 2  # annotated\n"
            return better
        harness.verify = verify
        sm = NS(source="b <- 2\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles={})
        raw = "# r2py:entity:e1\n# r2py:entity:extra\nb = 2\n"
        with tempfile.TemporaryDirectory() as d, \
             patch.object(agent._llm, "call", return_value=f"ACTION: rewrite\n```python\n{raw}```"), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            path = Path(d) / "t.jsonl"
            trajectory.begin(path)
            try:
                agent.reason("# r2py:entity:e1\nb = 1\n", start, harness, sm, model="openrouter:m", max_steps=3,
                             max_stalls=3, entity_repair=False, converse=True)
            finally:
                trajectory.end()
            acc = [r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r["kind"] == "accepted"]
        self.assertEqual(len(acc), 1)
        self.assertIn("# r2py:entity:extra", acc[0]["source"])          # the raw candidate stays logged
        self.assertEqual(acc[0]["scored_source"], "# r2py:entity:e1\nb = 2  # annotated\n")
        self.assertEqual(trajectory.program(acc[0]), acc[0]["scored_source"])

    def test_program_falls_back_to_the_raw_candidate_in_old_logs(self):
        self.assertEqual(trajectory.program({"kind": "accepted", "source": "x = 1\n"}), "x = 1\n")


if __name__ == "__main__":
    unittest.main()
