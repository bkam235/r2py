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


class TestCrashTargeting(unittest.TestCase):
    def test_the_entity_named_by_the_traceback_is_targeted_before_any_guess(self):
        r = NS(by_entity={"e2": es(ok=False), "e3": es(ok=False, score=0.0)}, crash_entities=["e3", "e2"])
        self.assertEqual(agent._pick_repair_entity(r, SRC, {}), "e3")           # not the earliest unexecuted one
        self.assertEqual(agent._pick_repair_entity(r, SRC, {"e3": 2}), "e2")   # next frame once e3 is exhausted
        self.assertEqual(agent._pick_repair_entity(r, SRC, {"e3": 2, "e2": 2}), None)

    def test_without_crash_attribution_the_old_rule_applies(self):
        r = NS(by_entity={"e2": es(ok=False), "e3": es(score=0.1)}, crash_entities=[])
        self.assertEqual(agent._pick_repair_entity(r, SRC, {}), "e2")


class TestRejectionNotes(unittest.TestCase):
    def test_only_entity_repairs_collect_notes(self):
        notes = {}
        agent._note_rejection(notes, "entity_repair", {"entity": "e3"}, "imported x")
        agent._note_rejection(notes, "rewrite", {}, "ignored")
        agent._note_rejection(notes, "entity_repair", {"entity": "e3"}, "syntax error: line 2")
        self.assertEqual(notes, {"e3": ["imported x", "syntax error: line 2"]})


class TestSpliceIndent(unittest.TestCase):
    def test_fragment_takes_the_indentation_of_the_code_it_replaces(self):
        from r2py.stage2.stitch import splice_entity
        # insert_sentinels writes sentinels at column 0 even inside a block
        src = "def f():\n# r2py:entity:e1\n    a = 1\n    b = 2\n# r2py:entity:e2\n    c = 3\n"
        out, err = splice_entity(src, "e1", "a = 10\nif a:\n    b = 20")
        self.assertEqual(err, "")
        self.assertEqual(out, "def f():\n# r2py:entity:e1\n    a = 10\n    if a:\n        b = 20\n# r2py:entity:e2\n    c = 3\n")
        import ast
        ast.parse(out)

    def test_module_level_entities_are_untouched_by_the_reindent(self):
        from r2py.stage2.stitch import splice_entity
        out, _ = splice_entity("# r2py:entity:e1\na = 1\n", "e1", "a = 2\n")
        self.assertEqual(out, "# r2py:entity:e1\na = 2\n")


