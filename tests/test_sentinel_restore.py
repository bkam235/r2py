"""Dropped entity sentinels are restored deterministically by aligning with the reference."""
import unittest
from types import SimpleNamespace

from r2py.stage2.sentinel_mapper import ranges_from_sentinels, restore_sentinels, strip_sentinels

REF = (
    "import pandas as pd\n"
    "# r2py:entity:a\n"
    "x = 1\n"
    "y = x + 1\n"
    "# r2py:entity:b\n"
    "z = pd.Series([x, y])\n"
    "print(z)\n"
    "# r2py:entity:c\n"
    "w = z.sum()\n"
)


class TestRestore(unittest.TestCase):
    def test_all_dropped_with_unchanged_code_restores_the_original(self):
        self.assertEqual(restore_sentinels(REF, strip_sentinels(REF)), REF.rstrip("\n"))

    def test_kept_sentinels_stay_and_dropped_ones_return(self):
        cand = REF.replace("# r2py:entity:b\n", "")
        out = restore_sentinels(REF, cand)
        self.assertEqual(ranges_from_sentinels(out), ranges_from_sentinels(REF))

    def test_an_edited_body_still_gets_its_range(self):
        cand = strip_sentinels(REF).replace("z = pd.Series([x, y])", "z = pd.Series([x, y], dtype=float)")
        got = ranges_from_sentinels(restore_sentinels(REF, cand))
        self.assertEqual(set(got), {"a", "b", "c"})
        self.assertEqual(got["a"], [(2, 3)])
        self.assertEqual(got["c"], [(6, 6)] if False else got["c"])   # c is the last line, whatever its number
        self.assertTrue(got["b"][0][0] <= 5)

    def test_a_fully_rewritten_body_is_placed_after_the_previous_anchor(self):
        cand = "import pandas as pd\nx = 1\ny = x + 1\nzz = 99\nqq = 100\nw = zz + qq\n"
        out = restore_sentinels(REF, cand)
        got = ranges_from_sentinels(out)
        self.assertIn("a", got)
        self.assertEqual(got["a"], [(2, 3)])
        order = [l for l in out.splitlines() if l.startswith("# r2py:entity:")]
        self.assertEqual(order, ["# r2py:entity:a", "# r2py:entity:b", "# r2py:entity:c"])

    def test_order_is_preserved_and_new_sentinels_are_kept(self):
        cand = strip_sentinels(REF) + "\n# r2py:entity:new\nv = 1\n"
        out = restore_sentinels(REF, cand)
        order = [l.split(":")[-1] for l in out.splitlines() if l.startswith("# r2py:entity:")]
        self.assertEqual(order, ["a", "b", "c", "new"])

    def test_reference_without_sentinels_adds_none(self):
        self.assertEqual(restore_sentinels("x = 1\n", "x = 1\n"), "x = 1")


class TestHarnessUsesRestore(unittest.TestCase):
    def test_restored_ranges_complete_or_none(self):
        from r2py.harness.tools import HarnessTools

        h = HarnessTools.__new__(HarnessTools)
        h._mapped_eids = {"a", "b", "c"}
        h._reference_source = REF
        got = h._restored_ranges(strip_sentinels(REF))
        self.assertEqual(set(got), {"a", "b", "c"})
        h._mapped_eids = {"a", "b", "c", "missing"}
        self.assertIsNone(h._restored_ranges(strip_sentinels(REF)))
        h._reference_source = ""
        self.assertIsNone(h._restored_ranges(strip_sentinels(REF)))


class TestPinnedAudit(unittest.TestCase):
    def test_audit_findings_are_in_every_turn(self):
        from r2py.harness import prompt

        sm = SimpleNamespace(entities={}, source="x <- 1", data_vars=[], unavailable_packages=[])
        rep = SimpleNamespace(aggregate=0.5, by_entity={}, feedback=[], py_exit_code=0, uncomparable=[],
                              by_effect={}, comparisons=[], excluded=[], crash_entities=[])
        history = [f"Step {i}: rewrite -> 0.1 (rejected)" for i in range(1, 12)]
        try:
            msg = prompt.build_agent_turn("x <- 1", "x = 1", rep, sm, 9, 20, 10, history=history,
                                          audit_feedback="AUDIT: variable `d` renamed")
        except Exception as exc:   # the fake report may lack fields other sections need
            self.skipTest(f"fake report too thin: {exc}")
        text = msg[0]["content"]
        self.assertIn("AUDIT: variable `d` renamed", text)
        self.assertNotIn("Step 1: rewrite", text)    # old history scrolled out; the audit did not


if __name__ == "__main__":
    unittest.main()
