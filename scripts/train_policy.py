"""Offline contextual bandit edit policy trainer — §12.6 B.

Reads logged PolicyTransition records from work/outputs/*/edits.log.jsonl,
trains a LinUCB contextual bandit via offline IPS, and writes a versioned
artifact to work/models/policy/ only if it beats the ε-greedy baseline.

CLI: python scripts/train_policy.py [--min-transitions 200] [--out work/models/policy/]

Requirements: no external dependencies beyond the standard library.
"""
import argparse
import sys
from pathlib import Path

# Allow running as a script from the project root.
sys.path.insert(0, str(Path(__file__).parent.parent))

from r2py.library.bandit import train


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train the optional contextual bandit edit policy (§12.6 B)."
    )
    parser.add_argument(
        "--min-transitions", type=int, default=200, dest="min_transitions",
        help="Minimum logged policy transitions required (default: 200).",
    )
    parser.add_argument(
        "--min-per-arm", type=int, default=30, dest="min_per_arm",
        help="Minimum transitions per EditKind arm before warning (default: 30).",
    )
    parser.add_argument(
        "--out", default="work/models/policy/",
        help="Output directory for the trained artifact.",
    )
    parser.add_argument(
        "--log-glob", default="work/outputs/*/edits.log.jsonl", dest="log_glob",
        help="Glob pattern for edits.log.jsonl files.",
    )
    args = parser.parse_args()

    rc = train(
        out_dir=args.out,
        min_transitions=args.min_transitions,
        min_per_arm=args.min_per_arm,
        log_glob=args.log_glob,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
