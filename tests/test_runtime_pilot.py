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
        self.assertIn("R returns 2", text)
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


if __name__ == "__main__":
    unittest.main()
