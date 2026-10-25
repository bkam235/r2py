"""Scoring epochs and the scorer regression check (2026-10-24).

A scoring epoch is a period with one scorer (`r2py.scoring.scoring_version()`: scorer code + stored R ground truth).
When the scorer changes, a fixed reference set of programs is re-verified (no model calls: attribution is read off
the programs' own sentinels) and every score that moved is reported, entity by entity. A human reviews the report;
`accept` then opens a new epoch with a new baseline.

The reference set: the 60 training-pool start states and the final programs of the default run of 2026-10-20 and of
the width-3 runs of 2026-10-17 (sample 0). Each is verified twice for the baseline; a program whose two scores differ
(random output, e.g. openssl keys) is marked flaky and judged against the range it showed.

    python scripts/scoring_epoch.py baseline --note "..."   # first epoch: build the reference set and its scores
    python scripts/scoring_epoch.py check                    # after a scorer change: what moved?
    python scripts/scoring_epoch.py check --force            # re-verify even if the version is unchanged
    python scripts/scoring_epoch.py accept --note "..."      # open a new epoch at the current scorer, then rebuild
                                                             # the learning curves in it (--no-curves to skip)
    python scripts/scoring_epoch.py status

Files in work/scoring/: programs/ (the reference programs), reference.json, baseline.json, epochs.json, and a
report check_<time>.md per check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "work/scoring"
MAPS = ROOT / "work/reverify/script_maps"
TOL = 1e-4          # a score that moves less than this has not moved
# Verification noise seen with an unchanged scorer (2026-10-24, 147 programs): 4 moved by at most 0.002, no entity by
# more than 0.006, no run/crash flip. Moves inside this band are listed but do not fail the check; the scorer changes
# of October moved scores by 0.1-0.3.
SMALL_AGG, SMALL_ENTITY = 0.005, 0.02


# ---------------------------------------------------------------------------------------------- reference set

def _final_programs(run: str, policy: str, sample) -> dict[str, str]:
    """script -> source of the program the run returned (the best chain's last accepted program)."""
    out = {}
    for r in map(json.loads, (ROOT / run / "results.jsonl").open(encoding="utf-8")):
        if r["policy"] != policy or r["sample"] != sample:
            continue
        recs = [json.loads(l) for l in (ROOT / run / "trajectories" / f"{Path(r['script']).stem}.{policy}.{sample}.jsonl").open(encoding="utf-8")]
        ver = {(x.get("branch"), x.get("step")): (x.get("exit_code") == 0, x["aggregate"])
               for x in recs if x["kind"] == "step" and "aggregate" in x}
        cur = {}
        for x in recs:
            if x["kind"] == "accepted" and x.get("source") and (x.get("branch"), x["step"]) in ver:
                cur[x.get("branch")] = (ver[(x.get("branch"), x["step"])], x["source"])
        best = max(cur.values(), default=None, key=lambda v: v[0])
        if best is not None:
            out[r["script"]] = best[1]
    return out


def build_reference() -> list[dict]:
    import replay
    progs = {}
    for name, s in sorted(replay.training_states().items()):
        progs[f"start:{Path(name).stem}"] = (name, s["source"])
    for label, run, policy, sample in (("final_default", "work/replay_default", "default_2026_10_20", 0),
                                       ("final_w3", "work/replay_k3", "rewrite_w3", 0)):
        for name, src in sorted(_final_programs(run, policy, sample).items()):
            progs[f"{label}:{Path(name).stem}"] = (name, src)
    seen, ref = set(), []
    (OUT / "programs").mkdir(parents=True, exist_ok=True)
    for pid, (name, src) in progs.items():
        sha = hashlib.sha1(src.encode("utf-8")).hexdigest()
        if sha in seen:
            continue
        seen.add(sha)
        f = OUT / "programs" / (re.sub(r"[^A-Za-z0-9_.-]", "_", pid) + ".py")
        f.write_text(src, encoding="utf-8")
        ref.append({"id": pid, "script": name, "file": f.relative_to(ROOT).as_posix(), "sha": sha})
    (OUT / "reference.json").write_text(json.dumps(ref, indent=1), encoding="utf-8")
    return ref


# ---------------------------------------------------------------------------------------------- verification

def verify_one(item: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from prompt_load import _tools
    from r2py.harness import tools as T
    from r2py.harness.objective import entity_score
    stem = Path(item["script"]).stem
    src = (ROOT / item["file"]).read_text(encoding="utf-8")
    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    T.drain_cache_stats()
    t = _tools(sm, stem)
    t.note_reference(src)        # attribution from the program's own sentinels, as the loop does
    try:
        rep = t.verify(src)
    except Exception as exc:
        return {"id": item["id"], "error": f"{type(exc).__name__}: {exc}"[:200]}
    return {"id": item["id"], "aggregate": round(rep.aggregate, 6), "exit": rep.py_exit_code,
            "entities": {e: round(entity_score(es), 6) for e, es in rep.by_entity.items() if es.active_dims},
            "paths": T.drain_cache_stats()}


def verify_all(ref: list[dict], workers: int) -> dict:
    with ProcessPoolExecutor(workers) as ex:
        return {r["id"]: r for r in ex.map(verify_one, ref)}


# ---------------------------------------------------------------------------------------------- comparison

def compare(base: dict, new: dict) -> dict:
    """Per program: unchanged / changed / flaky-in-range / error, with what moved."""
    out = {"unchanged": [], "changed": [], "small": [], "flaky_in_range": [], "error": []}
    for pid, b in base.items():
        n = new.get(pid)
        if n is None or "error" in n or "error" in b["runs"][0]:
            out["error"].append({"id": pid, "detail": (n or {}).get("error", "missing")})
            continue
        lo = min(r["aggregate"] for r in b["runs"]); hi = max(r["aggregate"] for r in b["runs"])
        ref = b["runs"][0]
        moved = {e: (ref["entities"].get(e), s) for e, s in n["entities"].items()
                 if ref["entities"].get(e) is None or abs(ref["entities"][e] - s) > TOL}
        moved.update({e: (s, None) for e, s in ref["entities"].items() if e not in n["entities"]})
        same = abs(n["aggregate"] - ref["aggregate"]) <= TOL and n["exit"] == ref["exit"] and not moved
        if same:
            out["unchanged"].append(pid)
        elif b["flaky"] and lo - TOL <= n["aggregate"] <= hi + TOL:
            out["flaky_in_range"].append(pid)
        else:
            item = {"id": pid, "before": ref["aggregate"], "after": n["aggregate"], "exit": (ref["exit"], n["exit"]),
                    "entities": moved}
            small = (abs(n["aggregate"] - ref["aggregate"]) <= SMALL_AGG and n["exit"] == ref["exit"]
                     and all(a is not None and b is not None and abs(a - b) <= SMALL_ENTITY for a, b in moved.values()))
            out["small" if small else "changed"].append(item)
    return out


def report(cmp: dict, epoch: dict, version: str, r_capture_changed: bool) -> str:
    ch = sorted(cmp["changed"], key=lambda c: c["after"] - c["before"])
    lines = [f"# Scorer regression check, {time.strftime('%Y-%m-%d %H:%M')}", "",
             f"- Epoch {epoch['epoch']} scorer `{epoch['scoring_version']}`; current scorer `{version}`.",
             f"- Programs: {sum(len(v) for v in cmp.values())}; unchanged {len(cmp['unchanged'])}, "
             f"**changed {len(ch)}**, small moves within noise {len(cmp['small'])}, flaky within their range "
             f"{len(cmp['flaky_in_range'])}, errors {len(cmp['error'])}."]
    if r_capture_changed:
        lines.append("- **The R capture code changed since the epoch began.** The stored script maps may be stale: "
                     "re-capture them (`scripts/refresh_entity_bundles.py`) and check again before accepting.")
    if ch:
        d = [c["after"] - c["before"] for c in ch]
        lines += [f"- Mean change over the changed programs {sum(d) / len(d):+.4f}; up {sum(x > TOL for x in d)}, "
                  f"down {sum(x < -TOL for x in d)}; run/crash flips {sum(c['exit'][0] != c['exit'][1] for c in ch)}.", "",
                  "| program | before | after | exit | entities that moved (before -> after) |", "|---|---|---|---|---|"]
        for c in ch:
            ents = "; ".join(f"{e} {a if a is None else round(a, 3)}->{b if b is None else round(b, 3)}"
                             for e, (a, b) in list(c["entities"].items())[:6])
            lines.append(f"| {c['id']} | {c['before']:.4f} | {c['after']:.4f} | {c['exit'][0]}->{c['exit'][1]} | {ents} |")
    if cmp["small"]:
        lines.append("")
        lines.append(f"Small moves (aggregate <= {SMALL_AGG}, no entity > {SMALL_ENTITY}, no run/crash flip; not counted as changes): "
                     + ", ".join(f"{c['id']} {c['before']:.4f}->{c['after']:.4f}" for c in cmp["small"]))
    for e in cmp["error"]:
        lines.append(f"- error: {e['id']}: {e['detail']}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------------- commands

def _epochs() -> list[dict]:
    f = OUT / "epochs.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else []


def make_baseline(note: str, workers: int, rebuild_reference: bool) -> None:
    from r2py.scoring import r_capture_hash, scoring_version
    OUT.mkdir(parents=True, exist_ok=True)
    ref = build_reference() if rebuild_reference or not (OUT / "reference.json").exists() \
        else json.loads((OUT / "reference.json").read_text(encoding="utf-8"))
    print(f"{len(ref)} reference programs; verifying twice", flush=True)
    first, second = verify_all(ref, workers), verify_all(ref, workers)
    base = {}
    for r in ref:
        a, b = first[r["id"]], second[r["id"]]
        flaky = "error" not in a and "error" not in b and (abs(a["aggregate"] - b["aggregate"]) > TOL or a["entities"] != b["entities"])
        base[r["id"]] = {"runs": [a, b], "flaky": flaky}
    (OUT / "baseline.json").write_text(json.dumps(base), encoding="utf-8")
    epochs = _epochs()
    model_maps = sum((r.get("paths") or {}).get("mapping_ok", 0) for r in first.values())
    epochs.append({"epoch": len(epochs) + 1, "scoring_version": scoring_version(), "r_capture": r_capture_hash(),
                   "date": time.strftime("%Y-%m-%d %H:%M"), "programs": len(ref),
                   "flaky": sorted(k for k, v in base.items() if v["flaky"]),
                   "errors": sorted(k for k, v in base.items() if "error" in v["runs"][0]),
                   "model_mappings": model_maps, "note": note})
    (OUT / "epochs.json").write_text(json.dumps(epochs, indent=1), encoding="utf-8")
    e = epochs[-1]
    print(f"epoch {e['epoch']} at scorer {e['scoring_version']}: {e['programs']} programs, flaky {len(e['flaky'])}, "
          f"errors {len(e['errors'])}, model mappings {model_maps}")


def check(force: bool, workers: int) -> int:
    from r2py.scoring import r_capture_hash, scoring_version
    epochs = _epochs()
    if not epochs:
        print("no epoch yet: run `baseline` first")
        return 2
    epoch, version = epochs[-1], scoring_version()
    if version == epoch["scoring_version"] and not force:
        print(f"scorer unchanged since epoch {epoch['epoch']} ({version}): nothing to check")
        return 0
    ref = json.loads((OUT / "reference.json").read_text(encoding="utf-8"))
    base = json.loads((OUT / "baseline.json").read_text(encoding="utf-8"))
    print(f"re-verifying {len(ref)} reference programs (epoch {epoch['epoch']} scorer {epoch['scoring_version']} -> {version})", flush=True)
    new = verify_all(ref, workers)
    cmp = compare(base, new)
    text = report(cmp, epoch, version, r_capture_hash() != epoch["r_capture"])
    f = OUT / f"check_{time.strftime('%Y%m%d_%H%M')}.md"
    f.write_text(text, encoding="utf-8")
    print(text)
    print(f"report: {f.relative_to(ROOT)}")
    return 1 if cmp["changed"] or cmp["error"] else 0


def status() -> None:
    from r2py.scoring import r_capture_hash, scoring_version
    epochs = _epochs()
    if not epochs:
        print("no epoch yet")
        return
    e = epochs[-1]
    print(f"epoch {e['epoch']} since {e['date']}: scorer {e['scoring_version']} ({e['note']})")
    print(f"current scorer {scoring_version()}: " + ("same" if scoring_version() == e["scoring_version"] else "CHANGED, run `check`")
          + ("; R capture code changed" if r_capture_hash() != e["r_capture"] else ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baseline"); b.add_argument("--note", required=True); b.add_argument("--rebuild-reference", action="store_true")
    c = sub.add_parser("check"); c.add_argument("--force", action="store_true")
    a = sub.add_parser("accept"); a.add_argument("--note", required=True)
    a.add_argument("--no-curves", action="store_true", help="do not rebuild the learning curves in the new epoch")
    sub.add_parser("status")
    for p in (b, c, a):
        p.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    if args.cmd == "baseline":
        make_baseline(args.note, args.workers, args.rebuild_reference)
    elif args.cmd == "accept":
        make_baseline(args.note, args.workers, False)
        if not args.no_curves:   # a new epoch rebuilds the curves by default (user's decision, 2026-10-24)
            import subprocess
            print("rebuilding the learning curves in the new epoch", flush=True)
            subprocess.run([sys.executable, str(ROOT / "scripts/learning_curves.py")], check=False)
    elif args.cmd == "check":
        return check(args.force, args.workers)
    else:
        status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
