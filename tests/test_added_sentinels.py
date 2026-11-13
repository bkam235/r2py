"""Added sentinels (2026-11-13): a sentinel the candidate carries for a script-map entity that the reference does
not map is attributed too, in addition to the reference's entities, never instead of them. Before, the reference's
set was the only one, so an entity the seed mapping missed could never score (farver spec_lab 0.25 against 1.0)."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.harness import tools
from r2py.stage2 import sentinel_mapper as sm
from r2py.stage4 import verifier

REF = "# r2py:entity:e1\na = 1\n# r2py:entity:e2\nb = 2\nc = 3\n"


class TestAddedSentinels(unittest.TestCase):
    def tool(self, entities=("e1", "e2", "e3")):
        ht = tools.HarnessTools.__new__(tools.HarnessTools)
        ht._script_map, ht._model, ht._data_compare = NS(entities={e: 1 for e in entities}, source=""), "m", "auto"
        ht._sidecar_filename, ht._timeout_s, ht._verify_kwargs = "", 5, {}
        ht._verify_cache, ht.last_annotated_source, ht._mapped_eids = {}, "", set()
        ht.runtime = None
        tools.drain_cache_stats()
        ht.note_reference(REF)
        return ht

    def line_map(self, ht, candidate):
        with patch.object(sm, "map_entities_to_lines") as mapper, \
             patch.object(verifier, "verify", return_value="R") as v:
            ht.verify(candidate)
        mapper.assert_not_called()
        return v.call_args.kwargs["entity_line_map"], ht.last_annotated_source

    def test_an_added_sentinel_of_a_script_map_entity_is_attributed(self):
        lm, annotated = self.line_map(self.tool(), REF.replace("c = 3", "# r2py:entity:e3\nc = 3"))
        self.assertEqual(lm, {"e1": (1, 1), "e2": (2, 2), "e3": (3, 3)})
        self.assertIn("# r2py:entity:e3", annotated)            # the chain continues with it

    def test_a_sentinel_naming_no_script_map_entity_is_ignored(self):
        lm, annotated = self.line_map(self.tool(), REF.replace("c = 3", "# r2py:entity:made_up\nc = 3"))
        self.assertEqual(set(lm), {"e1", "e2"})
        self.assertNotIn("made_up", annotated)

    def test_added_sentinels_count_when_dropped_ones_are_restored(self):
        # e2's sentinel dropped, e3's added: e2 is restored from the reference, e3 kept
        cand = "# r2py:entity:e1\na = 1\nb = 2\n# r2py:entity:e3\nc = 3\n"
        lm, _ = self.line_map(self.tool(), cand)
        self.assertEqual(set(lm), {"e1", "e2", "e3"})
        self.assertEqual(tools.drain_cache_stats()["sentinel_restored"], 1)

    def test_the_reference_set_alone_still_reads_as_before(self):
        lm, _ = self.line_map(self.tool(), REF.replace("a = 1", "a = 10"))
        self.assertEqual(lm, {"e1": (1, 1), "e2": (2, 3)})


if __name__ == "__main__":
    unittest.main()
