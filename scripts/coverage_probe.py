"""How much of the held-out loss could knowledge learned from the training set ever reach?

Offline, structural, no LLM calls and no new translations. Reads
  * the entity scores of the first experiment's `empty` runs (work/heldout/scores.w*.jsonl),
  * the trained library (work/heldout/checkpoints/full),
  * the (package, function) inventory of the 256 training scripts
    (work/coverage_probe/train_inventory.jsonl, written by the inventory step).

For every held-out entity it asks which retrieval scheme would find *something* learned from a
training script, and weighs the answer by the points the harness actually loses on that entity.
Coverage of an entity that already scores 1.0 is worth nothing, so entity counts alone mislead.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROBE = ROOT / "work" / "coverage_probe"
BOILERPLATE = "base.suppresspackagestartupmessages"


def _fn(key: str) -> str:
    """The function part of a pattern id (`timechange.time-add` -> `time-add`)."""
    return key.split(".", 1)[1] if key and "." in key else key


def _pkg(key: str) -> str:
    return key.split(".", 1)[0] if key else ""


def heldout_entities(checkpoint: str = "empty") -> dict:
    """Mean entity score over the reps of one checkpoint, with the entity's key and base calls."""
    rows = []
    for f in (ROOT / "work" / "heldout").glob("scores.w*.jsonl"):
        rows += [json.loads(l) for l in f.open(encoding="utf-8")]
    rows = [r for r in rows if r.get("entities") and r.get("checkpoint") == checkpoint]
    agg: dict = defaultdict(list)
    meta: dict = {}
    for r in rows:
        for e in r["entities"]:
            if e["key"] == BOILERPLATE:
                continue
            agg[(r["script"], e["id"])].append(e["score"])
            meta[(r["script"], e["id"])] = e
    return {k: {"mean": statistics.mean(v), "key": meta[k]["key"] or "",
                "calls": meta[k].get("calls") or [], "script": k[0]} for k, v in agg.items()}


def training_supply() -> dict:
    """What the training set contains: keys, function names, packages, and the calls inside entities."""
    rows = [json.loads(l) for l in (PROBE / "train_inventory.jsonl").open(encoding="utf-8")]
    keys, calls, scripts = Counter(), Counter(), 0
    errors = 0
    for r in rows:
        if "error" in r:
            errors += 1
            continue
        scripts += 1
        for e in r["entities"]:
            if e["key"]:
                keys[e["key"]] += 1
            for c in e["calls"]:
                calls[c] += 1
    return {"keys": keys, "calls": calls, "scripts": scripts, "errors": errors,
            "names": {_fn(k) for k in keys} | {_fn(c) for c in calls},
            "packages": {_pkg(k) for k in keys}}


def report() -> str:
    ents = heldout_entities()
    sup = training_supply()
    learned = set(json.load((PROBE / "full_shown_ids.json").open()))
    anything = set(sup["keys"]) | set(sup["calls"])
    total = sum(1 - v["mean"] for v in ents.values())

    def hit(v, scheme: str) -> bool:
        key, calls = v["key"], v["calls"]
        if scheme == "learned":                       # the library as it was trained and shown
            return key in learned or any(c in learned for c in calls)
        if scheme == "key":                           # perfect harvest, exact (package, function)
            return key in anything
        if scheme == "key_or_call":                   # ... plus the base-R functions inside the entity
            return key in anything or any(c in anything for c in calls)
        if scheme == "name":                          # ... plus the same function name in any package
            return _fn(key) in sup["names"] or any(_fn(c) in sup["names"] for c in calls)
        if scheme == "package":                       # ... plus anything at all from the same package
            return _pkg(key) in sup["packages"]
        raise ValueError(scheme)

    out = [f"held-out entities (excl. boilerplate): {len(ents)} from "
           f"{len({v['script'] for v in ents.values()})} scripts",
           f"mean entity score at `empty`: {statistics.mean(v['mean'] for v in ents.values()):.3f}"
           f"   lost points: {total:.1f}",
           f"training inventory: {sup['scripts']} scripts parsed ({sup['errors']} failed), "
           f"{len(sup['keys'])} distinct keys, {len(sup['calls'])} distinct base calls",
           f"library as trained: {len(learned)} patterns shown",
           "",
           f"{'scheme':<14}{'entities':>12}{'lost points reachable':>24}"]
    for scheme in ("learned", "key", "key_or_call", "name", "package"):
        n = sum(1 for v in ents.values() if hit(v, scheme))
        lost = sum(1 - v["mean"] for v in ents.values() if hit(v, scheme))
        out.append(f"{scheme:<14}{n:>6} {n/len(ents):>5.0%}{lost:>16.1f} {lost/total:>6.0%}")

    out += ["", "the biggest losses the training set has nothing for (key not in training, 10 worst):"]
    byk: Counter = Counter()
    for v in ents.values():
        if not hit(v, "key_or_call"):
            byk[v["key"] or "(no key)"] += 1 - v["mean"]
    for key, lost in byk.most_common(10):
        out.append(f"  {lost:6.2f}  {key}")
    return "\n".join(out)


if __name__ == "__main__":
    text = report()
    print(text)
    (PROBE / "report.txt").write_text(text + "\n", encoding="utf-8")
