"""Learning-curve instrument: does the translator get better as the harness learns?  (Roadmap step 5.)

The first held-out experiment scored whole scripts under five library snapshots and could not resolve the effect (the
library's script-level ceiling is a few hundredths against a per-script spread of 0.2).  This instrument is built for
resolution:

* it generates *seeds only* (one translation, no agent), so every observation is cheap and independent;
* the order of (snapshot, script, seed) is randomised over the whole job, so provider drift cannot line up with a snapshot;
* every seed records the score of each *entity*; the analysis is paired by entity, restricted to the entities the final
  snapshot can say something about (``targetable``), which is where an effect can live, and resampled by script, the
  independent unit;
* it reports coverage (share of held-out entities each snapshot can inform), the curve, its slope with a bootstrap
  interval, and the smallest effect the sample could detect.

A snapshot is a library directory with a number of training scripts behind it.  Other mechanisms (a runtime, a lesson
store) enter the same way once they have a directory per snapshot; ``--snapshots name=path:n_train`` adds one.

    python scripts/learning_curve.py run --seeds 2 --workers 6        # the five library checkpoints, 60 held-out scripts
    python scripts/learning_curve.py summary
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import random
import shutil
import statistics as st
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

DEFAULT_MANIFEST = ROOT / "experiments/heldout/manifest.json"
DEFAULT_WORKDIR = ROOT / "work/heldout"
DEFAULT_OUT = ROOT / "work/learning_curve/rows.jsonl"


def snapshots_from(manifest: dict, workdir: Path, extra: list[str]) -> list[dict]:
    snaps = [{"name": n, "n_train": c, "library": str(workdir / "checkpoints" / n)} for n, c in manifest["checkpoints"].items()]
    for spec in extra or []:
        name, rest = spec.split("=", 1)
        path, n = rest.rsplit(":", 1)
        snaps.append({"name": name, "n_train": int(n), "library": path})
    return snaps


def curve_task(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import replay
    from r2py import heldout as ho
    from r2py import seed as seed_mod
    from r2py.library import PatternLibrary
    from r2py.stage2.sentinel_mapper import strip_sentinels
    from r2py.stage4 import verifier

    manifest = ho.load_manifest(task["manifest"])
    cfg = manifest["protocol"]["translate"]
    row = {k: task[k] for k in ("snapshot", "n_train", "script", "idx")}
    started = time.monotonic()
    try:
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            sm = replay._script_map(task["script"], manifest, Path(task["cache"]))
            stem = Path(task["script"]).stem
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                shutil.copytree(Path(task["library"]), Path(tmp) / "lib")
                source, elmap = seed_mod.translate(
                    sm, PatternLibrary(Path(tmp) / "lib"), model=cfg["model"],
                    sidecar_filename=f"{stem}.r2py_data.json", script_relpath=f"work/learning_curve/{stem}.py",
                    style="structured", gate=True)
            rep = verifier.verify(sm, source, data_compare=cfg["data_compare"], entity_line_map=elmap,
                                  sidecar_filename=f"{stem}.r2py_data.json", timeout_s=cfg["timeout_s"])
            row.update(aggregate=round(rep.aggregate, 4), exit_code=rep.py_exit_code,
                       entities=ho._entity_records(sm, rep))
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


# --------------------------------------------------------------------------------------------- analysis

def bootstrap(clusters: dict, stat, n: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """(estimate, 2.5%, 97.5%) of ``stat(list of cluster values)``, resampling whole clusters (scripts)."""
    keys = sorted(clusters)
    est = stat([clusters[k] for k in keys])
    rng = random.Random(seed)
    draws = sorted(stat([clusters[rng.choice(keys)] for _ in keys]) for _ in range(n))
    return est, draws[int(0.025 * n)], draws[int(0.975 * n)]


def slope(xs: list[float], ys: list[float]) -> float:
    mx, my = st.mean(xs), st.mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def summarise(rows: list[dict], manifest: dict, snaps: list[dict]) -> str:
    from r2py import heldout as ho

    ok = [r for r in rows if "aggregate" in r]
    if not ok:
        return "no finished seeds"
    order = [s["name"] for s in sorted(snaps, key=lambda s: s["n_train"])]
    n_of = {s["name"]: s["n_train"] for s in snaps}
    full = max(snaps, key=lambda s: s["n_train"])
    ids_by_snap = {s["name"]: ho.targetable_ids(s["library"]) for s in snaps}
    out = [f"{len(ok)} seeds ({len(rows) - len(ok)} errors) over {len({r['script'] for r in ok})} scripts, "
           f"snapshots {', '.join(f'{n}({n_of[n]})' for n in order)}", ""]

    # ---- per-snapshot table, script level
    out.append("snapshot      n_train  seeds  P(runs)  P(>=.5)  mean seed score  targetable entities")
    ent_meta: dict = {}
    for r in ok:
        for e in r["entities"]:
            if e["name"] not in ho.BOILERPLATE_ENTITIES:
                ent_meta[(r["script"], e["id"])] = e
    for n in order:
        rs = [r for r in ok if r["snapshot"] == n]
        if not rs:
            continue
        cov = sum(ho.is_targetable(e, ids_by_snap[n]) for e in ent_meta.values()) / max(1, len(ent_meta))
        out.append(f"{n:12s} {n_of[n]:7d} {len(rs):6d}  {sum(r['exit_code'] == 0 for r in rs) / len(rs):6.0%}  "
                   f"{sum(r['aggregate'] >= .5 for r in rs) / len(rs):6.0%}  {st.mean(r['aggregate'] for r in rs):15.3f}  {cov:18.1%}")

    # ---- script-level curve (mean over seeds, per script, per snapshot), paired by script
    per_script: dict = {}
    for r in ok:
        per_script.setdefault(r["script"], {}).setdefault(r["snapshot"], []).append(r["aggregate"])
    scripts = {s: {n: st.mean(v) for n, v in d.items()} for s, d in per_script.items() if all(n in d for n in order)}
    out.append("")
    if scripts:
        xs = [n_of[n] / 100 for n in order]
        clusters = {s: [d[n] for n in order] for s, d in scripts.items()}
        est, lo, hi = bootstrap(clusters, lambda cl: slope(xs, [st.mean(c[i] for c in cl) for i in range(len(order))]))
        diffs = {s: [c[-1] - c[0]] for s, c in clusters.items()}
        d_est, d_lo, d_hi = bootstrap(diffs, lambda cl: st.mean(c[0] for c in cl))
        sd = st.stdev(c[0] for c in diffs.values()) if len(diffs) > 1 else float("nan")
        out.append(f"script level ({len(scripts)} scripts, all snapshots): slope {est:+.4f} per +100 training scripts "
                   f"[{lo:+.4f}, {hi:+.4f}];  {order[-1]} - {order[0]} {d_est:+.3f} [{d_lo:+.3f}, {d_hi:+.3f}];  "
                   f"smallest detectable difference ~ {2.8 * sd / len(diffs) ** 0.5:.3f}")

    # ---- entity level, targetable under the final snapshot, paired by entity
    fids = ids_by_snap[full["name"]]
    by_ent: dict = {}
    for r in ok:
        for e in r["entities"]:
            key = (r["script"], e["id"])
            if key in ent_meta and ho.is_targetable(ent_meta[key], fids) and e["executed_ok"]:
                by_ent.setdefault(key, {}).setdefault(r["snapshot"], []).append(e["score"])
    ent = {k: {n: st.mean(v) for n, v in d.items()} for k, d in by_ent.items() if all(n in d for n in order)}
    if ent:
        by_script: dict = {}
        for (s, _eid), d in ent.items():
            by_script.setdefault(s, []).append([d[n] for n in order])
        xs = [n_of[n] / 100 for n in order]

        def ent_slope(cl):
            rows_ = [row for c in cl for row in c]
            return slope(xs, [st.mean(row[i] for row in rows_) for i in range(len(order))])

        est, lo, hi = bootstrap(by_script, ent_slope)
        means = [st.mean(row[i] for c in by_script.values() for row in c) for i in range(len(order))]
        sd = st.stdev([row[-1] - row[0] for c in by_script.values() for row in c]) if len(ent) > 1 else float("nan")
        out.append(f"entity level, {len(ent)} entities targetable under {full['name']} that ran in every snapshot "
                   f"({len(by_script)} scripts): mean score by snapshot " + "  ".join(f"{n}={m:.3f}" for n, m in zip(order, means)))
        out.append(f"   slope {est:+.4f} per +100 training scripts [{lo:+.4f}, {hi:+.4f}];  "
                   f"smallest detectable change over the whole range ~ {2.8 * sd / len(ent) ** 0.5:.3f} (entities as independent: optimistic)")
    else:
        out.append("entity level: no targetable entity ran in every snapshot yet")
    return "\n".join(out)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("run", "summary"))
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--workdir", default=str(DEFAULT_WORKDIR))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--seeds", type=int, default=2, help="structured seeds per (snapshot, script)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--snapshots", nargs="*", help="extra snapshots: name=path:n_train")
    ap.add_argument("--only", nargs="+", help="substrings of script names")
    ap.add_argument("--limit", type=int, help="first N held-out scripts")
    args = ap.parse_args()

    from r2py import heldout as ho
    manifest = ho.load_manifest(args.manifest)
    snaps = snapshots_from(manifest, Path(args.workdir), args.snapshots)
    out = Path(args.out)
    rows = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()] if out.exists() else []
    if args.mode == "summary":
        print(summarise(rows, manifest, snaps))
        return 0

    scripts = [e["script"] for e in manifest["heldout"]]
    if args.only:
        scripts = [s for s in scripts if any(o in s for o in args.only)]
    scripts = scripts[: args.limit] if args.limit else scripts
    done = {(r["snapshot"], r["script"], r["idx"]) for r in rows if "aggregate" in r}
    tasks = [dict(snapshot=s["name"], n_train=s["n_train"], library=s["library"], script=sc, idx=i, manifest=args.manifest,
                  cache=str(ROOT / "work/replay/script_maps"))
             for s in snaps for sc in scripts for i in range(args.seeds) if (s["name"], sc, i) not in done]
    random.Random(20261004).shuffle(tasks)       # interleaved: provider drift cannot line up with a snapshot
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"{len(tasks)} seeds to generate ({len(done)} done), {len(snaps)} snapshots x {len(scripts)} scripts, "
          f"{args.workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(curve_task, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['snapshot']:7s} {row['script'][:40]:40s} #{row['idx']}: "
                  + (f"{row['aggregate']:.2f}" if "aggregate" in row else f"ERROR {row['error'][:70]}"), flush=True)
    rows = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]
    print("\n" + summarise(rows, manifest, snaps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
