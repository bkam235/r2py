"""Agent width: independent loops from one state, best verified result wins."""
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from r2py.harness import agent


def _rep(score, exit_code=0):
    return SimpleNamespace(aggregate=score, py_exit_code=exit_code, by_entity={}, crash_entities=[])


class TestStepContext(unittest.TestCase):
    def test_context_is_per_thread(self):
        agent._ctx.clear()
        agent._ctx.update(step=1)
        seen = {}

        def other():
            seen["empty"] = dict(agent._ctx)
            agent._ctx.update(step=99)
            seen["own"] = dict(agent._ctx)

        t = threading.Thread(target=other)
        t.start()
        t.join()
        self.assertEqual(seen, {"empty": {}, "own": {"step": 99}})
        self.assertEqual(dict(agent._ctx), {"step": 1})
        self.assertEqual({**agent._ctx}, {"step": 1})


class TestReasonWide(unittest.TestCase):
    def _run(self, results):
        calls = []

        def fake(*, current_source, score_report, harness, script_map, branch=None, **kw):
            calls.append((harness, branch))
            r = results[harness]
            if isinstance(r, Exception):
                raise r
            return r

        with patch.object(agent, "reason", side_effect=fake):
            out = agent.reason_wide(list(results), current_source="x", score_report=_rep(0.0), script_map=None)
        return out, calls

    def test_best_branch_wins(self):
        out, calls = self._run({"h0": ("a", _rep(0.4)), "h1": ("b", _rep(0.8)), "h2": ("c", _rep(0.6))})
        self.assertEqual(out[0], "b")
        self.assertEqual(sorted(b for _, b in calls), [0, 1, 2])

    def test_failing_or_empty_branches_do_not_lose_the_others(self):
        out, _ = self._run({"h0": RuntimeError("boom"), "h1": None, "h2": ("c", _rep(0.6))})
        self.assertEqual(out[0], "c")
        out, _ = self._run({"h0": None, "h1": None})
        self.assertIsNone(out)

    def test_width_one_is_the_plain_loop(self):
        out, calls = self._run({"h0": ("a", _rep(0.4))})
        self.assertEqual(out[0], "a")
        self.assertEqual(calls, [("h0", None)])


if __name__ == "__main__":
    unittest.main()


class TestEntityWidth(unittest.TestCase):
    SRC = "# r2py:entity:a\nx = 1\n# r2py:entity:b\ny = 2\n"

    class _Harness:
        def __init__(self):
            self.verified = []

        def verify(self, source):
            self.verified.append(source)
            return _rep(0.9 if "y = 3" in source else 0.2 if "y = 4" in source else 0.5)

    def _widen(self, replies, first="y = 4"):
        import json
        calls = iter(replies)
        h = self._Harness()
        with patch.object(agent._llm, "call", side_effect=lambda *a, **k: next(calls)):
            out = agent._widen_entity_repair({"action": "entity_repair", "entity": "b", "new_source": first},
                                             [], "sys", "m", 3, self.SRC, h)
        return out, h

    @staticmethod
    def _reply(code):
        import json
        return json.dumps({"action": "rewrite", "new_source": code})

    def test_best_verified_fragment_wins(self):
        out, h = self._widen([self._reply("y = 3"), self._reply("y = 5")])
        self.assertEqual(out["new_source"], "y = 3")
        self.assertEqual(len(h.verified), 3)

    def test_unusable_samples_leave_the_first_fragment(self):
        out, h = self._widen([RuntimeError("boom"), "not json"])
        self.assertEqual(out["new_source"], "y = 4")
        self.assertEqual(len(h.verified), 1)

    def test_identical_fragments_are_verified_once(self):
        out, h = self._widen([self._reply("y = 4"), self._reply("y = 4")])
        self.assertEqual(len(h.verified), 1)
