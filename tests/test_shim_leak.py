"""The data shim pre-loads inputs, never values the script computes itself (2026-10-16).

Rule (1) of collect_shim_needed_names admitted any name an entity references without defining it, judged per
entity, so `e <- estimate(...)` followed by `e` put R's computed `e` into the shim: a translation that never
computes `e` still ran (lava 0.694 vs a crash without it), and one that computes it correctly got no credit for
it, because the verifier skips names bound before the first entity (lubridate 0.850 vs 1.000).
"""
import unittest

from r2py.stage0.effects.bundle import EffectBundle
from r2py.stage1.entities import Entity, SourceLocation
from r2py.stage1.script_map import ScriptMap
from r2py.types import EntityKind


def ent(eid, name, line, kind=EntityKind.VARIABLE, refs=(), data=None):
    e = Entity(id=eid, kind=kind, name=name,
               source_span=SourceLocation(file="t.R", start_line=line, start_col=0, end_line=line, end_col=40))
    e.free_variable_refs = list(refs)
    if data is not None:
        e.actual_bundle = EffectBundle(data=data)
    return e


DATA = {"e": [1.0], "storms": {"a": [1]}, "df": {"b": [2]}, "iris": {"c": [3]}}


class TestShimInputsOnly(unittest.TestCase):
    def sm(self):
        src = ("e <- estimate(y)\n"            # 0: computed by the script
               "e\n"                           # 1: used
               "storms\n"                      # 2: a package dataset, printed bare (an input)
               "df <- iris\n"                  # 3: computed from an input
               "summary(df)\n"                 # 4
               "storms <- head(storms)\n")     # 5: an input the script reassigns after using it
        es = {"e": ent("e", "e", 0, data=DATA), "e_1": ent("e_1", "e", 1, refs=["e"]),
              "storms": ent("storms", "storms", 2, kind=EntityKind.EXTERNAL_SYMBOL, refs=["storms"]),
              "df": ent("df", "df", 3, refs=["iris"]), "summary": ent("summary", "summary", 4,
                                                                      kind=EntityKind.FUNCTION_CALL, refs=["df"]),
              "storms_1": ent("storms_1", "storms", 5, refs=["storms"])}
        return ScriptMap(source=src, entities=es)

    def test_values_the_script_computes_before_using_them_are_not_preloaded(self):
        from r2py.stage2.stitch import collect_shim_needed_names
        needed = collect_shim_needed_names(self.sm())
        self.assertNotIn("e", needed)
        self.assertNotIn("df", needed)

    def test_inputs_stay_including_one_used_before_the_script_reassigns_it(self):
        from r2py.stage2.stitch import collect_shim_needed_names
        needed = collect_shim_needed_names(self.sm())
        self.assertIn("iris", needed)
        self.assertIn("storms", needed)

    def test_names_the_script_never_assigns_are_the_ones_guarded(self):
        from r2py.stage2.stitch import shim_input_names
        self.assertEqual(shim_input_names(self.sm()), ["iris"])     # storms is reassigned by R itself


if __name__ == "__main__":
    unittest.main()


