"""Offline retrieval reranker trainer — §12.6 A.

Reads logged retrieval episodes from work/outputs/*/edits.log.jsonl,
trains a LightGBM LambdaMART model, and writes a versioned artifact to
work/models/reranker/ only if it beats the heuristic baseline on NDCG@3.

CLI: python scripts/train_reranker.py [--min-episodes 500] [--out work/models/reranker/]
     r2py library train-reranker [--min-episodes 500] [--out work/models/reranker/]

Requirements: pip install lightgbm numpy
"""
import argparse
import sys
from pathlib import Path

# Allow running as a script from the project root.
sys.path.insert(0, str(Path(__file__).parent.parent))

from r2py.library.reranker import train


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train the optional retrieval reranker (§12.6 A)."
    )
    parser.add_argument(
        "--min-episodes", type=int, default=500, dest="min_episodes",
        help="Minimum logged retrieval episodes required (default: 500).",
    )
    parser.add_argument(
        "--out", default="work/models/reranker/",
        help="Output directory for the trained artifact.",
    )
    parser.add_argument(
        "--log-glob", default="work/outputs/*/edits.log.jsonl", dest="log_glob",
        help="Glob pattern for edits.log.jsonl files.",
    )
    parser.add_argument(
        "--library-dir", default="work/library", dest="library_dir",
        help="Path to the Pattern Library directory.",
    )
    args = parser.parse_args()

    rc = train(
        out_dir=args.out,
        min_episodes=args.min_episodes,
        log_glob=args.log_glob,
        library_dir=args.library_dir,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
