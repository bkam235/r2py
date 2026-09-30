"""Harness-driven single-entity repair: which entity is picked, and what it is asked."""
import unittest
from types import SimpleNamespace as NS

from r2py.harness import agent, prompt

SRC = ("import os\n# r2py:entity:e1\na = 1\n# r2py:entity:e2\nb = a +\\n  1\n"
       "# r2py:entity:e3\nc = 3\n# r2py:entity:e1\nd = 4\n")


def es(ok=True, score=1.0, dims=("d",)):
    return NS(executed_ok=ok, active_dims=frozenset(dims), **{d: score for d in dims})


class TestPick(unittest.TestCase):
    def report(self, **by):
        return NS(by_entity=by)

    def test_first_crashed_entity_wins_over_a_lower_score(self):
        r = self.report(e2=es(ok=False), e3=es(score=0.1))
        self.assertEqual(agent._pick_repair_entity(r, SRC, {}), "e2")

    def test_lowest_scoring_otherwise(self):
        r = self.report(e2=es(score=0.5), e3=es(score=0.2))
        self.assertEqual(agent._pick_repair_entity(r, SRC, {}), "e3")

    def test_skips_good_vacuous_multi_span_and_exhausted_entities(self):
        r = self.report(e1=es(score=0.0),                       # two spans in SRC -> not spliceable
                        e2=es(score=0.95),                      # good enough
                        e3=es(score=0.1, dims=()),              # nothing to verify
                        e4=es(score=0.0))                       # not in the source
        self.assertIsNone(agent._pick_repair_entity(r, SRC, {}))
        self.assertIsNone(agent._pick_repair_entity(self.report(e3=es(score=0.0)), SRC, {"e3": 2}))


class TestPrompt(unittest.TestCase):
    def test_turn_names_the_entity_and_carries_its_feedback_and_history(self):
        c = NS(entity_id="e3", effect_class=NS(value="data"), score=0.0, r_value="3", py_value="4",
               diff_summary="c differs")
        other = NS(entity_id="e2", effect_class=NS(value="data"), score=0.0, r_value="x", py_value="y",
                   diff_summary="")
        rep = NS(by_entity={"e3": es(score=0.0)}, comparisons=[c, other], feedback=[], py_exit_code=0)
        msgs = prompt.build_entity_repair_turn("c <- 3", SRC, rep, "e3", "c", "c <- 3", "c = 4",
                                               ["aggregate went 0.5 -> 0.4"])
        text = msgs[0]["content"]
        self.assertIn("e3", text)
        self.assertIn("c differs", text)
        self.assertNotIn("R produced:      x", text)          # the other entity's comparison stays out
        self.assertIn("aggregate went 0.5 -> 0.4", text)
        self.assertIn("ACTION: replace_entity", prompt.ENTITY_REPAIR_SYSTEM)


if __name__ == "__main__":
    unittest.main()
