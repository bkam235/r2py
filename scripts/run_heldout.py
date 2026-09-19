"""Held-out experiment: does a trained Pattern Library help on unseen scripts?

Run the steps in order:

    python scripts/run_heldout.py select            # writes experiments/heldout/manifest.json
    python scripts/run_heldout.py train             # builds empty/half/full library checkpoints
    python scripts/run_heldout.py score             # scores held-out set at every checkpoint
    python scripts/run_heldout.py analyze           # paired Wilcoxon + trend test

Commit the manifest BEFORE running train/score. train and score are resumable.
Score after training has finished (not before) so that the checkpoints are compared
under the same model and the same installed packages.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env", override=True)

from r2py import heldout as ho

MANIFEST = "experiments/heldout/manifest.json"
WORKDIR = "work/heldout"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", default=MANIFEST)
    parser.add_argument("--workdir", default=WORKDIR,
                        help="checkpoints, outputs and scores (default: %(default)s)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("select", help="draw the held-out and training sets")
    p.add_argument("--pool", default=ho.DEFAULT_POOL)
    p.add_argument("--n-heldout", type=int, default=ho.DEFAULT_PROTOCOL["n_heldout"])
    p.add_argument("--n-train", type=int, default=ho.DEFAULT_PROTOCOL["n_train"])
    p.add_argument("--reps", type=int, default=ho.DEFAULT_PROTOCOL["reps"])
    p.add_argument("--seed", type=int, default=ho.DEFAULT_PROTOCOL["seed"])
    p.add_argument("--force", action="store_true", help="overwrite an existing manifest")

    sub.add_parser("train", help="build the library on the training set")

    p = sub.add_parser("score", help="score the held-out set at each checkpoint")
    p.add_argument("--checkpoints", nargs="+", default=["empty", "half", "full"])

    sub.add_parser("analyze", help="run the pre-specified tests on scores.jsonl")

    args = parser.parse_args()
    manifest_path = ROOT / args.manifest
    workdir = ROOT / args.workdir

    if args.cmd == "select":
        if manifest_path.exists() and not args.force:
            print(f"{manifest_path} exists; refusing to overwrite (--force to override)")
            return 1
        m = ho.select(args.pool, n_heldout=args.n_heldout, n_train=args.n_train,
                      reps=args.reps, seed=args.seed)
        ho.write_manifest(m, manifest_path)
        print(f"pool={m['pool_size']}  held-out={len(m['heldout'])}  train={len(m['train'])}")
        for s, quota in m["stratum_quotas"].items():
            pkgs = sorted({e["package"] for e in m["heldout"] if e["stratum"] == s})
            print(f"  {s:<15} {quota:>2} scripts from {len(pkgs)} packages")
        print(f"wrote {manifest_path}")
        return 0

    manifest = ho.load_manifest(manifest_path)
    if args.cmd == "train":
        ho.train(manifest, workdir)
    elif args.cmd == "score":
        ho.score(manifest, workdir, args.checkpoints)
    elif args.cmd == "analyze":
        result = ho.analyze(manifest, workdir / "scores.jsonl")
        (workdir / "analysis.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(ho.format_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
