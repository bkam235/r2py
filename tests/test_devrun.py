"""Development-run options: manifest-level LLM settings (unpinned provider) and select overrides."""
import unittest
from collections import Counter
from types import SimpleNamespace

from r2py import heldout as ho


class TestLlmSettings(unittest.TestCase):
    def test_defaults_and_override(self):
        base = {"protocol": {}}
        self.assertEqual(ho.llm_settings(base), ho.LLM_SETTINGS)
        s = ho.llm_settings({"protocol": {"llm": {"provider": None}}})
        self.assertIsNone(s["provider"])
        self.assertEqual(s["temperature"], ho.LLM_SETTINGS["temperature"])  # only what was overridden

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
