"""Entity mapping by model (2026-10-17): temperature 0 and cached per (model, entities, source), so a candidate
that lost its sentinels scores the same on every verification."""
import os
import tempfile
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch

from r2py.stage2 import sentinel_mapper as sm_mod


class TestMappingCache(unittest.TestCase):
    def test_temperature_zero_and_a_repeat_is_served_from_disk(self):
        ent = NS(source_span=NS(start_line=0, end_line=0), name="x", kind=NS(value="variable"))
        script_map = NS(entities={"x": ent}, source="x <- 1\n")
        calls = []

        def call(messages, system, **kw):
            calls.append(kw.get("temperature"))
            return '[{"entity_id": "x", "ranges": [[1, 1]]}]'
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"R2PY_MAPPING_CACHE": d}), \
             patch.object(sm_mod._llm, "call", side_effect=call), \
             patch.object(sm_mod, "_build_entity_listing", return_value="x: x <- 1"), \
             patch.object(sm_mod, "_parse_response", return_value={"x": [(1, 1)]}):
            first = sm_mod.map_entities_to_lines(script_map, "x = 1\n", model="m")
            second = sm_mod.map_entities_to_lines(script_map, "x = 1\n", model="m")
            other = sm_mod.map_entities_to_lines(script_map, "x = 2\n", model="m")
        self.assertEqual(first, second)
        self.assertEqual(other, {"x": [(1, 1)]})
        self.assertEqual(calls, [0.0, 0.0])          # the repeat cost no call; a different source did


if __name__ == "__main__":
    unittest.main()
