"""Stage 0d (review fails closed), 2b-1 (shadow auto-fixers), 2b-2 (assembled-file syntax gate)."""
import unittest
from unittest.mock import patch

from r2py.harness import review
from r2py.harness.agent import _check_syntax
from r2py.stage2 import stitch


class TestReviewFailsClosed(unittest.TestCase):
    def _run(self, responses):
        it = iter(responses)

        def fake(*a, **k):
            r = next(it)
            if isinstance(r, Exception):
                raise r
            return r
        with patch.object(review._llm, "call", side_effect=fake):
            return review.review_translation("x <- 1", "x = 1")

    def test_truncated_rejection_is_still_a_rejection(self):
        ok, reason = self._run(['{"pass": false, "reason": "hardcodes the output (e.g., print(\\"/*'])
        self.assertFalse(ok)

    def test_llm_errors_and_garbage_fail_closed_after_retries(self):
        ok, reason = self._run([RuntimeError("429"), "junk", RuntimeError("429")])
        self.assertEqual((ok, reason), (False, review.REVIEW_UNAVAILABLE))

    def test_retry_recovers(self):
        self.assertEqual(self._run([RuntimeError("429"), '{"pass": true}']), (True, ""))


class TestShadowAutofix(unittest.TestCase):
    def setUp(self):
        stitch.drain_shadow_log()

    def test_records_a_genuine_save_without_touching_the_source(self):
        src = "f(from=1)\n"   # `from` is a keyword: invalid, and the renamer would make it valid
        stitch.shadow_autofix(src, "agent")
        log = stitch.drain_shadow_log()
        self.assertEqual([(e["fixer"], e["bucket"]) for e in log],
                         [("sanitize_keyword_args", "invalid->valid")])

    def test_clean_source_logs_nothing(self):
        stitch.shadow_autofix("f(1, a=2)\n", "seed")
        self.assertEqual(stitch.drain_shadow_log(), [])


class TestAssembledSyntaxGate(unittest.TestCase):
    def test_prose_inside_the_data_shim_is_caught(self):
        src = (f"x = 1\n{stitch.DATA_SHIM_BEGIN}\n# if True:\n# The shim will be inserted here\n"
               f"{stitch.DATA_SHIM_END}\n")
        self.assertIn("data shim", _check_syntax(src) or "")


if __name__ == "__main__":
    unittest.main()


class TestEnvIgnoresROptions(unittest.TestCase):
    def test_r_option_diff_does_not_fail_a_correct_translation(self):
        from r2py.stage4.comparators.env import EnvComparator
        c = EnvComparator()
        self.assertEqual(c.compare({"option:callr.x": 1}, {}).score, 1.0)
        self.assertEqual(c.compare({"option:digits": 4, "envvar:A": "1"}, {"envvar:A": "1"}).score, 1.0)
        self.assertEqual(c.compare({"envvar:A": "1"}, {}).score, 0.0)


class TestRequestDeadline(unittest.TestCase):
    def test_a_stalled_call_is_abandoned_and_errors_and_results_pass_through(self):
        import time
        from r2py import heldout as ho
        with self.assertRaises(TimeoutError):
            ho._with_deadline(lambda: time.sleep(5), 0.1)
        self.assertEqual(ho._with_deadline(lambda: 7, 5), 7)
        with self.assertRaises(ValueError):
            ho._with_deadline(lambda: (_ for _ in ()).throw(ValueError("x")), 5)



class TestEnvIgnoresPythonLibraryExtras(unittest.TestCase):
    def test_python_only_changes_do_not_fail_but_missing_r_changes_do(self):
        from r2py.stage4.comparators.env import EnvComparator
        c = EnvComparator()
        self.assertEqual(c.compare({}, {"envvar:KMP_DUPLICATE_LIB_OK": True, "sys_path": ["/x"]}).score, 1.0)
        self.assertEqual(c.compare({"envvar:A": "1"}, {"envvar:A": "1", "envvar:KMP": "T"}).score, 1.0)
        self.assertEqual(c.compare({"envvar:A": "1"}, {"envvar:KMP": "T"}).score, 0.0)
        self.assertEqual(c.compare({"envvar:A": "1"}, {"envvar:A": "2"}).score, 0.0)


class TestExcludedWorklist(unittest.TestCase):
    def test_groups_by_r_class_and_python_type_most_common_first(self):
        from r2py import heldout as ho
        rows = [{"excluded": [{"var": "m", "r_class": "lm", "py_type": "statsmodels.X"},
                              {"var": "g", "r_class": "glm", "py_type": "statsmodels.Y"}]},
                {"excluded": [{"var": "m2", "r_class": "lm", "py_type": "statsmodels.X"}]}, {}]
        self.assertEqual(ho.excluded_worklist(rows),
                         [(("lm", "statsmodels.X"), 2), (("glm", "statsmodels.Y"), 1)])


class TestBytesSerialisation(unittest.TestCase):
    def test_bytes_serialise_like_r_raw(self):
        # R: as.raw(c(1,2,255)) -> "AQL/" ; charToRaw("hi") -> "aGk="
        from r2py.stage0.effects.data import _R2PyEncoder
        import json
        self.assertEqual(json.loads(json.dumps({"x": bytes([1, 2, 255]), "y": b"hi"}, cls=_R2PyEncoder)),
                         {"x": "AQL/", "y": "aGk="})


class TestSandboxInterpreterSyntax(unittest.TestCase):
    def test_syntax_gate_uses_the_interpreter_that_runs_the_code(self):
        from r2py.stage0.env.py_runtime import sandbox_version_info
        nested = 'x = ["a"]\nprint(f"{", ".join(x)}")\n'  # nested same-quote f-string: 3.12+
        if sandbox_version_info()[:2] >= (3, 12):
            self.assertIsNone(_check_syntax(nested))
        else:
            self.assertIsNotNone(_check_syntax(nested))
        self.assertIn("invalid syntax", _check_syntax("def f(:\n") or "")


class TestImportGate(unittest.TestCase):
    def test_imports_are_collected_and_unresolvable_ones_flagged_without_the_network(self):
        from unittest.mock import patch
        from r2py.stage0.env import module_check as mc
        src = "import numpy as np\nfrom pkg_x.sub import y\nimport os.path\nfrom . import rel\nimport magrittr\n"
        self.assertEqual(mc.imported_modules(src), {"numpy", "pkg_x", "os", "magrittr"})
        with patch.object(mc, "_not_importable", return_value=["pkg_x", "magrittr", "maybe"]), \
             patch.object(mc, "_on_pypi", side_effect=lambda n: {"pkg_x": False, "maybe": True}.get(n)):
            # pkg_x: not on PyPI -> flagged; magrittr: known unavailable -> flagged (no lookup);
            # maybe: on PyPI -> the sandbox will install it
            self.assertEqual(mc.unavailable_imports(src, {"magrittr"}), ["pkg_x", "magrittr"])
        with patch.object(mc, "_not_importable", return_value=["x"]), patch.object(mc, "_on_pypi", return_value=None):
            self.assertEqual(mc.unavailable_imports("import x"), [])  # undecidable (offline): do not block
