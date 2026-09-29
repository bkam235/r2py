"""Stage 3: the replace_entity action (splice + parse)."""
import unittest

from r2py.harness.agent import _check_syntax, _parse_action
from r2py.stage2.stitch import splice_entity

SRC = """import os
# r2py:entity:e1
a = 1
# r2py:entity:e2
b = (
    2
)

# r2py:entity:e3
c = 3
# r2py:entity:e1
d = 4
"""


class TestSplice(unittest.TestCase):
    def test_replaces_only_that_entity_and_keeps_the_sentinel(self):
        out, err = splice_entity(SRC, "e2", "b = 20\nb2 = 21")
        self.assertEqual(err, "")
        self.assertEqual(out.splitlines(), [
            "import os", "# r2py:entity:e1", "a = 1", "# r2py:entity:e2", "b = 20", "b2 = 21",
            "", "# r2py:entity:e3", "c = 3", "# r2py:entity:e1", "d = 4"])

    def test_last_entity_and_stray_sentinels_in_the_body(self):
        out, _ = splice_entity(SRC, "e3", "# r2py:entity:e3\nc = 30")
        self.assertIn("# r2py:entity:e3\nc = 30\n# r2py:entity:e1", out)
        self.assertEqual(out.count("# r2py:entity:e3"), 1)
        self.assertIsNone(_check_syntax(out))

    def test_unknown_and_multi_span_entities_are_refused(self):
        self.assertIn("unknown", splice_entity(SRC, "e9", "x = 1")[1])
        self.assertIn("2 separate spans", splice_entity(SRC, "e1", "x = 1")[1])


class TestParse(unittest.TestCase):
    def test_replace_entity_tag(self):
        raw = "It fails on b.\n\nACTION: replace_entity\nentity: e2\n```python\nb = 20\n```\n"
        self.assertEqual(_parse_action(raw),
                         {"action": "replace_entity", "entity": "e2", "new_source": "b = 20"})

    def test_missing_entity_does_not_parse_as_a_rewrite(self):
        raw = "ACTION: replace_entity\n```python\nb = 20\n```\n"
        self.assertEqual(_parse_action(raw)["action"], "replace_entity")  # refused by the loop
        self.assertEqual(_parse_action(raw)["entity"], "")


if __name__ == "__main__":
    unittest.main()
