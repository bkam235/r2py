"""Does what one translation could teach recur in the next? Two learning curves, no model calls.

A harness gets better with more translations only if its unit of knowledge (1) gets used, (2) can be
verified automatically and (3) recurs: knowledge from script N helps script N+1 only if N+1 needs it
again. Verified callable functions pass (1) and (2); (3) has never been measured, and the held-out
loss is known to sit in a long tail. This measures it, as an upper bound, for two candidate units:

  function   a verified `r_*` function for every pure candidate function met in the first N scripts
             (`runtime_ceiling` classification), optionally discounted by the pilot's measured pass
             rates (base/stats/utils 59%, package functions 22%)
  failure    a harness rule for every failure *kind* (coarse: extra stdout, extra files, missing
             figures, crash, missing data variable, ...) or failure *instance* (fine: which env var,
             which data variable, which exception) met in the first N scripts; an entity counts as
             reachable only if every one of its failures is of a kind already seen

Evaluation: the last 64 training scripts (manifest order) are "unseen", the first N of the other 186
are the experience - both curves on the same split. A split inside the training set shares packages
(the training set was drawn per held-out package), so it flatters recurrence; the function curve is
therefore also computed against the real held-out loss. Each point is the mean over 20 random orders
of the experience pool (min-max in brackets).

    python scripts/recurrence_curves.py
"""
from __future__ import annotations

import json
import pickle
import random
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

ROWS = ROOT / "work" / "reverify" / "rows_v3.jsonl"   # v3: after the sidecar fix (v2 carried a false files complaint)
MAPS = ROOT / "work" / "reverify" / "script_maps"
MANIFEST = ROOT / "experiments" / "heldout" / "manifest.json"
OUT = ROOT / "work" / "coverage_probe" / "recurrence.json"
BOILERPLATE = "suppressPackageStartupMessages"
BASE = {"", "base", "stats", "utils"}
PASS_RATE = {"base": 30 / 51, "package": 10 / 45}
N_EVAL = 64
ORDERS = 20


# ------------------------------------------------------------------------------------------ failure kinds

def failure_kind(msg: str) -> tuple[str, str]:
    """(kind, instance) of one comparison complaint. The kind is what a harness rule would target;
    the instance is the specific subject (env var, data variable, exception) inside it."""
    cls, _, rest = msg.partition(": ")
    low = rest.lower()
    if cls == "stdout":
        if "r printed ''" in low or "r printed \"\"" in low:
            return "stdout: Python prints, R silent", ""
        if "auto-prints" in low:
            return "stdout: R auto-prints, Python silent", ""
        return "stdout: printed text differs", ""
    if cls == "files":
        if "r wrote no files" in low:
            return "files: Python writes, R did not", ""
        if low.startswith("missing"):
            return "files: R wrote, Python did not", ""
        return "files: other", ""
    if cls == "graphics":
        m = re.search(r"R=(\d+) Python=(\d+)", rest)
        if m and int(m.group(1)) > int(m.group(2)):
            return "graphics: figures missing in Python", ""
        if m and int(m.group(1)) < int(m.group(2)):
            return "graphics: extra figures in Python", ""
        return "graphics: plotted content differs", ""
    if cls == "syntax":
        exc = re.findall(r"\b([A-Z][A-Za-z]+(?:Error|Exception))\b", rest)
        return "crash: Python crashed where R ran", exc[-1] if exc else ""
    if cls == "env":
        names = re.findall(r"'([^']+)'", rest)
        side = "only in R" if "only in r" in low else "only in Python" if "only in python" in low else "other"
        return f"env: {side}", ",".join(sorted(names))[:60]
    if cls == "data":
        var = rest.split(":", 1)[0].strip()
        if "missing in python" in low:
            return "data: variable missing in Python", var
        if "uncomparable" in low:
            return "data: uncomparable", ""
        if "column sets differ" in low or "columns" in low:
            return "data: columns differ", var
        return "data: value differs", var
    if cls == "rng":
        return ("rng: sequence length differs" if "length" in low else
                "rng: call count differs" if "count" in low else "rng: other"), ""
    if cls == "warnings":
        return "warnings: differ", ""
    if cls == "html":
        return ("html: present on one side only" if "one side" in low else "html: differs"), ""
    return f"{cls}: other", ""


# ------------------------------------------------------------------------------------------ data

def training_entities() -> dict[str, list[dict]]:
    """script -> its non-boilerplate entities: score, failure kinds, and the function behind it."""
    out: dict[str, list[dict]] = {}
    for line in ROWS.open(encoding="utf-8"):
        row = json.loads(line)
        if "error" in row:
            continue
        stem = Path(row["script"]).stem
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes()) if (MAPS / f"{stem}.pkl").exists() else None
        ents = []
        for e in row["entities"]:
            if e["name"] == BOILERPLATE:
                continue
            ent = sm.entities.get(e["id"]) if sm else None
            rhs = getattr(ent, "rhs_call_name", None) if ent else None
            fn = rhs or (getattr(ent, "name", "") if ent else "")
            pkg = ((getattr(ent, "rhs_call_package", None) if rhs else None) or getattr(ent, "package", "") or "") \
                if ent else ""
            kinds = [failure_kind(f) for f in e.get("feedback") or []]
            if e["score"] <= 0.999 and not kinds:
                # It lost points and no comparison said why: a gap in the feedback, not a failure kind a
                # rule could target. Counted so that its share is visible.
                kinds = [("silent: lost points, no complaint recorded", "")]
            ents.append({"score": e["score"], "fn": (fn, pkg), "kinds": kinds})
        out[row["script"]] = ents
    return out


