"""free_probe (2026-11-08): a probe_r costs no stall and shows its full result; past the probe limit it stalls."""
import unittest
from types import SimpleNamespace as NS
from pathlib import Path
from unittest.mock import patch

from r2py.harness import agent
from tests import test_entity_repair as _er

LONG = "x" * 500 + "END_OF_PROBE"


class TestFreeProbe(unittest.TestCase):

    def run_loop(self, probe_answers, n_probes=3, **kw):
        T = _er.TestCrashFirst
        rep = NS(by_entity={"e1": T.full("e1", True, 0.5)}, crash_entities=[], py_exit_code=0,
                 aggregate=0.5, feedback=[], comparisons=[], uncomparable=[])
        sent = []

        def call(messages, system, **ckw):
            sent.append(messages[-1]["content"])
            if len(sent) <= n_probes:
                return '{"action": "probe_r", "expression": "print(1)"}'
            return f"ACTION: rewrite\n```python\n# r2py:entity:e1\nb = {len(sent) + 1}\n```"
        answers = iter(probe_answers)
        harness = NS(verify=lambda src: rep, _probe_count=0, last_annotated_source="", _sidecar_filename="",
                     note_reference=lambda src: None, probe_r=lambda expr: next(answers))
        sm = NS(source="b <- 1\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="b")},
                entity_bundles={})
        with patch.object(agent._llm, "call", side_effect=call), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason("# r2py:entity:e1\nb = 1\n", rep, harness, sm, model="openrouter:m", max_steps=10,
                         max_stalls=3, entity_repair=False, converse=True, **kw)
        return agent.drain_agent_stats(), sent

    def test_by_default_three_probes_end_the_chain_and_the_result_is_cut(self):
        stats, sent = self.run_loop([LONG] * 3)
        self.assertEqual(stats["stop"].get("stalled"), 1)
        self.assertEqual(len(sent), 3)                       # three probes, no rewrite
        self.assertNotIn("END_OF_PROBE", "".join(sent))      # 100 characters only

    def test_free_probes_cost_no_stall_and_show_the_result(self):
        stats, sent = self.run_loop([LONG] * 3, free_probe=True)
        self.assertEqual(stats["outcome"].get("probe_r:free"), 3)
        self.assertEqual(len(sent), 6)                       # 3 probes, then 3 failed rewrites stall it
        self.assertIn("END_OF_PROBE", sent[1])               # the next turn shows the whole result

    def test_a_probe_past_the_limit_still_stalls(self):
        stats, sent = self.run_loop(["(probe limit reached)"] * 3, free_probe=True)
        self.assertNotIn("probe_r:free", stats["outcome"])
        self.assertEqual(len(sent), 3)

    def test_start_stalls_gives_the_hint_before_the_first_call(self):
        _, sent = self.run_loop([], n_probes=0, start_stalls=2)
        self.assertEqual(len(sent), 1)                       # one rewrite at stall 2, then the third stall
        self.assertIn("action:done", sent[0])                # the default hint

    def test_free_probe_hint_offers_the_probe_once_and_no_done(self):
        _, sent = self.run_loop([LONG] * 2, n_probes=2, start_stalls=2, free_probe=True)
        self.assertNotIn("action:done", "".join(sent))
        self.assertEqual("".join(sent).count("Before you rewrite again"), 1)
        self.assertEqual(len(sent), 3)                       # two free probes, one failed rewrite

    def test_probe_state_runs_the_probe_after_the_script(self):
        seen = []
        with patch("r2py.harness.probe_state.probe", side_effect=lambda h, sm, e: seen.append(e) or "[1] 3"):
            _, sent = self.run_loop([], n_probes=1, start_stalls=2, free_probe=True, probe_state=True)
        self.assertEqual(seen, ["print(1)"])
        self.assertIn("the script's variables and packages are there", sent[0])
        self.assertIn("[1] 3", sent[1])


class TestProbeStateProgram(unittest.TestCase):

    def test_the_script_runs_silently_then_the_expression_prints_like_a_console(self):
        import subprocess, tempfile
        from r2py.harness import probe_state
        from r2py.stage0.sandbox.r_sandbox import find_rscript
        try:
            rscript = find_rscript()
        except Exception:
            self.skipTest("no Rscript")
        prog = probe_state.program('x <- 41\nprint("noise")\nstop("skipped")\ny <- x + 1\n', 'y\ninvisible(5)\nstop("bad")')
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.R"
            f.write_text(prog, encoding="utf-8")
            out = subprocess.run([str(rscript), str(f)], capture_output=True, text=True).stdout
        self.assertNotIn("noise", out)
        self.assertIn("[1] 42", out)
        self.assertNotIn("[1] 5", out)
        self.assertIn("Error: bad", out)


if __name__ == "__main__":
    unittest.main()
