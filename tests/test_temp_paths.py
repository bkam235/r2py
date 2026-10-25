"""Temp paths are random in R itself (2026-10-18): two temp paths with the same extension compare equal."""
import unittest

from r2py.stage4.comparators.data import _compare_pair, _temp_path_ext


class TestTempPaths(unittest.TestCase):
    R = r"C:\Users\u\AppData\Local\Temp\r2py_sandbox_5tb8\Rtmpu6i0mD\file68c066eb7067.jpeg"

    def test_recognised_only_as_absolute_paths_in_a_temp_dir(self):
        self.assertEqual(_temp_path_ext(self.R), "jpeg")
        self.assertEqual(_temp_path_ext("/tmp/abc"), "")
        self.assertIsNone(_temp_path_ext("relative/tmp/x.csv"))
        self.assertIsNone(_temp_path_ext(r"C:\Users\u\data\x.jpeg"))
        self.assertIsNone(_temp_path_ext("temp"))

    def test_same_extension_matches_other_extension_does_not(self):
        py = r"C:\Users\u\AppData\Local\Temp\tmp8x2k.jpeg"
        self.assertEqual(_compare_pair("file", self.R, py, 1e-6, 1e-8)[0], 1.0)
        self.assertEqual(_compare_pair("file", self.R, py.replace(".jpeg", ".png"), 1e-6, 1e-8)[0], 0.0)
        self.assertEqual(_compare_pair("file", self.R, r"C:\Users\u\out.jpeg", 1e-6, 1e-8)[0], 0.0)


if __name__ == "__main__":
    unittest.main()


class TestTextFallbackCap(unittest.TestCase):
    def test_a_huge_value_is_compared_quickly(self):
        import time
        from r2py.stage4.comparators.data import _text_fallback
        a = [[i % 251 for i in range(400)] for _ in range(400)]     # a raster-sized value, ~600 KB of text
        b = [[(i + 1) % 251 for i in range(400)] for _ in range(400)]
        t = time.time()
        s = _text_fallback(a, b)
        self.assertLess(time.time() - t, 10)
        self.assertTrue(0.0 <= s <= 1.0)


class TestTextFallbackWindows(unittest.TestCase):
    def test_a_difference_after_the_first_characters_still_counts(self):
        from r2py.stage4.comparators.data import _text_fallback
        same_start = "x" * 6000
        a, b = same_start + "a" * 20000, same_start + "b" * 20000
        self.assertLess(_text_fallback(a, b), 0.6)          # a prefix-only comparison would give 1.0
        self.assertEqual(_text_fallback(a, a), 1.0)

    def test_a_small_insertion_keeps_almost_full_credit(self):
        from r2py.stage4.comparators.data import _text_fallback
        vals = [round(i * 0.37, 2) for i in range(5000)]
        a = str(vals)
        b = str([99.99, 88.88] + vals)                      # two extra values at the front
        self.assertGreater(_text_fallback(a, b), 0.95)     # fixed-position windows gave about half
