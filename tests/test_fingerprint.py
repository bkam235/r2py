"""Generic fingerprints: capture of unserialisable Python objects and by-value comparison with R."""
import unittest

from r2py.stage0.effects import data as D
from r2py.stage4.comparators import fingerprint as F
from r2py.stage4.comparators.data import DataComparator

# Fields need >= 5 values of >= 5 significant digits to be informative (calibrated chance-match rate < 1e-3).
COEF = [37.28513, -5.344472, 1.234567, 0.4521983, -2.718281]
RES = [-2.282611, -0.91977, -2.085865, 1.297241, -0.200144, -0.693258]
FIT = [23.282611, 21.91977, 24.885865, 20.102759, 18.900144, 18.793258]
R_LM = {"coefficients": dict(zip("abcde", COEF)), "residuals": dict(zip("uvwxyz", RES)), "fitted": FIT}


def _py(numbers, texts=()):
    return {"__r2py_fp__": True, "type": "t", "numbers": numbers, "texts": list(texts)}


class TestCapture(unittest.TestCase):
    def setUp(self):
        self.ns = {}
        exec(D.build_py_preamble(), self.ns)

    def test_numbers_are_harvested_from_public_non_callable_attributes(self):
        import numpy as np

        class Fit:
            def __init__(self):
                self.coef_ = np.array([[0.5, -0.25]])
                self.intercept_ = np.array([3.21])
                self._private = np.array([99.0])
                self.helper = lambda x: x

        fp, ok = self.ns["_r2py_try_serialize"]("m", Fit())
        self.assertTrue(ok)
        self.assertEqual(fp["numbers"], {".coef_": [0.5, -0.25], ".intercept_": [3.21]})

    def test_properties_and_nested_objects_are_followed(self):
        import numpy as np

        class Inner:
            weights = np.array([1.5, 2.5])

        class Res:
            inner = Inner()

            @property
            def params(self):
                return np.array([3.0, 4.5])

        fp, ok = self.ns["_r2py_try_serialize"]("m", Res())
        self.assertTrue(ok)
        self.assertIn(".params", fp["numbers"])
        self.assertEqual(fp["numbers"][".inner.weights"], [1.5, 2.5])

    def test_json_serialisable_values_are_unchanged(self):
        self.assertEqual(self.ns["_r2py_try_serialize"]("x", {"a": [1, 2]}), ({"a": [1, 2]}, True))

    def test_objects_with_nothing_to_compare_stay_uncapturable(self):
        self.assertEqual(self.ns["_r2py_try_serialize"]("o", object()), (None, False))

    def test_a_raising_property_does_not_break_capture(self):
        class Bad:
            value = 2.5

            @property
            def boom(self):
                raise RuntimeError("no")

        fp, ok = self.ns["_r2py_try_serialize"]("b", Bad())
        self.assertTrue(ok)
        self.assertEqual(fp["numbers"], {".value": [2.5]})


class TestNumericTier(unittest.TestCase):
    def test_label_and_layout_free_match(self):
        py = _py({".params": COEF, ".resid": RES, ".fitted": FIT})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[:2], (1.0, "pass"))

    def test_order_and_split_intercept_do_not_matter(self):
        py = _py({".coef_": COEF[1:], ".intercept_": COEF[:1], ".r": RES[::-1], ".f": FIT[::-1]})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[0], 1.0)

    def test_missing_fields_are_named_and_cost_their_weight(self):
        py = _py({".coef_": COEF[1:], ".intercept_": COEF[:1]})
        score, verdict, tag, why = F.compare("m", R_LM, py, 1e-6, 1e-9)
        self.assertEqual((verdict, tag), ("fail", "value"))
        self.assertAlmostEqual(score, 5 / 17)
        self.assertIn("residuals", why)
        self.assertIn("fitted", why)

    def test_wrong_numbers_fail(self):
        py = _py({".params": [v * 1.1 for v in COEF], ".resid": [v + 0.5 for v in RES], ".fitted": [v * 2 for v in FIT]})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[0], 0.0)

    def test_python_side_plain_values_work_as_a_pool(self):
        py = {"coefficients": dict(zip("abcde", COEF)), "residuals": RES[:5]}
        r = {"__r2py_fp__": True, "numbers": COEF + RES}
        self.assertAlmostEqual(F.compare("m", r, py, 1e-6, 1e-9)[0], 10 / 11)

    def test_uninformative_integer_fields_are_ignored(self):
        self.assertFalse(F.informative([32.0]))
        self.assertFalse(F.informative(list(map(float, range(50)))))          # integers: shared by many objects
        self.assertFalse(F.informative([0.5, 0.25, 3.141593, 0.1, 2.5]))      # few significant digits
        self.assertFalse(F.informative(COEF[:4]))                             # too few distinctive values
        self.assertTrue(F.informative(COEF))
        self.assertEqual(F.significant_digits(0.30000000000000004), 1)        # float noise is not precision
        r = {"__r2py_fp__": True, "class": ["x"], "numbers": [32.0]}
        self.assertEqual(F.compare("m", r, _py({".n": [32.0]}), 1e-6, 1e-9)[1], "skip")


class TestTextTier(unittest.TestCase):
    RX = {"__r2py_fp__": True, "class": ["xml_document"], "text": '<?xml version="1.0"?>\n<a>\n <b x="1">t</b>\n</a>'}

    def test_canonical_equal_text_passes(self):
        self.assertEqual(F.compare("x", self.RX, _py({}, ['<a><b x="1">t</b></a>']), 1e-6, 1e-9)[:2], (1.0, "pass"))

    def test_different_text_costs_more_than_its_edit_distance(self):
        score, verdict, _, why = F.compare("x", self.RX, _py({}, ['<a><b x="1">u</b></a>']), 1e-6, 1e-9)
        self.assertEqual(verdict, "fail")
        self.assertTrue(0.5 < score < 1.0)
        self.assertIn("similarity", why)

    def test_python_without_text_fails(self):
        self.assertEqual(F.compare("x", self.RX, _py({".n": [0.5]}), 1e-6, 1e-9)[:2], (0.0, "fail"))


class TestDataComparatorIntegration(unittest.TestCase):
    def test_fingerprint_pair_is_scored_instead_of_excluded(self):
        res = DataComparator().compare({"m": R_LM}, {"m": _py({".p": COEF, ".r": RES, ".f": FIT})})
        self.assertEqual(res.score, 1.0)
        self.assertEqual(res.verdict, "pass")

    def test_skip_becomes_uncomparable(self):
        r = {"__r2py_fp__": True, "class": ["x"], "numbers": [32.0]}
        res = DataComparator().compare({"m": r}, {"m": _py({".n": [32.0]})})
        self.assertEqual(res.verdict, "uncomparable")


if __name__ == "__main__":
    unittest.main()
