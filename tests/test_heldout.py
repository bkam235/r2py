"""Tests for r2py/heldout.py — the held-out train/test experiment."""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from r2py import heldout as ho
from r2py.library import PatternLibrary
from r2py.library.pattern import Pattern, TranslationExample
from r2py.library.store import PatternStore
from r2py.types import EntityKind

# Three packages per stratum, plus three "other" packages, five scripts each.
_PACKAGES = [p for pkgs in ho.STRATA.values() for p in pkgs[:3]] + ["rlang", "testthat", "cli"]


def _make_pool(root: Path) -> Path:
    pool = root / "pool"
    pool.mkdir()
    for pkg in _PACKAGES:
        for i in range(5):
            (pool / f"{pkg}__rd_example__f{i}_Rd.R").write_text(f"x <- {i}\n", encoding="utf-8")
    return pool


def _select(pool: Path, **kw) -> dict:
    """12 held-out scripts (2 per stratum, 12 packages); one training script per package -> 12."""
    kw.setdefault("n_intervals", 2)  # empty / half / full keeps most tests small
    kw.setdefault("per_package", 1)
    return ho.select(pool, n_heldout=12, reps=2, **kw)


def _fake_translate(score: float = 1.0, learned: list | None = None, entities: list | None = None):
    """Stand-in for _translate_once that 'learns' a pattern whenever it is allowed to
    (learn=True) and vandalises the library when it isn't, to prove nothing sticks."""
    def fake(r_path, py_path, lib, cfg, *, learn):
        pid = f"pat-{r_path.stem}"
        lib.store.save(Pattern(id=pid, package="x", confidence="tentative", seed=True, guidance="g"))
        lib.index.rebuild(lib.store)
        if learned is not None:
            learned.append((r_path.name, learn))
        result = SimpleNamespace(final_score=score, iterations=1, final_exit_code=0, final_score_report=None)
        return result, list(entities or [])
    return fake


