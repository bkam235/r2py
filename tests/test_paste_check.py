"""The deterministic pasting check must catch pasted R results and not flag computed code or R's own literals."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paste_check import check  # noqa: E402

BUNDLES = {"m": NS(stdout="[1] 3.1416  2.7183\n# A tibble: 2 x 2\n", data={"m": [3.14159265, 2.71828183, 1.41421356]}),
           "s": NS(stdout="", data={"s": "Mean of x is 3.5 (n = 6)"})}
R_SOURCE = "m <- c(pi, exp(1), sqrt(2))\nprint(round(m, 4))\nx <- c(1.2345, 7)\n"
PREVIOUS = "import numpy as np\nm = np.array([1.0])\n"


class TestPasteCheck(unittest.TestCase):
    def test_pasted_values_are_caught(self):
        cand = "m = [3.14159265, 2.71828183, 1.41421356]\n"
        self.assertTrue(check(cand, PREVIOUS, R_SOURCE, BUNDLES)["pasted"])

    def test_a_pasted_printed_line_is_caught(self):
        cand = 'print("# A tibble: 2 x 2")\n'
        r = check(cand, PREVIOUS, R_SOURCE, BUNDLES)
        self.assertTrue(r["pasted"])
        self.assertEqual(r["lines"], 1)

    def test_a_pasted_string_value_is_counted(self):
        cand = 's = "Mean of x is 3.5 (n = 6)"\n'
        self.assertEqual(check(cand, PREVIOUS, R_SOURCE, BUNDLES)["strings"], 1)

    def test_computed_code_is_not_flagged(self):
        cand = "import numpy as np\nm = np.array([np.pi, np.e, np.sqrt(2)])\nprint(np.round(m, 4))\n"
        self.assertFalse(check(cand, PREVIOUS, R_SOURCE, BUNDLES)["pasted"])

    def test_literals_from_the_r_script_or_the_previous_python_are_not_pasting(self):
        cand = "x = [1.2345, 7]\nm = np.array([1.0])\n"
        r = check(cand, PREVIOUS, R_SOURCE, BUNDLES)
        self.assertFalse(r["pasted"])
        self.assertEqual(r["numbers"], 0)

    def test_short_generic_lines_do_not_count(self):
        cand = 'print("[1] TRUE")\n'
        self.assertFalse(check(cand, PREVIOUS, R_SOURCE, {"t": NS(stdout="[1] TRUE\n", data={})})["pasted"])


if __name__ == "__main__":
    unittest.main()