def heldout_function_losses() -> list[tuple[tuple[str, str], float]]:
    from coverage_probe import heldout_entities
    fns = {}
    for line in (ROOT / "work/coverage_probe/heldout_functions.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if "error" in r:
            continue
        for e in r["entities"]:
            fns[(r["script"], e["id"])] = (e["fn"], e["package"])
    return [(fns.get(k, ("", "")), 1 - v["mean"]) for k, v in heldout_entities("empty").items()]


# ------------------------------------------------------------------------------------------ curves

def curve(points, pool, seen_of, reach):
    """Mean (min, max) over random orders of the pool, at each experience size N."""
    out = {}
    for n in points:
        vals = []
        for k in range(ORDERS):
            order = pool[:]
            random.Random(f"{k}").shuffle(order)
            seen = set()
            for s in order[:n]:
                seen |= seen_of(s)
            vals.append(reach(seen))
        out[n] = (st.mean(vals), min(vals), max(vals))
    return out


def main() -> int:
    import argparse
    from runtime_ceiling import _classify, probe
    global ROWS
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default=str(ROWS))
    ROWS = Path(ap.parse_args().rows)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ents = training_entities()
    order = [e["script"] for e in manifest["train"] if e["script"] in ents]
    pool, unseen = order[:-N_EVAL], order[-N_EVAL:]
    held = heldout_function_losses()

    pairs = {e["fn"] for es in ents.values() for e in es if e["fn"][0]} | {p for p, _ in held if p[0]}
    info = probe(sorted(pairs))
    cand = {p for p in pairs if _classify(info.get(p), p[1]) == "candidate"}

    def rate(p):
        return PASS_RATE["base"] if p[1] in BASE else PASS_RATE["package"]

    def fn_seen(s):
        return {e["fn"] for e in ents[s] if e["fn"] in cand}

    def fn_reach(targets, discounted):
        total = sum(l for _, l in targets)

        def reach(seen):
            got = sum(l * (rate(p) if discounted else 1.0) for p, l in targets if p in seen)
            return got / total
        return reach

    eval_fn = [(e["fn"], 1 - e["score"]) for s in unseen for e in ents[s]]
    kinds_eval = [e for s in unseen for e in ents[s] if e["score"] <= 0.999]
    eval_total = sum(1 - e["score"] for s in unseen for e in ents[s])

    def kind_seen(level):
        def seen_of(s):
            return {(k if level == "kind" else (k, inst)) for e in ents[s] for k, inst in e["kinds"]}
        return seen_of

    def kind_reach(level):
        def reach(seen):
            got = 0.0
            for e in kinds_eval:
                ks = [(k if level == "kind" else (k, inst)) for k, inst in e["kinds"]]
                if ks and all(k in seen for k in ks):
                    got += 1 - e["score"]
            return got / eval_total
        return reach

    pts = [8, 16, 32, 64, 128, len(pool)]
    pts_held = [8, 16, 32, 64, 128, len(order)]
    res = {
        "function, unseen training scripts": curve(pts, pool, fn_seen, fn_reach(eval_fn, False)),
        "function, discounted by pass rate": curve(pts, pool, fn_seen, fn_reach(eval_fn, True)),
        "function, real held-out loss": curve(pts_held, order, fn_seen, fn_reach(held, False)),
        "function, held-out, discounted": curve(pts_held, order, fn_seen, fn_reach(held, True)),
        "failure kind (coarse)": curve(pts, pool, kind_seen("kind"), kind_reach("kind")),
        "failure instance (fine)": curve(pts, pool, kind_seen("instance"), kind_reach("instance")),
    }
    print(f"experience pool {len(pool)} scripts, unseen {len(unseen)}; "
          f"unseen loss {eval_total:.1f} points; {len(cand)} pure candidate functions overall\n")
    for name, c in res.items():
        print(f"{name}")
        print("   " + "   ".join(f"N={n:<3} {m:5.1%} [{lo:.0%}-{hi:.0%}]" for n, (m, lo, hi) in c.items()))
    OUT.write_text(json.dumps({k: {str(n): v for n, v in c.items()} for k, c in res.items()}, indent=1),
                   encoding="utf-8")

    # what the kinds are, and how many there are as experience grows
    from collections import Counter
    kind_loss: Counter = Counter()
    for e in kinds_eval:
        for k, _ in set(e["kinds"]):
            kind_loss[k] += (1 - e["score"]) / max(1, len(set(e["kinds"])))
    print("\nfailure kinds by share of unseen loss:")
    for k, l in kind_loss.most_common(12):
        print(f"   {l / eval_total:6.1%}  {k}")
    n_kinds = {n: len(set().union(*(kind_seen('kind')(s) for s in order[:n]))) for n in (8, 32, 128, len(order))}
    n_inst = {n: len(set().union(*(kind_seen('instance')(s) for s in order[:n]))) for n in (8, 32, 128, len(order))}
    print(f"\ndistinct failure kinds seen after N scripts:     {n_kinds}")
    print(f"distinct failure instances seen after N scripts: {n_inst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
