"""Manual stratified ablation harness — §12.4.1.

Reads the pinned slice manifest (work/inputs/ablation_slice.txt), translates it
twice (library frozen vs. learning on, identical seeds/max_iters), and writes
per-script A/B scores, aggregate B-A with significance check, and the regression
list to work/analysis/ablation/<ts>/.

Usage:
    python scripts/run_ablation.py [--slice FILE] [--compare MODE]

CLI: r2py ablation [--slice FILE] [--compare MODE]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow importing r2py when run directly from the project root
sys.path.insert(0, str(Path(__file__).parent.parent))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="run_ablation",
        description="Run the manual stratified ablation experiment (§12.4.1).",
    )
    parser.add_argument("--slice", default="work/inputs/ablation_slice.txt",
                        help="Path to the pinned slice manifest")
    parser.add_argument("--compare", default="frozen-vs-learning",
                        choices=["frozen-vs-learning", "heuristic-vs-learned"],
                        help="Which pair to compare (default: frozen-vs-learning)")
    parser.add_argument("--output-dir", default="work/analysis/ablation",
                        dest="output_dir")
    parser.add_argument("--max-iters", type=int, default=8, dest="max_iters")
    args = parser.parse_args()

    from r2py.ablation import run_ablation

    summary = run_ablation(
        slice_path=args.slice,
        compare=args.compare,
        output_dir=args.output_dir,
        max_iters=args.max_iters,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
