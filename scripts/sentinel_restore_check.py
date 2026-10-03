"""How well does deterministic sentinel restoration work on logged sources?  (Stage 8b follow-up; no model calls.)

1. Synthetic: drop random sentinels from logged annotated sources, restore from the original, compare ranges.
2. Real: agent candidates that lost sentinels relative to the source they were derived from (the trajectory's
   ``best_hash``): how often does restoration give every entity a range again?

    python scripts/sentinel_restore_check.py work/replay work/smoke/<arm> ...
"""
from __future__ import annotations

import glob
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from r2py.harness import trajectory
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels, restore_sentinels, strip_sentinels

    dirs = sys.argv[1:] or [str(ROOT / "work/replay")]
    files = [f for d in dirs for f in glob.glob(str(Path(d) / "**" / "trajectories" / "*.jsonl"), recursive=True)
             + glob.glob(str(Path(d) / "trajectories" / "*.jsonl"))]
    files = sorted(set(files))
    rng = random.Random(0)
    syn_total = syn_exact = 0
    real_total = real_complete = real_partial = 0
    for f in files:
        recs = trajectory.read(f)
        by_hash = {}
        for r in recs:
            if r.get("source"):
                by_hash.setdefault(r.get("source_hash"), r["source"])
        for r in recs:
            src = r.get("source")
            if not src or r["kind"] not in ("seed", "step"):
                continue
            ranges = ranges_from_sentinels(src)
            if len(ranges) >= 3 and r["kind"] == "seed":
                eids = list(ranges)
                drop = set(rng.sample(eids, rng.randint(1, max(1, len(eids) // 2))))
                lines = [l for l in src.splitlines() if not any(l.strip() == f"# r2py:entity:{e}" for e in drop)]
                got = ranges_from_sentinels(restore_sentinels(src, "\n".join(lines)))
                syn_total += 1
                syn_exact += got == ranges
            if r["kind"] == "step" and r.get("best_hash") in by_hash:
                ref = by_hash[r["best_hash"]]
                want = set(ranges_from_sentinels(ref))
                if want and want - set(ranges):
                    real_total += 1
                    got = set(ranges_from_sentinels(restore_sentinels(ref, src)))
                    real_complete += want <= got
                    real_partial += bool(got & want) and not want <= got
    print(f"{len(files)} trajectories")
    print(f"synthetic (drop 1..half of the sentinels of a seed): {syn_exact}/{syn_total} restored to exactly the original ranges")
    print(f"real candidates that lost sentinels: {real_total}; every entity got a range back in {real_complete}, "
          f"some in {real_partial}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
