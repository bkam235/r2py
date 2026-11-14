"""2026-11-14: a module imported above the first entity and rebound by an entity (`from shiny import ui` then
`ui = ui.page_fluid(...)`) was never recorded at that entity. The baseline kept no id for modules, so the changed
binding looked like an old name and was skipped; the entity scored 0 on data, type and value while the end-of-run
capture (and so its feedback) showed the right value (shiny updateRadioButtons 0.25 against 0.96 for the same
program with the import renamed)."""
import tempfile
import unittest
from pathlib import Path


def run_instrumented(head, e1, e2="y = 1"):
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    from r2py.stage4.verifier import (_ALL_CAPTURE, _PY_CHECKPOINT_PREAMBLE, _collect_py_checkpoints,
                                      _inject_py_checkpoints)
    src = f"{head}\n# r2py:entity:e1\n{e1}\n# r2py:entity:e2\n{e2}\n"
    h = head.count("\n") + 1
    instrumented, eids = _inject_py_checkpoints(src, {"e1": (h + 2, h + 2), "e2": (h + 4, h + 4)})
    with tempfile.TemporaryDirectory() as d:
        bundle = PySandbox().run(instrumented, workdir=Path(d), capture=_ALL_CAPTURE, timeout_s=60,
                                 preamble=_PY_CHECKPOINT_PREAMBLE)
        assert bundle.exit_code == 0, (bundle.stderr or "")[-800:]
        return {e: b.data for e, b in _collect_py_checkpoints(Path(d), eids).items()}


class TestModuleRebound(unittest.TestCase):
    def test_a_module_rebound_by_an_entity_is_recorded_there(self):
        cps = run_instrumented("from os import path", "path = path.join('a', 'b')")
        self.assertIn("path", cps["e1"])
        self.assertTrue(str(cps["e1"]["path"]).replace("\\", "/").endswith("a/b"))
        self.assertNotIn("path", cps["e2"])              # recorded once, where it changed

    def test_a_module_rebound_in_a_later_entity_is_recorded_there(self):
        cps = run_instrumented("import os.path as path", "z = 1", "path = path.join('a', 'b')")
        self.assertNotIn("path", cps["e1"])
        self.assertIn("path", cps["e2"])

    def test_a_module_left_alone_is_not_recorded(self):
        cps = run_instrumented("import math", "z = math.floor(2.5)")
        self.assertNotIn("math", cps["e1"])
        self.assertEqual(cps["e1"].get("z"), 2)


if __name__ == "__main__":
    unittest.main()
