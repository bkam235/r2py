"""Guidance code carries the helpers it calls (2026-10-11): donor snippets that called `format_hms` or
`year_month_day`, defined elsewhere in the donor's program, moved the crash into the target entity."""
import ast
import unittest

from r2py.stage2.stitch import self_contained

SOURCE = """import numpy as np
from datetime import timedelta as td

SCALE = 60


def _pad(x):
    return str(x).zfill(2)


def format_hms(s):
    return ":".join(_pad(v) for v in (s // 3600, s // 60 % 60, s % 60))


class Clock:
    pass


# r2py:entity:x
x = 3725
# r2py:entity:y
y = format_hms(x) + str(np.int64(1)) + str(td(seconds=1))
"""


class TestSelfContained(unittest.TestCase):
    def test_helpers_and_imports_used_are_prepended_transitively_in_source_order(self):
        out = self_contained("y = format_hms(x) + str(np.int64(1)) + str(td(seconds=1))", SOURCE)
        self.assertIn("def format_hms(s):", out)
        self.assertIn("def _pad(x):", out)                     # needed by format_hms
        self.assertIn("import numpy as np", out)
        self.assertIn("from datetime import timedelta as td", out)
        self.assertLess(out.index("def _pad"), out.index("def format_hms"))
        self.assertTrue(out.rstrip().endswith("str(td(seconds=1))"))
        ast.parse(out)

    def test_unused_definitions_and_script_variables_stay_out(self):
        out = self_contained("y = format_hms(x)", SOURCE)
        self.assertNotIn("class Clock", out)
        self.assertNotIn("SCALE", out)
        self.assertNotIn("x = 3725", out)                      # the target script has its own data
        self.assertNotIn("import numpy", out)

    def test_a_snippet_that_needs_nothing_is_unchanged(self):
        self.assertEqual(self_contained("z = 1 + 2", SOURCE), "z = 1 + 2")

    def test_definitions_inside_the_snippet_are_not_duplicated(self):
        snippet = "def format_hms(s):\n    return str(s)\ny = format_hms(1)"
        self.assertEqual(self_contained(snippet, SOURCE), snippet)

    def test_unparsable_input_is_returned_as_is(self):
        self.assertEqual(self_contained("y = (", SOURCE), "y = (")


if __name__ == "__main__":
    unittest.main()
