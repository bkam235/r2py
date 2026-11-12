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

    def test_check_rejects_a_single_pasted_value(self):
        self.assertIsNone(lc.check("a = 1\n", "", SM.source, SM))
        self.assertIn("1 numeric literal equal", lc.check("a = 53.24080\n", "", SM.source, SM))

    def test_trailing_zeros_carry_no_significance(self):
        sm = NS(source="", entity_bundles={"x": NS(stdout="100.00000 12.50000", data={})})
        self.assertEqual(lc.pasted("a = 100.00000\nb = 12.50000\n", "", "", lc.truth_numbers(sm)), [])


class TestGate(unittest.TestCase):

    def run_loop(self, pasted_src="# r2py:entity:e1\nb = 53.24080\n", verdict=(True, ""), exit_code=0, **kw):
        T = _er.TestCrashFirst
        low = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=exit_code,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        high = NS(by_entity={"e1": T.full("e1", True, 1.0)}, crash_entities=[], py_exit_code=exit_code,
                  aggregate=1.0, feedback=[], comparisons=[], uncomparable=[])
        reviews = []
        harness = NS(verify=lambda src: high if src.strip() != "# r2py:entity:e1\nb = 1" else low, _probe_count=0,
                     last_annotated_source="", _sidecar_filename="", note_reference=lambda src: None)
        sm = NS(source=SM.source, entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles=SM.entity_bundles)
        with patch.object(agent._llm, "call", return_value=f"ACTION: rewrite\n```python\n{pasted_src}```"), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", side_effect=lambda *a, **k: reviews.append(1) or verdict):
            out = agent.reason("# r2py:entity:e1\nb = 1\n", low, harness, sm, model="openrouter:m", max_steps=2,
                               max_stalls=3, entity_repair=False, converse=True, **kw)
        return out, agent.drain_agent_stats(), reviews

    def test_off_by_default_the_pasted_candidate_is_reviewed_and_kept(self):
        out, _, reviews = self.run_loop()
        self.assertIsNotNone(out)
        self.assertEqual(len(reviews), 1)

    def test_on_the_pasted_candidate_is_rejected_and_still_reviewed(self):
        out, stats, reviews = self.run_loop(literal_check=True)
        self.assertIsNone(out)
        self.assertEqual(len(reviews), 2)                      # the review runs on every running candidate
        self.assertEqual(stats["outcome"].get("literal_check_rejected"), 2)
        self.assertEqual(stats["literal_check"].get("review_passed"), 2)

    def test_on_a_clean_candidate_is_reviewed_and_the_review_can_still_reject_it(self):
        out, stats, reviews = self.run_loop(literal_check=True, pasted_src="# r2py:entity:e1\nb = compute()\n",
                                            verdict=(False, "hardcoded"))
        self.assertIsNone(out)
        self.assertEqual(len(reviews), 2)
        self.assertNotIn("literal_check_rejected", stats["outcome"])

    def test_a_crashing_candidate_is_unreviewed_by_default(self):
        out, _, reviews = self.run_loop(literal_check=True, exit_code=1)
        self.assertIsNotNone(out)                              # adopted as a stepping stone, unreviewed
        self.assertEqual(reviews, [])

    def test_review_crashing_judges_a_crashing_candidate_with_both_gates(self):
        out, stats, reviews = self.run_loop(literal_check=True, review_crashing=True, exit_code=1)
        self.assertIsNone(out)
        self.assertEqual(len(reviews), 2)
        self.assertEqual(stats["outcome"].get("literal_check_rejected"), 2)


if __name__ == "__main__":
    unittest.main()
