"""Freeze the held-out pool of the meta-loop (2026-10-24).

The 60-state training pool (`replay.training_states()`) is where harness changes are tried and chosen. Winners are
confirmed on states the cycle never tuned on before a default changes. Drawn once, with a fixed seed, from the
training translations outside that pool whose start is below the threshold and whose source and script map exist:
40 that run and every one that crashes (only 6 remain, so crash-specific changes cannot be confirmed here). Most of
their packages also appear in the training pool: this holds out scripts, not packages.

    python scripts/select_heldout.py    # writes experiments/pools/heldout.json; refuses to overwrite it
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "experiments/pools/heldout.json"
N_RUNNING, SEED = 40, 1


def main() -> int:
    import replay
    if OUT.exists():
        print(f"{OUT.relative_to(ROOT)} exists: the held-out pool is frozen")
        return 1
    pool = set(replay.training_states())
    rows = [json.loads(l) for l in (ROOT / "work/reverify/rows_v3.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if "error" not in r and r["aggregate"] < 0.9 and r["script"] not in pool
            and (replay.TRAIN_SOURCES / f"{Path(r['script']).stem}.py").exists()
            and (replay.TRAIN_MAPS / f"{Path(r['script']).stem}.pkl").exists()]
    running = sorted(r["script"] for r in rows if r.get("py_exit") == 0)
    crashing = sorted(r["script"] for r in rows if r.get("py_exit") != 0)
    picked = sorted(random.Random(SEED).sample(running, N_RUNNING) + crashing)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"selected": "2026-10-24", "seed": SEED, "running": N_RUNNING, "crashing": len(crashing),
                               "states": picked}, indent=1), encoding="utf-8")
    print(f"{len(picked)} held-out states ({N_RUNNING} running, {len(crashing)} crashing) -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
