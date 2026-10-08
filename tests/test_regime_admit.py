"""Admitting a runtime function for the option values it is verified on, and refusing the rest loudly."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import regime_admit as ra  # noqa: E402

from r2py.runtime.store import RuntimeStore  # noqa: E402

IMPL = ("def r_shift(x, by=1, roll='keep'):\n"
        "    if roll == 'wrap':\n"
        "        return (x + by) % 10\n"
        "    return x + by\n")


class TestGuard(unittest.TestCase):
    def setUp(self):
        ns: dict = {}
        exec(ra.guarded(IMPL, "r_shift", {"roll": {"wrap"}}), ns)
        self.f = ns["r_shift"]

    def test_inside_the_verified_regime_it_runs_the_implementation(self):
        self.assertEqual(self.f(3), 4)
        self.assertEqual(self.f(3, by=2, roll="keep"), 5)

    def test_a_fenced_option_value_raises_instead_of_guessing(self):
        with self.assertRaises(NotImplementedError) as cm:
            self.f(9, roll="wrap")
        self.assertIn("not verified against R", str(cm.exception))

    def test_the_fence_also_catches_positional_and_length_one_values(self):
        with self.assertRaises(NotImplementedError):
            self.f(9, 1, "wrap")
        with self.assertRaises(NotImplementedError):
            self.f(9, roll=["wrap"])

    def test_leaving_the_option_at_its_default_is_not_refused(self):
        self.assertEqual(self.f(9), 10)


class TestWhatCanBeFenced(unittest.TestCase):
    def test_numeric_amounts_are_inputs_not_regimes(self):
        self.assertTrue(ra._numeric([1]))
        self.assertTrue(ra._numeric(2.5))
        self.assertFalse(ra._numeric(["pre"]))
        self.assertFalse(ra._numeric(True))
        self.assertEqual(ra._scalar(["pre"]), "pre")
        self.assertIsNone(ra._scalar([1, 2]))

    def test_an_incomplete_failure_record_is_never_admitted(self):
        rec = {"function": "shift", "code": IMPL, "core_total": 16, "core_passed": 0,
               "failures": [{"call": f"shift({i})"} for i in range(5)]}
        out = ra.assess(rec, cases=[])
        self.assertIn("incomplete (5 of 16", out["verdict"])


class TestStoreLoadsRestrictedEntries(unittest.TestCase):
    def test_the_restriction_reaches_the_translator(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "pkg__shift.json").write_text(json.dumps(
                {"function": "shift", "package": "pkg", "status": "passed_restricted",
                 "unverified": {"roll": ["wrap"]}}), encoding="utf-8")
            (Path(d) / "pkg__shift.py").write_text(ra.guarded(IMPL, "r_shift", {"roll": {"wrap"}}), encoding="utf-8")
            (Path(d) / "pkg__other.json").write_text(json.dumps(
                {"function": "other", "package": "pkg", "status": "failed"}), encoding="utf-8")
            (Path(d) / "pkg__other.py").write_text("def r_other(x):\n    return x\n", encoding="utf-8")
            store = RuntimeStore(d)
            self.assertEqual(sorted(store.entries), ["r_shift"])
            section = store.prompt_section("library(pkg)\nshift(3, roll = 'keep')\n")
            self.assertIn("except roll = 'wrap'", section)
            self.assertIn("NotImplementedError", section)


if __name__ == "__main__":
    unittest.main()
