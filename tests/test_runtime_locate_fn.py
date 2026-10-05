"""Function-level locator: where inside an R function a Python reimplementation first departs from R."""
import unittest
from unittest.mock import patch

import pytest

from r2py.runtime import difftest, locate_fn, propose


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


BAD = ("import numpy as np\n"
       "def r_IQR(x, na_rm=False, type=7):\n"
       "    x = np.asarray(x, float)\n"
       "    q = np.percentile(x, [25, 75], method='nearest')\n"
       "    return float(q[1] - q[0])\n")


@pytest.mark.skipif(not _has_r(), reason="R not available")
class TestAgainstR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = difftest.build_cases("IQR", ["IQR(c(2.5,3.1,4.7,5.2,6.8,7.4,9.9,10.3))", "IQR(c(1,5,2,8,3,9,4))"])["cases"][0]

    def test_r_probes_cover_the_calls_inside_the_function_body_in_order(self):
        probes = locate_fn.r_probes("IQR", None, self.case)
        exprs = [p["expr"] for p in probes]
        self.assertTrue(exprs[0].startswith("as.numeric(x)"))
        self.assertTrue(any(e.startswith("quantile(") for e in exprs))
        self.assertTrue(exprs[-1].startswith("diff("))

    def test_the_first_departing_step_and_the_nearest_python_value_are_named(self):
        text = locate_fn.explain("IQR", None, BAD, self.case, {})
        self.assertIn("`quantile(", text)
        self.assertIn("[4.3, 8.025]", text)                  # R's value
        self.assertIn("np.percentile", text)                 # the nearest thing Python computed
        self.assertIn("relative error", text)

    def test_r_probes_are_cached_per_case(self):
        cache = {}
        locate_fn.explain("IQR", None, BAD, self.case, cache)
        with patch.object(locate_fn, "r_probes", side_effect=AssertionError("R must not run twice")):
            locate_fn.explain("IQR", None, BAD, self.case, cache)


class TestRepairMessage(unittest.TestCase):
    def test_locate_note_is_attached_to_the_first_failing_ordinary_case_only(self):
        res = difftest.Result(passed=1, total=3, core_passed=1, core_total=2, failures=[
            {"call": "odd(df)", "expected": 1, "got": 2, "core": False},
            {"call": "f(1:3)", "expected": 1, "got": 2, "core": True},
            {"call": "f(4:6)", "expected": 1, "error": "KeyError", "core": True}])
        cases = [{"call": "odd(df)"}, {"call": "f(1:3)"}, {"call": "f(4:6)"}]
        with patch.object(locate_fn, "explain", return_value="STEP X") as ex:
            text = propose._locate("f", None, "code", res, cases, {})
        self.assertIn("STEP X", text)
        self.assertIn("f(1:3)", text)
        self.assertEqual(ex.call_args[0][3]["call"], "f(1:3)")

    def test_a_locator_failure_never_breaks_the_loop(self):
        res = difftest.Result(failures=[{"call": "f(1)", "expected": 1, "got": 2, "core": True}])
        with patch.object(locate_fn, "explain", side_effect=RuntimeError("boom")):
            self.assertEqual(propose._locate("f", None, "code", res, [{"call": "f(1)"}], {}), "")
        self.assertEqual(propose._locate("f", None, "code", difftest.Result(), [], {}), "")


if __name__ == "__main__":
    unittest.main()
