"""Stage 7: the search climbs a shaped value on crashing scripts; the official score is untouched."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import agent, objective
from r2py.types import EntityScore, ScoreReport

ALL = frozenset({"type_match", "control_flow_match", "data_output", "variable_output",
                 "callable_output", "side_effects"})


def es(eid, ok, v):
    return EntityScore(entity_id=eid, executed_ok=ok, type_match=v, control_flow_match=v, data_output=v,
                       variable_output=v, callable_output=v, side_effects=v, active_dims=ALL)


def crash(*scored):                      # a crashing run: aggregate forced to 0.0
    return ScoreReport(aggregate=0.0, py_exit_code=1, by_entity={e.entity_id: e for e in scored})


def ran(aggregate, *scored):
    return ScoreReport(aggregate=aggregate, py_exit_code=0, by_entity={e.entity_id: e for e in scored})


class TestKey(unittest.TestCase):
    def test_a_candidate_that_runs_always_beats_one_that_crashes(self):
        self.assertTrue(objective.better(ran(0.1), crash(es("a", True, 1.0), es("b", True, 1.0))))
        self.assertFalse(objective.better(crash(es("a", True, 1.0), es("b", True, 1.0)), ran(0.1)))

    def test_getting_further_or_scoring_better_before_the_crash_is_progress(self):
        base = crash(es("a", True, 1.0), es("b", False, 0.0), es("c", False, 0.0))
        further = crash(es("a", True, 1.0), es("b", True, 0.5), es("c", False, 0.0))
        better_before = crash(es("a", True, 1.0), es("b", False, 0.0), es("c", False, 0.0))
        self.assertTrue(objective.better(further, base))
        self.assertFalse(objective.better(better_before, base))          # identical: not progress
        self.assertFalse(objective.better(base, further))

    def test_no_per_entity_table_means_no_gradient(self):
        self.assertEqual(objective.search_key(ScoreReport(aggregate=0.0, py_exit_code=1)), (0, 0.0))

    def test_among_runnable_candidates_the_official_score_decides(self):
        self.assertTrue(objective.better(ran(0.6), ran(0.5)))
        self.assertFalse(objective.better(ran(0.5), ran(0.5)))


class TestLoop(unittest.TestCase):
    def run_loop(self, start, candidates):
        it = iter(candidates)
        harness = NS(verify=lambda src: next(it), _probe_count=0, last_annotated_source="", _sidecar_filename="")
        sm = NS(source="x <- 1\n", entities={}, entity_bundles={})
        with patch.object(agent._llm, "call", return_value="ACTION: rewrite\n```python\nx = 1\n```"), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")) as review:
            out = agent.reason("x = 0\n", start, harness, sm, model="openrouter:m", max_steps=6, max_stalls=3)
        agent.drain_agent_stats()
        return out, review

    def test_progress_on_a_crashing_script_is_accepted_and_reaches_a_running_one(self):
        start = crash(es("a", True, 1.0), es("b", False, 0.0))
        further = crash(es("a", True, 1.0), es("b", True, 0.3))          # still crashes, gets further
        done = ran(0.95, es("a", True, 1.0), es("b", True, 0.9))
        out, review = self.run_loop(start, [further, done])
        self.assertIsNotNone(out)
        self.assertEqual(out[1].aggregate, 0.95)
        self.assertEqual(review.call_count, 1)        # the review judged only the candidate that runs

    def test_returned_report_is_the_best_report_even_after_rejections(self):
        start = crash(es("a", True, 1.0), es("b", False, 0.0))
        worse = crash(es("a", False, 0.0), es("b", False, 0.0))
        out, _ = self.run_loop(start, [worse, worse, worse])
        self.assertIsNone(out)                         # nothing better was found
