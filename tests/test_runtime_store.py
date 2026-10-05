"""The managed runtime block: which functions a script needs, regeneration from usage, idempotence."""
import json
import tempfile
import unittest
from pathlib import Path

from r2py.runtime.store import BEGIN, END, RuntimeStore

MEDIAN = "import numpy as np\n\n\ndef r_median(x, na_rm=False):\n    x = np.asarray(x, float)\n    return float(np.nanmedian(x) if na_rm else np.median(x))\n"
TIMESLICES = "def r_createTimeSlices(y, initialWindow, horizon=1):\n    return {}\n"


def _store(d: Path) -> RuntimeStore:
    for name, pkg, code, status in (("median", None, MEDIAN, "passed"), ("createTimeSlices", "caret", TIMESLICES, "passed"),
                                    ("density", None, "def r_density(x):\n    pass\n", "failed")):
        stem = f"{pkg or 'base'}__{name}"
        (d / f"{stem}.json").write_text(json.dumps({"function": name, "package": pkg, "status": status}), encoding="utf-8")
        (d / f"{stem}.py").write_text(code, encoding="utf-8")
    return RuntimeStore(d)


class TestStore(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = _store(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_only_accepted_functions_are_loaded(self):
        self.assertEqual(sorted(self.store.entries), ["r_createTimeSlices", "r_median"])
        self.assertEqual(self.store.entries["r_median"].signature(), "r_median(x, na_rm=False)")

    def test_a_script_needs_the_functions_it_calls(self):
        self.assertEqual([e.function for e in self.store.needed_by("x <- median(c(1, 2))\n")], ["median"])
        self.assertEqual(self.store.needed_by("# median(x)\ny <- 1\n"), [])                 # comments do not count
        self.assertEqual(self.store.needed_by("median <- function(x) 1\nmedian(2)\n"), [])  # the script's own median
        self.assertEqual(self.store.needed_by("mymedian(x)\n"), [])

    def test_package_functions_need_their_package(self):
        self.assertEqual([e.function for e in self.store.needed_by("caret::createTimeSlices(y, 5)\n")], ["createTimeSlices"])
        self.assertEqual([e.function for e in self.store.needed_by("library(caret)\ncreateTimeSlices(y, 5)\n")], ["createTimeSlices"])
        self.assertEqual(self.store.needed_by("createTimeSlices(y, 5)\n"), [])             # not attached: another function

    def test_prompt_section_lists_signatures_and_is_empty_when_nothing_is_needed(self):
        text = self.store.prompt_section("median(x)\n")
        self.assertIn("r_median(x, na_rm=False)", text)
        self.assertIn("never define or import them", text)
        self.assertEqual(self.store.prompt_section("print(1)\n"), "")

    def test_sync_adds_a_block_for_referenced_names_after_the_header(self):
        src = "# Translated by r2py\n# Model: m\n\nx = [1.0, 2.0]\nm = r_median(x)\n"
        out = self.store.sync(src)
        self.assertTrue(out.startswith("# Translated by r2py\n# Model: m\n\n" + BEGIN))
        self.assertIn("def r_median(", out)
        self.assertIn(END, out)
        self.assertTrue(out.rstrip().endswith("m = r_median(x)"))
        ns = {}
        exec(out, ns)
        self.assertEqual(ns["m"], 1.5)

    def test_sync_is_idempotent_and_goes_after_the_data_shim(self):
        src = "# header\n# r2py:data_shim:begin\n# x\n# r2py:data_shim:end\n\nm = r_median([1, 2, 3])\n"
        once = self.store.sync(src)
        self.assertLess(once.index("# r2py:data_shim:end"), once.index(BEGIN))
        self.assertEqual(self.store.sync(once), once)

    def test_sync_regenerates_a_damaged_block_and_removes_an_unused_one(self):
        good = self.store.sync("m = r_median([1, 2, 3])\n")
        damaged = good.replace("np.median", "np.mean")
        self.assertEqual(self.store.sync(damaged), good)
        unused = good.replace("m = r_median([1, 2, 3])", "m = 5")
        self.assertNotIn(BEGIN, self.store.sync(unused))

    def test_names_inside_strings_or_comments_do_not_pull_in_functions(self):
        src = "# uses r_median later\ns = 'r_median'\n"
        self.assertEqual(self.store.sync(src), src)

    def test_a_source_that_does_not_parse_still_syncs_by_name(self):
        out = self.store.sync("def (:\nm = r_median(x)\n")
        self.assertIn(BEGIN, out)

    def test_the_block_goes_before_the_first_entity_sentinel_not_inside_it(self):
        src = "# r2py:entity:x\nx = [1.0, 2.0]\n# r2py:entity:m\nm = r_median(x)\n"
        out = self.store.sync(src)
        self.assertLess(out.index(END), out.index("# r2py:entity:x"))
        self.assertTrue(out.index("# r2py:entity:x") < out.index("x = [1.0, 2.0]"))
        self.assertEqual(out.splitlines()[out.splitlines().index("# r2py:entity:x") + 1], "x = [1.0, 2.0]")

    def test_unknown_r_names_are_flagged_unless_defined_or_provided(self):
        self.assertEqual(self.store.unknown_references("m = r_median([1])\nh = r_holidayNYSE(2022)\n"), ["r_holidayNYSE"])
        self.assertEqual(self.store.unknown_references("def r_helper(x):\n    return x\nm = r_helper(1)\n"), [])
        self.assertEqual(self.store.unknown_references("m = r_median([1])\n"), [])
        self.assertEqual(self.store.unknown_references("def (:\n"), [])

    def test_seed_gate_reports_unknown_functions_only_with_a_store(self):
        from r2py.seed import seed_problems
        code = "h = r_holidayNYSE(2022)\n"
        self.assertEqual(seed_problems(code), [])
        problems = seed_problems(code, self.store)
        self.assertEqual(len(problems), 1)
        self.assertIn("r_holidayNYSE", problems[0])


if __name__ == "__main__":
    unittest.main()
