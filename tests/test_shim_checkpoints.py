"""Seed-path runtime SyntaxErrors found by the smoke test: markers/checkpoints inside the data shim."""
import ast
import unittest

from r2py.harness.agent import _check_syntax
from r2py.stage2.sentinel_mapper import strip_sentinels
from r2py.stage4.verifier import _activate_data_shim, _inject_py_checkpoints

# The line mapper can put an entity's first line inside the (commented) shim block.
SRC = (
    "import json\n"
    "# r2py:data_shim:begin\n"
    "# for n in ['x']:\n"
    "#     if n in d:\n"
    "# r2py:entity:x\n"
    "#         globals()[n] = d[n]\n"
    "# r2py:data_shim:end\n"
    "y = 1\n"
)


class TestShim(unittest.TestCase):
    def test_activation_keeps_r2py_markers_as_comments(self):
        out, has = _activate_data_shim(SRC)
        self.assertTrue(has)
        self.assertIn("\n# r2py:entity:x\n", out)
        ast.parse(out)

    def test_checkpoints_never_land_inside_the_shim_body(self):
        shimmed, _ = _activate_data_shim(SRC)
        out, _ = _inject_py_checkpoints(shimmed, {"x": (5, 6), "y": (8, 8)})
        ast.parse(out)


class TestIndentedSentinel(unittest.TestCase):
    def test_indented_sentinel_after_a_continuation_is_stripped_before_running(self):
        src = "x = f(1) + \\\n    # r2py:entity:e2\n    g(2)\n"
        self.assertIsNone(_check_syntax(src))      # the gate ignores it...
        with self.assertRaises(SyntaxError):
            ast.parse(src)                         # ...but it breaks the real file
        ast.parse(strip_sentinels(src))            # so the runner strips it too


if __name__ == "__main__":
    unittest.main()


class TestRestoreShim(unittest.TestCase):
    def test_altered_shim_is_put_back_and_the_rest_kept(self):
        from r2py.harness.agent import restore_data_shim
        best = "import os\n# r2py:data_shim:begin\n# x = 1\n# r2py:data_shim:end\ny = 1\n"
        new = "import os\n# r2py:data_shim:begin\nSimulating tables\n# r2py:data_shim:end\ny = 2\n"
        fixed, changed = restore_data_shim(best, new)
        self.assertTrue(changed)
        self.assertEqual(fixed, "import os\n# r2py:data_shim:begin\n# x = 1\n# r2py:data_shim:end\ny = 2\n")
        self.assertEqual(restore_data_shim(best, best), (best, False))
        self.assertEqual(restore_data_shim("y = 1\n", new), (new, False))  # no shim to restore from
