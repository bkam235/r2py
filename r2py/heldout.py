"""Held-out experiment: does a trained Pattern Library help on unseen scripts?

Protocol:

1. ``select``  — fix a stratified held-out set (never used to train the library) and an
   ordered training set drawn from the packages the held-out set contains, and write both to
   a manifest with content hashes.
2. ``train``   — build the library from empty on the training set only, snapshotting it at
   evenly spaced checkpoints (``empty``, ``f1of8`` ... ``full``).
3. ``score``   — score every held-out script under every checkpoint, ``reps`` times, in a
   randomised order. Each run gets a throwaway copy of the checkpoint, so held-out scripts
   can never teach the library (or each other).
4. ``analyze`` — pair by script and average over reps. PRIMARY: one-sided Wilcoxon
   signed-rank on (full - empty) of the mean score over the targetable entities, i.e. those
   the full library could tell the translator something about. The whole-script aggregate is
   secondary; a trend test across all checkpoints goes with each.

``status`` reports progress from the result files; train and score print it after every run.
"""
from __future__ import annotations

import hashlib
import json
import math
import multiprocessing
import os
import random
import shutil
import sys
import tempfile
import threading
import time
import traceback
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POOL = "work/inputs/harvested"

# Stratum of each package in the harvested corpus. Held-out scripts are drawn
# equally from every stratum and spread across packages within it.
STRATA: dict[str, tuple[str, ...]] = {
    "data_wrangling": (
        "dplyr", "tidyr", "tibble", "purrr", "data.table", "dtplyr", "dbplyr", "DBI",
        "plyr", "reshape2", "stringr", "stringi", "forcats", "vctrs", "readr", "vroom",
        "readxl", "haven", "cellranger", "jsonlite", "yaml", "ini", "bit", "bit64",
        "tidyselect", "magrittr", "glue", "sparsevctrs", "blob", "rematch", "rematch2",
        "utf8",
    ),
    "date_time": ("clock", "lubridate", "timeDate", "timechange", "hms"),
    "graphics": (
        "ggplot2", "scales", "gtable", "isoband", "farver", "ragg", "systemfonts",
        "textshaping", "diagram", "shape", "RColorBrewer", "labeling",
    ),
    "html": (
        "shiny", "bslib", "htmltools", "htmlwidgets", "sass", "rvest", "xml2", "pkgdown",
        "miniUI", "rmarkdown", "knitr", "fontawesome", "downlit", "selectr", "highr",
        "xtable",
    ),
    "stats_objects": (
        "broom", "recipes", "hardhat", "glmnet", "caret", "e1071", "lava", "prodlim",
        "ipred", "pROC", "ModelMetrics", "ranger", "gbm", "modelr", "mlbench", "numDeriv",
        "proxy", "gower",
    ),
}
OTHER = "other"  # everything not listed above: programming / system infrastructure
ALL_STRATA = (*STRATA, OTHER)
_STRATUM_OF_PACKAGE = {pkg: s for s, pkgs in STRATA.items() for pkg in pkgs}

DEFAULT_PROTOCOL = {
    "seed": 20260919,
    "n_heldout": 60,
    "per_package": 6,  # training scripts drawn per held-out package (fewer if it has fewer spare)
    "n_intervals": 4,  # checkpoints at every 1/4 of the training set (5 including empty)
    "reps": 3,
    # Mirrors the settings in scripts/translate.py.
    "translate": {
        "model": "openrouter:google/gemma-4-31b-it",
        "score_threshold": 0.9,
        "n_bare_seeds": 2,
        "n_structured_seeds": 2,
        "max_iters": 20,
        "max_stalls": 3,
        "timeout_s": 60,
        "agent_budget_s": 2700,  # wall-clock cap for the agent loop, per script
        "data_compare": "auto",
    },
    "primary_test": {
        "name": "wilcoxon_signed_rank",
        # Primary: mean score over the entities the trained library could tell the translator
        # something about (see analyze); the whole-script aggregate is secondary.
        "endpoint": "targetable_entity_mean",
        "before": "empty",
        "after": "full",
        "alternative": "greater",
        "alpha": 0.05,
        "zero_method": "wilcox",
    },
}

# Forced onto every OpenRouter request, in training and scoring alike (see pinned_llm).
# temperature 1.0 is OpenRouter's documented default, i.e. what unpinned runs already used.
# The provider pin fixes the weights/quantisation (and provider-side defaults such as top_p)
# behind the model string, which otherwise routes across ~12 providers.
LLM_SETTINGS = {
    "temperature": 1.0,
    "provider": {"only": ["novita/bf16"], "allow_fallbacks": False},
    "request_timeout_s": 300,  # per network read
    "request_deadline_s": 420,  # whole request, wall clock (see _with_deadline); llm.py retries it
}


def llm_settings(manifest: dict) -> dict:
    """The LLM settings a run uses: the module defaults, overridden by ``protocol["llm"]``.

    ``{"provider": None}`` leaves provider routing to OpenRouter (a development run: faster and
    cheaper, but the weights/quantisation behind the model string are no longer fixed).
    """
    return {**LLM_SETTINGS, **(manifest["protocol"].get("llm") or {})}


def package_of(script: str) -> str:
    return script.split("__")[0]


def stratum_of(script: str) -> str:
    return _STRATUM_OF_PACKAGE.get(package_of(script), OTHER)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def harness_hash() -> str:
    """Hash of the translation harness (r2py source except this module and the bundled
    R environment), so a mid-experiment change to it is detectable. Line endings are
    normalised so the value is the same for a Windows checkout and for the git blobs."""
    h = hashlib.sha256()
    files = {p.relative_to(ROOT).as_posix(): p for p in (ROOT / "r2py").rglob("*.py")}
    for rel in sorted(files):
        if rel == "r2py/heldout.py" or rel.startswith("r2py/stage0/r_env/"):
            continue
        h.update(rel.encode())
        h.update(files[rel].read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:12]


