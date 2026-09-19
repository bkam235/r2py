"""Held-out experiment: does a trained Pattern Library help on unseen scripts?

Protocol (steps 1-6):

1. ``select``  — fix a stratified held-out set (never used to train the library)
   plus an ordered training set, and write both to a manifest with content hashes.
2. ``train``   — build the library from empty on the training set only, snapshotting
   it at the ``empty`` / ``half`` / ``full`` checkpoints.
3. ``score``   — score every held-out script under every checkpoint, ``reps`` times.
   Each run gets a throwaway copy of the checkpoint, so held-out scripts can never
   teach the library (or each other).
4. ``analyze`` — pair by script, average over reps, one-sided Wilcoxon signed-rank on
   (full - empty); Page's trend test over empty < half < full is secondary.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

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
    "n_train": 227,
    "reps": 3,
    # Mirrors the settings in scripts/translate.py.
    "translate": {
        "model": "openrouter:google/gemma-4-31b-it",
        "score_threshold": 0.9,
        "n_bare_seeds": 2,
        "n_structured_seeds": 2,
        "max_iters": 20,
        "max_stalls": 10,
        "timeout_s": 60,
        "data_compare": "auto",
    },
    "primary_test": {
        "name": "wilcoxon_signed_rank",
        "before": "empty",
        "after": "full",
        "alternative": "greater",
        "alpha": 0.05,
        "zero_method": "wilcox",
    },
}


def package_of(script: str) -> str:
    return script.split("__")[0]


def stratum_of(script: str) -> str:
    return _STRATUM_OF_PACKAGE.get(package_of(script), OTHER)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def harness_hash() -> str:
    """Hash of all r2py source, so a mid-experiment code change is detectable."""
    h = hashlib.sha256()
    for p in sorted((ROOT / "r2py").rglob("*.py")):
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(p.read_bytes())
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
    n_train: int = DEFAULT_PROTOCOL["n_train"],
    reps: int = DEFAULT_PROTOCOL["reps"],
    seed: int = DEFAULT_PROTOCOL["seed"],
) -> dict:
    """Draw the held-out and training sets from pool_dir and return the manifest."""
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
    if len(remaining) < n_train:
        raise ValueError(f"only {len(remaining)} scripts left for training, need {n_train}")
    train = rng.sample(remaining, n_train)

    def entry(name: str) -> dict:
        return {"script": name, "package": package_of(name),
                "stratum": stratum_of(name), "sha256": _sha256(pool_path / name)}

    protocol = {**DEFAULT_PROTOCOL, "seed": seed, "n_heldout": n_heldout,
                "n_train": n_train, "reps": reps}
    return {
        "protocol": protocol,
        "pool_dir": str(pool_dir),
        "pool_size": len(pool),
        "checkpoints": {"empty": 0, "half": n_train // 2, "full": n_train},
        "stratum_quotas": quotas,
        "heldout": [entry(n) for n in heldout],
        "train": [entry(n) for n in train],
    }


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

def _translate_once(r_path: Path, py_path: Path, lib, cfg: dict, *, learn: bool):
    """analyze -> run_loop, then (only if learn) seed the library.

    r2py.translate() also seeds unconditionally, git-commits the library, and appends
    to run_history.jsonl; none of that belongs in an experiment.
    """
    from r2py import seed_from_translation
    from r2py.loop import run_loop
    from r2py.stage1 import analyze

    py_path.parent.mkdir(parents=True, exist_ok=True)
    result = run_loop(
        analyze(r_path), lib,
        max_iters=cfg["max_iters"],
        score_threshold=cfg["score_threshold"],
        data_compare=cfg["data_compare"],
        n_bare_seeds=cfg["n_bare_seeds"],
        n_structured_seeds=cfg["n_structured_seeds"],
        checkpoint_path=py_path,
        model=cfg["model"],
        escalation_model=cfg["model"],
        timeout_s=cfg["timeout_s"],
        max_stalls=cfg["max_stalls"],
    )
    py_path.write_text(result.python_source, encoding="utf-8")
    if learn and result.final_score >= cfg["score_threshold"]:
        seed_from_translation(
            r_path, py_path, library=lib, script_id=r_path.stem,
            score_report=result.final_score_report,
            entity_score_threshold=cfg["score_threshold"],
        )
    return result


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
# Step 2 — train
# ---------------------------------------------------------------------------

def train(manifest: dict, workdir: str | Path, *, log=print) -> None:
    """Build the library from empty on the training set, snapshotting each checkpoint.

    Resumable: scripts already recorded in train_progress.jsonl are skipped.
    """
    from r2py.library import PatternLibrary

    workdir = Path(workdir)
    verify_inputs(manifest, manifest["train"])
    cfg = manifest["protocol"]["translate"]
    pool = _pool_path(manifest)
    ckpt_dir = workdir / "checkpoints"
    progress_path = workdir / "train_progress.jsonl"
    done = {r["script"] for r in _read_jsonl(progress_path)}

    counts = {n: c for n, c in manifest["checkpoints"].items() if c > 0}
    if not (ckpt_dir / "empty").exists():
        if done:
            raise RuntimeError("training already started but the empty checkpoint is missing")
        PatternLibrary(ckpt_dir / "empty")  # creates the empty store + index

    lib = PatternLibrary(workdir / "lib_live")
    for i, e in enumerate(manifest["train"], start=1):
        if e["script"] not in done:
            log(f"[train {i}/{len(manifest['train'])}] {e['script']}")
            row = {"script": e["script"], "index": i, "timestamp": _now()}
            try:
                r = _translate_once(pool / e["script"],
                                    workdir / "train_outputs" / (Path(e["script"]).stem + ".py"),
                                    lib, cfg, learn=True)
                row.update(score=r.final_score, patterns=len(lib.index.all_ids()))
            except Exception as exc:
                row["error"] = f"{type(exc).__name__}: {exc}"
                log(f"  ERROR: {row['error']}")
            _append_jsonl(progress_path, row)
        for name, count in counts.items():
            if i == count and not (ckpt_dir / name).exists():
                shutil.copytree(workdir / "lib_live", ckpt_dir / name)
                log(f"checkpoint {name!r} at {i} scripts ({len(lib.index.all_ids())} patterns)")


# ---------------------------------------------------------------------------
# Step 3 — score (with repetitions)
# ---------------------------------------------------------------------------

def score(
    manifest: dict,
    workdir: str | Path,
    checkpoints: list[str],
    *,
    log=print,
) -> None:
    """Score each held-out script under each checkpoint, ``reps`` times.

    Order is rep -> script -> checkpoint so a script's paired runs are adjacent in
    time; model drift between weeks then cannot masquerade as a library effect.
    Resumable: (checkpoint, script, rep) triples already in scores.jsonl are skipped.
    """
    from r2py.library import PatternLibrary

    workdir = Path(workdir)
    verify_inputs(manifest, manifest["heldout"])
    cfg = manifest["protocol"]["translate"]
    pool = _pool_path(manifest)
    scores_path = workdir / "scores.jsonl"
    done = {(r["checkpoint"], r["script"], r["rep"]) for r in _read_jsonl(scores_path)}
    lib_hashes = {}
    for cp in checkpoints:
        if not (workdir / "checkpoints" / cp).exists():
            raise FileNotFoundError(f"checkpoint {cp!r} not found — run train first")
        lib_hashes[cp] = library_hash(workdir / "checkpoints" / cp)
    hh = harness_hash()

    for rep in range(manifest["protocol"]["reps"]):
        for e in manifest["heldout"]:
            for cp in checkpoints:
                if (cp, e["script"], rep) in done:
                    continue
                log(f"[score rep{rep}] {cp} | {e['script']}")
                row = {"checkpoint": cp, "script": e["script"], "rep": rep,
                       "library_hash": lib_hashes[cp], "harness_hash": hh,
                       "model": cfg["model"], "timestamp": _now()}
                # Fresh copy per run: whatever the loop writes is discarded.
                with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                    shutil.copytree(workdir / "checkpoints" / cp, Path(tmp) / "lib")
                    try:
                        r = _translate_once(
                            pool / e["script"],
                            workdir / "outputs" / cp / f"rep{rep}" / (Path(e["script"]).stem + ".py"),
                            PatternLibrary(Path(tmp) / "lib"), cfg, learn=False)
                        report = r.final_score_report
                        row.update(
                            score=r.final_score, iterations=r.iterations,
                            exit_code=r.final_exit_code,
                            infra_crash=bool(report.infra_crash) if report else False,
                            by_effect={ec.value: s for ec, s in report.by_effect.items()}
                            if report else {})
                    except Exception as exc:
                        row["error"] = f"{type(exc).__name__}: {exc}"
                        log(f"  ERROR: {row['error']}")
                _append_jsonl(scores_path, row)

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


def analyze(manifest: dict, scores_path: str | Path) -> dict:
    """Pre-specified primary test plus the secondary three-checkpoint trend test."""
    from scipy import stats

    spec = manifest["protocol"]["primary_test"]
    rows = _read_jsonl(Path(scores_path))
    means = per_script_means(rows)
    before, after = spec["before"], spec["after"]
    stratum = {e["script"]: e["stratum"] for e in manifest["heldout"]}
    scripts = [e["script"] for e in manifest["heldout"]
               if e["script"] in means.get(before, {}) and e["script"] in means.get(after, {})]
    diffs = [means[after][s] - means[before][s] for s in scripts]
    n = len(diffs)

    out: dict = {
        "n_heldout": len(manifest["heldout"]), "n_paired": n,
        "n_excluded": len(manifest["heldout"]) - n,
        "n_errored_runs": sum(1 for r in rows if "error" in r),
        "n_infra_crash_runs": sum(1 for r in rows if r.get("infra_crash")),
        "harness_hashes": sorted({r["harness_hash"] for r in rows}),
        "mean_before": sum(means[before][s] for s in scripts) / n if n else None,
        "mean_after": sum(means[after][s] for s in scripts) / n if n else None,
        "mean_diff": sum(diffs) / n if n else None,
        "median_diff": _median(diffs),
        "n_improved": sum(d > 0 for d in diffs),
        "n_worse": sum(d < 0 for d in diffs),
        "n_tied": sum(d == 0 for d in diffs),
    }
    if n > 1:
        mean = out["mean_diff"]
        out["se_diff"] = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1) / n)

    out["primary"] = {**spec, "statistic": None, "p_value": None,
                      "significant": None, "n_nonzero": sum(d != 0 for d in diffs)}
    if out["primary"]["n_nonzero"] == 0:
        out["primary"]["p_value"] = 1.0  # scipy refuses an all-zero difference vector
    elif n > 0:
        res = stats.wilcoxon(diffs, alternative=spec["alternative"],
                             zero_method=spec["zero_method"])
        out["primary"].update(statistic=float(res.statistic), p_value=float(res.pvalue))
    if out["primary"]["p_value"] is not None:
        out["primary"]["significant"] = out["primary"]["p_value"] < spec["alpha"]

    out["by_stratum"] = {
        s: {"n": len(d), "mean_diff": sum(d) / len(d)}
        for s in ALL_STRATA
        if (d := [x for sc, x in zip(scripts, diffs) if stratum[sc] == s])
    }

    # Secondary (step 5): trend across empty < half < full, script as the block.
    order = [c for c in ("empty", "half", "full") if c in means]
    if len(order) == 3:
        trio = [s for s in scripts if s in means["half"]]
        rows3 = [[means[c][s] for c in order] for s in trio]
        out["trend"] = {
            "n": len(trio),
            "n_monotone_nondecreasing": sum(r[0] <= r[1] <= r[2] for r in rows3),
            "n_strictly_increasing": sum(r[0] < r[1] < r[2] for r in rows3),
            "n_decreasing_somewhere": sum(r[0] > r[1] or r[1] > r[2] for r in rows3),
        }
        if len(trio) > 1:
            res = stats.page_trend_test(rows3)
            out["trend"].update(page_L=float(res.statistic), p_value=float(res.pvalue))
    return out


def _median(xs: list[float]) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def format_report(a: dict) -> str:
    p = a["primary"]
    lines = [
        f"Paired scripts: {a['n_paired']} of {a['n_heldout']} "
        f"({a['n_excluded']} excluded: no valid score at both checkpoints)",
        f"Errored runs: {a['n_errored_runs']}   infra-crash runs: {a['n_infra_crash_runs']}",
        f"Harness hashes seen: {', '.join(a['harness_hashes']) or '-'}"
        + ("   <-- MORE THAN ONE" if len(a["harness_hashes"]) > 1 else ""),
    ]
    if a["n_paired"]:
        lines += [
            f"Mean score {p['before']}: {a['mean_before']:.3f}   {p['after']}: {a['mean_after']:.3f}",
            f"Mean diff: {a['mean_diff']:+.3f}"
            + (f" (SE {a['se_diff']:.3f})" if "se_diff" in a else "")
            + f"   median: {a['median_diff']:+.3f}",
            f"Improved / tied / worse: {a['n_improved']} / {a['n_tied']} / {a['n_worse']}",
        ]
    if p["p_value"] is not None:
        verdict = "significant" if p["significant"] else "not significant"
        lines.append(
            f"PRIMARY  Wilcoxon signed-rank ({p['alternative']}, zero_method={p['zero_method']}): "
            f"p={p['p_value']:.4f} at alpha={p['alpha']} -> {verdict} (n_nonzero={p['n_nonzero']})")
    for s, v in a["by_stratum"].items():
        lines.append(f"  {s:<15} n={v['n']:<3} mean diff {v['mean_diff']:+.3f}  (descriptive)")
    if "trend" in a:
        t = a["trend"]
        lines.append(
            f"SECONDARY trend (empty<half<full), n={t['n']}: monotone {t['n_monotone_nondecreasing']}, "
            f"strictly increasing {t['n_strictly_increasing']}, non-monotone {t['n_decreasing_somewhere']}"
            + (f", Page L p={t['p_value']:.4f}" if "p_value" in t else ""))
    return "\n".join(lines)
