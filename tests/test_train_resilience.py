"""Training and scoring survive a provider outage (no credits, no network) and an interruption without losing work."""
import sys
import tempfile
import unittest
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_heldout as th  # noqa: E402

from r2py import heldout as ho  # noqa: E402
from r2py.stage2 import llm  # noqa: E402


class TestProviderFailureBookkeeping(unittest.TestCase):
    def setUp(self):
        llm.drain_provider_failures()

    def test_classification(self):
        class E(Exception):
            def __init__(self, code, msg):
                self.status_code = code
                super().__init__(msg)
        self.assertEqual(llm.classify_failure(E(402, "Error code: 402 - more credits")), "credits")
        self.assertEqual(llm.classify_failure(E(429, "slow down")), "rate_limit")
        self.assertEqual(llm.classify_failure(E(503, "overloaded")), "server")
        self.assertEqual(llm.classify_failure(RuntimeError("Connection error.")), "network")
        self.assertEqual(llm.classify_failure(ValueError("boom")), "other")

    def test_a_call_that_fails_for_good_is_recorded_and_drained(self):
        class Boom(Exception):
            status_code = 402

        class Client:
            class chat:
                class completions:
                    @staticmethod
                    def create(**kw):
                        raise Boom("Error code: 402")
        llm._openrouter_clients["k"] = Client
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "k"}), patch.object(llm.time, "sleep"):
            with self.assertRaises(RuntimeError):
                llm.call([{"role": "user", "content": "x"}], "s", model="openrouter:m")
        self.assertEqual(llm.peek_provider_failures(), {"credits": 1})
        self.assertEqual(llm.drain_provider_failures(), {"credits": 1})
        self.assertEqual(llm.peek_provider_failures(), {})
        llm._openrouter_clients.pop("k")


class _Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.m = th._select(th._make_pool(root))
        self.work = root / "work"
        self.lines: list[str] = []
        self.polls: list = []

    def tearDown(self):
        self._tmp.cleanup()

    def _log(self, *a):
        self.lines.append(" ".join(str(x) for x in a))

    def rows(self):
        return ho._read_jsonl(self.work / "train_progress.jsonl")

    def provider(self, answers):
        """provider_ok that answers from a list (the last answer repeats)."""
        it = iter(answers)
        last = [True]

        def ok(manifest):
            last[0] = next(it, last[0])
            self.polls.append(last[0])
            return last[0], "credits: out of credits"
        return ok


