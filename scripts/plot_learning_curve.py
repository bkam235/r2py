"""Plot how mean translation scores evolve over successive runs.

Reads work/analysis/run_history.jsonl (one JSON object per line) and
produces two charts:

1. Cumulative mean score — running average across all runs, ordered
   chronologically.  Shows whether the system improves as the pattern
   library grows.

2. Per-script best score over time — for scripts translated more than
   once, tracks the best score achieved so far at each attempt.

Usage:
    python scripts/plot_learning_curve.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "work" / "analysis" / "run_history.jsonl"
OUT_DIR = ROOT / "assets"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    raise SystemExit("matplotlib is required: pip install matplotlib")


def load_runs() -> list[dict]:
    with open(HISTORY, encoding="utf-8") as f:
        runs = [json.loads(line) for line in f if line.strip()]
    runs.sort(key=lambda r: r["timestamp"])
    return runs


def cumulative_mean(scores: list[float]) -> list[float]:
    out: list[float] = []
    total = 0.0
    for i, s in enumerate(scores, 1):
        total += s
        out.append(total / i)
    return out


def rolling_mean(scores: list[float], window: int) -> list[float]:
    out: list[float] = []
    buf: list[float] = []
    for s in scores:
        buf.append(s)
        if len(buf) > window:
            buf.pop(0)
        out.append(sum(buf) / len(buf))
    return out


STYLE = {
    "bg": "#ffffff",
    "text": "#0b0b0b",
    "muted": "#52514e",
    "grid": "#e1e0d9",
    "spine": "#c3c2b7",
    "blue": "#2a78d6",
    "orange": "#eb6834",
    "green": "#1baf7a",
}


def style_ax(ax, ylabel: str) -> None:
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=STYLE["grid"], linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(STYLE["spine"])
    ax.spines["bottom"].set_color(STYLE["spine"])
    ax.tick_params(axis="both", colors=STYLE["muted"], labelsize=9)
    ax.set_ylabel(ylabel, fontsize=10, color=STYLE["muted"])


def main() -> None:
    runs = load_runs()
    if not runs:
        print("No runs found in run_history.jsonl")
        return

    OUT_DIR.mkdir(exist_ok=True)
    scores = [r["final_score"] for r in runs]
    xs = list(range(1, len(scores) + 1))

    # ── Chart 1: cumulative mean + rolling mean ─────────────────────────
    cum = cumulative_mean(scores)
    roll = rolling_mean(scores, window=20)
    unique_scripts: list[int] = []
    seen: set[str] = set()
    for r in runs:
        seen.add(r["script"])
        unique_scripts.append(len(seen))

    fig, ax1 = plt.subplots(figsize=(9, 5))
    fig.subplots_adjust(top=0.85, bottom=0.12, left=0.09, right=0.88)

    ax1.scatter(xs, scores, s=12, alpha=0.35, color=STYLE["blue"],
                zorder=2, label="Individual run")
    ax1.plot(xs, cum, color=STYLE["blue"], linewidth=2,
             label="Cumulative mean", zorder=3)
    ax1.plot(xs, roll, color=STYLE["orange"], linewidth=1.5,
             linestyle="--", label="Rolling mean (w=20)", zorder=3)
    ax1.set_xlabel("Run number (chronological)", fontsize=10,
                   color=STYLE["muted"])
    ax1.set_ylim(-0.05, 1.1)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    style_ax(ax1, "Score")
    ax1.legend(loc="lower right", fontsize=9, framealpha=0.9)

    ax2 = ax1.twinx()
    ax2.plot(xs, unique_scripts, color=STYLE["green"], linewidth=1.5,
             alpha=0.6, zorder=1)
    ax2.set_ylabel("Unique scripts translated", fontsize=10,
                   color=STYLE["green"])
    ax2.tick_params(axis="y", colors=STYLE["green"], labelsize=9)
    ax2.spines["right"].set_color(STYLE["green"])
    ax2.spines["top"].set_visible(False)

    fig.suptitle("Translation score over successive runs",
                 fontsize=13, fontweight="medium", color=STYLE["text"],
                 x=0.09, ha="left")
    fig.text(0.09, 0.89,
             f"{len(runs)} runs across {len(seen)} scripts — "
             "does the pattern library improve scores over time?",
             fontsize=9, color=STYLE["muted"], ha="left")

    path1 = OUT_DIR / "chart_learning_curve.png"
    fig.savefig(path1, dpi=200, facecolor="white")
    plt.close(fig)
    print(f"Saved {path1}")

    # ── Chart 2: per-script best-so-far across attempts ─────────────────
    # For scripts with multiple runs, show how the best score evolves.
    from collections import defaultdict
    script_runs: dict[str, list[float]] = defaultdict(list)
    for r in runs:
        script_runs[r["script"]].append(r["final_score"])

    multi = {s: v for s, v in script_runs.items() if len(v) >= 3}
    if not multi:
        print("Not enough multi-run scripts for per-script chart.")
        return

    fig2, ax3 = plt.subplots(figsize=(9, 5))
    fig2.subplots_adjust(top=0.85, bottom=0.12, left=0.09, right=0.95)

    # Compute best-so-far for each script and plot
    for script, sc in sorted(multi.items(), key=lambda x: -len(x[1])):
        best_so_far: list[float] = []
        best = 0.0
        for s in sc:
            best = max(best, s)
            best_so_far.append(best)
        attempts = list(range(1, len(best_so_far) + 1))
        short = script.split("__")[0]
        ax3.plot(attempts, best_so_far, marker="o", markersize=4,
                 linewidth=1.5, alpha=0.7, label=f"{short} ({len(sc)}x)")

    ax3.set_xlabel("Attempt number", fontsize=10, color=STYLE["muted"])
    ax3.set_ylim(-0.05, 1.1)
    ax3.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    style_ax(ax3, "Best score so far")
    ax3.legend(loc="lower right", fontsize=8, framealpha=0.9, ncol=2)

    fig2.suptitle("Per-script best score across repeated attempts",
                  fontsize=13, fontweight="medium", color=STYLE["text"],
                  x=0.09, ha="left")
    fig2.text(0.09, 0.89,
              f"Scripts with 3+ runs — best-so-far trajectory",
              fontsize=9, color=STYLE["muted"], ha="left")

    path2 = OUT_DIR / "chart_per_script_progress.png"
    fig2.savefig(path2, dpi=200, facecolor="white")
    plt.close(fig2)
    print(f"Saved {path2}")


if __name__ == "__main__":
    main()
