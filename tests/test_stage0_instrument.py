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
        src = "f(a=1, 2)\n"
        stitch.shadow_autofix(src, "agent")
        log = stitch.drain_shadow_log()
        self.assertEqual([(e["fixer"], e["bucket"]) for e in log],
                         [("reorder_positional_before_kwargs", "invalid->valid")])

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