class TestSequentialTraining(_Base):
    def test_an_outage_discards_the_run_waits_and_repeats_the_script(self):
        learned: list = []
        inner = th._fake_translate(learned=learned)
        calls = Counter()

        def flaky(r_path, py_path, lib, cfg, *, learn):
            calls[r_path.name] += 1
            if sum(calls.values()) in (3, 4):          # the third and fourth call hit an outage
                raise llm.ProviderUnavailable({"credits": 2})
            return inner(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", flaky), patch.object(ho, "provider_ok", self.provider([False, False, True])), \
                patch.object(ho.time, "sleep"):
            finished = ho.train(self.m, self.work, log=self._log, poll_s=1)
        self.assertTrue(finished)
        rows = self.rows()
        self.assertEqual(len(rows), 12)                                  # one row per script, none for the discarded runs
        self.assertTrue(all(r["attempt"] == 1 and "error" not in r for r in rows))
        self.assertEqual(len(learned), 12)                               # the library learned only from real runs
        events = ho._read_jsonl(self.work / "train_events.jsonl")
        self.assertEqual([e["event"] for e in events], ["provider_unavailable"] * 2)
        self.assertTrue(any("provider is back" in l for l in self.lines))

    def test_giving_up_stops_cleanly_and_the_same_command_resumes(self):
        inner = th._fake_translate()
        n = [0]

        def dies_at_five(r_path, py_path, lib, cfg, *, learn):
            n[0] += 1
            if n[0] >= 5:
                raise llm.ProviderUnavailable({"credits": 1})
            return inner(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", dies_at_five), patch.object(ho, "provider_ok", self.provider([False])), \
                patch.object(ho.time, "sleep"):
            finished = ho.train(self.m, self.work, log=self._log, poll_s=1, max_wait_s=3)
        self.assertFalse(finished)
        self.assertEqual(len(self.rows()), 4)
        redone: list = []
        with patch.object(ho, "_translate_once", th._fake_translate(learned=redone)):
            self.assertTrue(ho.train(self.m, self.work, log=self._log))
        self.assertEqual(len(redone), 8)                                  # only the unfinished scripts
        self.assertEqual(len(self.rows()), 12)

    def test_ctrl_c_in_the_middle_loses_only_the_script_in_progress(self):
        inner = th._fake_translate()
        n = [0]

        def interrupted(r_path, py_path, lib, cfg, *, learn):
            n[0] += 1
            if n[0] == 6:
                raise KeyboardInterrupt
            return inner(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", interrupted):
            with self.assertRaises(KeyboardInterrupt):
                ho.train(self.m, self.work, log=self._log)
        self.assertEqual(len(self.rows()), 5)
        redone: list = []
        with patch.object(ho, "_translate_once", th._fake_translate(learned=redone)):
            self.assertTrue(ho.train(self.m, self.work, log=self._log))
        self.assertEqual(len(redone), 7)
        self.assertEqual(sorted(Counter(r["script"] for r in self.rows()).values()), [1] * 12)


class TestParallelTraining(_Base):
    def test_the_driver_pauses_requeues_without_counting_and_resumes(self):
        calls = Counter()

        def fake_task(manifest, snapshot, script, py_path):
            calls[script] += 1
            if sum(calls.values()) <= 3:                                  # the first three tasks meet an outage
                return {"script": script, "provider_unavailable": {"credits": 1}, "seconds": 0.1}
            return {"script": script, "score": 0.9, "score_report": None, "seed_source": "x = 1",
                    "seed_score_report": None, "served": {}, "seconds": 0.1}

        class Pool(ThreadPoolExecutor):
            def __init__(self, max_workers=None, mp_context=None):
                super().__init__(max_workers=max_workers)

        with patch("concurrent.futures.ProcessPoolExecutor", Pool), patch.object(ho, "_train_task", fake_task), \
                patch("r2py.seed_from_translation", lambda *a, **k: None), patch.object(ho, "verify_inputs", lambda *a: None), \
                patch.object(ho, "provider_ok", self.provider([False, True])), patch.object(ho.time, "sleep"):
            finished = ho.train(self.m, self.work, workers=3, log=self._log, poll_s=1)
        self.assertTrue(finished)
        rows = self.rows()
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(r["attempt"] == 1 for r in rows))
        self.assertEqual(len(ho._read_jsonl(self.work / "train_events.jsonl")), 3)
        self.assertTrue(any("provider is back" in l for l in self.lines))


class TestScoring(_Base):
    def _trained(self):
        with patch.object(ho, "_translate_once", th._fake_translate()):
            ho.train(self.m, self.work, log=lambda *_: None)

    def test_an_outage_never_becomes_an_error_row_and_the_run_is_repeated(self):
        self._trained()
        inner = th._fake_translate(score=0.8)
        calls = [0]

        def flaky(r_path, py_path, lib, cfg, *, learn):
            calls[0] += 1
            if calls[0] <= 3:
                raise llm.ProviderUnavailable({"network": 1})
            return inner(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", flaky), patch.object(ho, "wait_for_provider", lambda *a, **k: True):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertEqual(len(rows), 24)
        self.assertTrue(all("error" not in r and r["attempts"] == 1 and r["score"] == 0.8 for r in rows))

    def test_giving_up_exits_without_writing_the_run_and_resumes(self):
        self._trained()

        def down(*a, **k):
            raise llm.ProviderUnavailable({"credits": 1})

        with patch.object(ho, "_translate_once", down), patch.object(ho, "wait_for_provider", lambda *a, **k: False):
            with self.assertRaises(SystemExit) as cm:
                ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        self.assertEqual(cm.exception.code, 3)
        self.assertEqual(ho._read_jsonl(self.work / "scores.jsonl"), [])
        with patch.object(ho, "_translate_once", th._fake_translate(score=0.7)):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        self.assertEqual(len(ho._read_jsonl(self.work / "scores.jsonl")), 24)


class TestTranslateOnceGuard(unittest.TestCase):
    def test_a_run_with_failed_provider_calls_is_not_a_result(self):
        cfg = {"model": "m", "max_iters": 1, "score_threshold": 0.9, "data_compare": "auto", "n_bare_seeds": 1,
               "n_structured_seeds": 1, "timeout_s": 5, "max_stalls": 1}
        result = SimpleNamespace(python_source="x = 1", final_score=0.0, iterations=0, final_score_report=None,
                                 seed_source="", score_history=[])

        def run_loop(*a, **k):
            llm._record_failure(RuntimeError("Error code: 402"))
            return result

        with tempfile.TemporaryDirectory() as d, patch("r2py.loop.run_loop", run_loop), \
                patch("r2py.stage1.analyze", lambda p: SimpleNamespace(entities={})):
            with self.assertRaises(llm.ProviderUnavailable) as cm:
                ho._translate_once(Path("a__b__c.R"), Path(d) / "o" / "c.py", object(), cfg, learn=True)
        self.assertEqual(cm.exception.kinds, {"credits": 1})
        self.assertFalse((Path(d) / "o" / "c.py").exists())      # nothing written, nothing learned


if __name__ == "__main__":
    unittest.main()
