"""Frozen helper interfaces (translation manual, stage 1, 2026-10-16).

52% of rewrites change the helper interface, so an improvement is valid only inside the design it was written in.
Stage 1 freezes the interface of the best program's helpers for a step: a candidate that drops, renames away from
or re-parameterises one gets the best program's definition back; bodies and new helpers are free.
"""
import ast
import unittest

from r2py.harness.manual import enforce_interfaces, helper_interfaces, interface_note

BEST = """import numpy as np

def r_tidy(fit, data):
    return fit + data


class Fit:
    def __init__(self, x):
        self.x = x


# r2py:entity:tidy
res = r_tidy(1, 2)
"""


class TestInterfaces(unittest.TestCase):
    def test_interfaces_are_top_level_defs_and_classes(self):
        self.assertEqual(helper_interfaces(BEST), {"r_tidy": ("fit", "data"), "Fit": ("class",)})

    def test_a_renamed_helper_is_put_back_and_the_new_one_kept(self):
        cand = BEST.replace("def r_tidy(fit, data):", "def r_tidy_factanal(fit, data):").replace(
            "res = r_tidy(1, 2)", "res = r_tidy_factanal(1, 2)")
        out, info = enforce_interfaces(BEST, cand)
        self.assertEqual(info["restored"], ["r_tidy"])
        self.assertEqual(info["changed"], ["r_tidy"])
        self.assertEqual(set(helper_interfaces(out)), {"r_tidy", "r_tidy_factanal", "Fit"})
        ast.parse(out)

    def test_changed_parameters_are_put_back(self):
        cand = BEST.replace("def r_tidy(fit, data):\n    return fit + data", "def r_tidy(fit):\n    return fit")
        out, info = enforce_interfaces(BEST, cand)
        self.assertEqual(info["restored"], ["r_tidy"])
        self.assertEqual(helper_interfaces(out)["r_tidy"], ("fit", "data"))
        self.assertIn("return fit + data", out)

    def test_a_new_body_with_the_same_interface_is_kept(self):
        cand = BEST.replace("return fit + data", "return fit * data")
        out, info = enforce_interfaces(BEST, cand)
        self.assertEqual(info["restored"], [])
        self.assertEqual(out, cand)

    def test_a_dropped_helper_is_put_back_before_the_first_entity(self):
        cand = BEST.replace("class Fit:\n    def __init__(self, x):\n        self.x = x\n", "")
        out, info = enforce_interfaces(BEST, cand)
        self.assertEqual(info["restored"], ["Fit"])
        self.assertLess(out.index("class Fit"), out.index("# r2py:entity:tidy"))
        ast.parse(out)

    def test_the_note_lists_the_frozen_signatures(self):
        note = interface_note(BEST)
        self.assertIn("r_tidy(fit, data)", note)
        self.assertIn("class Fit", note)

    def test_a_program_without_helpers_is_untouched(self):
        src = "# r2py:entity:a\na = 1\n"
        self.assertEqual(enforce_interfaces(src, "# r2py:entity:a\na = 2\n")[0], "# r2py:entity:a\na = 2\n")
        self.assertEqual(interface_note(src), "")


if __name__ == "__main__":
    unittest.main()


class TestInsertionPoint(unittest.TestCase):
    def test_a_dropped_helper_is_never_inserted_inside_a_function_whose_body_holds_the_first_marker(self):
        # hms: the first entity marker sits inside `def hms(...)`; inserting before the marker broke the function
        best = "def fmt(td):\n    return str(td)\n\n\ndef hms(s):\n# r2py:entity:hms\n    return s\n\nx = fmt(hms(1))\n"
        cand = "def hms(s):\n# r2py:entity:hms\n    return s * 2\n\nx = fmt(hms(1))\n"
        out, info = enforce_interfaces(best, cand)
        self.assertEqual(info["restored"], ["fmt"])
        ast.parse(out)
        self.assertLess(out.index("def fmt"), out.index("def hms"))
