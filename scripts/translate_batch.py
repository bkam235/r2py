"""Batch translation runner — §10.

Iterates over work/inputs/ (or --input-dir), writes results to work/outputs/,
and appends rows to work/analysis/learning_curve.csv and
work/analysis/scoring_table.csv.

Usage:
    python scripts/translate_batch.py [--input-dir DIR] [--force] [--max-iters N]

CLI: r2py translate <input.R> <output.py> (single script)
     This script handles the bulk corpus run.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow importing r2py when run directly from the project root
sys.path.insert(0, str(Path(__file__).parent.parent))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="translate_batch",
        description="Batch-translate all R scripts in a directory.",
    )
    parser.add_argument("--input-dir", default="work/inputs",
                        help="Directory to scan for .R files (default: work/inputs)")
    parser.add_argument("--output-dir", default="work/outputs",
                        help="Root directory for output runs (default: work/outputs)")
    parser.add_argument("--learning-curve-csv", default="work/analysis/learning_curve.csv",
                        dest="learning_curve_csv")
    parser.add_argument("--scoring-table-csv", default="work/analysis/scoring_table.csv",
                        dest="scoring_table_csv")
    parser.add_argument("--max-iters", type=int, default=8, dest="max_iters")
    parser.add_argument("--score-threshold", type=float, default=0.85, dest="score_threshold")
    parser.add_argument("--no-seeds", action="store_true", dest="no_seeds")
    parser.add_argument("--data-compare", default="auto", dest="data_compare",
                        choices=["auto", "exact", "embedding"])
    parser.add_argument("--force", action="store_true",
                        help="Re-translate scripts that already have an output dir")
    parser.add_argument("--no-recursive", action="store_true", dest="no_recursive",
                        help="Do not recurse into subdirectories")
    args = parser.parse_args()

    from r2py.batch import translate_batch

    results = translate_batch(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        learning_curve_csv=args.learning_curve_csv,
        scoring_table_csv=args.scoring_table_csv,
        recursive=not args.no_recursive,
        max_iters=args.max_iters,
        score_threshold=args.score_threshold,
        no_seeds=args.no_seeds,
        data_compare=args.data_compare,
        force=args.force,
    )

    errors = [r for r in results if "error" in r]
    successes = [r for r in results if "error" not in r]
    print(f"\nDone: {len(successes)} translated, {len(errors)} errors.")


if __name__ == "__main__":
    main()
