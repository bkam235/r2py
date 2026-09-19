"""Tests for r2py/heldout.py — the held-out train/test experiment."""
from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from r2py import heldout as ho
from r2py.library import PatternLibrary
from r2py.library.pattern import Pattern

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
    return ho.select(pool, n_heldout=12, n_train=10, reps=2, **kw)


def _fake_translate(score: float = 1.0, learned: list | None = None):
    """Stand-in for _translate_once that 'learns' a pattern whenever it is allowed to
    (learn=True) and vandalises the library when it isn't, to prove nothing sticks."""
    def fake(r_path, py_path, lib, cfg, *, learn):
        pid = f"pat-{r_path.stem}"
        lib.store.save(Pattern(id=pid, package="x", confidence="tentative", seed=True, guidance="g"))
        lib.index.rebuild(lib.store)
        if learned is not None:
            learned.append((r_path.name, learn))
        return SimpleNamespace(final_score=score, iterations=1, final_exit_code=0,
                               final_score_report=None)
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
        self.assertEqual((len(held), len(train)), (12, 10))
        self.assertFalse(held & train)

    def test_equal_quota_per_stratum_spread_across_packages(self):
        m = _select(self.pool)
        for s in ho.ALL_STRATA:
            picked = [e for e in m["heldout"] if e["stratum"] == s]
            self.assertEqual(len(picked), 2, s)
            self.assertEqual(len({e["package"] for e in picked}), 2, s)

    def test_checkpoints_and_hashes_recorded(self):
        m = _select(self.pool)
        self.assertEqual(m["checkpoints"], {"empty": 0, "half": 5, "full": 10})
        self.assertEqual(len(m["heldout"][0]["sha256"]), 64)

    def test_too_few_scripts_in_a_stratum_raises(self):
        with self.assertRaises(ValueError):
            ho.select(self.pool, n_heldout=96, n_train=10)  # quota 16 > 15 per stratum

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


class TestTranslateOnce(unittest.TestCase):
    """The one function that touches the real pipeline; autospec catches signature drift."""

    def _run(self, *, learn: bool, score: float):
        import r2py
        import r2py.loop
        import r2py.stage1
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        fake = SimpleNamespace(python_source="x = 1\n", final_score=score, final_score_report=None)
        cfg = ho.DEFAULT_PROTOCOL["translate"]
        with patch.object(r2py.stage1, "analyze", autospec=True), \
             patch.object(r2py.loop, "run_loop", autospec=True, return_value=fake) as loop, \
             patch.object(r2py, "seed_from_translation", autospec=True) as seed:
            ho._translate_once(Path("a__b__c.R"), Path(tmp.name) / "o" / "c.py", object(), cfg, learn=learn)
        return loop, seed

    def test_learn_seeds_library_only_at_or_above_threshold(self):
        _, seed = self._run(learn=True, score=0.95)
        seed.assert_called_once()
        self.assertEqual(seed.call_args.kwargs["script_id"], "a__b__c")
        _, seed = self._run(learn=True, score=0.5)
        seed.assert_not_called()

    def test_scoring_never_seeds_library(self):
        _, seed = self._run(learn=False, score=1.0)
        seed.assert_not_called()

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

    def tearDown(self):
        self._tmp.cleanup()

    def _train(self, **kw):
        learned: list = []
        with patch.object(ho, "_translate_once", _fake_translate(learned=learned, **kw)):
            ho.train(self.m, self.work, log=lambda *_: None)
        return learned

    def test_train_snapshots_empty_half_full(self):
        learned = self._train()
        self.assertTrue(all(flag for _, flag in learned))
        n = {cp: len(PatternLibrary(self.work / "checkpoints" / cp).store.list_ids())
             for cp in ("empty", "half", "full")}
        self.assertEqual(n, {"empty": 0, "half": 5, "full": 10})

    def test_train_never_touches_heldout_scripts(self):
        learned = self._train()
        held = {e["script"] for e in self.m["heldout"]}
        self.assertFalse({name for name, _ in learned} & held)

    def test_train_resumes_without_redoing_work(self):
        self._train()
        self.assertEqual(self._train(), [])

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
        # Every run started from a pristine checkpoint: 0 patterns for empty, 10 for full.
        self.assertEqual(sorted(set(seen)), [0, 10])
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertEqual(len(rows), 12 * 2 * 2)  # scripts x reps x checkpoints

    def test_score_records_errors_and_resumes(self):
        self._train()

        def boom(*a, **k):
            raise RuntimeError("api down")

        with patch.object(ho, "_translate_once", boom):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        rows = ho._read_jsonl(self.work / "scores.jsonl")
        self.assertTrue(all("error" in r and "score" not in r for r in rows))

        # Resuming re-runs nothing that already has a row.
        calls: list = []
        with patch.object(ho, "_translate_once", lambda *a, **k: calls.append(1)):
            ho.score(self.m, self.work, ["empty"], log=lambda *_: None)
        self.assertEqual(calls, [])

    def test_score_requires_checkpoint(self):
        with self.assertRaises(FileNotFoundError):
            ho.score(self.m, self.work, ["full"], log=lambda *_: None)


