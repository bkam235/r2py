"""Beam search over restarts: chains restart from the best distinct states found so far."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from r2py.harness import agent, beam


def _rep(score):
    return SimpleNamespace(aggregate=score, py_exit_code=0, by_entity={}, crash_entities=[])


class TestTopDistinct(unittest.TestCase):
    def test_ranks_and_pads(self):
        pool = [("a", _rep(0.2)), ("b", _rep(0.8)), ("c", _rep(0.5))]
        self.assertEqual([s for s, _ in beam._top_distinct(pool, 2)], ["b", "c"])
        self.assertEqual([s for s, _ in beam._top_distinct(pool, 5)], ["b", "c", "a", "b", "b"])


class TestReasonBeam(unittest.TestCase):
    def _run(self, fake, rounds=3, width=3):
        calls = []

        def wrapped(*, current_source, score_report, harness, script_map, branch=None, **kw):
            calls.append((current_source, branch))
            return fake(current_source, branch)

        with patch.object(agent, "reason", side_effect=wrapped):
            out = beam.reason_beam(list(range(width)), current_source="s0", score_report=_rep(0.1),
                                   script_map=None, max_rounds=rounds, max_steps=4)
        return out, calls

    def test_second_round_restarts_from_the_best_state(self):
        # round 1: branch i reaches state "r1b<i>" scoring 0.3 + 0.1*i; round 2 must start from the best of those
        def fake(src, branch):
            if src == "s0":
                return (f"r1b{branch}", _rep(0.3 + 0.1 * branch))
            return (src + "+", _rep(0.9)) if src == "r1b2" else None

        out, calls = self._run(fake)
        round2 = [s for s, _ in calls[3:]]
        self.assertEqual(round2[0], "r1b2")                       # the best state leads the next round
        self.assertEqual(set(round2), {"r1b2", "r1b1", "r1b0"})   # and the others follow, distinct
        self.assertEqual(out[0], "r1b2+")

    def test_stops_when_no_chain_improves(self):
        out, calls = self._run(lambda src, b: None)
        self.assertIsNone(out)
        self.assertEqual(len(calls), 3)    # one round only

    def test_stops_at_the_threshold(self):
        out, calls = self._run(lambda src, b: ("won", _rep(0.95)))
        self.assertEqual(out[1].aggregate, 0.95)
        self.assertEqual(len(calls), 3)

    def test_a_failing_chain_does_not_lose_the_others(self):
        def fake(src, b):
            if b == 0:
                raise RuntimeError("boom")
            return (f"x{b}", _rep(0.5))

        out, _ = self._run(fake, rounds=1)
        self.assertEqual(out[1].aggregate, 0.5)


if __name__ == "__main__":
    unittest.main()
