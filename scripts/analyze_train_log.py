"""Training-run metrics from the plan's Measurement table, computed the same way every time.

Compare a run with the baseline by running this on both and diffing the output:

    python scripts/analyze_train_log.py                                  # the first run
    python scripts/analyze_train_log.py --progress P.jsonl --stdout S.txt --library L/

Inputs: the run's ``train_progress.jsonl`` (one row per script: score, patterns, seconds), the
captured stdout (agent steps and rewrite scores), and optionally a library directory (examples
per pattern).  Every figure is derived, none is typed in.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_ACTION = re.compile(r"\[Agent\]\s+Step \d+: (\w+)")
_SCORED = re.compile(r"\[Agent\]\s+Rewrite scored: ([\d.]+) \(was ([\d.]+)\)")
_SYNTAX = re.compile(r"\[Agent\]\s+Syntax error")
_EPS = 1e-9


def progress_metrics(rows: list[dict], threshold: float = 0.9) -> dict:
    """Per-script figures.  A script "contributed" if the library grew while it ran."""
    rows = [r for r in rows if "score" in r]
    prev, contributed, wasted = 0, 0, 0.0
    for r in rows:
        if r["patterns"] > prev:
            contributed += 1
        else:
            wasted += r["seconds"]
        prev = r["patterns"]
    secs = sorted(r["seconds"] for r in rows)
    hours = sum(secs) / 3600
    return {
        "scripts": len(rows),
        "compute_hours": hours,
        "patterns": rows[-1]["patterns"] if rows else 0,
        "patterns_per_compute_hour": (rows[-1]["patterns"] / hours) if rows and hours else 0.0,
        "share_scripts_contributing": contributed / len(rows) if rows else 0.0,
        "share_reaching_threshold": sum(r["score"] >= threshold for r in rows) / len(rows) if rows else 0.0,
        "share_compute_on_scripts_teaching_nothing": wasted / sum(secs) if secs else 0.0,
        "p95_seconds": secs[min(len(secs) - 1, int(0.95 * len(secs)))] if secs else 0.0,
        "worst_three_hours": sum(secs[-3:]) / 3600,
    }


def stdout_metrics(text: str) -> dict:
    """Agent behaviour from the run's captured output."""
    actions = Counter(a for a in _ACTION.findall(text))
    scored = [(float(n), float(o)) for n, o in _SCORED.findall(text)]
    n = len(scored)
    improved = sum(new > old + _EPS for new, old in scored)
    worse = sum(new < old - _EPS for new, old in scored)
    total_actions = sum(actions.values())
    return {
        "actions": dict(actions),
        "share_non_rewrite_actions": (1 - actions.get("rewrite", 0) / total_actions) if total_actions else 0.0,
        "rewrites_scored": n,
        "share_rewrites_improving": improved / n if n else 0.0,
        "share_rewrites_unchanged": (n - improved - worse) / n if n else 0.0,
        "share_rewrites_worsening": worse / n if n else 0.0,
        "share_rewrites_catastrophic": sum(new == 0 and old > 0 for new, old in scored) / n if n else 0.0,
        "syntax_rejections": len(_SYNTAX.findall(text)),
        "share_rewrites_syntax_rejected": len(_SYNTAX.findall(text)) / (n + len(_SYNTAX.findall(text)))
        if n or _SYNTAX.search(text) else 0.0,
    }


def library_metrics(library: Path) -> dict:
    """Examples per pattern, from the ``## Translation Examples`` bullets of each pattern file."""
    counts = []
    for f in sorted((library / "patterns").glob("*.md")):
        body = f.read_text(encoding="utf-8")
        section = body.split("## Translation Examples", 1)[1].split("\n## ", 1)[0] \
            if "## Translation Examples" in body else ""  # stop before "## Edit Examples"
        counts.append(sum(1 for line in section.splitlines() if line.startswith("- {")))
    return {
        "patterns_in_library": len(counts),
        "median_examples_per_pattern": statistics.median(counts) if counts else 0,
        "share_single_example": sum(c == 1 for c in counts) / len(counts) if counts else 0.0,
    }


def render(m: dict) -> str:
    out = []
    for section, vals in m.items():
        out.append(f"[{section}]")
        for k, v in vals.items():
            out.append(f"  {k:44s} {v:.3f}" if isinstance(v, float) else f"  {k:44s} {v}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--progress", type=Path, default=ROOT / "work/heldout/train_progress.jsonl")
    ap.add_argument("--stdout", type=Path, default=ROOT / "experiments/train_stdout.txt")
    ap.add_argument("--library", type=Path, default=ROOT / "work/heldout/lib_live")
    ap.add_argument("--threshold", type=float, default=0.9)
    args = ap.parse_args()

    metrics: dict[str, dict] = {}
    if args.progress.exists():
        rows = [json.loads(line) for line in args.progress.read_text(encoding="utf-8").splitlines() if line]
        metrics["progress"] = progress_metrics(rows, args.threshold)
    if args.stdout.exists():
        metrics["agent"] = stdout_metrics(args.stdout.read_text(encoding="utf-8", errors="replace"))
    if args.library.exists():
        metrics["library"] = library_metrics(args.library)
    if not metrics:
        sys.exit("no inputs found")
    print(render(metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main())