def library_hash(lib_dir: Path) -> str:
    """Hash of a library's pattern files (index.json is derived and mutates on use)."""
    h = hashlib.sha256()
    for p in sorted((lib_dir / "patterns").rglob("*.md")):
        h.update(p.relative_to(lib_dir).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


# ---------------------------------------------------------------------------
# Step 1 — select
# ---------------------------------------------------------------------------

def select(
    pool_dir: str | Path = DEFAULT_POOL,
    *,
    n_heldout: int = DEFAULT_PROTOCOL["n_heldout"],
    per_package: int = DEFAULT_PROTOCOL["per_package"],
    n_intervals: int = DEFAULT_PROTOCOL["n_intervals"],
    reps: int = DEFAULT_PROTOCOL["reps"],
    seed: int = DEFAULT_PROTOCOL["seed"],
    llm: dict | None = None,
    agent_budget_s: float | None = None,
) -> dict:
    """Draw the held-out and training sets from pool_dir and return the manifest.

    The held-out set is stratified by domain and spread across packages. The training set
    comes only from packages that appear in the held-out set: up to ``per_package`` scripts
    of each, drawn at random and interleaved package by package, so every checkpoint holds a
    proportional share of every package.
    """
    pool_path = Path(pool_dir)
    if not pool_path.is_absolute():
        pool_path = ROOT / pool_path
    pool = sorted(p.name for p in pool_path.glob("*.R"))

    by_stratum: dict[str, dict[str, list[str]]] = {s: {} for s in ALL_STRATA}
    for name in pool:
        by_stratum[stratum_of(name)].setdefault(package_of(name), []).append(name)

    k = len(ALL_STRATA)
    quotas = {s: n_heldout // k + (i < n_heldout % k) for i, s in enumerate(ALL_STRATA)}

    rng = random.Random(seed)
    heldout: list[str] = []
    for stratum, quota in quotas.items():
        available = sum(len(v) for v in by_stratum[stratum].values())
        if available < quota:
            raise ValueError(f"stratum {stratum!r} has {available} scripts, need {quota}")
        heldout += _draw_spread(rng, by_stratum[stratum], quota)

    remaining = sorted(set(pool) - set(heldout))
    held_packages = sorted({package_of(n) for n in heldout})
    spare = {p: [n for n in remaining if package_of(n) == p] for p in held_packages}
    train_rng = random.Random(f"{seed}:train")  # independent of the held-out draw above
    queues = {p: train_rng.sample(v, min(per_package, len(v))) for p, v in spare.items() if v}
    train = _interleave(train_rng, queues)
    if len(train) < n_intervals:
        raise ValueError(f"{len(train)} training scripts is too few for {n_intervals} checkpoint intervals")

    def entry(name: str) -> dict:
        return {"script": name, "package": package_of(name),
                "stratum": stratum_of(name), "sha256": _sha256(pool_path / name)}

    protocol = {**DEFAULT_PROTOCOL, "seed": seed, "n_heldout": n_heldout, "per_package": per_package,
                "n_train": len(train), "n_intervals": n_intervals, "reps": reps}
    protocol["translate"] = dict(DEFAULT_PROTOCOL["translate"])
    if agent_budget_s is not None:
        protocol["translate"]["agent_budget_s"] = agent_budget_s
    if llm:
        protocol["llm"] = llm
    return {
        "protocol": protocol,
        "pool_dir": str(pool_dir),
        "pool_size": len(pool),
        "checkpoints": _checkpoints(len(train), n_intervals),
        "stratum_quotas": quotas,
        "train_packages": {p: len(q) for p, q in sorted(queues.items())},
        "uncovered_packages": [p for p in held_packages if not spare[p]],  # no spare script to train on
        "heldout": [entry(n) for n in heldout],
        "train": [entry(n) for n in train],
    }


def _interleave(rng: random.Random, queues: dict[str, list[str]]) -> list[str]:
    """Round-robin over packages (order reshuffled each round): any prefix of the result
    holds a proportional share of every package."""
    order: list[str] = []
    for r in range(max((len(q) for q in queues.values()), default=0)):
        pkgs = sorted(p for p, q in queues.items() if r < len(q))
        rng.shuffle(pkgs)
        order += [queues[p][r] for p in pkgs]
    return order


def _checkpoints(n_train: int, k: int) -> dict[str, int]:
    """Ordered {name: number of training scripts seen}: empty, k-1 evenly spaced, full."""
    def name(i: int) -> str:
        return "half" if 2 * i == k else f"f{i}of{k}"

    cps = {"empty": 0}
    cps.update({name(i): (n_train * i + k // 2) // k for i in range(1, k)})
    cps["full"] = n_train
    return cps


def _draw_spread(rng: random.Random, by_pkg: dict[str, list[str]], k: int) -> list[str]:
    """Pick k scripts round-robin over packages, so no package dominates a stratum."""
    pkgs = sorted(by_pkg)
    rng.shuffle(pkgs)
    queues = {p: rng.sample(sorted(by_pkg[p]), len(by_pkg[p])) for p in pkgs}
    picked: list[str] = []
    while len(picked) < k:
        for p in pkgs:
            if queues[p] and len(picked) < k:
                picked.append(queues[p].pop())
    return picked


def write_manifest(manifest: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def load_manifest(path: str | Path) -> dict:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    overlap = {e["script"] for e in manifest["heldout"]} & {e["script"] for e in manifest["train"]}
    if overlap:
        raise ValueError(f"held-out and train sets overlap: {sorted(overlap)[:5]}")
    return manifest


def _pool_path(manifest: dict) -> Path:
    p = Path(manifest["pool_dir"])
    return p if p.is_absolute() else ROOT / p


def verify_inputs(manifest: dict, entries: list[dict]) -> None:
    """The corpus is not under version control, so check files match the manifest."""
    pool = _pool_path(manifest)
    for e in entries:
        path = pool / e["script"]
        if not path.exists() or _sha256(path) != e["sha256"]:
            raise ValueError(f"{e['script']}: missing or changed since the manifest was written")


# ---------------------------------------------------------------------------
# One translation — same path as r2py.translate(), minus its library side effects
# ---------------------------------------------------------------------------

def entity_score(es) -> float:
    """An entity's score as the verifier averages it: its active dimensions, 0 if it did not run."""
    if not es.executed_ok:
        return 0.0
    vals = [getattr(es, d) for d in es.active_dims]
    return sum(vals) / len(vals) if vals else 1.0


def _entity_records(script_map, report) -> list[dict]:
    """Per scored entity: how it scored, and what the library could say about it.

    ``key`` is the id of the pattern keying the entity (its own call, or an assignment's
    right-hand call) and ``calls`` the ids of the informative base-R functions inside it.
    The analysis decides from these, and the trained library alone, which entities the
    translator could have been told something about.
    """
    from r2py.harness.objective import entity_status
    from r2py.library.pattern import correction_functions, pattern_id, pattern_key
    from r2py.types import EntityKind

    records = []
    for eid, entity in script_map.entities.items():
        es = report.by_entity.get(eid) if report is not None else None
        if es is None or entity.kind == EntityKind.LIBRARY_IMPORT:
            continue
        key = pattern_key(entity)
        dims = sorted(es.active_dims)
        records.append({
            "active_dims": dims,
            "dim_scores": {d: getattr(es, d) for d in dims},
            "executed_ok": es.executed_ok,
            # blocked = never reached because the program crashed earlier: not evidence about this entity
            "status": entity_status(report, eid),
            "uncomparable": eid in report.uncomparable,
            "id": eid, "name": entity.name,
            "key": pattern_id(*key) if key else None,
            "calls": [pattern_id(*q.split("::")) for q in correction_functions(entity.base_r_calls)],
            "score": entity_score(es),
        })
    return records


class _Tee:
    def __init__(self, *streams) -> None:
        self._streams = streams

    def write(self, s: str) -> int:
        for st in self._streams:
            st.write(s)
        return len(s)

    def flush(self) -> None:
        for st in self._streams:
            st.flush()

    def __getattr__(self, name):  # encoding, isatty, ... from the first (real) stream
        return getattr(self._streams[0], name)


def _log_to_file(path: Path) -> None:
    """Also write this process's stdout/stderr to ``path`` (appending), so a parallel run leaves
    a record the analysis scripts can read: worker output otherwise exists only on the console."""
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open("a", encoding="utf-8", buffering=1)
    sys.stdout = _Tee(sys.stdout, f)
    sys.stderr = _Tee(sys.stderr, f)


def _drain_diagnostics() -> dict:
    """Shadow-fixer outcomes and review failures since the last call, for the run's row."""
    from r2py.harness.agent import drain_agent_stats
    from r2py.harness.review import review_stats
    from r2py.harness.tools import drain_cache_stats
    from r2py.seed import seed_gate_stats
    from r2py.stage2.stitch import drain_shadow_log
    out = {"shadow_fixers": drain_shadow_log(), "review_failures": dict(review_stats),
           "agent": drain_agent_stats(), "verify_cache": drain_cache_stats(),
           "seed_gate": dict(seed_gate_stats)}
    seed_gate_stats.clear()
    for k in review_stats:
        review_stats[k] = 0
    return out


def _translate_once(r_path: Path, py_path: Path, lib, cfg: dict, *, learn: bool):
    """analyze -> run_loop, then (only if learn) seed the library.

    Returns (result, per-entity records). r2py.translate() also seeds unconditionally,
    git-commits the library, and appends to run_history.jsonl; none of that belongs in an
    experiment.
    """
    from r2py import seed_from_translation
    from r2py.loop import (DEFAULT_AGENT_WIDTH, DEFAULT_CRASH_BUDGET_FACTOR, DEFAULT_CRASH_STALLS,
                           DEFAULT_CRASH_WIDTH, run_loop)
    from r2py.stage1 import analyze

    from r2py.harness import trajectory
    from r2py.stage2 import llm as _llm

    py_path.parent.mkdir(parents=True, exist_ok=True)
    trajectory.begin(py_path.parent / "trajectories" / (py_path.stem + ".jsonl"),
                     script=r_path.name, learn=learn, model=cfg["model"])
    _llm.drain_provider_failures()
    script_map = analyze(r_path)
    result = run_loop(
        script_map, lib,
        max_iters=cfg["max_iters"],
        score_threshold=cfg["score_threshold"],
        data_compare=cfg["data_compare"],
        n_bare_seeds=cfg["n_bare_seeds"],
        n_structured_seeds=cfg["n_structured_seeds"],
        n_planned_seeds=cfg.get("n_planned_seeds", 0),
        checkpoint_path=py_path,
        model=cfg["model"],
        escalation_model=cfg["model"],
        timeout_s=cfg["timeout_s"],
        max_stalls=cfg["max_stalls"],
        agent_budget_s=cfg.get("agent_budget_s"),
        agent_replace_entity=cfg.get("replace_entity", True),
        agent_entity_repair=cfg.get("entity_repair", False),
        agent_width=cfg.get("agent_width", DEFAULT_AGENT_WIDTH),
        agent_crash_width=cfg.get("agent_crash_width", DEFAULT_CRASH_WIDTH),
        agent_crash_stalls=cfg.get("agent_crash_stalls", DEFAULT_CRASH_STALLS),
        agent_crash_budget_factor=cfg.get("agent_crash_budget_factor", DEFAULT_CRASH_BUDGET_FACTOR),
        agent_entity_width=cfg.get("entity_width", 1),
        agent_locate=cfg.get("locate", False),
        runtime_dir=cfg.get("runtime_dir"),
        ondemand=cfg.get("ondemand"),
    )
    failures = _llm.drain_provider_failures()
    if failures:
        # No credits, no network, an overloaded provider: seeds came back empty and the agent stopped.  That run says
        # nothing about the harness and must neither be recorded as a score nor taught to the library.
        trajectory.end(provider_unavailable=failures)
        raise _llm.ProviderUnavailable(failures)
    py_path.write_text(result.python_source, encoding="utf-8")
    trajectory.end(final_score=round(result.final_score, 4), iterations=result.iterations,
                   final_hash=trajectory.source_hash(result.python_source))
    # Seed from every run. seed_from_translation keeps only entities at or above
    # entity_score_threshold, so a sub-threshold script still teaches the statements
    # that verified against R. The old script-level gate discarded those: in the first
    # training run, 90% of the compute (101h of 112h) produced no patterns at all.
    if learn:
        seed_from_translation(
            r_path, py_path, library=lib, script_id=r_path.stem,
            score_report=result.final_score_report,
            entity_score_threshold=cfg["score_threshold"],
            seed_source=result.seed_source,
            seed_score_report=result.score_history[0] if result.score_history else None,
        )
    return result, _entity_records(script_map, result.final_score_report)


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Fixed LLM settings — applied from outside so the frozen harness stays byte-identical
# ---------------------------------------------------------------------------

RATE_LIMIT_TRIES = 7     # 429s are waited out (5, 10, 20, 40, 80, 160 s; upstream pool limits last minutes) before the harness sees an error
RATE_LIMIT_WAIT_S = 5.0


def _with_deadline(fn, deadline_s: float):
    """Run ``fn`` but give up after ``deadline_s`` seconds of wall clock.

    The client's own ``timeout`` is per network read; OpenRouter keeps a slow request alive
    with keepalive bytes, so a stalled call never tripped it (a smoke test sat 85 minutes on
    one request).  The abandoned worker thread is left to die with its connection.
    """
    box: dict = {}

    def run():
        try:
            box["result"] = fn()
        except BaseException as exc:  # re-raised in the caller
            box["error"] = exc

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(deadline_s)
    if t.is_alive():
        raise TimeoutError(f"LLM request exceeded {deadline_s:.0f}s wall clock")
    if "error" in box:
        raise box["error"]
    return box["result"]


class _PinnedClient:
    """Proxy for an openai client that forces settings onto every chat request."""

    def __init__(self, inner, settings: dict, served: Counter) -> None:
        self._inner, self._settings, self._served = inner, settings, served
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        import openai

        extra = dict(kw.pop("extra_body", None) or {})
        if self._settings.get("provider"):
            extra["provider"] = self._settings["provider"]
        kw.setdefault("temperature", self._settings["temperature"])   # a call may fix its own (entity mapping: 0)
        kw.setdefault("timeout", self._settings["request_timeout_s"])
        for attempt in range(RATE_LIMIT_TRIES):
            try:
                resp = _with_deadline(
                    lambda: self._inner.chat.completions.create(extra_body=extra, **kw),
                    self._settings["request_deadline_s"])
                break
            except openai.RateLimitError:
                if attempt == RATE_LIMIT_TRIES - 1:
                    raise
                time.sleep(RATE_LIMIT_WAIT_S * 2 ** attempt)  # parallel workers back off, not fail
        self._served[getattr(resp, "provider", None)] += 1  # OpenRouter reports who answered
        return resp


@contextmanager
def pinned_llm(model: str, settings: dict = LLM_SETTINGS):
    """Force ``settings`` onto all OpenRouter requests the harness makes; yields a
    Counter of the providers that actually served them.

    Only OpenRouter models are supported: refusing anything else is deliberate, since
    an unenforced setting would silently give an unfixed experiment.
    """
    import openai
    from r2py.stage2 import llm

    if not model.startswith("openrouter:"):
        raise ValueError(f"cannot pin LLM settings for {model!r}: only openrouter: models are supported")
    served: Counter = Counter()
    real = openai.OpenAI
    llm._openrouter_clients.clear()  # drop any unpinned client cached earlier in this process
    openai.OpenAI = lambda *a, **kw: _PinnedClient(real(*a, **kw), settings, served)
    try:
        yield served
    finally:
        openai.OpenAI = real
        llm._openrouter_clients.clear()


def check_llm(manifest: dict, *, log=print) -> None:
    """One tiny pinned request, to confirm the key works and the provider pin resolves."""
    from r2py.stage2 import llm

    model = manifest["protocol"]["translate"]["model"]
    settings = llm_settings(manifest)
    with pinned_llm(model, settings) as served:
        reply = llm.call([{"role": "user", "content": "Reply with the single word OK."}],
                        "You are terse.", model=model, max_tokens=16)
    log(f"reply={reply!r}  served by: {dict(served)}  settings: {settings}")


# ---------------------------------------------------------------------------
# Progress — printed after every run, and recomputable from the result files
# ---------------------------------------------------------------------------

MAX_ATTEMPTS = 2  # a run that errors is retried once, then recorded as failed


def _fmt_duration(seconds: float) -> str:
    h, rest = divmod(int(seconds), 3600)
    m, s = divmod(rest, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def _progress_line(phase: str, done: int, total: int, durations: list[float], workers: int = 1) -> str:
    """e.g. "[train 12/268 4%] last 3m10s | avg 5m02s | active 1h01m | ETA 21h30m".

    ETA counts run time only (pauses between sessions are not part of it). With several
    workers, avg is still the time of one run, while active time and ETA are wall-clock.
    """
    avg = sum(durations) / len(durations) if durations else 0.0
    last = durations[-1] if durations else 0.0
    return (f"[{phase} {done}/{total} {100 * done / total if total else 100:.0f}%] last {_fmt_duration(last)}"
            f" | avg {_fmt_duration(avg)} | active {_fmt_duration(sum(durations) / workers)}"
            f" | ETA {_fmt_duration(avg * (total - done) / workers)}")


# ---------------------------------------------------------------------------
# Step 2 — train
# ---------------------------------------------------------------------------

def provider_ok(manifest: dict) -> tuple[bool, str]:
    """One tiny request through the pinned model: is the provider answering (credits, network)?"""
    from r2py.stage2 import llm

    cfg = manifest["protocol"]["translate"]
    try:
        with pinned_llm(cfg["model"], llm_settings(manifest)):
            llm.call([{"role": "user", "content": "Reply with the word ok."}], "You reply with one word.",
                     model=cfg["model"], max_tokens=8)
        return True, ""
    except Exception as exc:
        return False, f"{llm.classify_failure(exc)}: {str(exc)[:160]}"
    finally:
        llm.drain_provider_failures()


def wait_for_provider(manifest: dict, kinds: dict, *, log=print, poll_s: float = 60.0, max_wait_s: float = 6 * 3600.0) -> bool:
    """Block until the provider answers again; False after ``max_wait_s`` (the caller then stops cleanly: the
    progress files hold every finished script, so the same command resumes)."""
    log(f"provider unavailable ({kinds}); pausing, checking every {poll_s:.0f}s for up to {max_wait_s / 3600:.1f} h. "
        "Add credits / restore the network and it continues by itself; Ctrl-C stops, the same command resumes.")
    waited = 0.0
    while waited <= max_wait_s:
        ok, why = provider_ok(manifest)
        if ok:
            log(f"provider is back after {waited / 60:.0f} min; resuming")
            return True
        time.sleep(poll_s)
        waited += poll_s
        if int(waited / poll_s) % 10 == 0:
            log(f"  still unavailable after {waited / 60:.0f} min ({why})")
    return False


def _train_task(manifest: dict, snapshot: str, script: str, py_path: str) -> dict:
    """One training translation in its own process, against a private copy of the library.

    Does not learn: the parent seeds the live library from what comes back, one result at a
    time, so the library is only ever written by one process.
    """
    from r2py.library import PatternLibrary

    sys.stdout.reconfigure(line_buffering=True)
    _log_to_file(Path(py_path).parents[1] / "logs" / f"train.p{os.getpid()}.txt")
    cfg = manifest["protocol"]["translate"]
    out: dict = {"script": script}
    started = time.monotonic()
    try:
        with pinned_llm(cfg["model"], llm_settings(manifest)) as served:
            r, _ = _translate_once(_pool_path(manifest) / script, Path(py_path),
                                   PatternLibrary(Path(snapshot)), cfg, learn=False)
        out.update(score=r.final_score, score_report=r.final_score_report, seed_source=r.seed_source,
                   seed_score_report=r.score_history[0] if r.score_history else None,
                   served=dict(served))
    except Exception as exc:
        if type(exc).__name__ == "ProviderUnavailable":
            out["provider_unavailable"] = dict(getattr(exc, "kinds", {}))
        else:
            out["error"] = f"{type(exc).__name__}: {exc}"
            out["traceback"] = traceback.format_exc()[-1500:]
    out.update(_drain_diagnostics())
    out["seconds"] = round(time.monotonic() - started, 1)
    shutil.rmtree(snapshot, ignore_errors=True)
    return out


def _train_parallel(manifest: dict, workdir: Path, workers: int, *, log=print, poll_s: float = 60.0,
                    max_wait_s: float = 6 * 3600.0) -> bool:
    """Train with ``workers`` translations in flight at once.

    Each task translates against a snapshot of the library taken when it starts, so it does not
    see patterns learned by tasks that finish after that -- up to ``workers - 1`` scripts stale.
    The parent seeds the live library from finished tasks one at a time.  For development runs:
    the sequential path is the one that gives every script the full library learned before it.
    """
    from collections import deque
    from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait

    from r2py import seed_from_translation
    from r2py.library import PatternLibrary

    verify_inputs(manifest, manifest["train"])
    cfg = manifest["protocol"]["translate"]
    pool = _pool_path(manifest)
    ckpt_dir = workdir / "checkpoints"
    progress_path = workdir / "train_progress.jsonl"
    rows = _read_jsonl(progress_path)
    attempts = Counter(r["script"] for r in rows)
    ok = {r["script"] for r in rows if "error" not in r}
    durations = [r["seconds"] for r in rows if "seconds" in r]

    def finished(script: str) -> bool:
        return script in ok or attempts[script] >= MAX_ATTEMPTS

    total = len(manifest["train"])
    counts = {n: c for n, c in manifest["checkpoints"].items() if c > 0}
    if not (ckpt_dir / "empty").exists():
        if rows:
            raise RuntimeError("training already started but the empty checkpoint is missing")
        PatternLibrary(ckpt_dir / "empty")
    lib = PatternLibrary(workdir / "lib_live")
    todo = deque((i, e["script"]) for i, e in enumerate(manifest["train"], start=1) if not finished(e["script"]))
    n_done = total - len(todo)
    log(f"train: {n_done}/{total} already finished, {len(todo)} to go, {workers} in parallel")

    served: Counter = Counter()
    snapshots = workdir / "train_snapshots"
    ctx = multiprocessing.get_context("spawn")
    pending: dict = {}
    outage: dict = {}                 # kinds of the provider failures seen since the last time the provider answered
    completed = True
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
        def submit() -> None:
            while todo and len(pending) < workers and not outage:
                i, script = todo.popleft()
                snap = snapshots / f"{i}_{attempts[script] + 1}"
                shutil.rmtree(snap, ignore_errors=True)
                shutil.copytree(workdir / "lib_live", snap)
                py_path = workdir / "train_outputs" / (Path(script).stem + ".py")
                log(f"[train {i}/{total}] starting {script} (attempt {attempts[script] + 1})")
                pending[ex.submit(_train_task, manifest, str(snap), script, str(py_path))] = (i, script, py_path)

        submit()
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done:
                i, script, py_path = pending.pop(fut)
                row = {"script": script, "index": i, "attempt": attempts[script] + 1,
                       "timestamp": _now(), "llm": llm_settings(manifest)}
                try:
                    res = fut.result()
                except Exception as exc:  # the worker process itself died
                    res = {"error": f"{type(exc).__name__}: {exc}", "seconds": 0.0}
                if res.get("provider_unavailable"):
                    # Not a result: back to the front of the queue, no attempt counted, nothing recorded as a score.
                    todo.appendleft((i, script))
                    for k, v in res["provider_unavailable"].items():
                        outage[k] = outage.get(k, 0) + v
                    _append_jsonl(workdir / "train_events.jsonl", {"event": "provider_unavailable", "script": script,
                                                                 "kinds": res["provider_unavailable"], "timestamp": _now()})
                    log(f"[train {i}/{total}] {script}: provider failed ({res['provider_unavailable']}); will be repeated")
                    continue
                served.update(res.pop("served", {}))
                for k in ("shadow_fixers", "review_failures", "traceback", "error", "seconds"):
                    if k in res:
                        row[k] = res[k]
                if "error" not in res:
                    try:
                        seed_from_translation(
                            pool / script, py_path, library=lib, script_id=Path(script).stem,
                            score_report=res["score_report"], entity_score_threshold=cfg["score_threshold"],
                            seed_source=res["seed_source"], seed_score_report=res["seed_score_report"])
                        row.update(score=res["score"], patterns=len(lib.index.all_ids()))
                    except Exception as exc:
                        row["error"] = f"{type(exc).__name__}: {exc}"
                        row["traceback"] = traceback.format_exc()[-1500:]
                _append_jsonl(progress_path, row)
                attempts[script] += 1
                durations.append(row.get("seconds", 0.0))
                if "error" not in row:
                    ok.add(script)
                elif not finished(script):
                    todo.appendleft((i, script))  # one retry, ahead of the rest
                if finished(script):
                    n_done += 1
                    result = (f"score {row['score']:.3f}, {row['patterns']} patterns"
                              if "error" not in row else f"FAILED after retries: {row['error'][:80]}")
                    log(_progress_line("train", n_done, total, durations, workers) + f" | {script}: {result}")
                    for name, count in counts.items():
                        if n_done == count and not (ckpt_dir / name).exists():
                            shutil.copytree(workdir / "lib_live", ckpt_dir / name)
                            log(f"checkpoint {name!r} at {n_done} scripts ({len(lib.index.all_ids())} patterns)")
            if outage and not pending:
                # everything in flight has come back: wait for the provider, then carry on with the same queue
                if not wait_for_provider(manifest, outage, log=log, poll_s=poll_s, max_wait_s=max_wait_s):
                    log(f"gave up waiting; {len(todo)} scripts unfinished. Run the same command to resume.")
                    completed = False
                    break
                outage.clear()
            submit()
    shutil.rmtree(snapshots, ignore_errors=True)
    log(f"providers that served this session: {dict(served)}")
    return completed


def train(manifest: dict, workdir: str | Path, *, workers: int = 1, log=print, poll_s: float = 60.0,
          max_wait_s: float = 6 * 3600.0) -> bool:
    """Build the library from empty on the training set, snapshotting each checkpoint.

    Resumable: a script is finished once it has a successful row in train_progress.jsonl, or
    MAX_ATTEMPTS failed ones. A failing script is retried at once, so the checkpoints stay
    a clean prefix of the training order.

    A provider outage (no credits, no network) is not a failed attempt: the run is discarded without a row,
    the driver waits until a tiny request succeeds (``poll_s``, at most ``max_wait_s``) and repeats the script.
    If the wait runs out, or on Ctrl-C, nothing is lost: the same command resumes with the unfinished scripts.
    Returns True when every script is finished.
    """
    from r2py.library import PatternLibrary

    workdir = Path(workdir)
    if workers > 1:
        return _train_parallel(manifest, workdir, workers, log=log, poll_s=poll_s, max_wait_s=max_wait_s)
    verify_inputs(manifest, manifest["train"])
    cfg = manifest["protocol"]["translate"]
    pool = _pool_path(manifest)
    ckpt_dir = workdir / "checkpoints"
    progress_path = workdir / "train_progress.jsonl"
    rows = _read_jsonl(progress_path)
    attempts = Counter(r["script"] for r in rows)
    ok = {r["script"] for r in rows if "error" not in r}
    durations = [r["seconds"] for r in rows if "seconds" in r]

    def finished(script: str) -> bool:
        return script in ok or attempts[script] >= MAX_ATTEMPTS

    total = len(manifest["train"])
    n_done = sum(1 for e in manifest["train"] if finished(e["script"]))
    counts = {n: c for n, c in manifest["checkpoints"].items() if c > 0}
    if not (ckpt_dir / "empty").exists():
        if rows:
            raise RuntimeError("training already started but the empty checkpoint is missing")
        PatternLibrary(ckpt_dir / "empty")  # creates the empty store + index

    lib = PatternLibrary(workdir / "lib_live")
    log(f"train: {n_done}/{total} already finished, {total - n_done} to go")
    settings = llm_settings(manifest)
    with pinned_llm(cfg["model"], settings) as served:
        for i, e in enumerate(manifest["train"], start=1):
            script = e["script"]
            while not finished(script):
                log(f"[train {i}/{total}] starting {script} (attempt {attempts[script] + 1})")
                row = {"script": script, "index": i, "attempt": attempts[script] + 1,
                       "timestamp": _now(), "llm": settings}
                started = time.monotonic()
                try:
                    r, _ = _translate_once(pool / script,
                                           workdir / "train_outputs" / (Path(script).stem + ".py"),
                                           lib, cfg, learn=True)
                    row.update(score=r.final_score, patterns=len(lib.index.all_ids()))
                except Exception as exc:
                    if type(exc).__name__ == "ProviderUnavailable":
                        _drain_diagnostics()
                        _append_jsonl(workdir / "train_events.jsonl", {"event": "provider_unavailable", "script": script,
                                                                     "kinds": getattr(exc, "kinds", {}), "timestamp": _now()})
                        if not wait_for_provider(manifest, getattr(exc, "kinds", {}), log=log, poll_s=poll_s, max_wait_s=max_wait_s):
                            log(f"gave up waiting at {script}. Run the same command to resume.")
                            return False
                        continue                      # the same script again; no attempt counted, no row written
                    row["error"] = f"{type(exc).__name__}: {exc}"
                    row["traceback"] = traceback.format_exc()[-1500:]  # e.g. which frame recursed
                    log(f"  ERROR: {row['error']}")
                row.update(_drain_diagnostics())
                row["seconds"] = round(time.monotonic() - started, 1)
                _append_jsonl(progress_path, row)
                attempts[script] += 1
                durations.append(row["seconds"])
                if "error" not in row:
                    ok.add(script)
                if finished(script):
                    n_done += 1
                    result = (f"score {row['score']:.3f}, {row['patterns']} patterns"
                              if "error" not in row else "FAILED after retries")
                    log(_progress_line("train", n_done, total, durations) + f" | {script}: {result}")
            for name, count in counts.items():
                if i == count and not (ckpt_dir / name).exists():
                    shutil.copytree(workdir / "lib_live", ckpt_dir / name)
                    log(f"checkpoint {name!r} at {i} scripts ({len(lib.index.all_ids())} patterns)")
    log(f"providers that served this session: {dict(served)}")
    return True


# ---------------------------------------------------------------------------
# Step 3 — score (with repetitions)
# ---------------------------------------------------------------------------

def score_order(manifest: dict, checkpoints: list[str], rep: int) -> list[tuple[dict, str]]:
    """Randomised run order for one rep: scripts shuffled, and each script's checkpoints
    shuffled, so a script's paired runs stay adjacent in time but no checkpoint is
    systematically first. Seeded from the protocol seed, so it is reproducible and a
    resumed run continues the same sequence."""
    rng = random.Random(f"{manifest['protocol']['seed']}:score:{rep}")
    order: list[tuple[dict, str]] = []
    for e in rng.sample(manifest["heldout"], len(manifest["heldout"])):
        order += [(e, cp) for cp in rng.sample(checkpoints, len(checkpoints))]
    return order


def read_scores(scores_path: str | Path) -> list[dict]:
    """Rows of scores.jsonl plus those of the per-worker files (scores.w<i>.jsonl) beside it."""
    scores_path = Path(scores_path)
    rows = _read_jsonl(scores_path)
    for extra in sorted(scores_path.parent.glob(scores_path.stem + ".w*" + scores_path.suffix)):
        rows += _read_jsonl(extra)
    return rows


def _claim(claims: Path, rep: int, cp: str, script: str) -> bool:
    """Take a run for this worker; exactly one process can succeed for a given run."""
    try:
        os.close(os.open(claims / f"{rep}__{cp}__{script}", os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        return False


def _score_loop(manifest: dict, workdir: Path, checkpoints: list[str], *, out: Path,
                claims: Path | None, worker: int | None, workers: int, log) -> None:
    """Score runs in randomised order (see score_order), appending rows to ``out``.

    With ``claims`` set, several such loops share the work: each takes the next unclaimed
    run, so the order is the same and the runs are simply spread over the workers."""
    from r2py.library import PatternLibrary

    cfg = manifest["protocol"]["translate"]
    pool = _pool_path(manifest)
    scores_path = workdir / "scores.jsonl"
    total = manifest["protocol"]["reps"] * len(manifest["heldout"]) * len(checkpoints)
    lib_hashes = {cp: library_hash(workdir / "checkpoints" / cp) for cp in checkpoints}
    hh = harness_hash()

    def tally() -> tuple[set, list[float], dict[str, list[float]]]:
        rows = read_scores(scores_path)
        running: dict[str, list[float]] = {}
        for r in rows:
            if "score" in r and r["checkpoint"] in checkpoints:
                running.setdefault(r["checkpoint"], []).append(r["score"])
        return ({(r["checkpoint"], r["script"], r["rep"]) for r in rows},
                [r["seconds"] for r in rows if "seconds" in r], running)

    done, durations, _ = tally()
    n_done = sum(1 for d in done if d[0] in checkpoints)
    if worker is None:
        log(f"score: {n_done}/{total} already done, {total - n_done} to go")

    settings = llm_settings(manifest)
    with pinned_llm(cfg["model"], settings) as served:
        for rep in range(manifest["protocol"]["reps"]):
            for e, cp in score_order(manifest, checkpoints, rep):
                if (cp, e["script"], rep) in done:
                    continue
                if claims is not None and not _claim(claims, rep, cp, e["script"]):
                    continue
                log(f"[score rep{rep}] starting {cp} | {e['script']}")
                row = {"checkpoint": cp, "script": e["script"], "rep": rep,
                       "order_seed": f"{manifest['protocol']['seed']}:score:{rep}",
                       "library_hash": lib_hashes[cp], "harness_hash": hh,
                       "model": cfg["model"], "llm": settings, "timestamp": _now()}
                if worker is not None:
                    row["worker"] = worker
                started = time.monotonic()
                attempt = 0
                while attempt < MAX_ATTEMPTS:
                    attempt += 1
                    row.pop("error", None)
                    row.pop("traceback", None)
                    # Fresh copy per run: whatever the loop writes is discarded.
                    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                        shutil.copytree(workdir / "checkpoints" / cp, Path(tmp) / "lib")
                        try:
                            r, entities = _translate_once(
                                pool / e["script"],
                                workdir / "outputs" / cp / f"rep{rep}" / (Path(e["script"]).stem + ".py"),
                                PatternLibrary(Path(tmp) / "lib"), cfg, learn=False)
                            report = r.final_score_report
                            row.update(
                                score=r.final_score, iterations=r.iterations,
                                exit_code=r.final_exit_code,
                                infra_crash=bool(report.infra_crash) if report else False,
                                by_effect={ec.value: s for ec, s in report.by_effect.items()}
                                if report else {},
                                excluded=report.excluded if report else [],
                                entities=entities)
                            break
                        except Exception as exc:
                            if type(exc).__name__ == "ProviderUnavailable":
                                # Not a result: wait for the provider and repeat this attempt (no row, no attempt counted).
                                _drain_diagnostics()
                                if not wait_for_provider(manifest, getattr(exc, "kinds", {}), log=log):
                                    log("gave up waiting; the same command resumes with the unfinished runs.")
                                    raise SystemExit(3)
                                attempt -= 1
                                continue
                            row["error"] = f"{type(exc).__name__}: {exc}"
                            row["traceback"] = traceback.format_exc()[-1500:]
                            log(f"  ERROR (attempt {attempt}/{MAX_ATTEMPTS}): {row['error']}")
                row.update(_drain_diagnostics())
                row["attempts"] = attempt
                row["seconds"] = round(time.monotonic() - started, 1)
                _append_jsonl(out, row)
                done, durations, running = tally()  # includes the other workers' runs
                n_done = sum(1 for d in done if d[0] in checkpoints)
                result = f"{row['score']:.3f}" if "score" in row else "FAILED after retries"
                log(_progress_line("score", n_done, total, durations, workers)
                    + f" | {cp} {e['script']} rep{rep}: {result}")
                if n_done % 20 == 0:
                    log("  running means: " + "  ".join(
                        f"{c} {sum(v) / len(v):.3f} (n={len(v)})" for c, v in running.items()))
    who = "this session" if worker is None else f"worker {worker}"
    log(f"providers that served {who}: {dict(served)}")


def _score_worker(manifest: dict, workdir: str, checkpoints: list[str], worker: int, workers: int) -> None:
    """Entry point of one scoring process (must be importable for multiprocessing 'spawn')."""
    sys.stdout.reconfigure(line_buffering=True)
    workdir = Path(workdir)
    _log_to_file(workdir / "logs" / f"score.w{worker}.txt")
    _score_loop(manifest, workdir, checkpoints, out=workdir / f"scores.w{worker}.jsonl",
                claims=workdir / "claims", worker=worker, workers=workers,
                log=lambda msg: print(f"[w{worker}] {msg}"))


def score(
    manifest: dict,
    workdir: str | Path,
    checkpoints: list[str],
    *,
    workers: int = 1,
    log=print,
) -> None:
    """Score each held-out script under each checkpoint, ``reps`` times.

    Order is rep -> script -> checkpoint (each shuffled, see score_order) so a script's
    paired runs are adjacent in time; model drift between weeks then cannot masquerade
    as a library effect. Resumable: (checkpoint, script, rep) triples already in the score
    files are skipped. A run that errors is retried once before its error row is written.

    ``workers`` > 1 runs that many processes over the same order, each taking the next
    unclaimed run and writing its own scores.w<i>.jsonl. Runs are independent of each other
    (throwaway library copy, own temp dirs), so this changes only how long the experiment takes.
    """
    workdir = Path(workdir)
    verify_inputs(manifest, manifest["heldout"])
    lib_hashes = {}
    for cp in checkpoints:
        if not (workdir / "checkpoints" / cp).exists():
            raise FileNotFoundError(f"checkpoint {cp!r} not found — run train first")
        lib_hashes[cp] = library_hash(workdir / "checkpoints" / cp)

    if workers <= 1:
        _score_loop(manifest, workdir, checkpoints, out=workdir / "scores.jsonl",
                    claims=None, worker=None, workers=1, log=log)
    else:
        claims = workdir / "claims"
        shutil.rmtree(claims, ignore_errors=True)  # claims only mean something within one session
        claims.mkdir(parents=True)
        ctx = multiprocessing.get_context("spawn")
        procs = [ctx.Process(target=_score_worker, args=(manifest, str(workdir), checkpoints, i, workers))
                 for i in range(workers)]
        log(f"score: {workers} workers")
        try:
            for p in procs:
                p.start()
            for p in procs:
                p.join()
        finally:
            for p in procs:
                if p.is_alive():
                    p.terminate()
        bad = [i for i, p in enumerate(procs) if p.exitcode != 0]
        if bad:
            raise RuntimeError(f"scoring workers {bad} exited abnormally; rerun to resume")

    # Guard: the snapshots must still be byte-identical to when scoring began.
    for cp, h in lib_hashes.items():
        if library_hash(workdir / "checkpoints" / cp) != h:
            raise RuntimeError(f"checkpoint {cp!r} changed during scoring")


# ---------------------------------------------------------------------------
# Steps 4-6 — analyze
# ---------------------------------------------------------------------------

def per_script_means(rows: list[dict]) -> dict[str, dict[str, float]]:
    """{checkpoint: {script: mean score over valid reps}}; errored reps are dropped."""
    acc: dict[str, dict[str, list[float]]] = {}
    for r in rows:
        s = r.get("score")
        if s is None or (isinstance(s, float) and math.isnan(s)):
            continue
        acc.setdefault(r["checkpoint"], {}).setdefault(r["script"], []).append(s)
    return {cp: {sc: sum(v) / len(v) for sc, v in d.items()} for cp, d in acc.items()}


# The one statement every Rd example starts with: the model already gets it right, and it would
# make nearly every script "targetable". Left out of every entity endpoint.
BOILERPLATE_ENTITIES = frozenset({"suppressPackageStartupMessages"})


def targetable_ids(library_dir: str | Path) -> set[str]:
    """Ids of the patterns in a library that hold a verified translation example, i.e. what
    the translator can be shown. Defined by the trained library alone, never by held-out scores."""
    from r2py.library.store import PatternStore

    return {pid for pid, p in PatternStore(Path(library_dir)).load_all().items() if p.translation_examples}


def is_targetable(entity: dict, ids: set[str]) -> bool:
    """Could the library have told the translator something about this entity? Its own
    function has a pattern, or a base-R function it calls has one."""
    return entity["key"] in ids or any(c in ids for c in entity["calls"])


def _entity_means(rows: list[dict]) -> tuple[dict, dict]:
    """({checkpoint: {script: {entity id: mean score over reps}}}, {script: {entity id: record}})."""
    acc: dict = {}
    meta: dict = {}
    for r in rows:
        for e in r.get("entities") or []:
            if e["name"] in BOILERPLATE_ENTITIES:
                continue
            acc.setdefault(r["checkpoint"], {}).setdefault(r["script"], {}).setdefault(e["id"], []).append(e["score"])
            meta.setdefault(r["script"], {})[e["id"]] = e
    means = {cp: {s: {eid: sum(v) / len(v) for eid, v in ents.items()} for s, ents in d.items()}
             for cp, d in acc.items()}
    return means, meta


def _endpoint(ent_means: dict, meta: dict, ids: set[str], checkpoints: list[str], *,
              targetable: bool) -> dict[str, dict[str, float]]:
    """{checkpoint: {script: mean entity score}} over the entities (targetable, or all the others)
    that were scored under EVERY listed checkpoint, so each script is compared on the same entities."""
    out: dict[str, dict[str, float]] = {cp: {} for cp in checkpoints}
    if not checkpoints:
        return out
    for s in set.intersection(*(set(ent_means.get(cp, {})) for cp in checkpoints)):
        eids = [e for e in set.intersection(*(set(ent_means[cp][s]) for cp in checkpoints))
                if is_targetable(meta[s][e], ids) == targetable]
        for cp in checkpoints:
            if eids:
                out[cp][s] = sum(ent_means[cp][s][e] for e in eids) / len(eids)
    return out


def _trend(means: dict[str, dict[str, float]], order: list[str]) -> dict | None:
    """Page's trend test over the checkpoints in ``order``, script as the block; None if fewer than 3."""
    from scipy import stats

    order = [c for c in order if c in means]
    if len(order) < 3:
        return None
    scripts = [s for s in means[order[0]] if all(s in means[c] for c in order)]
    rows_k = [[means[c][s] for c in order] for s in scripts]
    out = {
        "checkpoints": order, "n": len(scripts),
        "n_monotone_nondecreasing": sum(all(a <= b for a, b in zip(r, r[1:])) for r in rows_k),
        "n_strictly_increasing": sum(all(a < b for a, b in zip(r, r[1:])) for r in rows_k),
        "mean_by_checkpoint": {c: _mean([means[c][s] for s in scripts]) for c in order},
    }
    if len(scripts) > 1:
        res = stats.page_trend_test(rows_k)
        out.update(page_L=float(res.statistic), p_value=float(res.pvalue))
    return out


def _paired_stats(before: dict[str, float], after: dict[str, float], manifest: dict) -> dict:
    """Paired one-sided Wilcoxon signed-rank on per-script (after - before), plus effect sizes."""
    from scipy import stats

    spec = manifest["protocol"]["primary_test"]
    stratum = {e["script"]: e["stratum"] for e in manifest["heldout"]}
    scripts = [e["script"] for e in manifest["heldout"] if e["script"] in before and e["script"] in after]
    diffs = [after[s] - before[s] for s in scripts]
    n = len(diffs)
    out: dict = {
        "n_paired": n,
        "mean_before": _mean([before[s] for s in scripts]),
        "mean_after": _mean([after[s] for s in scripts]),
        "mean_diff": _mean(diffs), "median_diff": _median(diffs),
        "n_improved": sum(d > 0 for d in diffs), "n_worse": sum(d < 0 for d in diffs),
        "n_tied": sum(d == 0 for d in diffs),
    }
    if n > 1:
        out["se_diff"] = math.sqrt(sum((d - out["mean_diff"]) ** 2 for d in diffs) / (n - 1) / n)
    test = {"alternative": spec["alternative"], "zero_method": spec["zero_method"], "alpha": spec["alpha"],
            "statistic": None, "p_value": None, "p_value_two_sided": None, "rank_biserial": None,
            "significant": None, "n_nonzero": sum(d != 0 for d in diffs)}
    if test["n_nonzero"] == 0:
        test.update(p_value=1.0, p_value_two_sided=1.0)  # scipy refuses an all-zero difference vector
    elif n > 0:
        res = stats.wilcoxon(diffs, alternative=spec["alternative"], zero_method=spec["zero_method"])
        two = stats.wilcoxon(diffs, alternative="two-sided", zero_method=spec["zero_method"])
        test.update(statistic=float(res.statistic), p_value=float(res.pvalue),
                    p_value_two_sided=float(two.pvalue), rank_biserial=_rank_biserial(diffs))
    if test["p_value"] is not None:
        test["significant"] = test["p_value"] < spec["alpha"]
    out["test"] = test
    out["by_stratum"] = {
        s: {"n": len(d), "mean_diff": sum(d) / len(d)}
        for s in ALL_STRATA
        if (d := [x for sc, x in zip(scripts, diffs) if stratum[sc] == s])
    }
    return out


def excluded_worklist(rows: list[dict]) -> list[tuple[tuple[str, str], int]]:
    """Data entities left out of scoring, grouped by (R class, Python type), most common first.

    A developer worklist for serialisation adapters: a group is one adapter that would bring
    those variables back into the comparison (Stage 4 Phase 0).  Not shown to the agent --
    the correct translation of ``glm()`` *is* a statsmodels object, so it cannot fix this.
    """
    counts = Counter((x.get("r_class", ""), x.get("py_type", "")) for r in rows for x in r.get("excluded") or [])
    return counts.most_common()


def analyze(manifest: dict, scores_path: str | Path, library_dir: str | Path | None = None,
            checkpoints: list[str] | None = None) -> dict:
    """The pre-specified tests.

    PRIMARY: mean score over the *targetable* entities (those the trained library at
    ``library_dir`` could tell the translator something about), paired by script, full vs
    empty. CONTROL: the same for all other entities. SECONDARY: the whole-script aggregate
    score, the endpoint registered originally. Each also gets a trend test over all checkpoints.
    """
    spec = manifest["protocol"]["primary_test"]
    before, after = spec["before"], spec["after"]
    # Which checkpoints this analysis covers. Defaults to the manifest, but a run that
    # scored only a subset must say so: _trend keeps a checkpoint as soon as ANY row
    # mentions it, then keeps only scripts present in EVERY one — so leftover rows from a
    # dropped checkpoint would silently shrink the trend's n instead of being ignored.
    order_all = [c for c in (checkpoints or manifest["checkpoints"]) if c in manifest["checkpoints"]]
    rows = read_scores(scores_path)
    rows = [r for r in rows if r["checkpoint"] in order_all]
    script_means = per_script_means(rows)
    out: dict = {
        "n_heldout": len(manifest["heldout"]),
        "checkpoints_analyzed": order_all,
        "n_errored_runs": sum(1 for r in rows if "error" in r),
        "n_infra_crash_runs": sum(1 for r in rows if r.get("infra_crash")),
        "harness_hashes": sorted({r["harness_hash"] for r in rows}),
        "llm_settings": sorted({json.dumps(r["llm"], sort_keys=True) for r in rows if "llm" in r}),
        "script_aggregate": {
            **_paired_stats(script_means.get(before, {}), script_means.get(after, {}), manifest),
            "trend": _trend(script_means, order_all),
        },
        "primary": None, "control": None, "share_targetable": None,
    }
    if library_dir is None:
        return out
    ids = targetable_ids(library_dir)
    ent_means, meta = _entity_means(rows)
    pair = _endpoint(ent_means, meta, ids, [before, after], targetable=True)
    rest = _endpoint(ent_means, meta, ids, [before, after], targetable=False)
    order = [c for c in order_all if c in ent_means]
    every = _endpoint(ent_means, meta, ids, order, targetable=True)
    out["primary"] = {**_paired_stats(pair[before], pair[after], manifest), "trend": _trend(every, order)}
    out["control"] = _paired_stats(rest[before], rest[after], manifest)
    entities = [e for d in meta.values() for e in d.values()]
    out["share_targetable"] = _mean([is_targetable(e, ids) for e in entities])
    out["excluded_worklist"] = excluded_worklist(rows)
    return out


def _rank_biserial(diffs: list[float]) -> float:
    """Matched-pairs rank-biserial correlation: (W+ - W-) / (W+ + W-), zero diffs dropped."""
    from scipy.stats import rankdata

    nz = [d for d in diffs if d != 0]
    ranks = rankdata([abs(d) for d in nz])
    pos = sum(r for r, d in zip(ranks, nz) if d > 0)
    return (2 * pos - sum(ranks)) / sum(ranks)


def _mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def _median(xs: list[float]) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def _block(title: str, r: dict | None, spec: dict) -> list[str]:
    if r is None:
        return [f"{title}: not computed (needs the full-checkpoint library)"]
    lines = [f"{title}: {r['n_paired']} paired scripts"]
    if not r["n_paired"]:
        return lines
    t = r["test"]
    lines += [
        f"  mean {spec['before']} {r['mean_before']:.3f}  ->  {spec['after']} {r['mean_after']:.3f}   "
        f"diff {r['mean_diff']:+.3f}" + (f" (SE {r['se_diff']:.3f})" if "se_diff" in r else "")
        + f"   median {r['median_diff']:+.3f}",
        f"  improved / tied / worse: {r['n_improved']} / {r['n_tied']} / {r['n_worse']}",
    ]
    if t["p_value"] is not None:
        verdict = "significant" if t["significant"] else "not significant"
        lines.append(f"  Wilcoxon ({t['alternative']}, zero_method={t['zero_method']}): p={t['p_value']:.4f} "
                     f"at alpha={t['alpha']} -> {verdict} (n_nonzero={t['n_nonzero']}); "
                     f"two-sided p={t['p_value_two_sided']:.4f}"
                     + (f"; rank-biserial r={t['rank_biserial']:+.3f}" if t["rank_biserial"] is not None else ""))
    for s, v in r["by_stratum"].items():
        lines.append(f"    {s:<15} n={v['n']:<3} mean diff {v['mean_diff']:+.3f}  (descriptive)")
    tr = r.get("trend")
    if tr:
        curve = "  ".join(f"{c}={v:.3f}" for c, v in tr["mean_by_checkpoint"].items())
        lines.append(f"  by checkpoint: {curve}")
        lines.append(f"  trend over {len(tr['checkpoints'])} checkpoints, n={tr['n']}: non-decreasing "
                     f"{tr['n_monotone_nondecreasing']}, strictly increasing {tr['n_strictly_increasing']}"
                     + (f", Page L p={tr['p_value']:.4f}" if "p_value" in tr else ""))
    return lines


def format_report(a: dict, manifest: dict) -> str:
    spec = manifest["protocol"]["primary_test"]
    lines = [
        f"Held-out scripts: {a['n_heldout']}   errored runs: {a['n_errored_runs']}   "
        f"infra-crash runs: {a['n_infra_crash_runs']}",
        f"Harness hashes seen: {', '.join(a['harness_hashes']) or '-'}"
        + ("   <-- MORE THAN ONE" if len(a["harness_hashes"]) > 1 else ""),
        f"LLM settings seen: {'; '.join(a['llm_settings']) or '-'}"
        + ("   <-- MORE THAN ONE" if len(a["llm_settings"]) > 1 else ""),
    ]
    if a["share_targetable"] is not None:
        lines.append(f"Share of scored entities the trained library could say something about: {a['share_targetable']:.0%}")
    lines += [""] + _block("PRIMARY   targetable-entity mean", a["primary"], spec)
    lines += [""] + _block("CONTROL   other entities (descriptive; the library had nothing for them)", a["control"], spec)
    lines += [""] + _block("SECONDARY whole-script aggregate score", a["script_aggregate"], spec)
    wl = a.get("excluded_worklist") or []
    if wl:
        lines += ["", "Data entities excluded from scoring (adapter worklist: R class -> Python type):"]
        lines += [f"  {n:4d}  {rc or '?'} -> {pt or '?'}" for (rc, pt), n in wl[:10]]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Progress summary (behind `status`)
# ---------------------------------------------------------------------------

def progress(manifest: dict, workdir: str | Path, checkpoints: list[str] | None = None) -> dict:
    """Where training and scoring stand, computed from the result files alone, so it works from
    another terminal or after a crash."""
    workdir = Path(workdir)
    t_rows = _read_jsonl(workdir / "train_progress.jsonl")
    attempts = Counter(r["script"] for r in t_rows)
    ok = {r["script"] for r in t_rows if "error" not in r}
    finished = {s for s in attempts if s in ok or attempts[s] >= MAX_ATTEMPTS}
    s_rows = read_scores(workdir / "scores.jsonl")
    checkpoints = [c for c in (checkpoints or manifest["checkpoints"])
                   if c in manifest["checkpoints"]]
    by_cp: dict[str, list[float]] = {}
    for r in s_rows:
        if "score" in r:
            by_cp.setdefault(r["checkpoint"], []).append(r["score"])
    return {
        "train": {
            "done": len(finished), "total": len(manifest["train"]), "failed": len(finished - ok),
            "durations": [r["seconds"] for r in t_rows if "seconds" in r],
            "patterns": next((r["patterns"] for r in reversed(t_rows) if "patterns" in r), None),
            "last": t_rows[-1]["timestamp"] if t_rows else None,
        },
        "score": {
            "done": len({(r["checkpoint"], r["script"], r["rep"]) for r in s_rows
                         if r["checkpoint"] in checkpoints}),
            "total": manifest["protocol"]["reps"] * len(manifest["heldout"]) * len(checkpoints),
            "errors": sum(1 for r in s_rows if "error" in r),
            "durations": [r["seconds"] for r in s_rows if "seconds" in r],
            "by_checkpoint": {c: {"n": len(v), "mean": sum(v) / len(v)}
                              for c, v in by_cp.items() if c in checkpoints},
            "last": s_rows[-1]["timestamp"] if s_rows else None,
            # parallel sessions: the workers seen among the most recent runs
            "workers": max(1, len({r["worker"] for r in s_rows[-30:] if r.get("worker") is not None})),
        },
    }


def format_progress(p: dict) -> str:
    def stage(name: str, s: dict, extra: str) -> list[str]:
        d = s["durations"]
        avg = sum(d) / len(d) if d else 0.0
        head = (f"{name}: {s['done']}/{s['total']} ({100 * s['done'] / s['total'] if s['total'] else 100:.0f}%)"
                f"{extra}")
        if not d:
            return [head + "   (not started)"]
        w = s.get("workers", 1)
        return [head, f"  avg {_fmt_duration(avg)}/run | active {_fmt_duration(sum(d) / w)} | "
                      f"ETA {_fmt_duration(avg * (s['total'] - s['done']) / w)} | last run started {s['last']}"
                      + (f" | {w} workers" if w > 1 else "")]

    t, s = p["train"], p["score"]
    lines = stage("Training", t, f"   failed: {t['failed']}   patterns: {t['patterns']}")
    lines += stage("Scoring", s, f"   errored runs: {s['errors']}")
    if s["by_checkpoint"]:
        lines.append("  mean score so far: " + "  ".join(
            f"{c} {v['mean']:.3f} (n={v['n']})" for c, v in s["by_checkpoint"].items()))
    return "\n".join(lines)