def _write_scores(path: Path, manifest: dict, fn) -> None:
    """fn(script_index, checkpoint, rep) -> score or None (None = errored run)."""
    for rep in range(manifest["protocol"]["reps"]):
        for i, e in enumerate(manifest["heldout"]):
            for cp in ("empty", "half", "full"):
                s = fn(i, cp, rep)
                row = {"checkpoint": cp, "script": e["script"], "rep": rep, "harness_hash": "h"}
                row.update(score=s) if s is not None else row.update(error="x")
                ho._append_jsonl(path, row)


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.m = _select(_make_pool(root))
        self.path = root / "scores.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def test_consistent_improvement_is_significant(self):
        base = {"empty": 0.5, "half": 0.6, "full": 0.7}
        _write_scores(self.path, self.m, lambda i, cp, rep: base[cp] + 0.01 * i / 12 + 0.01 * rep)
        a = ho.analyze(self.m, self.path)
        self.assertEqual(a["n_paired"], 12)
        self.assertAlmostEqual(a["mean_diff"], 0.2)
        self.assertTrue(a["primary"]["significant"])
        self.assertLess(a["primary"]["p_value"], 0.001)
        self.assertEqual(a["trend"]["n_strictly_increasing"], 12)
        self.assertLess(a["trend"]["p_value"], 0.01)

    def test_no_effect_is_not_significant_and_direction_is_one_sided(self):
        _write_scores(self.path, self.m, lambda i, cp, rep: 0.5 + (0.05 if i % 2 else -0.05) * (cp == "full"))
        self.assertFalse(ho.analyze(self.m, self.path)["primary"]["significant"])
        # A uniform *decline* must not be significant in a greater-than test.
        _write_scores(self.path.with_name("down.jsonl"), self.m,
                      lambda i, cp, rep: 0.8 - 0.1 * (cp == "full") - 0.001 * i)
        self.assertGreater(ho.analyze(self.m, self.path.with_name("down.jsonl"))["primary"]["p_value"], 0.95)

    def test_reps_are_averaged_before_pairing(self):
        # Alternating reps average to the same mean at both checkpoints -> zero diff.
        _write_scores(self.path, self.m, lambda i, cp, rep: 0.4 + 0.2 * (rep % 2))
        a = ho.analyze(self.m, self.path)
        self.assertEqual(a["n_tied"], 12)
        self.assertEqual(a["primary"]["p_value"], 1.0)

    def test_scripts_without_valid_score_are_excluded_not_zeroed(self):
        def fn(i, cp, rep):
            return None if i < 2 else {"empty": 0.4, "half": 0.5, "full": 0.6}[cp] + 0.001 * i
        _write_scores(self.path, self.m, fn)
        a = ho.analyze(self.m, self.path)
        self.assertEqual((a["n_paired"], a["n_excluded"]), (10, 2))
        self.assertAlmostEqual(a["mean_diff"], 0.2)

    def test_partial_errors_use_remaining_reps(self):
        _write_scores(self.path, self.m,
                      lambda i, cp, rep: None if rep == 0 else {"empty": 0.4, "half": 0.5, "full": 0.6}[cp])
        a = ho.analyze(self.m, self.path)
        self.assertEqual(a["n_paired"], 12)
        self.assertEqual(a["n_errored_runs"], 36)

    def test_report_renders(self):
        _write_scores(self.path, self.m, lambda i, cp, rep: {"empty": 0.4, "half": 0.5, "full": 0.6}[cp] + 0.01 * i)
        text = ho.format_report(ho.analyze(self.m, self.path))
        self.assertIn("PRIMARY", text)
        self.assertIn("SECONDARY", text)


if __name__ == "__main__":
    unittest.main()
