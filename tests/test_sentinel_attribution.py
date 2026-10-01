"""Stage 8b: attribution read off preserved sentinels, with the model mapper as the fallback."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import tools
from r2py.stage2 import sentinel_mapper as sm

ANNOTATED = ("import os\n# r2py:entity:e1\na = 1\n\n# r2py:entity:e2\nb = (\n  2\n)\n"
             "# r2py:entity:e3\nc = 3\n# r2py:entity:e1\nd = 4\n")


class TestRanges(unittest.TestCase):
    def test_ranges_are_in_the_numbering_of_the_source_without_sentinels(self):
        r = sm.ranges_from_sentinels(ANNOTATED)
        clean = sm.strip_sentinels(ANNOTATED).splitlines()
        self.assertEqual(r["e1"], [(2, 2), (8, 8)])
        self.assertEqual(r["e2"], [(4, 6)])
        self.assertEqual(r["e3"], [(7, 7)])
        self.assertEqual(clean[r["e2"][0][0] - 1], "b = (")
        self.assertEqual(clean[r["e2"][0][1] - 1], ")")

    def test_agrees_with_what_insert_sentinels_writes(self):
        clean = "x = 1\ny = 2\nz = 3\n"
        ranges = {"e1": [(1, 1)], "e2": [(2, 3)]}
        self.assertEqual(sm.ranges_from_sentinels(sm.insert_sentinels(clean, ranges)), ranges)

    def test_no_sentinels_no_ranges(self):
        self.assertEqual(sm.ranges_from_sentinels("x = 1\n"), {})


class TestVerifyUsesThem(unittest.TestCase):
    def tool(self):
        ht = tools.HarnessTools.__new__(tools.HarnessTools)
        ht._script_map, ht._model, ht._data_compare = NS(entities={"e1": 1}, source=""), "m", "auto"
        ht._sidecar_filename, ht._timeout_s, ht._verify_kwargs = "", 5, {}
        ht._verify_cache, ht.last_annotated_source, ht._mapped_eids = {}, "", set()
        tools.drain_cache_stats()
        return ht

    def test_all_sentinels_kept_means_no_model_call(self):
        ht = self.tool()
        ht.note_reference(ANNOTATED)
        from r2py.stage4 import verifier
        with patch.object(sm, "map_entities_to_lines") as mapper, \
             patch.object(verifier, "verify", return_value="R") as v:
            ht.verify(ANNOTATED.replace("a = 1", "a = 10"))
        mapper.assert_not_called()
        self.assertEqual(v.call_args.kwargs["entity_line_map"], {"e1": (8, 8), "e2": (4, 6), "e3": (7, 7)})
        self.assertEqual(tools.drain_cache_stats()["sentinel_reuse"], 1)

    def test_a_missing_sentinel_falls_back_to_the_mapper_and_retries_a_failure(self):
        ht = self.tool()
        ht.note_reference(ANNOTATED)
        from r2py.stage4 import verifier
        calls = []

        def flaky(*a, **k):
            calls.append(1)
            if len(calls) < 3:
                raise sm.SentinelMappingError("truncated")
            return {"e1": [(1, 1)]}
        with patch.object(sm, "map_entities_to_lines", side_effect=flaky), \
             patch.object(verifier, "verify", return_value="R"):
            ht.verify("a = 1\nb = 2\n")                # no sentinels at all
        self.assertEqual(len(calls), 3)
        stats = tools.drain_cache_stats()
        self.assertEqual((stats["mapping_ok"], stats.get("mapping_failed", 0)), (1, 0))

    def test_exhausted_retries_count_as_a_mapping_failure(self):
        ht = self.tool()
        from r2py.stage4 import verifier
        with patch.object(sm, "map_entities_to_lines", side_effect=sm.SentinelMappingError("x")), \
             patch.object(verifier, "verify", return_value="R") as v:
            ht.verify("a = 1\n")
        self.assertEqual(v.call_args.kwargs["entity_line_map"], {})
        self.assertEqual(tools.drain_cache_stats()["mapping_failed"], 1)


if __name__ == "__main__":
    unittest.main()
