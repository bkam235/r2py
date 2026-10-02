"""Lesson store: mining crash->fix pairs from trajectories, retrieval by imports, use in the seed gate."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from r2py import lessons as L

TB = ("Traceback (most recent call last):\r\n  File \"x.py\", line 3, in <module>\r\n    df.iloc[0]\r\n"
      "AttributeError: 'dict' object has no attribute 'iloc'\r\n")


def _write(d: Path, recs: list[dict]) -> Path:
    f = d / "t.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")
    return f


def _rec(kind, source, crash="", agg=0.0):
    return {"kind": kind, "source": source, "crash": crash, "aggregate": agg, "script": "s.R"}


class TestMining(unittest.TestCase):
    def test_signature_normalises_numbers_and_ignores_paths(self):
        a = L.signature("File \"a\", line 3\nValueError: bad value 12")
        b = L.signature("File \"b\", line 99\nValueError: bad value 7")
        self.assertEqual(a, b)
        self.assertEqual(L.signature("no exception here"), "")

    def test_fixed_crash_becomes_a_pair(self):
        with tempfile.TemporaryDirectory() as d:
            f = _write(Path(d), [{"kind": "run_start", "script": "s.R"},
                                 _rec("step", "import pandas\ndf.iloc[0]\n", TB, 0.0),
                                 _rec("step", "import pandas\ndf = pandas.DataFrame(df)\ndf.iloc[0]\n", "", 0.4)])
            pairs = L.mine_pairs([f])
        self.assertEqual(len(pairs), 1)
        self.assertIn("+df = pandas.DataFrame(df)", pairs[0].diff)
        self.assertIn("iloc", pairs[0].signature)

    def test_same_crash_or_lower_score_is_not_a_pair(self):
        with tempfile.TemporaryDirectory() as d:
            same = _write(Path(d), [_rec("step", "a\n", TB), _rec("step", "b\n", TB)])
            self.assertEqual(L.mine_pairs([same]), [])
        with tempfile.TemporaryDirectory() as d:
            worse = _write(Path(d), [_rec("step", "a\n", TB, 0.5), _rec("step", "b\n", "ValueError: x", 0.1)])
            self.assertEqual(L.mine_pairs([worse]), [])

    def test_excluded_scripts_are_not_mined(self):
        with tempfile.TemporaryDirectory() as d:
            f = _write(Path(d), [{"kind": "run_start", "script": "s.R"}, _rec("step", "a\n", TB),
                                 _rec("step", "b\n", "", 0.3)])
            self.assertEqual(L.mine_pairs([f], exclude_scripts={"s.R"}), [])


class TestRetrieval(unittest.TestCase):
    LES = [L.Lesson("sig1", ["pandas"], "s1", "use DataFrame", support=2),
           L.Lesson("sig2", ["lxml"], "s2", "wrap CDATA", support=1)]

    def test_matches_on_imported_modules(self):
        got = L.lessons_for("import pandas as pd\nfrom lxml import etree\n", self.LES)
        self.assertEqual([x.signature for x in got], ["sig1", "sig2"])
        self.assertEqual(L.lessons_for("import os\n", self.LES), [])
        self.assertEqual(L.lessons_for("def (:\n", self.LES), [])

    def test_merge_counts_support(self):
        merged = L.merge([L.Lesson("a", ["x"], "s", "l", 1, ["p.R"]), L.Lesson("a", ["y"], "s", "l", 1, ["q.R"])])
        self.assertEqual(len(merged), 1)
        self.assertEqual((merged[0].support, merged[0].libs, merged[0].scripts), (2, ["x", "y"], ["p.R", "q.R"]))

    def test_save_load_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            L.save(self.LES, Path(d) / "sub" / "l.json")
            self.assertEqual(L.load(Path(d) / "sub" / "l.json"), self.LES)

    def test_distill_rejects_script_specific_and_unparseable_replies(self):
        pair = L.Pair("s.R", TB, "-a\n+b", "sig")
        with patch("r2py.stage2.llm.call", return_value='{"libs": []}'):
            self.assertIsNone(L.distill(pair, "m"))
        with patch("r2py.stage2.llm.call", return_value="not json"):
            self.assertIsNone(L.distill(pair, "m"))
        ok = '{"libs": ["pandas"], "symptom": "dict has no iloc", "lesson": "build a DataFrame"}'
        with patch("r2py.stage2.llm.call", return_value="```json\n" + ok + "\n```"):
            self.assertEqual(L.distill(pair, "m").libs, ["pandas"])


class TestSeedGateWithLessons(unittest.TestCase):
    def setUp(self):
        from r2py import seed
        seed.seed_gate_stats.clear()
        self.les = [L.Lesson("sig", ["pandas"], "dict has no iloc", "build a DataFrame")]

    def test_matching_lesson_triggers_a_revision_that_is_taken(self):
        from r2py import seed
        with patch.object(seed._llm, "call", return_value="```python\nimport pandas\nx = 2\n```") as call:
            out = seed._corrective_round([], "sys", "raw", "import pandas\nx = 1\n", "m", self.les)
        self.assertEqual(out.strip(), "import pandas\nx = 2")
        self.assertIn("build a DataFrame", call.call_args[0][0][-1]["content"])
        self.assertEqual(seed.seed_gate_stats["lessons_applied"], 1)

    def test_no_matching_lesson_means_no_call(self):
        from r2py import seed
        with patch.object(seed._llm, "call") as call:
            out = seed._corrective_round([], "sys", "raw", "import os\n", "m", self.les)
        self.assertEqual(out, "import os\n")
        call.assert_not_called()

    def test_a_revision_that_breaks_the_code_is_discarded(self):
        from r2py import seed
        with patch.object(seed._llm, "call", return_value="```python\nimport pandas\nx = (\n```"):
            out = seed._corrective_round([], "sys", "raw", "import pandas\nx = 1\n", "m", self.les)
        self.assertEqual(out, "import pandas\nx = 1\n")


if __name__ == "__main__":
    unittest.main()
