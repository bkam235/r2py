"""Guard: the graphics comparator must keep separating correct from wrong plots on the corpus."""
import importlib.util
import json
import unittest
from pathlib import Path

_DIR = Path(__file__).resolve().parents[1] / "experiments" / "graphics_corpus"
_spec = importlib.util.spec_from_file_location("graphics_corpus_evaluate", _DIR / "evaluate.py")
_ev = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ev)


class TestCorpus(unittest.TestCase):
    def test_no_correct_plot_fails_and_no_wrong_plot_passes(self):
        rows = _ev.score_entries(json.loads((_DIR / "corpus.json").read_text(encoding="utf-8")))
        false_fail, false_pass, _known = _ev.errors(rows)
        self.assertEqual([(r["case"], r["variant"]) for r in false_fail], [])
        self.assertEqual([(r["case"], r["variant"]) for r in false_pass], [])
        self.assertGreaterEqual(len(rows), 40)


if __name__ == "__main__":
    unittest.main()