class TestCrashFirst(unittest.TestCase):
    """While the program crashes, every step targets the crash (2026-10-11): an upstream crash nullifies any
    fix after it - in the prompt-load runs all 137 adopted-but-no-gain fixes were in crashing programs."""

    SRC = "# r2py:entity:e1\na = 1\n# r2py:entity:e2\nb = a + q\n# r2py:entity:e3\nc = b\n"

    @staticmethod
    def full(eid, ok=True, v=1.0):
        from r2py.types import EntityScore
        return EntityScore(entity_id=eid, executed_ok=ok, type_match=v, control_flow_match=v, data_output=v,
                           variable_output=v, callable_output=v, side_effects=v,
                           active_dims=frozenset({"data_output"}))

    def crashing(self, culprits=("e2",)):
        from r2py.types import FeedbackItem, EffectClass
        fb = [FeedbackItem(entity_id="e2", effect_class=EffectClass.SYNTAX, score=0.0,
                           message="R succeeded but Python crashed (exit 1). NameError: name 'q' is not defined")]
        return NS(by_entity={"e1": self.full("e1"), "e2": self.full("e2", False, 0.0),
                             "e3": self.full("e3", False, 0.0)}, crash_entities=list(culprits),
                  py_exit_code=1, aggregate=0.0, feedback=fb, comparisons=[], uncomparable=[])

    def test_the_traceback_culprit_is_picked(self):
        self.assertEqual(agent._pick_crash_entity(self.crashing(), self.SRC, {}), "e2")

    def test_a_culprit_that_cannot_be_replaced_as_one_block_gives_no_target(self):
        src = self.SRC.replace("# r2py:entity:e2\n", "")              # culprit lost its marker
        self.assertIsNone(agent._pick_crash_entity(self.crashing(), src, {}))
        self.assertIsNone(agent._pick_crash_entity(self.crashing(), self.SRC, {"e2": 2}))

    def test_without_attribution_the_first_entity_that_did_not_run_is_picked(self):
        self.assertEqual(agent._pick_crash_entity(self.crashing(culprits=()), self.SRC, {}), "e2")

    def test_the_crash_note_names_the_culprit_and_the_error(self):
        note = agent._crash_first_note(self.crashing())
        self.assertIn("`e2`", note)
        self.assertIn("NameError", note)

    def first_turn(self, report, source, **kw):
        return self.turns(report, source, max_steps=1, **{"crash_first": "on", **kw})[0]

    def turns(self, report, source, max_steps=1, **kw):
        from unittest.mock import patch
        sent = []

        def call(messages, system, **kw):
            sent.append((system, messages[-1]["content"]))
            return "ACTION: rewrite\n```python\nb = 1\n```"
        harness = NS(verify=lambda src: report, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        ent = NS(source_span=NS(start_line=1, end_line=1), name="b")
        sm = NS(source="a <- 1\nb <- a + 1\nc <- b\n", entities={"e1": ent, "e2": ent, "e3": ent},
                entity_bundles={})
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason(source, report, harness, sm, model="openrouter:m", max_steps=max_steps, entity_repair=False,
                         **kw)
        agent.drain_agent_stats()
        return sent

    def test_a_crashing_program_gets_an_entity_repair_of_the_culprit_even_with_entity_repair_off(self):
        system, user = self.first_turn(self.crashing(), self.SRC)
        self.assertEqual(system, prompt.ENTITY_REPAIR_SYSTEM)
        self.assertIn("Repair entity `e2`", user)

    def test_an_untargetable_culprit_gets_a_full_rewrite_told_to_fix_the_crash_first(self):
        src = self.SRC.replace("# r2py:entity:e2\n", "")
        system, user = self.first_turn(self.crashing(), src)
        self.assertNotEqual(system, prompt.ENTITY_REPAIR_SYSTEM)
        self.assertIn("Fix the crash first", user)

    def test_a_program_that_runs_is_left_to_the_policy(self):
        rep = NS(by_entity={"e1": self.full("e1"), "e2": self.full("e2", True, 0.5), "e3": self.full("e3")},
                 crash_entities=[], py_exit_code=0,
                 aggregate=0.8, feedback=[], comparisons=[], uncomparable=[])
        system, user = self.first_turn(rep, self.SRC)
        self.assertNotEqual(system, prompt.ENTITY_REPAIR_SYSTEM)
        self.assertNotIn("Fix the crash first", user)


class TestSystemOverride(unittest.TestCase):
    def test_a_given_system_prompt_replaces_the_built_one(self):
        from unittest.mock import patch
        sent = []

        def call(messages, system, **kw):
            sent.append(system)
            return "ACTION: rewrite\n```python\nb = 1\n```"
        rep = NS(by_entity={"e1": TestCrashFirst.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        ent = NS(source_span=NS(start_line=0, end_line=0), name="b")
        sm = NS(source="b <- 1\n", entities={"e1": ent}, entity_bundles={})
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason("# r2py:entity:e1\nb = 2\n", rep, harness, sm, model="openrouter:m", max_steps=1,
                         system_override="MINIMAL PROMPT")
        agent.drain_agent_stats()
        self.assertEqual(sent[0], "MINIMAL PROMPT")


class TestCrashModes(unittest.TestCase):
    """crash_first: "off" (default again after Part B, 2026-10-16), "on", "fallback"."""
    T = TestCrashFirst()

    def test_off_is_a_plain_full_rewrite(self):
        sent = self.T.turns(self.T.crashing(), self.T.SRC, max_steps=1)
        self.assertNotEqual(sent[0][0], prompt.ENTITY_REPAIR_SYSTEM)
        self.assertNotIn("Fix the crash first", sent[0][1])

    def test_fallback_rewrites_first_and_targets_the_culprit_after_a_rewrite_failed(self):
        sent = self.T.turns(self.T.crashing(), self.T.SRC, max_steps=2, crash_first="fallback")
        self.assertNotEqual(sent[0][0], prompt.ENTITY_REPAIR_SYSTEM)
        self.assertNotIn("Fix the crash first", sent[0][1])
        self.assertEqual(sent[1][0], prompt.ENTITY_REPAIR_SYSTEM)
        self.assertIn("Repair entity `e2`", sent[1][1])


class TestGuidedStep(unittest.TestCase):
    def running(self):
        T = TestCrashFirst
        return NS(by_entity={"e1": T.full("e1"), "e2": T.full("e2", True, 0.5), "e3": T.full("e3")},
                  crash_entities=[], py_exit_code=0, aggregate=0.8, feedback=[], comparisons=[], uncomparable=[])

    def sm(self):
        ent = NS(source_span=NS(start_line=1, end_line=1), name="b")
        bundles = {"e2": NS(stdout="[1] 2", data={"b": [2]})}
        return NS(source="a <- 1\nb <- a + 1\nc <- b\n", entities={"e1": ent, "e2": ent, "e3": ent},
                  entity_bundles=bundles)

    def test_the_target_is_the_worst_entity_that_ran_with_its_r_values(self):
        eid, text = agent._guided_target(self.running(), self.sm(), {})
        self.assertEqual(eid, "e2")
        self.assertIn('b = [2]', text)

    def test_no_target_once_an_entity_has_had_its_tries(self):
        self.assertIsNone(agent._guided_target(self.running(), self.sm(), {"e2": 2}))

    def test_a_guided_step_samples_k_answers_with_the_guidance_last(self):
        from unittest.mock import patch
        sent = []

        def call(messages, system, **kw):
            sent.append(messages[-1]["content"])
            return "ACTION: rewrite\n```python\n# r2py:entity:e1\na = 1\n# r2py:entity:e2\nb = 2\n```"
        rep = self.running()
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason(TestCrashFirst.SRC, rep, harness, self.sm(), model="openrouter:m", max_steps=1,
                         entity_repair=False, guided_k=3)
        agent.drain_agent_stats()
        self.assertEqual(len(sent), 3)
        self.assertTrue(all("What R computes for entity `e2`" in t for t in sent))


class TestStructuredGuidance(unittest.TestCase):
    def test_value_differences_and_print_lines_are_shown_not_the_whole_value(self):
        T = TestCrashFirst
        fb = [NS(entity_id="e2", effect_class=NS(value="data"), message="info.abbreviation[0]: 'EST' != 'UTC'"),
              NS(entity_id="e1", effect_class=NS(value="data"), message="other entity")]
        rep = NS(by_entity={"e1": T.full("e1"), "e2": T.full("e2", True, 0.5)}, feedback=fb,
                 py_entity_bundles={"e2": NS(stdout="a\nB\n")})
        sm = NS(entity_bundles={"e2": NS(stdout="a\nb\n", data={"info": list(range(5000))})})
        eid, text = agent._guided_target_structured(rep, sm, {})
        self.assertEqual(eid, "e2")
        self.assertIn("'EST' != 'UTC'", text)
        self.assertIn("R prints: 'b' | yours: 'B'", text)
        self.assertNotIn("other entity", text)
        self.assertLess(len(text), 1000)                     # a 5000-element value reduces to its differences


class TestSampledStep(unittest.TestCase):
    """3 per step (2026-10-17): k unguided rewrites of one turn; the review goes down the improving drafts."""

    @staticmethod
    def rep(agg, code=0):
        return NS(aggregate=agg, py_exit_code=code, by_entity={})

    def widen(self, rejected, first="x = 1"):
        from unittest.mock import patch
        from itertools import count
        drafts, n = iter(["x = 2", "x = 3"]), count()
        reviewed = []

        def call(messages, system, **kw):
            next(n)
            return f"ACTION: rewrite\n```python\n{next(drafts)}\n```"

        def review(src):
            reviewed.append(src.strip())
            return (src.strip() not in rejected, "pasted" if src.strip() in rejected else "")
        harness = NS(verify=lambda src: self.rep(0.3 * int(src.strip()[-1])))
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "unavailable_imports", return_value=[]):
            out = agent._widen_rewrite({"action": "rewrite", "new_source": first}, [], "", "m", 3, "", harness,
                                       report=self.rep(0.5), review=review)
        agent.drain_agent_stats()
        return out, reviewed

    def test_a_rejected_best_draft_falls_back_to_the_next_improving_one(self):
        out, reviewed = self.widen(rejected={"x = 3"})
        self.assertEqual(out["new_source"].strip(), "x = 2")
        self.assertEqual(out["reviewed"], (True, ""))
        self.assertEqual(reviewed, ["x = 3", "x = 2"])         # best first; x = 1 does not improve, never reviewed

    def test_all_improving_drafts_rejected_keeps_the_best_with_its_verdict(self):
        out, reviewed = self.widen(rejected={"x = 3", "x = 2"})
        self.assertEqual(out["new_source"].strip(), "x = 3")
        self.assertEqual(out["reviewed"], (False, "pasted"))

    def test_off_samples_k_unguided_answers(self):
        from unittest.mock import patch
        sent = []
        G = TestGuidedStep()

        def call(messages, system, **kw):
            sent.append(messages[-1]["content"])
            return "ACTION: rewrite\n```python\n# r2py:entity:e1\na = 1\n# r2py:entity:e2\nb = 2\n```"
        rep = G.running()
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason(TestCrashFirst.SRC, rep, harness, G.sm(), model="openrouter:m", max_steps=1,
                         entity_repair=False, guided_k=3, guided_mode="off")
        agent.drain_agent_stats()
        self.assertEqual(len(sent), 3)
        self.assertFalse(any("What R computes" in t for t in sent))


class TestAcceptEqual(unittest.TestCase):
    """accept_equal (2026-10-18): an equal-scoring, different running candidate becomes the current program."""

    def run_loop(self, accept_equal):
        from unittest.mock import patch
        T = TestCrashFirst
        rep = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        sent = []

        def call(messages, system, **kw):
            sent.append(messages[-1]["content"])
            return f"ACTION: rewrite\n```python\n# r2py:entity:e1\nb = {len(sent) + 1}\n```"
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        sm = NS(source="b <- 1\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles={})
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason("# r2py:entity:e1\nb = 1\n", rep, harness, sm, model="openrouter:m", max_steps=5,
                         max_stalls=3, entity_repair=False, accept_equal=accept_equal)
        return agent.drain_agent_stats()["outcome"], sent

    def test_equal_moves_are_taken_but_still_count_as_stalls(self):
        outcome, sent = self.run_loop(True)
        self.assertEqual(outcome.get("rewrite:equal_move"), 3)
        self.assertEqual(len(sent), 3)                       # three stalls stop the loop, as without the option
        self.assertIn("b = 2", sent[1])                     # step 2 starts from step 1's program

    def test_off_by_default(self):
        outcome, sent = self.run_loop(False)
        self.assertNotIn("rewrite:equal_move", outcome)
        self.assertNotIn("b = 2", sent[1])


class TestCrashStalls(unittest.TestCase):
    """crash_stalls (2026-10-18): 5 failed steps in a row before stopping while the best program crashes."""

    def steps(self, report, **kw):
        sent = TestCrashFirst().turns(report, TestCrashFirst.SRC, max_steps=10, **kw)
        return len(sent)

    def test_a_crashing_program_gets_more_patience_and_a_running_one_does_not(self):
        T = TestCrashFirst()
        crashing = T.crashing()
        running = NS(by_entity={"e1": T.full("e1"), "e2": T.full("e2", True, 0.5), "e3": T.full("e3")},
                     crash_entities=[], py_exit_code=0, aggregate=0.8, feedback=[], comparisons=[], uncomparable=[])
        self.assertEqual(self.steps(crashing, max_stalls=3), 3)
        self.assertEqual(self.steps(crashing, max_stalls=3, crash_stalls=5), 5)
        self.assertEqual(self.steps(running, max_stalls=3, crash_stalls=5), 3)
