"""Batch translation runner — §10."""
from __future__ import annotations

import csv
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


_LEARNING_CURVE_HEADER = [
    "timestamp", "script_id", "final_score", "iterations",
    "evidence_added", "contradictions_added",
]
_SCORING_TABLE_HEADER = [
    "script_id", "final_score", "iterations", "timestamp",
]


def translate_batch(
    input_dir: str | Path = "work/inputs",
    output_dir: str | Path = "work/outputs",
    learning_curve_csv: str | Path = "work/analysis/learning_curve.csv",
    scoring_table_csv: str | Path = "work/analysis/scoring_table.csv",
    *,
    recursive: bool = True,
    model: str | None = None,
    max_iters: int = 8,
    score_threshold: float = 0.85,
    no_seeds: bool = False,
    data_compare: str = "auto",
    force: bool = False,
    max_stalls: int = 3,
) -> list[dict]:
    """Translate all R scripts under input_dir, writing CSV tracking files.

    Returns a list of per-script result dicts with keys:
      script_id, final_score, iterations, evidence_added, contradictions_added,
      output_py, timestamp — or "error" on failure.
    """
    from r2py import translate as _translate
    from r2py.stage2.llm import _DEFAULT_MODEL
    if model is None:
        model = _DEFAULT_MODEL

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    lc_path = Path(learning_curve_csv)
    st_path = Path(scoring_table_csv)

    r_files = sorted(input_dir.rglob("*.R") if recursive else input_dir.glob("*.R"))
    if not r_files:
        print(f"No .R files found under {input_dir}", file=sys.stderr)
        return []

    # Load existing scoring table so we can upsert
    scoring: dict[str, dict] = _load_scoring_table(st_path)

    results: list[dict] = []

    for r_path in r_files:
        script_id = r_path.relative_to(input_dir).as_posix()

        # Skip if ANY prior timestamped run dir for this script already exists.
        # (Each run creates a new "<stem>__<ts>" dir, so checking the fresh dir's
        # existence would always be False — we match the stem prefix instead.)
        existing = (
            list(output_dir.glob(f"{r_path.stem}__*"))
            if output_dir.exists() else []
        )
        if not force and existing:
            print(f"skip {script_id} (prior run exists; use force=True to re-run)")
            continue

        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = output_dir / f"{r_path.stem}__{ts}"
        py_path = run_dir / "output.py"

        run_dir.mkdir(parents=True, exist_ok=True)
        print(f"translating {script_id} ...", end=" ", flush=True)

        try:
            result = _translate(
                r_path=r_path,
                py_path=py_path,
                model=model,
                max_iters=max_iters,
                score_threshold=score_threshold,
                no_seeds=no_seeds,
                data_compare=data_compare,
                output_dir=run_dir,
                max_stalls=max_stalls,
            )
            row = {
                "script_id": script_id,
                "final_score": result.final_score,
                "iterations": result.iterations,
                "evidence_added": len(result.pattern_evidence_added),
                "contradictions_added": len(result.pattern_contradictions_added),
                "output_py": str(py_path),
                "timestamp": ts,
            }
            print(f"score={result.final_score:.3f} iters={result.iterations}")
        except Exception as exc:
            traceback.print_exc()
            row = {
                "script_id": script_id,
                "error": str(exc),
                "timestamp": ts,
            }
            print(f"ERROR: {exc}")

        results.append(row)

        # Append to learning curve CSV (only successful runs)
        if "error" not in row:
            _append_learning_curve(lc_path, row)
            scoring[script_id] = {
                "script_id": script_id,
                "final_score": row["final_score"],
                "iterations": row["iterations"],
                "timestamp": ts,
            }

    _write_scoring_table(st_path, scoring)
    return results


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def _append_learning_curve(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_LEARNING_CURVE_HEADER,
                                extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def _load_scoring_table(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        return {r["script_id"]: r for r in csv.DictReader(f)}


def _write_scoring_table(path: Path, scoring: dict[str, dict]) -> None:
    if not scoring:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_SCORING_TABLE_HEADER,
                                extrasaction="ignore")
        writer.writeheader()
        for row in scoring.values():
            writer.writerow(row)
