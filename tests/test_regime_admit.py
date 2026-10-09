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


class TestInputClassFences(unittest.TestCase):
    """A near miss that fails only on vector or NA input is admitted with that input class refused."""

    VEC_IMPL = "def r_first(x):\n    return x[0] if isinstance(x, list) else x\n"

    def test_the_first_arguments_input_class(self):
        from r2py.runtime.admit import NA, VECTOR, input_classes
        self.assertEqual(input_classes({"args": [[None, [1, 2, 3]]]}), {VECTOR})
        self.assertEqual(input_classes({"args": [[None, [1, None]]]}), {VECTOR, NA})
        self.assertEqual(input_classes({"args": [[None, None]]}), {NA})
        self.assertEqual(input_classes({"args": [[None, 5]]}), set())

    def test_a_vector_fence_refuses_vectors_and_runs_single_values(self):
        from r2py.runtime.admit import VECTOR, guarded
        ns: dict = {}
        exec(guarded(self.VEC_IMPL, "r_first", {}, {VECTOR}), ns)
        self.assertEqual(ns["r_first"](7), 7)
        self.assertEqual(ns["r_first"]([7]), 7)                 # length one is a single value
        with self.assertRaises(NotImplementedError) as cm:
            ns["r_first"]([7, 8, 9])
        self.assertIn("length 3", str(cm.exception))            # the message carries the value, not "{len(items)}"

    def test_an_na_fence_refuses_na_and_nan(self):
        from r2py.runtime.admit import NA, guarded
        ns: dict = {}
        exec(guarded(self.VEC_IMPL, "r_first", {}, {NA}), ns)
        self.assertEqual(ns["r_first"](3), 3)
        for bad in (None, float("nan"), [1, None]):
            with self.assertRaises(NotImplementedError):
                ns["r_first"](bad)

    def test_the_option_fence_message_names_the_value(self):
        ns: dict = {}
        exec(ra.guarded(IMPL, "r_shift", {"roll": {"wrap"}}), ns)
        with self.assertRaises(NotImplementedError) as cm:
            ns["r_shift"](1, roll="wrap")
        self.assertIn("roll='wrap'", str(cm.exception))


class TestWhatCountsAsAnOption(unittest.TestCase):
    """Options are flags and enum keywords; the data a function works on is never fenced."""

    def opts(self, *args):
        from r2py.runtime.admit import option_values
        return option_values({"args": [list(a) for a in args]})

    def test_enum_keywords_and_flags_are_options(self):
        self.assertEqual(self.opts((None, [1.0]), ("roll_dst", ["pre"]), ("as_html", [True])),
                         {("roll_dst", "pre"), ("as_html", "True")})

    def test_the_first_argument_is_data_even_when_named(self):
        self.assertEqual(self.opts(("colour", ["grey10"]), ("alpha", ["keep"])), {("alpha", "keep")})

    def test_strings_that_are_not_keywords_are_data(self):
        self.assertEqual(self.opts((None, [1]), ("x", ["<!DOCTYPE doc>"]), ("encoding", [""]),
                                   ("sep", [", "])), set())

    def test_numbers_are_amounts_not_options(self):
        self.assertEqual(self.opts((None, [1]), ("hour", [1]), ("minute", [50.0])), set())
