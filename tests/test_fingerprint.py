"""Generic fingerprints: capture of unserialisable Python objects and by-value comparison with R."""
import unittest

from r2py.stage0.effects import data as D
from r2py.stage4.comparators import fingerprint as F
from r2py.stage4.comparators.data import DataComparator

R_LM = {"coefficients": {"(Intercept)": 37.2851, "wt": -5.3445},
        "residuals": {"a": -2.28, "b": -0.92, "c": -2.09},
        "fitted": {"a": 23.28, "b": 21.92, "c": 24.89}}


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
        py = _py({".params": [37.2851, -5.3445], ".resid": [-2.28, -0.92, -2.09], ".fitted": [23.28, 21.92, 24.89]})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[:2], (1.0, "pass"))

    def test_order_and_split_intercept_do_not_matter(self):
        py = _py({".coef_": [-5.3445], ".intercept_": [37.2851], ".r": [-2.09, -0.92, -2.28], ".f": [24.89, 21.92, 23.28]})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[0], 1.0)

    def test_missing_fields_are_named_and_cost_their_weight(self):
        py = _py({".coef_": [-5.3445], ".intercept_": [37.2851]})
        score, verdict, tag, why = F.compare("m", R_LM, py, 1e-6, 1e-9)
        self.assertEqual((verdict, tag), ("fail", "value"))
        self.assertAlmostEqual(score, 2 / 8)
        self.assertIn("residuals", why)
        self.assertIn("fitted", why)

    def test_wrong_numbers_fail(self):
        py = _py({".params": [30.0, -4.0], ".resid": [1.0, 2.0, 3.0], ".fitted": [9.0, 8.0, 7.0]})
        self.assertEqual(F.compare("m", R_LM, py, 1e-6, 1e-9)[0], 0.0)

    def test_python_side_plain_values_work_as_a_pool(self):
        py = {"coefficients": {"a": 37.2851, "b": -5.3445}, "residuals": [-2.28, -0.92, -2.09], "fitted": [23.28, 21.92, 24.89]}
        self.assertEqual(F.compare("m", {"__r2py_fp__": True, "numbers": [37.2851, -5.3445, 0.1234]}, py, 1e-6, 1e-9)[0], 2 / 3)

    def test_uninformative_integer_fields_are_ignored(self):
        self.assertFalse(F.informative([32.0]))
        self.assertFalse(F.informative([1.0, 2.0, 3.0]))
        self.assertTrue(F.informative([0.4231]))
        self.assertTrue(F.informative(list(map(float, range(20)))))
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
        res = DataComparator().compare({"m": R_LM}, {"m": _py({".p": [37.2851, -5.3445], ".r": [-2.28, -0.92, -2.09], ".f": [23.28, 21.92, 24.89]})})
        self.assertEqual(res.score, 1.0)
        self.assertEqual(res.verdict, "pass")

    def test_skip_becomes_uncomparable(self):
        r = {"__r2py_fp__": True, "class": ["x"], "numbers": [32.0]}
        res = DataComparator().compare({"m": r}, {"m": _py({".n": [32.0]})})
        self.assertEqual(res.verdict, "uncomparable")


if __name__ == "__main__":
    unittest.main()
