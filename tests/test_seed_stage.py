"""Seed-stage changes: DataFrame data shim, seed gate with a corrective round, evaluation summarisers."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def _run_shim(data: dict, body: str) -> str:
    from r2py.stage2.stitch import build_data_shim
    from r2py.stage4.verifier import _activate_data_shim

    with tempfile.TemporaryDirectory() as wd:
        wd = Path(wd)
        (wd / "d.r2py_data.json").write_text(json.dumps(data), encoding="utf-8")
        shim, _ = _activate_data_shim(build_data_shim(list(data), "d.r2py_data.json", script_relpath="x.py"))
        r = subprocess.run([sys.executable, "-c", shim + "\n" + body], cwd=str(wd),
                           capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, r.stderr
        return r.stdout.strip()


class TestDataFrameShim(unittest.TestCase):
    def test_equal_length_column_dict_becomes_a_dataframe(self):
        out = _run_shim({"df": {"a": [1, 2, 3], "b": ["x", "y", "z"]}},
                        "print(type(df).__name__, list(df.columns), len(df))")
        self.assertEqual(out, "DataFrame ['a', 'b'] 3")

    def test_unequal_lengths_stay_a_dict(self):
        out = _run_shim({"d": {"a": [1, 2, 3], "b": [1]}}, "print(type(d).__name__)")
        self.assertEqual(out, "dict")

    def test_lists_and_scalars_are_untouched(self):
        out = _run_shim({"v": [1, 2, 3], "s": 5}, "print(v, s)")
        self.assertEqual(out, "[1, 2, 3] 5")


class TestSeedGate(unittest.TestCase):
    def setUp(self):
        from r2py import seed
        seed.seed_gate_stats.clear()

    def test_clean_code_has_no_problems(self):
        from r2py.seed import seed_problems
        self.assertEqual(seed_problems("import os\nx = 1\n"), [])

    def test_syntax_error_is_reported_with_its_line(self):
        from r2py.seed import seed_problems
        problems = seed_problems("x = 1\ny = (\n")
        self.assertEqual(len(problems), 1)
        self.assertIn("syntax error", problems[0])

    def test_unresolvable_import_is_reported(self):
        from r2py.seed import seed_problems
        problems = seed_problems("import definitely_not_a_module_xyz\n")
        self.assertEqual(len(problems), 1)
        self.assertIn("definitely_not_a_module_xyz", problems[0])

    def test_no_corrective_call_for_clean_code(self):
        from r2py import seed
        with patch.object(seed._llm, "call") as call:
            out = seed._corrective_round([], "sys", "raw", "x = 1\n", "m")
        self.assertEqual(out, "x = 1\n")
        call.assert_not_called()
        self.assertEqual(dict(seed.seed_gate_stats), {})

    def test_corrective_round_returns_the_fixed_version(self):
        from r2py import seed
        with patch.object(seed._llm, "call", return_value="```python\nx = 1\n```") as call:
            out = seed._corrective_round([], "sys", "raw", "x = (\n", "m")
        self.assertEqual(out.strip(), "x = 1")
        self.assertEqual(call.call_count, 1)
        self.assertEqual(seed.seed_gate_stats["found"], 1)
        self.assertEqual(seed.seed_gate_stats["fixed"], 1)

    def test_still_broken_keeps_the_original_when_not_better(self):
        from r2py import seed
        with patch.object(seed._llm, "call", return_value="```python\ny = (\n```"):
            out = seed._corrective_round([], "sys", "raw", "x = (\n", "m")
        self.assertEqual(out, "x = (\n")
        self.assertEqual(seed.seed_gate_stats["still_broken"], 1)

    def test_a_failing_model_call_keeps_the_original(self):
        from r2py import seed
        with patch.object(seed._llm, "call", side_effect=RuntimeError("boom")):
            out = seed._corrective_round([], "sys", "raw", "x = (\n", "m")
        self.assertEqual(out, "x = (\n")
        self.assertEqual(seed.seed_gate_stats["still_broken"], 1)


class TestEvaluationScripts(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT / "scripts"))

    def test_seed_eval_summary(self):
        import seed_eval
        rows = [
            {"script": "a.R", "kind": "bare", "idx": 0, "aggregate": 0.8, "exit_code": 0, "class": "ran", "detail": "",
             "gate": {"found": 1, "fixed": 1}},
            {"script": "a.R", "kind": "structured", "idx": 0, "aggregate": 0.0, "exit_code": 1, "class": "import",
             "detail": "foo", "gate": {}},
            {"script": "b.R", "kind": "bare", "idx": 0, "error": "SandboxEscape: x"},
        ]
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.jsonl"
            f.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
            text = seed_eval.summarise([str(f)])
        self.assertIn("2 seeds (1 errors)", text)
        self.assertIn("P(runs) 50%", text)
        self.assertIn("seed gate: {'found': 1, 'fixed': 1}", text)
        self.assertIn("1x import: foo", text)

    def test_replay_summary_pairs_by_state(self):
        import replay

        def row(script, policy, sample, start, final):
            return {"script": script, "policy": policy, "sample": sample, "start_score": start,
                    "final_score": final, "improved": final > start}
        rows = [row(s, p, i, 0.2, f) for s, fs in (("a", (0.5, 0.7)), ("b", (0.6, 0.6)), ("c", (0.4, 0.5)))
                for p, f in zip(("rewrite", "entity_esc"), fs) for i in range(2)]
        text = replay.summarise(rows)
        self.assertIn("entity_esc - rewrite, paired by state", text)
        self.assertIn("+0.100", text.split("paired by state")[1][:60].replace("(mean over samples): ", ""))
        self.assertIn("better/worse/tied 2/0/1", text)

    def test_replay_summary_without_runs(self):
        import replay
        self.assertEqual(replay.summarise([{"error": "x"}]), "no finished runs")


if __name__ == "__main__":
    unittest.main()


class TestPlannedStyle(unittest.TestCase):
    def test_plan_lines_are_stripped_and_code_kept(self):
        from r2py import seed
        code = "# plan: x <- 1 -> plain assignment\n  # Plan: sum -> np.sum, 0-based\nx = 1\n# a normal comment\ny = 2\n"
        self.assertEqual(seed._PLAN_LINE_RE.sub("", code), "x = 1\n# a normal comment\ny = 2\n")

    def test_style_picks_the_prompt(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from r2py import seed

        sm = SimpleNamespace(source="x <- 1", entities={})
        seen = {}

        def fake_call(messages, system, **kw):
            seen["system"], seen["user"] = system, messages[0]["content"]
            return "# plan: x\nx = 1\n"

        for style, expected in (("bare", seed._BARE_SYSTEM_PROMPT), ("planned", seed._PLANNED_SYSTEM_PROMPT)):
            with patch.object(seed._llm, "call", side_effect=fake_call), \
                 patch.object(seed, "_assemble", side_effect=lambda code, *a, **k: code), \
                 patch("r2py.stage2.sentinel_mapper.map_entities_to_lines", return_value={}), \
                 patch("r2py.stage2.sentinel_mapper.insert_sentinels", side_effect=lambda c, m, *a, **k: c):
                try:
                    seed.translate(sm, None, style=style, gate=False)
                except Exception:
                    pass   # only the prompt choice is under test
            self.assertEqual(seen["system"], expected)
            self.assertIn("x <- 1", seen["user"])
