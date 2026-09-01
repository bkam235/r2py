#!/usr/bin/env python3
"""Model comparison test for r2py.

Test 1 — harness:  Translate N scripts with Gemma, Haiku and Sonnet via the
                   r2py pipeline (library frozen — no patterns recorded).
Test 2 — score:    Score Python files translated outside the harness so their
                   scores are directly comparable with Test 1.

Usage:
    python scripts/run_comparison.py select              # pick 10 random scripts
    python scripts/run_comparison.py harness              # run all three models
    python scripts/run_comparison.py harness --model gemma  # run one model only
    python scripts/run_comparison.py score                # score manual translations
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env", override=True)

# ── paths ────────────────────────────────────────────────────────────────────
INPUT_DIR   = ROOT / "work" / "inputs" / "harvested"
COMP_DIR    = ROOT / "work" / "comparison"
SCRIPT_LIST = COMP_DIR / "scripts.txt"
HARNESS_CSV = COMP_DIR / "harness_results.csv"
MANUAL_DIR  = COMP_DIR / "manual"
MANUAL_CSV  = COMP_DIR / "manual_results.csv"

N_SCRIPTS = 10

MODELS = {
    "gemma":  "openrouter:google/gemma-4-31b-it",
    "haiku":  "claude-haiku-4-5",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-6",
}

CSV_FIELDS = [
    "timestamp", "script", "model", "score",
    "iterations", "exit_code", "stdout", "data", "env",
]


# ── frozen library (read patterns, never write) ─────────────────────────────
class _FrozenLibrary:
    """Wraps a PatternLibrary so translations can READ patterns but never WRITE."""

    def __init__(self, inner):
        self._inner = inner

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def record_evidence(self, *a, **kw):     pass
    def record_tie(self, *a, **kw):          pass
    def record_contradiction(self, *a, **kw): pass


# ── helpers ──────────────────────────────────────────────────────────────────
def _load_scripts() -> list[str]:
    if not SCRIPT_LIST.exists():
        print(f"No {SCRIPT_LIST} found — run 'select' first.")
        sys.exit(1)
    return [l.strip() for l in SCRIPT_LIST.read_text().splitlines() if l.strip()]


def _by_effect(report) -> dict[str, float]:
    if report is None:
        return {}
    from r2py.types import EffectClass
    return {ec.value: score for ec, score in report.by_effect.items()}


def _append_csv(path: Path, row: dict) -> None:
    exists = path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def _progress(event) -> None:
    if event.kind == "analysis_done":
        print(f"  [Stage 1] {event.entity_count} entities")
    elif event.kind == "seed_done":
        print(f"  [Seed]    {event.score:.3f}")
    elif event.kind == "done":
        print(f"  [Done]    {event.score:.3f}")


# ── subcommands ──────────────────────────────────────────────────────────────
def cmd_select(args: argparse.Namespace) -> int:
    """Pick N random R scripts and save the list."""
    all_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".R")]
    if len(all_files) < N_SCRIPTS:
        print(f"Only {len(all_files)} scripts available, need {N_SCRIPTS}.")
        return 1

    chosen = sorted(random.sample(all_files, N_SCRIPTS))
    COMP_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_LIST.write_text("\n".join(chosen) + "\n", encoding="utf-8")
    print(f"Selected {N_SCRIPTS} scripts → {SCRIPT_LIST}")
    for s in chosen:
        print(f"  {s}")
    return 0


def cmd_harness(args: argparse.Namespace) -> int:
    """Test 1: translate with the r2py harness (frozen library)."""
    from r2py import analyze
    from r2py.library import get_library
    from r2py.loop import run_loop

    scripts = _load_scripts()
    lib = _FrozenLibrary(get_library())

    if args.model:
        if args.model not in MODELS:
            print(f"Unknown model alias '{args.model}'. Choose from: {', '.join(MODELS)}")
            return 1
        models = {args.model: MODELS[args.model]}
    else:
        models = MODELS

    for model_name, model_id in models.items():
        out_dir = COMP_DIR / "harness" / model_name
        out_dir.mkdir(parents=True, exist_ok=True)

        for r_file in scripts:
            stem = r_file.removesuffix(".R")
            py_path = out_dir / f"{stem}.py"
            r_path = INPUT_DIR / r_file

            print(f"\n{'='*60}")
            print(f"  {model_name} | {r_file}")
            print(f"{'='*60}")

            try:
                script_map = analyze(r_path)
                result = run_loop(
                    script_map, lib,
                    model=model_id,
                    escalation_model=model_id,
                    score_threshold=0.85,
                    n_bare_seeds=2,
                    n_structured_seeds=2,
                    max_iters=12,
                    max_stalls=5,
                    progress=_progress,
                )
                py_path.write_text(result.python_source, encoding="utf-8")

                effects = _by_effect(result.final_score_report)
                row = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "script":     stem,
                    "model":      model_name,
                    "score":      f"{result.final_score:.4f}",
                    "iterations": result.iterations,
                    "exit_code":  result.final_exit_code,
                    "stdout":     f"{effects.get('stdout', ''):.4f}" if "stdout" in effects else "",
                    "data":       f"{effects.get('data', ''):.4f}"   if "data"   in effects else "",
                    "env":        f"{effects.get('env', ''):.4f}"    if "env"    in effects else "",
                }
                _append_csv(HARNESS_CSV, row)
                print(f"  → score={result.final_score:.3f}  iters={result.iterations}")

            except Exception as exc:
                print(f"  ERROR: {exc}")
                _append_csv(HARNESS_CSV, {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "script": stem, "model": model_name,
                    "score": "0", "iterations": 0, "exit_code": -1,
                    "stdout": "", "data": "", "env": "",
                })

    print(f"\nResults written to {HARNESS_CSV}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    """Test 2: score Python files translated outside the harness."""
    from r2py import analyze
    from r2py.stage4 import verify

    scripts = _load_scripts()

    if not MANUAL_DIR.exists():
        MANUAL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Place manually-translated .py files in {MANUAL_DIR}/")
        print("Filenames must match the R scripts (with .py extension).")
        print(f"\nExpected files:")
        for s in scripts:
            print(f"  {s.removesuffix('.R')}.py")
        return 0

    scored = 0
    for r_file in scripts:
        stem = r_file.removesuffix(".R")
        py_path = MANUAL_DIR / f"{stem}.py"
        r_path = INPUT_DIR / r_file

        if not py_path.exists():
            print(f"  SKIP {stem} (no .py file in manual/)")
            continue

        print(f"\n  Scoring {stem} ...")
        try:
            script_map = analyze(r_path)
            py_source = py_path.read_text(encoding="utf-8")
            report = verify(script_map, py_source)

            effects = _by_effect(report)
            row = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "script":     stem,
                "model":      args.label,
                "score":      f"{report.aggregate:.4f}",
                "iterations": 0,
                "exit_code":  report.py_exit_code,
                "stdout":     f"{effects.get('stdout', ''):.4f}" if "stdout" in effects else "",
                "data":       f"{effects.get('data', ''):.4f}"   if "data"   in effects else "",
                "env":        f"{effects.get('env', ''):.4f}"    if "env"    in effects else "",
            }
            _append_csv(MANUAL_CSV, row)
            print(f"  → score={report.aggregate:.3f}")
            scored += 1

        except Exception as exc:
            print(f"  ERROR: {exc}")

    print(f"\n{scored} files scored → {MANUAL_CSV}")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(description="r2py model comparison test")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("select", help="Pick random R scripts for the test")

    p_harness = sub.add_parser("harness", help="Test 1: harness translations")
    p_harness.add_argument("--model", choices=list(MODELS), default=None,
                           help="Run a single model instead of all three")

    p_score = sub.add_parser("score", help="Test 2: score manual translations")
    p_score.add_argument("--label", default="manual",
                         help="Label for the model column (default: 'manual')")

    args = parser.parse_args()
    if args.cmd == "select":
        return cmd_select(args)
    elif args.cmd == "harness":
        return cmd_harness(args)
    elif args.cmd == "score":
        return cmd_score(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
