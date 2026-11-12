"""Development-run options: manifest-level LLM settings (unpinned provider) and select overrides."""
import unittest
from collections import Counter
from types import SimpleNamespace

from r2py import heldout as ho


class TestLlmSettings(unittest.TestCase):
    def test_defaults_and_override(self):
        base = {"protocol": {}}
        s = ho.llm_settings(base)
        self.assertEqual({k: s[k] for k in ho.LLM_SETTINGS}, ho.LLM_SETTINGS)
        s = ho.llm_settings({"protocol": {"llm": {"provider": None}}})
        self.assertIsNone(s["provider"])
        self.assertEqual(s["temperature"], ho.LLM_SETTINGS["temperature"])  # only what was overridden

    def test_the_default_agent_model_gets_its_own_pin_and_reasoning_cap(self):
        from r2py.loop import DEFAULT_AGENT_MODEL, DEFAULT_AGENT_PROVIDER, DEFAULT_AGENT_REASONING
        name = DEFAULT_AGENT_MODEL.removeprefix("openrouter:")
        s = ho.llm_settings({"protocol": {"translate": {"model": "openrouter:google/gemma-4-31b-it"}}})
        self.assertEqual(s["provider_by_model"], {name: DEFAULT_AGENT_PROVIDER})
        self.assertEqual(s["extra_by_model"], {name: {"reasoning": DEFAULT_AGENT_REASONING}})
        same = ho.llm_settings({"protocol": {"translate": {"model": "m", "agent_model": "m"}}})
        self.assertNotIn("provider_by_model", same)   # an agent on the manifest's model needs no pin of its own

    def test_unpinned_client_sends_no_provider(self):
        seen = {}

        def create(**kw):
            seen.update(kw)
            return SimpleNamespace(provider="X")

        inner = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        ho._PinnedClient(inner, ho.llm_settings({"protocol": {"llm": {"provider": None}}}), Counter())._create(model="m")
        self.assertNotIn("provider", seen["extra_body"])
        ho._PinnedClient(inner, ho.LLM_SETTINGS, Counter())._create(model="m")
        self.assertEqual(seen["extra_body"]["provider"], ho.LLM_SETTINGS["provider"])


class TestSelectOverrides(unittest.TestCase):
    def test_small_unpinned_dev_selection(self):
        m = ho.select(n_heldout=12, per_package=1, n_intervals=1, reps=1,
                      llm={"provider": None}, agent_budget_s=900)
        self.assertEqual(len(m["heldout"]), 12)
        self.assertEqual(list(m["checkpoints"]), ["empty", "full"])
        self.assertEqual(m["protocol"]["llm"], {"provider": None})
        self.assertEqual(m["protocol"]["translate"]["agent_budget_s"], 900)
        self.assertEqual(ho.DEFAULT_PROTOCOL["translate"]["agent_budget_s"], 2700)  # defaults untouched


if __name__ == "__main__":
    unittest.main()