class TestLoopGuard(unittest.TestCase):
    def test_an_agent_rewrite_that_assigns_a_shim_input_is_verified_without_that_assignment(self):
        from types import SimpleNamespace as NS
        from unittest.mock import patch
        from r2py.harness import agent
        from r2py.types import EntityScore
        es = EntityScore(entity_id="e1", executed_ok=True, type_match=.5, control_flow_match=.5, data_output=.5,
                         variable_output=.5, callable_output=.5, side_effects=.5, active_dims=frozenset({"data_output"}))
        rep = NS(by_entity={"e1": es}, crash_entities=[], py_exit_code=0, aggregate=0.5, feedback=[],
                 comparisons=[], uncomparable=[])
        seen = []

        def verify(src):
            seen.append(src)
            return rep
        harness = NS(verify=verify, _probe_count=0, last_annotated_source="", _sidecar_filename="")
        sm = NS(source="m <- mean(iris$x)\n", entities={"e1": NS(source_span=NS(start_line=0, end_line=0), name="m")},
                entity_bundles={})
        answer = "ACTION: rewrite\n```python\niris = {'x': [1, 2]}\n# r2py:entity:e1\nm = sum(iris['x'])\n```"
        with patch.object(agent._llm, "call", return_value=answer), \
             patch.object(agent, "shim_input_names", return_value=["iris"]), \
             patch.object(agent, "_prefetch_patterns", return_value={}), \
             patch.object(agent, "_prefetch_r_sources", return_value=([], "")), \
             patch.object(agent, "_get_unavailable_packages", return_value=[]), \
             patch.object(agent, "unavailable_imports", return_value=[]), \
             patch.object(agent, "_check_syntax", return_value=None), \
             patch.object(agent, "review_translation", return_value=(True, "")):
            agent.reason("# r2py:entity:e1\nm = 0\n", rep, harness, sm, model="openrouter:m", max_steps=1)
        stats = agent.drain_agent_stats()
        self.assertTrue(seen)
        self.assertNotIn("iris = {", seen[-1])
        self.assertIn("m = sum(iris['x'])", seen[-1])
        self.assertEqual(stats["outcome"].get("rewrite:shim_override_removed"), 1)


class TestPreloadedNameRecorded(unittest.TestCase):
    """A name bound before the first entity (by the data shim) and replaced by the code is recorded at the entity
    that replaces it, as R records it at the entity that assigns it; one the code leaves alone is not recorded."""

    def run_instrumented(self, body):
        import tempfile
        from pathlib import Path
        from r2py.stage0.sandbox.py_sandbox import PySandbox
        from r2py.stage4.verifier import (_ALL_CAPTURE, _PY_CHECKPOINT_PREAMBLE, _collect_py_checkpoints,
                                          _inject_py_checkpoints)
        src = "x = [9, 9]\nkeep = [7]\n# r2py:entity:e1\n" + body + "\n# r2py:entity:e2\ny = 1\n"
        n = body.count("\n") + 1                       # body lines: e1 spans 4..3+n, e2 the line after its marker
        instrumented, eids = _inject_py_checkpoints(src, {"e1": (4, 3 + n), "e2": (5 + n, 5 + n)})
        with tempfile.TemporaryDirectory() as d:
            bundle = PySandbox().run(instrumented, workdir=Path(d), capture=_ALL_CAPTURE,
                                     preamble=_PY_CHECKPOINT_PREAMBLE, timeout_s=60)
            self.assertEqual(bundle.exit_code, 0, (bundle.stderr or "")[-800:])
            return {e: b.data for e, b in _collect_py_checkpoints(Path(d), eids).items()}

    def test_a_preloaded_name_the_code_replaces_is_recorded_once_where_it_is_replaced(self):
        cps = self.run_instrumented("x = [1, 2, 3]")
        self.assertEqual(cps["e1"].get("x"), [1, 2, 3])
        self.assertNotIn("x", cps["e2"])
        self.assertNotIn("keep", cps["e1"])          # untouched preloaded values stay unrecorded, as before

    def test_a_preloaded_name_left_alone_is_not_recorded(self):
        cps = self.run_instrumented("z = len(x)")
        self.assertNotIn("x", cps["e1"])
        self.assertEqual(cps["e1"].get("z"), 2)


class TestShadowedBuiltins(unittest.TestCase):
    def test_a_script_variable_named_id_does_not_break_the_checkpoints(self):
        # lava assigns `id` (R's id <- foldr(...)); the identity check must not call the script's value
        cps = TestPreloadedNameRecorded().run_instrumented("id = [1, 2]\nx = [5]")
        self.assertEqual(cps["e1"].get("x"), [5])
        self.assertEqual(cps["e1"].get("id"), [1, 2])
