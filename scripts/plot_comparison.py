"""Generate comparison bar charts from work/comparison/all_results.csv."""

import csv
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "work" / "comparison" / "all_results.csv"
OUT_DIR = ROOT / "assets"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    raise SystemExit("matplotlib is required: pip install matplotlib")


def load_scores():
    groups = {}
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["model"], row["source"])
            groups.setdefault(key, []).append(float(row["score"]))
    out = {}
    for (model, source), vals in groups.items():
        n = len(vals)
        mean = sum(vals) / n
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / (n - 1))
        out[(model, source)] = (mean, std)
    return out


COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


def make_chart(ax, labels, means, stds, colors, title, subtitle):
    bars = ax.bar(labels, means, width=0.5, color=colors, zorder=3,
                  edgecolor="none", linewidth=0)
    for bar in bars:
        bar.set_clip_on(False)
    ax.errorbar(range(len(labels)), means, yerr=stds, fmt="none",
                ecolor="#52514e", elinewidth=1.5, capsize=5, capthick=1.5,
                zorder=4)
    for i, (m, s) in enumerate(zip(means, stds)):
        y = min(m + s, 1.0) + 0.03
        ax.text(i, y, f"{m:.2f}", ha="center", va="bottom",
                fontsize=11, fontweight="medium", color="#0b0b0b")
    ax.set_ylim(0, 1.15)
    ax.set_xlim(-0.6, len(labels) - 0.4)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7")
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(axis="x", colors="#898781", labelsize=10)
    ax.tick_params(axis="y", colors="#898781", labelsize=10)
    fig = ax.get_figure()
    fig.suptitle(title, fontsize=14, fontweight="medium", color="#0b0b0b",
                 x=0.1, ha="left", y=0.95)
    fig.text(0.1, 0.90, subtitle, fontsize=10, color="#52514e",
             ha="left", va="top")


def main():
    s = load_scores()
    OUT_DIR.mkdir(exist_ok=True)

    # Chart 1: harness comparison
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    fig1.subplots_adjust(top=0.82, bottom=0.10, left=0.1, right=0.95)
    labels1 = ["Gemma 4", "Haiku 4.5", "Sonnet 4.6", "Opus 4.6"]
    keys1 = [("gemma", "harness"), ("haiku", "harness"),
             ("sonnet", "harness"), ("opus", "harness")]
    means1 = [s[k][0] for k in keys1]
    stds1 = [s[k][1] for k in keys1]
    make_chart(ax1, labels1, means1, stds1, COLORS,
               "r2py harness: score by model",
               "Mean execution-equivalence score across 10 R scripts, "
               "error bars = 1 std dev")
    fig1.savefig(OUT_DIR / "chart_harness.png", dpi=200, facecolor="white")
    plt.close(fig1)
    print(f"Saved {OUT_DIR / 'chart_harness.png'}")

    # Chart 2: Gemma+harness vs Claude Code
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    fig2.subplots_adjust(top=0.82, bottom=0.13, left=0.1, right=0.95)
    labels2 = ["Gemma 4\n+ r2py", "Haiku 4.5\n+ Claude Code",
               "Sonnet 4.6\n+ Claude Code", "Opus 4.6\n+ Claude Code"]
    keys2 = [("gemma", "harness"), ("haiku", "claude_code"),
             ("sonnet", "claude_code"), ("opus", "claude_code")]
    means2 = [s[k][0] for k in keys2]
    stds2 = [s[k][1] for k in keys2]
    make_chart(ax2, labels2, means2, stds2, COLORS,
               "Gemma + r2py vs. Claude Code",
               "Local Gemma 4 with r2py harness vs. frontier models "
               "without harness support")
    fig2.savefig(OUT_DIR / "chart_vs_claude_code.png", dpi=200,
                 facecolor="white")
    plt.close(fig2)
    print(f"Saved {OUT_DIR / 'chart_vs_claude_code.png'}")


if __name__ == "__main__":
    main()
