"""Mine the lesson store from trajectory logs (r2py/lessons.py).

    python scripts/mine_lessons.py --arms work/smoke/<arm> ... --out work/lessons/pilot.json --holdout-half

--holdout-half leaves out the scripts whose name hashes odd and writes them to <out>.heldout.json, so the
lessons can be tested on scripts they were not mined from (``seed_eval.py --only`` the held-out names).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def is_heldout(script: str) -> bool:
    return int(hashlib.sha1(script.encode()).hexdigest(), 16) % 2 == 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--holdout-half", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    args = ap.parse_args()

    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py import lessons

    manifest = ho.load_manifest(args.manifest)
    model = manifest["protocol"]["translate"]["model"]
    held = {e["script"] for e in manifest["heldout"] if is_heldout(e["script"])} if args.holdout_half else set()
    files = [f for arm in args.arms for f in sorted((Path(arm) / "py" / "trajectories").glob("*.jsonl"))]
    pairs = lessons.mine_pairs(files, exclude_scripts=held)
    print(f"{len(files)} trajectories, {len(held)} scripts held out, {len(pairs)} crash->fix pairs "
          f"({len({p.signature for p in pairs})} signatures)", flush=True)

    with ho.pinned_llm(model, ho.llm_settings(manifest)), ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(lambda p: lessons.distill(p, model), pairs))
    kept = lessons.merge([x for x in results if x])
    lessons.save(kept, args.out)
    if held:
        Path(str(args.out) + ".heldout.json").write_text(json.dumps(sorted(held), indent=1), encoding="utf-8")
    print(f"{len(kept)} lessons kept of {len(pairs)} pairs -> {args.out}")
    for x in kept[:12]:
        print(f"  x{x.support} {x.libs}: {x.lesson[:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