class TestSelect(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.pool = _make_pool(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_deterministic_for_a_seed(self):
        self.assertEqual(_select(self.pool, seed=1), _select(self.pool, seed=1))
        self.assertNotEqual(_select(self.pool, seed=1)["heldout"], _select(self.pool, seed=2)["heldout"])

    def test_sets_are_disjoint_and_sized(self):
        m = _select(self.pool)
        held = {e["script"] for e in m["heldout"]}
        train = {e["script"] for e in m["train"]}
        self.assertEqual((len(held), len(train)), (12, 12))
        self.assertFalse(held & train)

    def test_equal_quota_per_stratum_spread_across_packages(self):
        m = _select(self.pool)
        for s in ho.ALL_STRATA:
            picked = [e for e in m["heldout"] if e["stratum"] == s]
            self.assertEqual(len(picked), 2, s)
            self.assertEqual(len({e["package"] for e in picked}), 2, s)

    def test_training_comes_only_from_held_out_packages_up_to_the_quota(self):
        m = _select(self.pool, per_package=3)
        held_pkgs = {e["package"] for e in m["heldout"]}
        counts = Counter(e["package"] for e in m["train"])
        self.assertEqual(set(counts), held_pkgs)
        self.assertEqual(set(counts.values()), {3})
        self.assertEqual(m["train_packages"], dict(sorted(counts.items())))
        self.assertEqual(m["protocol"]["n_train"], 36)

    def test_a_package_with_fewer_spare_scripts_contributes_what_it_has(self):
        m = _select(self.pool, per_package=9)  # each package has only 4 spare (5 minus the held-out one)
        self.assertEqual(set(Counter(e["package"] for e in m["train"]).values()), {4})

    def test_training_order_is_interleaved_package_by_package(self):
        m = _select(self.pool, per_package=3)
        pkgs = [e["package"] for e in m["train"]]
        for k in (1, 2, 3):  # after k rounds every package has appeared exactly k times
            self.assertEqual(set(Counter(pkgs[:12 * k]).values()), {k})

    def test_checkpoints_and_hashes_recorded(self):
        m = _select(self.pool)
        self.assertEqual(m["checkpoints"], {"empty": 0, "half": 6, "full": 12})
        self.assertEqual(len(m["heldout"][0]["sha256"]), 64)

    def test_eighths_checkpoints_are_ordered_distinct_and_named(self):
        cps = _select(self.pool, n_intervals=8)["checkpoints"]
        self.assertEqual(list(cps), ["empty", "f1of8", "f2of8", "f3of8", "half",
                                     "f5of8", "f6of8", "f7of8", "full"])
        values = list(cps.values())
        self.assertEqual(values, sorted(set(values)))  # strictly increasing
        self.assertEqual((values[0], values[-1]), (0, 12))

    def test_too_few_training_scripts_for_the_intervals_raises(self):
        with self.assertRaises(ValueError):
            _select(self.pool, n_intervals=13)  # 12 training scripts

    def test_heldout_set_does_not_depend_on_the_training_draw(self):
        a = _select(self.pool, per_package=1, n_intervals=2)
        b = _select(self.pool, per_package=3, n_intervals=8)
        self.assertEqual(a["heldout"], b["heldout"])

    def test_too_few_scripts_in_a_stratum_raises(self):
        with self.assertRaises(ValueError):
            ho.select(self.pool, n_heldout=96, per_package=1)  # quota 16 > 15 per stratum

    def test_load_manifest_rejects_overlap(self):
        m = _select(self.pool)
        m["train"][0] = m["heldout"][0]
        path = Path(self._tmp.name) / "m.json"
        ho.write_manifest(m, path)
        with self.assertRaises(ValueError):
            ho.load_manifest(path)

    def test_verify_inputs_detects_changed_file(self):
        m = _select(self.pool)
        ho.verify_inputs(m, m["heldout"])
        (self.pool / m["heldout"][0]["script"]).write_text("changed <- 1\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            ho.verify_inputs(m, m["heldout"])


def _assign(name, rhs, pkg):
    return SimpleNamespace(name=name, package=None, kind=EntityKind.VARIABLE, rhs_call_name=rhs,
                           rhs_call_package=pkg, base_r_calls=["base::paste", "base::c"] if rhs == "paste" else [])


class TestEntityRecords(unittest.TestCase):
    def test_entity_score_averages_active_dimensions_and_is_zero_if_it_did_not_run(self):
        es = SimpleNamespace(executed_ok=True, active_dims=frozenset({"a", "b"}), a=1.0, b=0.5)
        self.assertEqual(ho.entity_score(es), 0.75)
        self.assertEqual(ho.entity_score(SimpleNamespace(executed_ok=False, active_dims=frozenset({"a"}), a=1.0)), 0.0)
        self.assertEqual(ho.entity_score(SimpleNamespace(executed_ok=True, active_dims=frozenset())), 1.0)

    def test_records_carry_the_key_the_informative_calls_and_the_score(self):
        script_map = SimpleNamespace(entities={
            "e1": _assign("x", "paste", "base"),
            "e2": SimpleNamespace(name="dplyr", package="dplyr", kind=EntityKind.LIBRARY_IMPORT, base_r_calls=[]),
            "e3": SimpleNamespace(name="mutate", package="dplyr", kind=EntityKind.FUNCTION_CALL, base_r_calls=[]),
            "e4": SimpleNamespace(name="q", package=None, kind=EntityKind.VARIABLE, base_r_calls=[]),
        })
        es = lambda ok: SimpleNamespace(executed_ok=ok, active_dims=frozenset({"d"}), d=0.8)
        report = SimpleNamespace(by_entity={"e1": es(True), "e2": es(True), "e3": es(False)},
                                 uncomparable=["e3"])  # e4 not scored
        recs = {r["id"]: r for r in ho._entity_records(script_map, report)}
        self.assertEqual(set(recs), {"e1", "e3"})  # imports and unscored entities left out
        self.assertEqual(recs["e1"], {"id": "e1", "name": "x", "key": "base.paste",
                                      "calls": ["base.paste"], "score": 0.8,  # c() is not informative
                                      "active_dims": ["d"], "dim_scores": {"d": 0.8},
                                      "executed_ok": True, "uncomparable": False})
        self.assertTrue(recs["e3"]["uncomparable"])
        self.assertEqual((recs["e3"]["key"], recs["e3"]["score"]), ("dplyr.mutate", 0.0))

    def test_no_records_without_a_report(self):
        self.assertEqual(ho._entity_records(SimpleNamespace(entities={"e": _assign("x", "paste", "base")}), None), [])


class TestTranslateOnce(unittest.TestCase):
    """The one function that touches the real pipeline; autospec catches signature drift."""

    def _run(self, *, learn: bool, score: float):
        import r2py
        import r2py.loop
        import r2py.stage1
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        fake = SimpleNamespace(python_source="x = 1\n", final_score=score, final_score_report=None,
                               seed_source="", score_history=[], iterations=1)
        cfg = ho.DEFAULT_PROTOCOL["translate"]
        with patch.object(r2py.stage1, "analyze", autospec=True), \
             patch.object(r2py.loop, "run_loop", autospec=True, return_value=fake) as loop, \
             patch.object(r2py, "seed_from_translation", autospec=True) as seed:
            out = ho._translate_once(Path("a__b__c.R"), Path(tmp.name) / "o" / "c.py", object(), cfg, learn=learn)
        self.last_out = out
        return loop, seed

    def test_returns_the_result_and_entity_records(self):
        self._run(learn=False, score=0.7)
        result, records = self.last_out
        self.assertEqual(result.final_score, 0.7)
        self.assertEqual(records, [])

    def test_learn_seeds_library_from_every_script_entity_threshold_filters(self):
        _, seed = self._run(learn=True, score=0.95)
        seed.assert_called_once()
        self.assertEqual(seed.call_args.kwargs["script_id"], "a__b__c")
        # No script-level gate (patch 01): seed_from_translation filters per entity.
        _, seed = self._run(learn=True, score=0.5)
        seed.assert_called_once()

    def test_scoring_never_seeds_library(self):
        _, seed = self._run(learn=False, score=1.0)
        seed.assert_not_called()

    def test_learning_passes_the_pre_agent_translation_for_corrections(self):
        import r2py
        import r2py.loop
        import r2py.stage1
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        fake = SimpleNamespace(python_source="final\n", final_score=0.95, final_score_report="final report",
                               seed_source="seed src", score_history=["seed report", "final report"],
                               iterations=1)
        with patch.object(r2py.stage1, "analyze", autospec=True), \
             patch.object(r2py.loop, "run_loop", autospec=True, return_value=fake), \
             patch.object(r2py, "seed_from_translation", autospec=True) as seed, \
             patch.object(ho, "_entity_records", return_value=[]):
            ho._translate_once(Path("a__b__c.R"), Path(tmp.name) / "o" / "c.py", object(),
                               ho.DEFAULT_PROTOCOL["translate"], learn=True)
        kw = seed.call_args.kwargs
        self.assertEqual((kw["seed_source"], kw["seed_score_report"]), ("seed src", "seed report"))

    def test_run_loop_gets_protocol_settings(self):
        loop, _ = self._run(learn=False, score=0.1)
        kw = loop.call_args.kwargs
        cfg = ho.DEFAULT_PROTOCOL["translate"]
        self.assertEqual((kw["model"], kw["escalation_model"]), (cfg["model"], cfg["model"]))
        self.assertEqual(kw["score_threshold"], cfg["score_threshold"])


class TestTrainAndScore(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.m = _select(_make_pool(root))
        self.work = root / "work"
        self.lines: list[str] = []

    def tearDown(self):
        self._tmp.cleanup()

    def _log(self, *args):
        self.lines.append(" ".join(str(a) for a in args))

    def _train(self, fake=None, **kw):
        learned: list = []
        with patch.object(ho, "_translate_once", fake or _fake_translate(learned=learned, **kw)):
            ho.train(self.m, self.work, log=self._log)
        return learned

    def _count(self, cp):
        return len(PatternLibrary(self.work / "checkpoints" / cp).store.list_ids())

    def test_train_snapshots_empty_half_full(self):
        learned = self._train()
        self.assertTrue(all(flag for _, flag in learned))
        self.assertEqual({cp: self._count(cp) for cp in ("empty", "half", "full")},
                         {"empty": 0, "half": 6, "full": 12})

    def test_train_snapshots_every_checkpoint_of_a_finer_grid(self):
        root8 = Path(self._tmp.name) / "p8"
        root8.mkdir()
        self.m = _select(_make_pool(root8), n_intervals=8)
        self._train()
        self.assertEqual({cp: self._count(cp) for cp in self.m["checkpoints"]}, self.m["checkpoints"])

    def test_train_never_touches_heldout_scripts(self):
        learned = self._train()
        held = {e["script"] for e in self.m["heldout"]}
        self.assertFalse({name for name, _ in learned} & held)

    def test_train_resumes_without_redoing_work(self):
        self._train()
        self.assertEqual(self._train(), [])

    def test_train_prints_progress_after_every_script(self):
        self._train()
        done = [l for l in self.lines if l.startswith("[train ") and "%]" in l]
        self.assertEqual(len(done), 12)
        self.assertTrue(done[-1].startswith("[train 12/12 100%]"))
        self.assertIn("ETA 0m00s", done[-1])
        self.assertTrue(all("avg" in l and "active" in l and "ETA" in l for l in done))
        self.assertIn("train: 0/12 already finished, 12 to go", self.lines[0])

    def test_train_rows_record_the_time_taken(self):
        self._train()
        rows = ho._read_jsonl(self.work / "train_progress.jsonl")
        self.assertTrue(all(r["seconds"] >= 0 and r["attempt"] == 1 for r in rows))

    def test_a_failing_script_is_retried_once_then_recorded_as_failed(self):
        calls = Counter()
        bad = self.m["train"][3]["script"]

        def flaky(r_path, py_path, lib, cfg, *, learn):
            calls[r_path.name] += 1
            if r_path.name == bad:
                raise RuntimeError("api down")
            return _fake_translate()(r_path, py_path, lib, cfg, learn=learn)

        self._train(fake=flaky)
        self.assertEqual(calls[bad], ho.MAX_ATTEMPTS)
        self.assertTrue(any("FAILED after retries" in l for l in self.lines))
        self.assertEqual(self._count("full"), 11)  # the other eleven still learned
        self._train(fake=flaky)                    # resuming does not try the failed script again
        self.assertEqual(calls[bad], ho.MAX_ATTEMPTS)

    def test_a_script_that_succeeds_on_the_retry_counts_as_learned(self):
        calls = Counter()
        flaky_script = self.m["train"][0]["script"]

        def once(r_path, py_path, lib, cfg, *, learn):
            calls[r_path.name] += 1
            if r_path.name == flaky_script and calls[r_path.name] == 1:
                raise RuntimeError("transient")
            return _fake_translate()(r_path, py_path, lib, cfg, learn=learn)

        self._train(fake=once)
        self.assertEqual(calls[flaky_script], 2)
        self.assertEqual(self._count("full"), 12)
        self.assertFalse(any("FAILED" in l for l in self.lines))

    def test_score_leaves_checkpoints_untouched_and_isolates_runs(self):
        self._train()
        before = {cp: ho.library_hash(self.work / "checkpoints" / cp) for cp in ("empty", "full")}
        seen: list[int] = []

        def vandal(r_path, py_path, lib, cfg, *, learn):
            self.assertFalse(learn)
            seen.append(len(lib.store.list_ids()))  # would grow if runs leaked into each other
            return _fake_translate()(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", vandal):
            ho.score(self.m, self.work, ["empty", "full"], log=lambda *_: None)

        after = {cp: ho.library_hash(self.work / "checkpoints" / cp) for cp in ("empty", "full")}
        self.assertEqual(before, after)
        # Every run started from a pristine checkpoint: 0 patterns for empty, 12 for full.
        self.assertEqual(sorted(set(seen)), [0, 12])
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertEqual(len(rows), 12 * 2 * 2)  # scripts x reps x checkpoints

    def test_score_rows_record_entities_time_and_attempts(self):
        PatternLibrary(self.work / "checkpoints" / "empty")
        ents = [{"id": "e1", "name": "x", "key": "base.paste", "calls": [], "score": 0.5}]
        with patch.object(ho, "_translate_once", _fake_translate(entities=ents)):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        row = ho._read_jsonl(self.work / "scores.jsonl")[0]
        self.assertEqual((row["entities"], row["attempts"]), (ents, 1))
        self.assertGreaterEqual(row["seconds"], 0)

    def test_score_prints_progress_and_running_means(self):
        self._train()
        self.lines.clear()
        with patch.object(ho, "_translate_once", _fake_translate(score=0.8)):
            ho.score(self.m, self.work, ["empty", "full"], log=self._log)
        done = [l for l in self.lines if l.startswith("[score ") and "%]" in l]
        self.assertEqual(len(done), 48)
        self.assertTrue(done[-1].startswith("[score 48/48 100%]"))
        means = [l for l in self.lines if "running means" in l]
        self.assertEqual(len(means), 2)  # after run 20 and 40
        self.assertIn("empty 0.800", means[-1])
        self.assertIn("full 0.800", means[-1])

    def test_score_retries_an_erroring_run_once_and_records_the_error_if_it_persists(self):
        self._train()
        calls = Counter()

        def boom(r_path, *a, **k):
            calls[r_path.name] += 1
            raise RuntimeError("api down")

        with patch.object(ho, "_translate_once", boom):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertTrue(all("error" in r and "score" not in r and r["attempts"] == ho.MAX_ATTEMPTS for r in rows))
        self.assertEqual(sum(calls.values()), len(rows) * ho.MAX_ATTEMPTS)

        # Resuming re-runs nothing that already has a row.
        again: list = []
        with patch.object(ho, "_translate_once", lambda *a, **k: again.append(1)):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        self.assertEqual(again, [])

    def test_a_run_that_succeeds_on_the_retry_writes_a_clean_row(self):
        PatternLibrary(self.work / "checkpoints" / "empty")
        seen = Counter()

        def once(r_path, py_path, lib, cfg, *, learn):
            seen[r_path.name] += 1
            if seen[r_path.name] % 2 == 1:
                raise RuntimeError("transient")
            return _fake_translate()(r_path, py_path, lib, cfg, learn=learn)

        with patch.object(ho, "_translate_once", once):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertTrue(all("error" not in r and r["attempts"] == 2 and r["score"] == 1.0 for r in rows))

    def test_score_requires_checkpoint(self):
        with self.assertRaises(FileNotFoundError):
            ho.score(self.m, self.work, ["full"], log=lambda *_: None)


class TestScoreOrder(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.m = _select(_make_pool(root))
        self.work = root / "work"

    def tearDown(self):
        self._tmp.cleanup()

    def test_each_script_once_per_rep_with_all_checkpoints_adjacent(self):
        cps = ["empty", "half", "full"]
        order = ho.score_order(self.m, cps, 0)
        self.assertEqual(len(order), 12 * 3)
        for i in range(0, len(order), 3):
            self.assertEqual(len({e["script"] for e, _ in order[i:i + 3]}), 1)
            self.assertEqual(sorted(cp for _, cp in order[i:i + 3]), sorted(cps))
        self.assertEqual({e["script"] for e, _ in order}, {e["script"] for e in self.m["heldout"]})

    def test_reproducible_and_varies_by_rep_and_seed(self):
        cps = ["empty", "full"]
        self.assertEqual(ho.score_order(self.m, cps, 0), ho.score_order(self.m, cps, 0))
        self.assertNotEqual(ho.score_order(self.m, cps, 0), ho.score_order(self.m, cps, 1))
        other = {**self.m, "protocol": {**self.m["protocol"], "seed": 1}}
        self.assertNotEqual(ho.score_order(self.m, cps, 0), ho.score_order(other, cps, 0))

    def test_no_checkpoint_is_always_first(self):
        firsts = {ho.score_order(self.m, ["empty", "full"], r)[i][1]
                  for r in range(2) for i in range(0, 24, 2)}
        self.assertEqual(firsts, {"empty", "full"})

    def test_resumed_run_continues_the_same_sequence(self):
        for cp in ("empty", "full"):
            PatternLibrary(self.work / "checkpoints" / cp)
        calls: list = []

        def recorder(stop_after=None):
            def fake(r_path, py_path, lib, cfg, *, learn):
                if stop_after is not None and len(calls) >= stop_after:
                    raise KeyboardInterrupt
                calls.append((r_path.name, py_path.parent.parent.name, py_path.parent.name))
                return (SimpleNamespace(final_score=1.0, iterations=1, final_exit_code=0,
                                        final_score_report=None), [])
            return fake

        with patch.object(ho, "_translate_once", recorder(stop_after=7)):
            with self.assertRaises(KeyboardInterrupt):
                ho.score(self.m, self.work, ["empty", "full"], log=lambda *_: None)
        with patch.object(ho, "_translate_once", recorder()):
            ho.score(self.m, self.work, ["empty", "full"], log=lambda *_: None)

        expected = [(e["script"], cp, f"rep{rep}") for rep in range(2)
                    for e, cp in ho.score_order(self.m, ["empty", "full"], rep)]
        self.assertEqual(calls, expected)

    def test_rows_record_order_seed_and_llm_settings(self):
        PatternLibrary(self.work / "checkpoints" / "empty")
        with patch.object(ho, "_translate_once", _fake_translate()):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        row = ho._read_jsonl(self.work / "scores.jsonl")[0]
        self.assertEqual(row["order_seed"], f"{self.m['protocol']['seed']}:score:0")
        self.assertEqual(row["llm"], ho.LLM_SETTINGS)


class TestPinnedLlm(unittest.TestCase):
    """Runs the harness's real OpenRouter code path against a fake openai client."""

    def _fake_openai(self, sent: list):
        class Completions:
            def create(self, **kw):
                sent.append(kw)
                msg = SimpleNamespace(content="print(1)")
                return SimpleNamespace(choices=[SimpleNamespace(finish_reason="stop", message=msg)],
                                       provider="Novita")

        class FakeOpenAI:
            def __init__(self, **kw):
                self.chat = SimpleNamespace(completions=Completions())
        return FakeOpenAI

    def test_requests_carry_temperature_provider_pin_and_a_timeout(self):
        import openai
        from r2py.stage2 import llm
        sent: list = []
        with patch.object(openai, "OpenAI", self._fake_openai(sent)), \
             patch.dict(os.environ, {"OPENROUTER_API_KEY": "k"}):
            with ho.pinned_llm("openrouter:google/gemma-4-31b-it") as served:
                out = llm.call([{"role": "user", "content": "hi"}], "sys",
                               model="openrouter:google/gemma-4-31b-it")
        self.assertEqual(out, "print(1)")
        kw = sent[0]
        self.assertEqual(kw["temperature"], ho.LLM_SETTINGS["temperature"])
        self.assertEqual(kw["timeout"], ho.LLM_SETTINGS["request_timeout_s"])
        self.assertEqual(kw["extra_body"]["provider"], ho.LLM_SETTINGS["provider"])
        self.assertFalse(kw["extra_body"]["provider"]["allow_fallbacks"])
        self.assertEqual(kw["model"], "google/gemma-4-31b-it")  # harness behaviour untouched
        self.assertEqual(dict(served), {"Novita": 1})

    def test_cached_unpinned_client_is_not_reused_and_state_is_restored(self):
        import openai
        from r2py.stage2 import llm
        sent: list = []
        fake = self._fake_openai(sent)
        with patch.object(openai, "OpenAI", fake), patch.dict(os.environ, {"OPENROUTER_API_KEY": "k"}):
            llm._openrouter_clients["k"] = fake()  # an unpinned client cached earlier
            with ho.pinned_llm("openrouter:m"):
                llm.call([{"role": "user", "content": "hi"}], "sys", model="openrouter:m")
            self.assertIn("temperature", sent[0])
            self.assertIs(openai.OpenAI, fake)
            self.assertEqual(llm._openrouter_clients, {})

    def test_refuses_models_it_cannot_pin(self):
        with self.assertRaises(ValueError):
            with ho.pinned_llm("claude-haiku-4-5"):
                pass


# ---------------------------------------------------------------------------
# analyze
# ---------------------------------------------------------------------------

ENTITY_TEMPLATES = [
    {"id": "t1", "name": "x", "key": "base.paste", "calls": []},                  # own function has a pattern
    {"id": "t2", "name": "y", "key": None, "calls": ["base.format"]},             # a base function inside does
    {"id": "n1", "name": "z", "key": "dplyr.zzz", "calls": []},                   # nothing in the library
    {"id": "b1", "name": "suppressPackageStartupMessages", "key": "base.suppresspackagestartupmessages",
     "calls": []},                                                                # boilerplate: always left out
]


def _library(root: Path) -> Path:
    """A 'full' library holding patterns for base.paste and base.format (and one with only a fix)."""
    store = PatternStore(root)
    ex = TranslationExample("h", "r", "p", 1.0, "s")
    for pid in ("base.paste", "base.format", "base.suppresspackagestartupmessages"):
        store.save(Pattern(id=pid, package="base", confidence="tentative", seed=True, guidance="g",
                           translation_examples=[ex]))
    store.save(Pattern(id="dplyr.zzz", package="dplyr", confidence="tentative", seed=True, guidance="g"))
    return root


def _write_rows(path: Path, manifest: dict, fn, *, templates=ENTITY_TEMPLATES, checkpoints=("empty", "half", "full")):
    """fn(script index, checkpoint, rep, entity template) -> entity score, or None for an errored run."""
    for rep in range(manifest["protocol"]["reps"]):
        for i, e in enumerate(manifest["heldout"]):
            for cp in checkpoints:
                scores = [fn(i, cp, rep, t) for t in templates]
                row = {"checkpoint": cp, "script": e["script"], "rep": rep, "harness_hash": "h"}
                if any(s is None for s in scores):
                    row["error"] = "x"
                else:
                    row["score"] = sum(scores) / len(scores)
                    row["entities"] = [dict(t, score=s) for t, s in zip(templates, scores)]
                ho._append_jsonl(path, row)


GAIN = {"empty": 0.0, "half": 0.15, "full": 0.3}


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.pool = _make_pool(root)
        self.m = _select(self.pool)
        self.path = root / "scores.jsonl"
        self.lib = _library(root / "full")

    def tearDown(self):
        self._tmp.cleanup()

    def _improving(self, i, cp, rep, t):
        """Targetable entities improve with training; the others do not."""
        base = 0.4 + 0.01 * i + 0.005 * rep
        return base + (GAIN[cp] if t["id"] in ("t1", "t2") else 0.0)

    def test_targetable_endpoint_is_the_primary_and_ignores_other_entities(self):
        _write_rows(self.path, self.m, self._improving)
        a = ho.analyze(self.m, self.path, self.lib)
        p = a["primary"]
        self.assertEqual(p["n_paired"], 12)
        self.assertAlmostEqual(p["mean_diff"], 0.3)   # only t1 and t2, on which the gain is 0.3
        self.assertTrue(p["test"]["significant"])
        self.assertLess(p["test"]["p_value"], 0.001)
        self.assertAlmostEqual(a["control"]["mean_diff"], 0.0)   # n1: the library had nothing for it
        self.assertAlmostEqual(a["share_targetable"], 2 / 3)

    def test_the_script_aggregate_is_the_secondary_and_is_diluted(self):
        _write_rows(self.path, self.m, self._improving)
        a = ho.analyze(self.m, self.path, self.lib)
        # aggregate over all four entities: 0.3 gain on t1, t2 only -> 0.15 on average
        self.assertAlmostEqual(a["script_aggregate"]["mean_diff"], 0.15)
        self.assertLess(a["script_aggregate"]["mean_diff"], a["primary"]["mean_diff"])

    def test_the_boilerplate_entity_is_left_out_of_every_entity_endpoint(self):
        _write_rows(self.path, self.m, lambda i, cp, rep, t: 1.0 if t["id"] == "b1" else 0.5)
        a = ho.analyze(self.m, self.path, self.lib)
        self.assertAlmostEqual(a["primary"]["mean_before"], 0.5)   # b1 (score 1.0) is not averaged in
        self.assertAlmostEqual(a["control"]["mean_before"], 0.5)

    def test_scripts_with_no_targetable_entity_are_excluded_from_the_primary(self):
        only_untargetable = [ENTITY_TEMPLATES[2]]
        _write_rows(self.path, self.m, lambda i, cp, rep, t: 0.5 + GAIN[cp], templates=only_untargetable)
        a = ho.analyze(self.m, self.path, self.lib)
        self.assertEqual(a["primary"]["n_paired"], 0)
        self.assertEqual(a["control"]["n_paired"], 12)

    def test_entities_are_compared_on_the_same_entities_at_both_checkpoints(self):
        # t2 is only scored at 'full': it must not leak into the empty-vs-full comparison.
        for rep in range(2):
            for e in self.m["heldout"]:
                for cp in ("empty", "full"):
                    ents = [dict(ENTITY_TEMPLATES[0], score=0.4 if cp == "empty" else 0.6)]
                    if cp == "full":
                        ents.append(dict(ENTITY_TEMPLATES[1], score=1.0))
                    ho._append_jsonl(self.path, {"checkpoint": cp, "script": e["script"], "rep": rep,
                                                 "harness_hash": "h", "score": 0.5, "entities": ents})
        a = ho.analyze(self.m, self.path, self.lib)
        self.assertAlmostEqual(a["primary"]["mean_diff"], 0.2)

    def test_reps_are_averaged_and_errored_runs_are_dropped(self):
        def fn(i, cp, rep, t):
            if rep == 0 and i < 2:
                return None                                    # errored: those two scripts keep only rep 1
            return 0.4 + (0.3 if cp == "full" and t["id"] in ("t1", "t2") else 0.0) + 0.1 * rep
        _write_rows(self.path, self.m, fn)
        a = ho.analyze(self.m, self.path, self.lib)
        self.assertEqual(a["primary"]["n_paired"], 12)
        self.assertAlmostEqual(a["primary"]["mean_diff"], 0.3)
        self.assertEqual(a["n_errored_runs"], 2 * 3)

    def test_no_effect_is_not_significant_and_the_test_is_one_sided(self):
        _write_rows(self.path, self.m, lambda i, cp, rep, t: 0.5 + (0.05 if i % 2 else -0.05) * (cp == "full"))
        self.assertFalse(ho.analyze(self.m, self.path, self.lib)["primary"]["test"]["significant"])
        down = self.path.with_name("down.jsonl")
        _write_rows(down, self.m, lambda i, cp, rep, t: 0.8 - 0.1 * (cp == "full") - 0.001 * i)
        self.assertGreater(ho.analyze(self.m, down, self.lib)["primary"]["test"]["p_value"], 0.95)

    def test_trend_over_nine_checkpoints_on_the_primary_endpoint(self):
        m9 = _select(self.pool, n_intervals=8)
        names = list(m9["checkpoints"])
        path = self.path.with_name("nine.jsonl")
        _write_rows(path, m9, lambda i, cp, rep, t: 0.3 + (0.05 * names.index(cp) if t["id"] in ("t1", "t2") else 0.0)
                    + 0.001 * i, checkpoints=names)
        a = ho.analyze(m9, path, self.lib)
        tr = a["primary"]["trend"]
        self.assertEqual(tr["checkpoints"], names)
        self.assertEqual(tr["n_strictly_increasing"], 12)
        self.assertLess(tr["p_value"], 0.001)
        curve = list(tr["mean_by_checkpoint"].values())
        self.assertEqual(curve, sorted(curve))
        self.assertAlmostEqual(a["primary"]["mean_diff"], 0.4)  # empty vs full: 8 steps x 0.05

    def test_without_the_library_only_the_script_aggregate_is_computed(self):
        _write_rows(self.path, self.m, self._improving)
        a = ho.analyze(self.m, self.path)
        self.assertIsNone(a["primary"])
        self.assertEqual(a["script_aggregate"]["n_paired"], 12)

    def test_targetable_ids_are_the_patterns_that_hold_a_verified_example_and_nothing_is_written(self):
        before = sorted(p.name for p in self.lib.rglob("*"))
        ids = ho.targetable_ids(self.lib)
        self.assertEqual(ids, {"base.paste", "base.format", "base.suppresspackagestartupmessages"})
        self.assertEqual(before, sorted(p.name for p in self.lib.rglob("*")))  # no index.json created

    def test_rank_biserial_hand_cases(self):
        self.assertEqual(ho._rank_biserial([0.1, 0.2, 0.3]), 1.0)
        self.assertEqual(ho._rank_biserial([-0.1, -0.2]), -1.0)
        self.assertEqual(ho._rank_biserial([0.1, 0.2, -0.3]), 0.0)
        self.assertAlmostEqual(ho._rank_biserial([0.0, 0.1, -0.2]), -1 / 3)

    def test_reports_both_p_values_and_effect_size(self):
        _write_rows(self.path, self.m, lambda i, cp, rep, t: 0.5 + 0.3 * (cp == "full") + 0.01 * i)
        t = ho.analyze(self.m, self.path, self.lib)["primary"]["test"]
        self.assertLess(t["p_value"], t["p_value_two_sided"])
        self.assertAlmostEqual(t["p_value_two_sided"], 2 * t["p_value"], places=6)
        self.assertEqual(t["rank_biserial"], 1.0)

    def test_all_zero_diffs_have_no_effect_size(self):
        _write_rows(self.path, self.m, lambda i, cp, rep, t: 0.5)
        t = ho.analyze(self.m, self.path, self.lib)["primary"]["test"]
        self.assertEqual((t["p_value"], t["p_value_two_sided"], t["rank_biserial"]), (1.0, 1.0, None))

    def test_report_renders_all_three_endpoints(self):
        _write_rows(self.path, self.m, self._improving)
        text = ho.format_report(ho.analyze(self.m, self.path, self.lib), self.m)
        for word in ("PRIMARY", "CONTROL", "SECONDARY", "Wilcoxon", "by checkpoint", "trend over 3 checkpoints"):
            self.assertIn(word, text)

    def test_report_without_a_library_says_so(self):
        _write_rows(self.path, self.m, self._improving)
        self.assertIn("not computed", ho.format_report(ho.analyze(self.m, self.path), self.m))


# ---------------------------------------------------------------------------
# progress / status
# ---------------------------------------------------------------------------

class TestProgress(unittest.TestCase):
    def test_durations_format(self):
        self.assertEqual(ho._fmt_duration(65), "1m05s")
        self.assertEqual(ho._fmt_duration(3 * 3600 + 7 * 60 + 9), "3h07m")
        self.assertEqual(ho._fmt_duration(0), "0m00s")

    def test_progress_line_estimates_the_time_left_from_the_average_run(self):
        line = ho._progress_line("train", 2, 10, [60.0, 120.0])
        self.assertEqual(line, "[train 2/10 20%] last 2m00s | avg 1m30s | active 3m00s | ETA 12m00s")

    def test_progress_summary_is_computed_from_the_result_files(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            root = Path(tmp)
            m = _select(_make_pool(root))
            work = root / "work"
            train = m["train"]
            rows = [{"script": train[0]["script"], "score": 0.9, "patterns": 3, "seconds": 100.0, "timestamp": "t1"},
                    {"script": train[1]["script"], "error": "x", "seconds": 20.0, "timestamp": "t2"},
                    {"script": train[1]["script"], "error": "x", "seconds": 20.0, "timestamp": "t3"},   # 2nd failure: finished
                    {"script": train[2]["script"], "error": "x", "seconds": 20.0, "timestamp": "t4"}]   # 1st failure: not yet
            for r in rows:
                ho._append_jsonl(work / "train_progress.jsonl", r)
            cps = list(m["checkpoints"])
            for i, cp in enumerate(cps[:2]):
                ho._append_jsonl(work / "scores.jsonl", {"checkpoint": cp, "script": "s", "rep": 0, "score": 0.5 + 0.1 * i,
                                                          "seconds": 50.0, "timestamp": "t5"})
            ho._append_jsonl(work / "scores.jsonl", {"checkpoint": cps[0], "script": "s2", "rep": 0, "error": "x",
                                                      "seconds": 5.0, "timestamp": "t6"})
            p = ho.progress(m, work)
            self.assertEqual((p["train"]["done"], p["train"]["failed"], p["train"]["total"], p["train"]["patterns"]),
                             (2, 1, 12, 3))
            self.assertEqual((p["score"]["done"], p["score"]["errors"], p["score"]["total"]),
                             (3, 1, 2 * 12 * 3))
            self.assertAlmostEqual(p["score"]["by_checkpoint"][cps[1]]["mean"], 0.6)
            text = ho.format_progress(p)
            self.assertIn("Training: 2/12 (17%)   failed: 1   patterns: 3", text)
            self.assertIn("Scoring: 3/72 (4%)   errored runs: 1", text)
            self.assertIn(f"{cps[1]} 0.600 (n=1)", text)

    def test_status_before_anything_ran(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            root = Path(tmp)
            m = _select(_make_pool(root))
            text = ho.format_progress(ho.progress(m, root / "work"))
            self.assertIn("Training: 0/12 (0%)", text)
            self.assertIn("(not started)", text)


if __name__ == "__main__":
    unittest.main()


class TestParallelScore(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.m = _select(_make_pool(root))
        self.work = root / "work"
        for cp in ("empty", "full"):
            PatternLibrary(self.work / "checkpoints" / cp)

    def tearDown(self):
        self._tmp.cleanup()

    def _run_workers(self, n, fake):
        import threading
        claims = self.work / "claims"
        claims.mkdir(parents=True, exist_ok=True)
        cps = ["empty", "full"]
        threads = [threading.Thread(target=ho._score_loop, args=(self.m, self.work, cps), kwargs=dict(
            out=self.work / f"scores.w{i}.jsonl", claims=claims, worker=i, workers=n, log=lambda *_: None))
            for i in range(n)]
        with patch.object(ho, "_translate_once", fake):
            for t in threads:
                t.start()
            for t in threads:
                t.join()

    def test_claim_can_be_taken_once(self):
        claims = self.work / "claims"
        claims.mkdir(parents=True)
        self.assertTrue(ho._claim(claims, 0, "empty", "a.R"))
        self.assertFalse(ho._claim(claims, 0, "empty", "a.R"))
        self.assertTrue(ho._claim(claims, 1, "empty", "a.R"))

    def test_workers_share_the_runs_and_score_each_exactly_once(self):
        import time as _t
        inner = _fake_translate()

        def slow(*a, **kw):
            _t.sleep(0.01)
            return inner(*a, **kw)

        self._run_workers(3, slow)
        rows = ho.read_scores(self.work / "scores.jsonl")
        keys = [(r["checkpoint"], r["script"], r["rep"]) for r in rows]
        n_runs = self.m["protocol"]["reps"] * len(self.m["heldout"]) * 2
        self.assertEqual(len(keys), n_runs)
        self.assertEqual(len(set(keys)), n_runs)
        self.assertGreater(len({r["worker"] for r in rows}), 1)  # the work really was spread

    def test_a_restart_skips_what_any_worker_already_scored(self):
        self._run_workers(2, _fake_translate())
        shutil.rmtree(self.work / "claims")  # what score() does at the start of a session
        calls: list = []

        def counting(*a, **kw):
            calls.append(1)
            return _fake_translate()(*a, **kw)

        self._run_workers(2, counting)
        self.assertEqual(calls, [])

    def test_analysis_and_status_read_the_worker_files(self):
        self._run_workers(2, _fake_translate())
        p = ho.progress(self.m, self.work)
        self.assertEqual(p["score"]["done"], self.m["protocol"]["reps"] * len(self.m["heldout"]) * 2)
        self.assertEqual(p["score"]["workers"], 2)

    def test_wall_clock_estimates_divide_by_the_number_of_workers(self):
        self.assertEqual(ho._progress_line("score", 2, 10, [60.0, 120.0], workers=3),
                         "[score 2/10 20%] last 2m00s | avg 1m30s | active 1m00s | ETA 4m00s")


class TestRateLimit(unittest.TestCase):
    def test_a_429_is_waited_out_and_a_persistent_one_is_raised(self):
        import openai
        calls = {"n": 0}

        class Flaky:
            def __init__(self, fail_times):
                self.fail_times = fail_times
                self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

            def create(self, **kw):
                calls["n"] += 1
                if calls["n"] <= self.fail_times:
                    raise openai.RateLimitError("slow down", response=SimpleNamespace(
                        request=None, status_code=429, headers={}), body=None)
                return SimpleNamespace(provider="Novita")

        with patch.object(ho.time, "sleep") as sleep:
            client = ho._PinnedClient(Flaky(2), ho.LLM_SETTINGS, Counter())
            client._create(model="m")
            self.assertEqual([c.args[0] for c in sleep.call_args_list],
                             [ho.RATE_LIMIT_WAIT_S, 2 * ho.RATE_LIMIT_WAIT_S])
            calls["n"] = 0
            with self.assertRaises(openai.RateLimitError):
                ho._PinnedClient(Flaky(99), ho.LLM_SETTINGS, Counter())._create(model="m")
            self.assertEqual(calls["n"], ho.RATE_LIMIT_TRIES)
