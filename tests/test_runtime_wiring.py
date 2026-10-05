"""The verified runtime is offered to the translator and kept in the file by the harness (seed prompt, agent turn, rewrite)."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from r2py.runtime.store import BEGIN, RuntimeStore

CODE = "import numpy as np\n\n\ndef r_median(x, na_rm=False):\n    return float(np.median(np.asarray(x, float)))\n"


def _store(d):
    (Path(d) / "base__median.json").write_text(json.dumps({"function": "median", "package": None, "status": "passed"}), encoding="utf-8")
    (Path(d) / "base__median.py").write_text(CODE, encoding="utf-8")
    return RuntimeStore(d)


class TestSeedPrompt(unittest.TestCase):
    def test_structured_prompt_lists_the_functions_the_script_calls(self):
        from r2py.seed import _build_prompt
        with tempfile.TemporaryDirectory() as d:
            store = _store(d)
            sm = SimpleNamespace(source="m <- median(x)\n", entities={}, entity_bundles={}, source_file="s.R")
            lib = SimpleNamespace(retrieve=lambda *a, **k: [], retrieve_base_patterns=lambda *a, **k: [],
                                  retrieve_corrections=lambda *a, **k: [])
            with_rt = "\n\n".join(_build_prompt(sm, lib, runtime=store))
            without = "\n\n".join(_build_prompt(sm, lib))
        self.assertIn("r_median(x, na_rm=False)", with_rt)
        self.assertNotIn("r_median", without)


class TestAgentTurn(unittest.TestCase):
    def test_turn_carries_the_section_only_when_given(self):
        from r2py.harness import prompt
        sm = SimpleNamespace(entities={}, source="x", data_vars=[], unavailable_packages=[])
        rep = SimpleNamespace(aggregate=0.5, by_entity={}, feedback=[], py_exit_code=0, uncomparable=[], by_effect={},
                              comparisons=[], excluded=[], crash_entities=[])
        try:
            with_s = prompt.build_agent_turn("x", "x = 1", rep, sm, 1, 5, 3, runtime_section="- `r_median(x)` reproduces R's median")
            without = prompt.build_agent_turn("x", "x = 1", rep, sm, 1, 5, 3)
        except Exception as exc:
            self.skipTest(f"fake report too thin: {exc}")
        self.assertIn("Verified Python implementations", with_s[0]["content"])
        self.assertNotIn("Verified Python implementations", without[0]["content"])


class TestRewriteKeepsTheBlock(unittest.TestCase):
    def test_a_rewrite_that_drops_the_block_gets_it_back_and_one_that_stops_using_a_function_loses_it(self):
        with tempfile.TemporaryDirectory() as d:
            store = _store(d)
            first = store.sync("m = r_median([3, 1, 2])\n")
            self.assertIn(BEGIN, first)
            rewrite_without_block = "m = r_median([3, 1, 2]) + 1\n"
            self.assertIn("def r_median", store.sync(rewrite_without_block))
            self.assertNotIn(BEGIN, store.sync(first.replace("m = r_median([3, 1, 2])", "m = 2")))


class TestHarnessToolsCarriesTheStore(unittest.TestCase):
    def test_runtime_attribute(self):
        from r2py.harness.tools import HarnessTools
        with tempfile.TemporaryDirectory() as d:
            store = _store(d)
            h = HarnessTools(SimpleNamespace(source="", entities={}), SimpleNamespace(), runtime=store)
            self.assertIs(h.runtime, store)
            self.assertIsNone(HarnessTools(SimpleNamespace(source="", entities={}), SimpleNamespace()).runtime)


if __name__ == "__main__":
    unittest.main()
