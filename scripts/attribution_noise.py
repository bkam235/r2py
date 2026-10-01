"""Stage 8a: how much does verifying the SAME source twice differ?

Entity attribution is an LLM call on every verification (it maps R entities to Python lines, and the
per-entity score is built on those lines).  This verifies one fixed source several times in two ways:

  remapped   the real path (HarnessTools.verify): a fresh LLM mapping each time
  fixed map  one mapping, reused: isolates sandbox / comparator nondeterminism

and reports, per script, how much the aggregate, the per-entity scores and the entity line ranges move.
If "remapped" varies and "fixed map" does not, the mapping is a noise source that contaminates every
comparison made through it.

    python scripts/attribution_noise.py --arm work/smoke/20261001_065131 --scripts lubridate rmarkdown caret
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env", override=True)


def _entity_scores(report) -> dict[str, float]:
    from r2py.harness.agent import _entity_score
    return {eid: round(_entity_score(es), 3) for eid, es in report.by_entity.items()}


def spread(values: list[float]) -> str:
    return f"{min(values):.3f}..{max(values):.3f} (sd {st.pstdev(values):.3f})"


def analyse(runs: list[dict]) -> dict:
    """Disagreement between repeated verifications of one source."""
    aggs = [r["aggregate"] for r in runs]
    eids = sorted(set().union(*(r["scores"] for r in runs)))
    score_varying = [e for e in eids if len({r["scores"].get(e) for r in runs}) > 1]
    range_varying = [e for e in eids if len({tuple(map(tuple, r["ranges"].get(e, []))) for r in runs}) > 1]
    return {"aggregates": aggs, "agg_range": max(aggs) - min(aggs), "entities": len(eids),
            "entities_with_varying_score": len(score_varying), "entities_with_varying_range": len(range_varying),
            "varying_score": score_varying[:8]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, help="a smoke-test directory holding py/<script>.py translations")
    ap.add_argument("--scripts", nargs="+", required=True, help="substrings of held-out script names")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--out", default=str(ROOT / "work/attribution_noise.json"))
    args = ap.parse_args()

    from r2py import heldout as ho
    from r2py.harness.tools import HarnessTools
    from r2py.stage1 import analyze
    from r2py.stage2.sentinel_mapper import flatten_entity_line_map, strip_sentinels
    from r2py.stage2.stitch import rebuild_entity_line_map
    from r2py.stage4 import verifier

    manifest = ho.load_manifest(args.manifest)
    cfg = manifest["protocol"]["translate"]
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    names = [e["script"] for e in manifest["heldout"] if any(s in e["script"] for s in args.scripts)]

    results = {}
    with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
        for name in names:
            py = Path(args.arm) / "py" / (Path(name).stem + ".py")
            if not py.exists():
                print(f"{name}: no translation in {args.arm}")
                continue
            sm = analyze(next(pool.rglob(name)))
            source = strip_sentinels(py.read_text(encoding="utf-8"))
            ht = HarnessTools(sm, None, model=cfg["model"], data_compare=cfg["data_compare"],
                              timeout_s=cfg["timeout_s"], sidecar_filename=f"{Path(name).stem}.r2py_data.json")
            remapped = []
            for i in range(args.repeats):
                ht._verify_cache.clear()          # the cache would hide exactly the noise being measured
                rep = ht.verify(source)
                remapped.append({"aggregate": round(rep.aggregate, 4), "scores": _entity_scores(rep),
                                 "ranges": rebuild_entity_line_map(ht.last_annotated_source)})
                print(f"  {name[:40]} remap {i + 1}/{args.repeats}: {rep.aggregate:.3f}", flush=True)
            # One mapping in the numbering verify() expects (the CLEAN source; the ranges read back
            # from an annotated source are shifted by the inserted sentinel lines).
            from r2py.stage2.sentinel_mapper import map_entities_to_lines
            try:
                fixed_map = flatten_entity_line_map(map_entities_to_lines(sm, source, model=cfg["model"]))
            except Exception as exc:  # the mapper itself failing is a finding, not a reason to stop
                print(f"  {name[:40]}: mapping failed for the fixed-map condition ({exc}); skipped")
                results[name] = {"remapped": analyse(remapped), "fixed_map": analyse([{"aggregate": float("nan"),
                                 "scores": {}, "ranges": {}}]), "mapping_failed": True}
                continue
            fixed = []
            for i in range(args.repeats):
                rep = verifier.verify(sm, source, data_compare=cfg["data_compare"], entity_line_map=fixed_map,
                                      sidecar_filename=f"{Path(name).stem}.r2py_data.json",
                                      timeout_s=cfg["timeout_s"])
                fixed.append({"aggregate": round(rep.aggregate, 4), "scores": _entity_scores(rep),
                              "ranges": {e: [list(r)] for e, r in fixed_map.items()}})
            results[name] = {"remapped": analyse(remapped), "fixed_map": analyse(fixed)}

    Path(args.out).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"\n{'script':44s} {'aggregate, remapped':32s} {'aggregate, fixed map':28s} ent.score/range varying")
    for name, r in results.items():
        a, b = r["remapped"], r["fixed_map"]
        print(f"{name[:44]:44s} {spread(a['aggregates']):32s} {spread(b['aggregates']):28s} "
              f"{a['entities_with_varying_score']}/{a['entities_with_varying_range']} of {a['entities']} "
              f"(fixed map: {b['entities_with_varying_score']})")
    noisy = sum(1 for r in results.values() if r["remapped"]["agg_range"] > 1e-9)
    print(f"\nscripts whose aggregate moved when the SAME source was re-mapped: {noisy}/{len(results)}")
    print(f"scripts whose aggregate moved with the mapping held fixed:        "
          f"{sum(1 for r in results.values() if r['fixed_map']['agg_range'] > 1e-9)}/{len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
