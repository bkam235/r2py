"""
work/analysis/plot_learning_curve.py -- visualise r2py v0.2 translation progress.

Usage:
    python work/analysis/plot_learning_curve.py [options]

Options:
    --output-dir DIR          Where to write PNGs (default: work/analysis/plots)
    --learning-curve-csv PATH (default: work/analysis/learning_curve.csv)
    --scoring-table-csv PATH  (default: work/analysis/scoring_table.csv)
    --outputs-dir DIR         Run output dirs to scan (default: work/outputs)
    --plots LIST              Comma-separated subset of plot names to generate.
                              Names: timeline, distribution, iters, evidence,
                                     trajectories, effects, edits
                              Default: all

Data sources (written by existing pipeline):
    learning_curve.csv  -- one row per script per batch run (batch.py)
    scoring_table.csv   -- latest score per script (batch.py)
    work/outputs/<run>/score_report.{n}.json -- per-iteration decomposition (loop.py)
    work/outputs/<run>/edits.log.jsonl        -- edit episodes/transitions (loop.py)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_ALL_PLOTS = ("timeline", "distribution", "iters", "evidence",
              "trajectories", "effects", "edits")

_EFFECT_ORDER = ("data", "variable", "callable", "stdout",
                 "graphics", "html", "files", "env", "warnings", "rng", "network")

_EDIT_OUTCOMES = ("accepted", "tie", "rejected")
_OUTCOME_COLORS = {"accepted": "#4caf50", "tie": "#ff9800", "rejected": "#f44336"}

sns.set_theme(style="whitegrid", palette="muted", font_scale=0.95)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_csv(path: Path, name: str) -> pd.DataFrame | None:
    if not path.exists():
        print(f"  [skip] {name}: {path} not found", file=sys.stderr)
        return None
    try:
        df = pd.read_csv(path)
        if df.empty:
            print(f"  [skip] {name}: CSV is empty", file=sys.stderr)
            return None
        return df
    except Exception as exc:
        print(f"  [skip] {name}: {exc}", file=sys.stderr)
        return None


def load_learning_curve(path: Path) -> pd.DataFrame | None:
    df = _load_csv(path, "learning_curve")
    if df is None:
        return None
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    df["run_index"] = range(len(df))
    return df


def load_scoring_table(path: Path) -> pd.DataFrame | None:
    return _load_csv(path, "scoring_table")


def _iter_run_dirs(outputs_dir: Path) -> list[Path]:
    if not outputs_dir.exists():
        return []
    return sorted(p for p in outputs_dir.iterdir() if p.is_dir())


def _load_score_reports(run_dir: Path) -> list[dict]:
    """Return score_report dicts sorted by iteration index for one run dir."""
    reports = []
    for p in run_dir.glob("score_report.*.json"):
        try:
            idx = int(p.stem.split(".")[-1])
            data = json.loads(p.read_text(encoding="utf-8"))
            data["_idx"] = idx
            reports.append(data)
        except Exception:
            continue
    return sorted(reports, key=lambda r: r["_idx"])


def _load_edit_log(run_dir: Path) -> list[dict]:
    p = run_dir / "edits.log.jsonl"
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def load_run_data(outputs_dir: Path) -> tuple[list[list[dict]], list[list[dict]]]:
    """Return (all_score_report_sequences, all_edit_rows) across all run dirs."""
    all_reports: list[list[dict]] = []
    all_edits: list[list[dict]] = []
    for run_dir in _iter_run_dirs(outputs_dir):
        reports = _load_score_reports(run_dir)
        if reports:
            all_reports.append(reports)
        edits = _load_edit_log(run_dir)
        if edits:
            all_edits.append(edits)
    return all_reports, all_edits


# ---------------------------------------------------------------------------
# Plot 1 — Score timeline (learning curve proper)
# ---------------------------------------------------------------------------

def plot_score_timeline(lc_df: pd.DataFrame, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))

    scores = lc_df["final_score"].tolist()
    xs = lc_df["run_index"].tolist()

    # Raw dots
    ax.scatter(xs, scores, s=18, alpha=0.35, color="steelblue", zorder=2, label="Script score")

    # Rolling mean (window = min(20, N//4, 1))
    window = max(1, min(20, len(scores) // 4))
    if len(scores) >= 2:
        rm = pd.Series(scores).rolling(window, min_periods=1).mean()
        ax.plot(xs, rm, color="steelblue", lw=2, zorder=3,
                label=f"Rolling mean (w={window})")

    ax.axhline(0.85, color="grey", lw=0.9, linestyle=":", alpha=0.7)
    ax.text(0.01, 0.875, "pass threshold (0.85)", transform=ax.transAxes,
            fontsize=8, color="grey", va="bottom")

    ax.set_xlabel("Batch run order")
    ax.set_ylabel("Final score")
    ax.set_title("Learning Curve — Final Score per Script over Batch Runs")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=9, loc="lower right")

    _save(fig, out_dir / "score_timeline.png")


# ---------------------------------------------------------------------------
# Plot 2 — Score distribution
# ---------------------------------------------------------------------------

def plot_score_distribution(st_df: pd.DataFrame, out_dir: Path) -> None:
    scores = st_df["final_score"].dropna().astype(float)
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(scores, bins=20, kde=True, ax=ax, color="steelblue",
                 edgecolor="white", linewidth=0.4)

    ax.axvline(0.85, color="grey", lw=1.2, linestyle="--", alpha=0.8,
               label="Pass threshold (0.85)")
    ax.axvline(scores.mean(), color="steelblue", lw=1.5, linestyle="-.",
               label=f"Mean = {scores.mean():.3f}")

    n_pass = (scores >= 0.85).sum()
    ax.text(0.97, 0.95,
            f"n = {len(scores)}\npass = {n_pass} ({100*n_pass/len(scores):.0f}%)",
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

    ax.set_xlabel("Final score")
    ax.set_ylabel("Count")
    ax.set_title("Score Distribution Across Scripts (latest run per script)")
    ax.legend(fontsize=9)

    _save(fig, out_dir / "score_distribution.png")


# ---------------------------------------------------------------------------
# Plot 3 — Iterations vs score
# ---------------------------------------------------------------------------

def plot_iterations_vs_score(lc_df: pd.DataFrame, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    # Colour-encode by recency: older runs are lighter
    n = len(lc_df)
    colours = plt.cm.Blues(np.linspace(0.25, 0.95, n))

    sc = ax.scatter(
        lc_df["iterations"].astype(int),
        lc_df["final_score"].astype(float),
        c=colours, s=30, alpha=0.75, edgecolors="none", zorder=2,
    )

    # Add a colourbar indicating run order
    sm = plt.cm.ScalarMappable(cmap="Blues",
                                norm=plt.Normalize(vmin=1, vmax=n))
    sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, pad=0.02)
    cb.set_label("Run order (1 = oldest)", fontsize=8)

    ax.axhline(0.85, color="grey", lw=0.9, linestyle=":", alpha=0.7)
    ax.set_xlabel("Iterations used")
    ax.set_ylabel("Final score")
    ax.set_title("Iterations Used vs Final Score")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save(fig, out_dir / "iterations_vs_score.png")


# ---------------------------------------------------------------------------
# Plot 4 — Evidence / contradiction accumulation
# ---------------------------------------------------------------------------

def plot_evidence_accumulation(lc_df: pd.DataFrame, out_dir: Path) -> None:
    df = lc_df.sort_values("run_index")
    ev = df["evidence_added"].astype(int).cumsum()
    co = df["contradictions_added"].astype(int).cumsum()
    xs = df["run_index"].tolist()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(xs, ev, alpha=0.25, color="seagreen")
    ax.plot(xs, ev, color="seagreen", lw=1.8, label="Cumulative evidence added")
    ax.fill_between(xs, co, alpha=0.20, color="tomato")
    ax.plot(xs, co, color="tomato", lw=1.8, linestyle="--",
            label="Cumulative contradictions added")

    ax.set_xlabel("Batch run order")
    ax.set_ylabel("Cumulative count")
    ax.set_title("Library Growth — Evidence and Contradictions Accumulated")
    ax.legend(fontsize=9)

    _save(fig, out_dir / "evidence_accumulation.png")


# ---------------------------------------------------------------------------
# Plot 5 — Per-run iteration trajectories
# ---------------------------------------------------------------------------

def plot_run_trajectories(all_reports: list[list[dict]], out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    max_iters = max(len(seq) for seq in all_reports)
    matrix = np.full((len(all_reports), max_iters), np.nan)

    for row_i, seq in enumerate(all_reports):
        for rep in seq:
            col_i = rep["_idx"]
            if col_i < max_iters:
                matrix[row_i, col_i] = rep.get("aggregate", np.nan)

    xs = list(range(max_iters))
    for row in matrix:
        valid = ~np.isnan(row)
        if valid.any():
            ax.plot(np.where(valid)[0], row[valid],
                    color="steelblue", alpha=0.18, lw=0.9)

    # Mean trajectory (ignoring NaN)
    mean_traj = np.nanmean(matrix, axis=0)
    valid_mean = ~np.isnan(mean_traj)
    if valid_mean.any():
        ax.plot(np.where(valid_mean)[0], mean_traj[valid_mean],
                color="steelblue", lw=2.5, label=f"Mean ({len(all_reports)} runs)")

    ax.axhline(0.85, color="grey", lw=0.9, linestyle=":", alpha=0.7)
    ax.set_xlabel("Iteration index")
    ax.set_ylabel("Aggregate score")
    ax.set_title("Per-Run Score Trajectories Across Iterations")
    ax.set_ylim(-0.05, 1.05)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.legend(fontsize=9)

    _save(fig, out_dir / "run_trajectories.png")


# ---------------------------------------------------------------------------
# Plot 6 — Effect class score breakdown
# ---------------------------------------------------------------------------

def plot_effect_class_scores(all_reports: list[list[dict]], out_dir: Path) -> None:
    # Use the final score_report from each run (highest _idx per run).
    scores_by_effect: dict[str, list[float]] = {}
    for seq in all_reports:
        final = max(seq, key=lambda r: r["_idx"])
        for ec, score in final.get("by_effect", {}).items():
            scores_by_effect.setdefault(ec, []).append(float(score))

    if not scores_by_effect:
        print("  [skip] effect class scores: no by_effect data found", file=sys.stderr)
        return

    # Order by _EFFECT_ORDER then alphabetical for any extras.
    ordered = [ec for ec in _EFFECT_ORDER if ec in scores_by_effect]
    ordered += sorted(ec for ec in scores_by_effect if ec not in ordered)

    means = [np.mean(scores_by_effect[ec]) for ec in ordered]
    stds  = [np.std(scores_by_effect[ec])  for ec in ordered]

    fig, ax = plt.subplots(figsize=(8, max(3, len(ordered) * 0.5 + 1)))

    colours = ["#4caf50" if m >= 0.85 else "#ff9800" if m >= 0.5 else "#f44336"
               for m in means]
    y_pos = range(len(ordered))
    ax.barh(list(y_pos), means, xerr=stds, color=colours, alpha=0.85,
            error_kw=dict(ecolor="grey", capsize=3, lw=1), height=0.6)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(ordered)
    ax.axvline(0.85, color="grey", lw=0.9, linestyle=":", alpha=0.7)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Mean score (± std)")
    ax.set_title("Effect Class Score Breakdown (final iteration per run)")

    _save(fig, out_dir / "effect_class_scores.png")


# ---------------------------------------------------------------------------
# Plot 7 — Edit outcome rates by edit kind
# ---------------------------------------------------------------------------

def plot_edit_outcomes(all_edits: list[list[dict]], out_dir: Path) -> None:
    # Flatten and filter to rows that have edit_kind and outcome.
    flat = [row for seq in all_edits for row in seq
            if row.get("edit_kind") and row.get("outcome")]

    if not flat:
        print("  [skip] edit outcomes: no edit_kind/outcome data in edits.log.jsonl",
              file=sys.stderr)
        return

    df = pd.DataFrame(flat)
    kinds = sorted(df["edit_kind"].unique())
    counts = {kind: {o: 0 for o in _EDIT_OUTCOMES} for kind in kinds}
    for _, row in df.iterrows():
        k, o = row["edit_kind"], row["outcome"]
        if o in _EDIT_OUTCOMES:
            counts[k][o] += 1

    totals = {k: sum(counts[k].values()) for k in kinds}
    fracs  = {k: {o: counts[k][o] / totals[k] for o in _EDIT_OUTCOMES}
              for k in kinds}

    fig, ax = plt.subplots(figsize=(9, max(3, len(kinds) * 0.55 + 1.5)))
    y_pos = range(len(kinds))
    left = np.zeros(len(kinds))

    for outcome in _EDIT_OUTCOMES:
        vals = [fracs[k][outcome] for k in kinds]
        ax.barh(list(y_pos), vals, left=left, color=_OUTCOME_COLORS[outcome],
                alpha=0.85, label=outcome, height=0.6)
        left += np.array(vals)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(kinds)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Fraction of edits")
    ax.set_title("Edit Outcome Rates by Edit Kind")
    ax.legend(loc="lower right", fontsize=9)

    # Annotate with total counts
    for i, k in enumerate(kinds):
        ax.text(1.01, i, str(totals[k]), va="center", fontsize=8, color="grey")

    _save(fig, out_dir / "edit_outcomes.png")


# ---------------------------------------------------------------------------
# Save helper
# ---------------------------------------------------------------------------

def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot r2py v0.2 learning curves and diagnostics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--output-dir", default="work/analysis/plots",
                        help="Directory for output PNGs")
    parser.add_argument("--learning-curve-csv", default="work/analysis/learning_curve.csv")
    parser.add_argument("--scoring-table-csv",  default="work/analysis/scoring_table.csv")
    parser.add_argument("--outputs-dir",         default="work/outputs",
                        help="Directory containing per-run output subdirs")
    parser.add_argument("--plots", default=",".join(_ALL_PLOTS),
                        help=f"Comma-separated plot names. Available: {', '.join(_ALL_PLOTS)}")
    args = parser.parse_args()

    out_dir    = Path(args.output_dir)
    lc_path    = Path(args.learning_curve_csv)
    st_path    = Path(args.scoring_table_csv)
    runs_dir   = Path(args.outputs_dir)
    wanted     = {p.strip() for p in args.plots.split(",")}

    unknown = wanted - set(_ALL_PLOTS)
    if unknown:
        print(f"Unknown plot names: {unknown}. Choose from: {', '.join(_ALL_PLOTS)}",
              file=sys.stderr)
        sys.exit(1)

    # Load data
    lc_df = load_learning_curve(lc_path)
    st_df = load_scoring_table(st_path)
    all_reports, all_edits = load_run_data(runs_dir)

    generated = []

    # --- CSV-based plots ---
    csv_plots = {
        "timeline":     (plot_score_timeline,       lc_df,  "learning_curve.csv"),
        "distribution": (plot_score_distribution,   st_df,  "scoring_table.csv"),
        "iters":        (plot_iterations_vs_score,  lc_df,  "learning_curve.csv"),
        "evidence":     (plot_evidence_accumulation,lc_df,  "learning_curve.csv"),
    }
    for name, (fn, df, src) in csv_plots.items():
        if name not in wanted:
            continue
        if df is None:
            print(f"  [skip] {name}: requires {src}", file=sys.stderr)
            continue
        print(f"plotting {name} ...")
        fn(df, out_dir)
        generated.append(name)

    # --- Run-dir-based plots ---
    run_plots = {
        "trajectories": (plot_run_trajectories,    all_reports, "score_report.*.json"),
        "effects":      (plot_effect_class_scores, all_reports, "score_report.*.json"),
        "edits":        (plot_edit_outcomes,       all_edits,   "edits.log.jsonl"),
    }
    for name, (fn, data, src) in run_plots.items():
        if name not in wanted:
            continue
        if not data:
            print(f"  [skip] {name}: no {src} found under {runs_dir}", file=sys.stderr)
            continue
        print(f"plotting {name} ...")
        fn(data, out_dir)
        generated.append(name)

    print(f"\nDone. {len(generated)}/{len(wanted)} plots written to {out_dir}/")
    skipped = wanted - set(generated)
    if skipped:
        print(f"  Skipped (missing data): {', '.join(sorted(skipped))}")


if __name__ == "__main__":
    main()
