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
