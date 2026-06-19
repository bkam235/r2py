"""Manual stratified ablation harness — §12.4.1."""
from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from r2py.library import get_library


class _FrozenLibrary:
    """Wraps a PatternLibrary to disable all write operations (run A of ablation)."""

    def __init__(self, inner: Any) -> None:
        self._inner = inner

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def record_evidence(self, *args: Any, **kwargs: Any) -> None:  # noqa: D102
        pass

    def record_tie(self, *args: Any, **kwargs: Any) -> None:  # noqa: D102
        pass

    def record_contradiction(self, *args: Any, **kwargs: Any) -> None:  # noqa: D102
        pass


def run_ablation(
    slice_path: str | Path = "work/inputs/ablation_slice.txt",
    compare: str = "frozen-vs-learning",
    output_dir: str | Path = "work/analysis/ablation",
    *,
    max_iters: int = 8,
) -> dict:
    """Run the paired ablation experiment and write results.

    compare="frozen-vs-learning"  : run A = library frozen, run B = learning on
    compare="heuristic-vs-learned": run A = heuristic retrieval, run B = learned_retrieval=True

    Returns a summary dict with keys: n_scripts, mean_delta, p_value, test, regressions.
    Writes work/analysis/ablation/<ts>/per_script.csv and summary.json.
    """
    if compare not in ("frozen-vs-learning", "heuristic-vs-learned"):
        raise ValueError(f"compare must be 'frozen-vs-learning' or 'heuristic-vs-learned', got {compare!r}")

    slice_path = Path(slice_path)
    scripts = _read_slice(slice_path)
    if not scripts:
        raise ValueError(f"No scripts found in slice manifest {slice_path}")

    import r2py as _r2py

    library = get_library()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(output_dir) / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Ablation ({compare}) — {len(scripts)} scripts — results → {out_dir}")

    scores_a: dict[str, float] = {}
    scores_b: dict[str, float] = {}

    # ---- Run A ----
    # Always freeze in run A so the starting library state is identical for both
    # runs — this gives a clean comparison in both modes:
    #   frozen-vs-learning : A=no-learning baseline, B=learning on
    #   heuristic-vs-learned: A=heuristic-retrieval baseline (frozen), B=learned on
    lib_a = _FrozenLibrary(library)
    print("\n--- Run A ---")
    for idx, r_path_str in enumerate(scripts):
        r_path = Path(r_path_str)
        label = r_path.name
        try:
            result = _r2py.translate(
                r_path=r_path,
                py_path=str(out_dir / f"A_{idx:03d}_{r_path.stem}.py"),
                library=lib_a,
                max_iters=max_iters,
            )
            scores_a[r_path_str] = result.final_score
            print(f"  A {label}: {result.final_score:.3f}")
        except Exception as exc:
            print(f"  A {label}: ERROR — {exc}", file=sys.stderr)
            scores_a[r_path_str] = float("nan")

    # ---- Run B ----
    lib_b = library  # learning-enabled; sees library in its pre-run-A state
    if compare == "heuristic-vs-learned":
        lib_b.learned_retrieval = True
    print("\n--- Run B ---")
    for idx, r_path_str in enumerate(scripts):
        r_path = Path(r_path_str)
        label = r_path.name
        try:
            result = _r2py.translate(
                r_path=r_path,
                py_path=str(out_dir / f"B_{idx:03d}_{r_path.stem}.py"),
                library=lib_b,
                max_iters=max_iters,
            )
            scores_b[r_path_str] = result.final_score
            print(f"  B {label}: {result.final_score:.3f}")
        except Exception as exc:
            print(f"  B {label}: ERROR — {exc}", file=sys.stderr)
            scores_b[r_path_str] = float("nan")

    # ---- Statistics ----
    valid = [
        s for s in scripts
        if not math.isnan(scores_a.get(s, float("nan")))
        and not math.isnan(scores_b.get(s, float("nan")))
    ]
    deltas = [scores_b[s] - scores_a[s] for s in valid]
    mean_delta = sum(deltas) / len(deltas) if deltas else 0.0
    regressions = [s for s, d in zip(valid, deltas) if d < 0]

    p_value, test_name = _significance(deltas)

    # ---- Write per_script.csv ----
    csv_path = out_dir / "per_script.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["script_id", "score_A", "score_B", "delta"])
        for s in scripts:
            sa = scores_a.get(s, float("nan"))
            sb = scores_b.get(s, float("nan"))
            d = sb - sa if not (math.isnan(sa) or math.isnan(sb)) else float("nan")
            w.writerow([s, sa, sb, d])

    # ---- Write summary.json ----
    summary = {
        "compare": compare,
        "n_scripts": len(scripts),
        "n_valid": len(valid),
        "mean_delta": mean_delta,
        "p_value": p_value,
        "test": test_name,
        "regressions": regressions,
        "timestamp": ts,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nResults: n={len(valid)}  mean_delta={mean_delta:+.3f}"
          f"  p={p_value:.3f} ({test_name})"
          f"  regressions={len(regressions)}")
    print(f"Outputs written to {out_dir}")

    return summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_slice(path: Path) -> list[str]:
    """Return non-blank, non-comment lines from the slice manifest."""
    if not path.exists():
        raise FileNotFoundError(f"Slice manifest not found: {path}")
    scripts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            scripts.append(line)
    return scripts


def _significance(deltas: list[float]) -> tuple[float, str]:
    """Return (p_value, test_name) for a one-sample test of mean_delta == 0."""
    if len(deltas) < 2:
        return 1.0, "insufficient_data"

    try:
        from scipy import stats
        # Wilcoxon signed-rank test (non-parametric; handles small N well)
        # zero_method="zsplit" handles ties without dropping zero-delta pairs
        stat, p = stats.wilcoxon(deltas, zero_method="zsplit")
        return float(p), "wilcoxon"
    except ImportError:
        pass

    # Fallback: exact sign test using binomial CDF (two-tailed)
    n_pos = sum(1 for d in deltas if d > 0)
    n_neg = sum(1 for d in deltas if d < 0)
    n = n_pos + n_neg
    if n == 0:
        return 1.0, "sign_test"
    # P(X >= n_pos | H0: p=0.5) two-tailed via normal approx
    k = max(n_pos, n_neg)
    p = 2 * _binom_tail(k, n, 0.5)
    return min(p, 1.0), "sign_test"


def _binom_tail(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p) via normal approximation."""
    if n == 0:
        return 1.0
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    if sigma == 0:
        return 0.0 if k > mu else 1.0
    z = (k - 0.5 - mu) / sigma  # continuity correction
    return 0.5 * math.erfc(z / math.sqrt(2))
