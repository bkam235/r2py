"""agent_model (2026-11-08): the translating agent on another model; the review keeps its own model and provider."""
import unittest
from collections import Counter
from types import SimpleNamespace as NS
from unittest.mock import MagicMock, patch

from r2py import heldout as ho
from r2py.harness import agent
from tests import test_entity_repair as _er


class TestReviewModel(unittest.TestCase):

    def run_loop(self, **kw):
        T = _er.TestCrashFirst
        start = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                   aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        better = NS(by_entity={"e1": T.full("e1", True, 1.0)}, crash_entities=[], py_exit_code=0,
                    aggregate=1.0, feedback=[], comparisons=[], uncomparable=[])
        agent_models, review_models = [], []
        self.limits = []

        def call(messages, system, **ckw):
            agent_models.append(ckw["model"])
            self.limits.append(ckw["max_tokens"])
            return "ACTION: rewrite\n```python\n# r2py:entity:e1\nb = 2\n```"

        def review(r_source, py_source, script_map, **rkw):
            review_models.append(rkw["model"])
            return True, ""
        harness = NS(verify=lambda src: better, _probe_count=0, last_annotated_source="", _sidecar_filename="",
                     note_reference=lambda src: None)
        sm = NS(source="b <- 1\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles={})
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", side_effect=review):
            agent.reason("# r2py:entity:e1\nb = 1\n", start, harness, sm, model="openrouter:agent", max_steps=3,
                         max_stalls=3, entity_repair=False, converse=True, **kw)
        agent.drain_agent_stats()
        return agent_models, review_models

    def test_review_uses_review_model_and_the_agent_its_own(self):
        agent_models, review_models = self.run_loop(review_model="openrouter:judge")
        self.assertEqual(set(agent_models), {"openrouter:agent"})
        self.assertEqual(review_models, ["openrouter:judge"])

    def test_by_default_the_review_uses_the_agent_model(self):
        _, review_models = self.run_loop()
        self.assertEqual(review_models, ["openrouter:agent"])
        self.assertEqual(set(self.limits), {16384})

    def test_max_tokens_sets_the_agent_output_limit(self):
        self.run_loop(max_tokens=36000)
        self.assertEqual(set(self.limits), {36000})


class TestPinnedClientPerModel(unittest.TestCase):

    def client(self, settings):
        resp = NS(provider="p", usage=NS(prompt_tokens=100, completion_tokens=30, cost=0.002,
                                         completion_tokens_details=NS(reasoning_tokens=20)))
        inner = MagicMock()
        inner.chat.completions.create.return_value = resp
        return ho._PinnedClient(inner, settings, Counter()), inner

    def test_provider_by_model_pins_that_model_and_leaves_the_others(self):
        settings = {**ho.LLM_SETTINGS, "provider_by_model": {"z-ai/glm-5.3": {"only": ["novita/fp8"]}}}
        c, inner = self.client(settings)
        ho.drain_usage()
        c.chat.completions.create(model="z-ai/glm-5.3", messages=[])
        c.chat.completions.create(model="google/gemma-4-31b-it", messages=[])
        sent = [k.kwargs["extra_body"]["provider"] for k in inner.chat.completions.create.call_args_list]
        self.assertEqual(sent, [{"only": ["novita/fp8"]}, ho.LLM_SETTINGS["provider"]])

    def test_extra_by_model_adds_fields_to_that_model_only(self):
        settings = {**ho.LLM_SETTINGS, "extra_by_model": {"z-ai/glm-5.3": {"reasoning": {"max_tokens": 8000}}}}
        c, inner = self.client(settings)
        c.chat.completions.create(model="z-ai/glm-5.3", messages=[])
        c.chat.completions.create(model="google/gemma-4-31b-it", messages=[])
        sent = [k.kwargs["extra_body"].get("reasoning") for k in inner.chat.completions.create.call_args_list]
        self.assertEqual(sent, [{"max_tokens": 8000}, None])
        ho.drain_usage()

    def test_usage_is_recorded_per_model_and_drained(self):
        c, _ = self.client(dict(ho.LLM_SETTINGS))
        ho.drain_usage()
        c.chat.completions.create(model="m", messages=[])
        c.chat.completions.create(model="m", messages=[])
        u = ho.drain_usage()
        self.assertEqual(u["m"]["calls"], 2)
        self.assertEqual(u["m"]["prompt_tokens"], 200)
        self.assertEqual(u["m"]["reasoning_tokens"], 40)
        self.assertAlmostEqual(u["m"]["cost"], 0.004)
        self.assertEqual(ho.drain_usage(), {})


if __name__ == "__main__":
    unittest.main()
