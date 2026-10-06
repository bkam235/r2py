"""Verified runtime pilot: R-derived differential cases, comparison, the repair prompt pieces."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from r2py.runtime import difftest, propose

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


class TestPieces(unittest.TestCase):
    def test_python_names(self):
        self.assertEqual(difftest.py_name("na.rm"), "na_rm")
        self.assertEqual(difftest.py_name("as.hms"), "as_hms")

    def test_code_block_extraction(self):
        self.assertEqual(propose._code("text\n```python\nx = 1\n```\nmore"), "x = 1\n")
        self.assertEqual(propose._code("x = 2"), "x = 2\n")

    def test_failure_text_names_call_expected_and_got(self):
        res = difftest.Result(passed=1, total=2, failures=[{"call": "f(1)", "expected": 2, "got": 3},
                                                           {"call": "f(2)", "expected": 4, "error": "KeyError: 'x'"}])
        text = propose._failures(res)
        self.assertIn("f(1)", text)
        self.assertIn("as values) 2", text)
        self.assertIn("Python returned 3", text)
        self.assertIn("KeyError", text)

    def test_only_calls_to_the_function_are_kept(self):
        raw = "```r\nmedian(c(1,2,3))\nprint(1)\nmedian(x = c(4,5))\n# note\n```"
        with patch.object(propose._llm, "call", return_value=raw):
            self.assertEqual(propose.propose_calls("median", None, "usage", "m"), ["median(c(1,2,3))", "median(x = c(4,5))"])
        with patch.object(propose._llm, "call", return_value="pROC::roc(a, b)\nroc(a, b)\nother::roc(a, b)"):
            self.assertEqual(propose.propose_calls("roc", "pROC", "usage", "m"), ["pROC::roc(a, b)", "roc(a, b)"])

    def test_unwrap(self):
        self.assertEqual(difftest._unwrap([[3.5]]), 3.5)
        self.assertEqual(difftest._unwrap([1, 2]), [1, 2])

    def test_summary(self):
        import runtime_pilot
        rows = [{"function": "a", "status": "passed", "rounds": 2, "tag": "failing entity"},
                {"function": "b", "status": "failed", "rounds": 3, "passed": 3, "total": 9, "tag": "corpus frequency (base)"},
                {"function": "c", "status": "no_cases", "rounds": 0, "tag": "corpus frequency (base)"}]
        text = runtime_pilot.summarise(rows)
        self.assertIn("passed 1", text)
        self.assertIn("failed: b (3/9)", text)
        self.assertIn("no usable cases / errors: c", text)


class TestCoreLabelling(unittest.TestCase):
    def _case(self, call, cls):
        return {"call": call, "first_class": cls}

    def test_the_most_common_first_argument_class_defines_ordinary_use(self):
        cases = [self._case("f('a')", "character"), self._case("f('b')", "character"), self._case("f(df)", "data.frame"),
                 self._case("f('a')  [first argument: reversed]", "character"),
                 self._case("f(df)  [first argument: reversed]", "data.frame")]
        difftest.label_core(cases)
        self.assertEqual([c["core"] for c in cases], [True, True, False, True, False])

    def test_mutants_follow_their_parent_even_if_the_class_changes(self):
        cases = [self._case("f(1:3)", "integer"), self._case("f(1:4)", "integer"),
                 self._case("f(1:3)  [first argument: scaled]", "numeric")]
        difftest.label_core(cases)
        self.assertTrue(all(c["core"] for c in cases))

    def test_result_acceptance_counts_only_core_cases(self):
        r = difftest.Result(passed=3, total=5, core_passed=3, core_total=3)
        self.assertTrue(r.ok_core)
        self.assertFalse(r.ok)
        self.assertFalse(difftest.Result(core_passed=2, core_total=3).ok_core)
        self.assertFalse(difftest.Result().ok_core)

    def test_failures_shown_to_the_model_list_core_ones_first(self):
        res = difftest.Result(failures=[{"call": "odd", "expected": 1, "got": 2, "core": False},
                                        {"call": "plain", "expected": 1, "got": 3, "core": True}])
        self.assertTrue(propose._failures(res, n=1).startswith("plain"))


@pytest.mark.skipif(not _has_r(), reason="R not available")
class TestAgainstR(unittest.TestCase):
    CALLS = ["quantile(c(2.5,3.1,4.7,5.2,6.8,7.4,9.9,10.3), 0.9)", "quantile(c(1,5,2,8,3), probs=c(0.25,0.5), type=6)"]
    GOOD = ("import numpy as np\n"
            "def r_quantile(x, probs=(0, .25, .5, .75, 1), na_rm=False, names=True, type=7, digits=7):\n"
            "    x = np.asarray(x, float)\n"
            "    if na_rm:\n        x = x[~np.isnan(x)]\n"
            "    return np.quantile(x, probs, method={7: 'linear', 6: 'weibull'}.get(type, 'linear'))\n")
    BAD = ("import numpy as np\n"
           "def r_quantile(x, probs=(0, .25, .5, .75, 1), na_rm=False, names=True, type=7, digits=7):\n"
           "    return np.percentile(np.asarray(x, float), np.asarray(probs) * 100, method='nearest')\n")

    @classmethod
    def setUpClass(cls):
        cls.built = difftest.build_cases("quantile", cls.CALLS)

    def test_cases_include_r_answers_and_mutants_and_use_the_methods_formals(self):
        calls = [c["call"] for c in self.built["cases"]]
        self.assertTrue(any("a tie" in c for c in calls))   # NA is dropped: quantile() errors on NA without na.rm
        self.assertTrue(any("a single value" in c for c in calls))
        self.assertIn("probs", self.built["usage"])            # the S3 method's formals, not the generic's (x, ...)

    def test_a_correct_implementation_passes_every_case_and_a_wrong_one_does_not(self):
        good = difftest.run_python(self.GOOD, "quantile", self.built["cases"])
        bad = difftest.run_python(self.BAD, "quantile", self.built["cases"])
        self.assertTrue(good.ok, good.failures[:2])
        self.assertFalse(bad.ok)
        self.assertGreater(len(bad.failures), 0)

    def test_a_file_that_does_not_run_reports_pythons_message(self):
        res = difftest.run_python("def r_quantile(x, ...=None):\n    pass\n", "quantile", self.built["cases"])
        self.assertFalse(res.ok)
        self.assertIn("did not run to completion", res.failures[0]["error"])
        self.assertIn("SyntaxError", res.failures[0]["error"])


@pytest.mark.skipif(not _has_r(), reason="R not available")
class TestNaturalReturnTypes(unittest.TestCase):
    """The first pilot accepted `r_charToRaw` returning a base64 string, because the oracle compares serialised values."""

    @classmethod
    def setUpClass(cls):
        cls.built = difftest.build_cases("charToRaw", ["charToRaw('Hello')", "charToRaw('abc')", "charToRaw('R2')"])

    def test_cases_carry_r_class_and_printed_form(self):
        self.assertEqual(self.built["cases"][0]["rclass"], "raw")
        self.assertIn("48 65 6c 6c 6f", self.built["cases"][0]["shown"])
        self.assertIn("class 'raw'", propose._describe(self.built["cases"], 1))

    def test_a_serialised_form_is_rejected_and_the_natural_object_accepted(self):
        b64 = ("import base64\n"
               "def r_charToRaw(x):\n"
               "    t = x[0] if isinstance(x, list) else x\n"
               "    return base64.b64encode(str(t).encode()).decode()\n")
        nat = ("def r_charToRaw(x):\n"
               "    t = x[0] if isinstance(x, list) else x\n"
               "    return str(t).encode('utf-8')\n")
        bad = difftest.run_python(b64, "charToRaw", self.built["cases"])
        good = difftest.run_python(nat, "charToRaw", self.built["cases"])
        self.assertFalse(bad.ok_core)
        self.assertIn("natural Python object", bad.failures[0]["error"])
        self.assertTrue(good.ok_core)


if __name__ == "__main__":
    unittest.main()


@pytest.mark.skipif(not _has_r(), reason="R not available")
class TestMinedCases(unittest.TestCase):
    SOURCE = "set.seed(3)\nx <- c(5, 1, 4, 2, 3, 9)\nm <- median(x)\nq <- quantile(sort(x), 0.9)\n"

    def test_the_real_call_is_found_with_its_arguments_evaluated_in_the_scripts_environment(self):
        mined = difftest.mine_cases(self.SOURCE, (2, 2), "median")
        self.assertEqual(len(mined), 1)
        self.assertEqual(mined[0]["call"], "median(x)")
        self.assertEqual(mined[0]["args"][0][1], [5, 1, 4, 2, 3, 9])        # the value of x, which the model never saw
        self.assertEqual(mined[0]["expected"], 3.5)
        self.assertTrue(mined[0]["mined"])

    def test_nested_calls_are_found_and_unrelated_functions_ignored(self):
        mined = difftest.mine_cases(self.SOURCE, (3, 3), "sort")
        self.assertEqual([m["call"] for m in mined], ["sort(x)"])
        self.assertEqual(difftest.mine_cases(self.SOURCE, (3, 3), "median"), [])

    def test_describe_shows_the_values_of_mined_arguments(self):
        mined = difftest.mine_cases(self.SOURCE, (2, 2), "median")
        text = propose._describe(mined)
        self.assertIn("arguments evaluated in the script", text)
        self.assertIn("[5, 1, 4, 2, 3, 9]", text)


@pytest.mark.skipif(not _has_r(), reason="R not available")
class TestPurity(unittest.TestCase):
    def test_value_functions_are_pure_and_control_flow_or_system_functions_are_not(self):
        res = difftest.impure_calls([("median", None), ("try", None), ("local", None), ("system2", None), ("sort", None)])
        self.assertEqual(res["median"], [])            # stop() inside is an error message, not a side effect
        self.assertEqual(res["sort"], [])
        self.assertIn("tryCatch", res["try"])
        self.assertTrue(res["local"])                  # evaluates an unevaluated expression
        self.assertTrue(res["system2"])

    def test_store_skips_impure_entries(self):
        import json
        import tempfile
        from pathlib import Path
        from r2py.runtime.store import RuntimeStore
        with tempfile.TemporaryDirectory() as d:
            for name, impure in (("a", []), ("b", ["system2"])):
                (Path(d) / f"base__{name}.json").write_text(json.dumps({"function": name, "package": None, "status": "passed", "impure": impure}), encoding="utf-8")
                (Path(d) / f"base__{name}.py").write_text(f"def r_{name}(x):\n    return x\n", encoding="utf-8")
            self.assertEqual(sorted(RuntimeStore(d).entries), ["r_a"])
