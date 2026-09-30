"""Smoke-run findings: the entity-mapping call was truncated at 2048 tokens and choked on backslashes."""
import unittest
from unittest.mock import patch

from r2py.stage2 import sentinel_mapper as sm


class TestParse(unittest.TestCase):
    def test_lone_backslash_in_a_string_is_repaired(self):
        raw = r'[{"entity_id": "e1", "start_line": 1, "end_line": 2, "note": "C:\path\x"}]'
        self.assertEqual(sm._parse_response(raw, {"e1"}, 5), {"e1": [(1, 2)]})

    def test_valid_escapes_are_left_alone(self):
        raw = r'[{"entity_id": "e1", "start_line": 1, "end_line": 1, "note": "a\nb"}]'
        self.assertEqual(sm._parse_response(raw, {"e1"}, 5), {"e1": [(1, 1)]})

    def test_still_fails_on_real_garbage(self):
        with self.assertRaises(sm.SentinelMappingError):
            sm._parse_response("Expecting nothing", {"e1"}, 5)

    def test_token_budget_is_not_the_old_2048(self):
        import inspect
        src = inspect.getsource(sm.map_entities_to_lines)
        self.assertNotIn("max_tokens=2048", src)
        self.assertIn("max_tokens=8192", src)


class TestVerifyDoesNotLoseTheStep(unittest.TestCase):
    def test_mapping_failure_falls_back_to_aggregate_scoring(self):
        from r2py.harness.tools import HarnessTools
        from r2py.stage4 import verifier
        ht = HarnessTools.__new__(HarnessTools)
        ht._script_map, ht._model, ht._data_compare = object(), "m", "auto"
        ht._sidecar_filename, ht._timeout_s, ht._verify_kwargs = "", 5, {}
        with patch.object(sm, "map_entities_to_lines", side_effect=sm.SentinelMappingError("bad")), \
             patch.object(verifier, "verify", return_value="REPORT") as v:
            self.assertEqual(ht.verify("x = 1\n"), "REPORT")
        self.assertEqual(v.call_args.kwargs["entity_line_map"], {})


if __name__ == "__main__":
    unittest.main()
