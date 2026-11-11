"""literal_check (2026-11-11): numeric literals a candidate adds that equal R's recorded values."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import agent
from r2py.harness import literal_check as lc
from tests import test_entity_repair as _er

SM = NS(source="x <- convert(spectrum)\n",
        entity_bundles={"x": NS(stdout="[1,] 53.24080  78.60861\n", data={"y": "[61.96368, -41.9387857375941]"})})
TRUTH = lc.truth_numbers(SM)


class TestPasted(unittest.TestCase):

    def test_new_code_literals_equal_to_r_values_are_found_at_their_precision(self):
        self.assertEqual(lc.pasted("a = [53.24080, 78.6086, -41.94, 61.96368]\n", "", SM.source, TRUTH),
                         ["53.24080", "78.6086", "-41.94", "61.96368"])

    def test_strings_comments_short_and_known_literals_do_not_count(self):
        src = "s = 'path 53.24080'  # 78.60861\nb = 61.9\nc = 0.0031308\nd = 41.9387857375941\n"
        self.assertEqual(lc.pasted(src, "d = 41.9387857375941\n", SM.source, TRUTH), [])

    def test_check_rejects_from_three(self):
        self.assertIsNone(lc.check("a = [53.24080, 78.60861]\n", "", SM.source, SM))
        self.assertIn("3 numeric literals", lc.check("a = [53.24080, 78.60861, 61.96368]\n", "", SM.source, SM))


class TestGate(unittest.TestCase):

    def run_loop(self, **kw):
        T = _er.TestCrashFirst
        low = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        high = NS(by_entity={"e1": T.full("e1", True, 1.0)}, crash_entities=[], py_exit_code=0,
                  aggregate=1.0, feedback=[], comparisons=[], uncomparable=[])
        pasted_src = "# r2py:entity:e1\nb = [53.24080, 78.60861, 61.96368]\n"
        reviews = []
        harness = NS(verify=lambda src: high if "53.24080" in src else low, _probe_count=0,
                     last_annotated_source="", _sidecar_filename="", note_reference=lambda src: None)
        sm = NS(source=SM.source, entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles=SM.entity_bundles)
        with patch.object(agent._llm, "call", return_value=f"ACTION: rewrite\n```python\n{pasted_src}```"), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", side_effect=lambda *a, **k: reviews.append(1) or (True, "")):
            out = agent.reason("# r2py:entity:e1\nb = 1\n", low, harness, sm, model="openrouter:m", max_steps=2,
                               max_stalls=3, entity_repair=False, converse=True, **kw)
        return out, agent.drain_agent_stats(), reviews

    def test_off_by_default_the_pasted_candidate_is_reviewed_and_kept(self):
        out, _, reviews = self.run_loop()
        self.assertIsNotNone(out)
        self.assertEqual(len(reviews), 1)

    def test_on_the_pasted_candidate_is_rejected_without_a_review_call(self):
        out, stats, reviews = self.run_loop(literal_check=True)
        self.assertIsNone(out)
        self.assertEqual(reviews, [])
        self.assertEqual(stats["outcome"].get("literal_check_rejected"), 2)


if __name__ == "__main__":
    unittest.main()
