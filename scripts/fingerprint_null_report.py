"""Chance-match rate of numeric fingerprint fields, over the whole corpus (Stage 4 Phase 1 validation).

A numeric field of one R object counts as reproduced if its values are found in a Python object's number pool.  This
measures how often that happens by chance: each field is matched against pools built from unrelated variables of
*other scripts* (R numbers stand in for Python numbers; only the values matter).  Fields are bucketed by length and
by whether they contain non-integers; the rule for "informative" (``fingerprint.informative``) must keep the chance
rate of everything it admits under the target.  No labels and no model calls: the corpus is the pipeline's own capture
(``scripts/census_data_classes.py`` writes ``work/census/fields.jsonl``).

    python scripts/fingerprint_null_report.py [--target 1e-3] [--pools 150] [--pool-vars 10]

Exit status 1 if the constants currently in ``r2py/stage4/comparators/fingerprint.py`` miss the target.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load(path: Path) -> list[dict]:
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r for r in rows if "captured" in r]


def bucket(vals: list[float]) -> str:
    n = len(vals)
    non_int = sum(1 for v in vals if abs(v - round(v)) > 1e-9)
    size = "1" if n == 1 else "2-4" if n < 5 else "5-19" if n < 20 else "20+"
    return f"len {size:4s} " + ("has non-integers" if non_int else "integers only   ")


def chance_rates(corpus: list[dict], n_pools: int, pool_vars: int, rtol: float, atol: float, seed: int = 0):
    """rows of (script, field vals) and, for each, the fraction of sampled foreign pools that contain it."""
    from r2py.stage4.comparators import fingerprint as fp

    rng = random.Random(seed)
    variables = [(r["script"], v) for r in corpus for v in r["captured"].values() if v["fields"]]
    fields = [(r["script"], vals) for r in corpus for v in r["captured"].values()
              for _path, vals in v["fields"] if vals]
    pools_by_script: dict[str, list[list[float]]] = collections.defaultdict(list)
    for script, v in variables:
        pools_by_script[script].append(sorted(x for _p, vec in v["fields"] for x in vec))
    scripts = list(pools_by_script)
    # Pools are built once (each from pool_vars variables of different scripts) and reused; a field is only
    # matched against pools that contain nothing from its own script.
    pools = []
    for _ in range(max(n_pools * 3, 300)):
        members = rng.sample(scripts, min(pool_vars, len(scripts)))
        pools.append((set(members), sorted(x for s in members for x in rng.choice(pools_by_script[s]))))
    if len(fields) > 4000:
        fields = rng.sample(fields, 4000)
    results = []
    for script, vals in fields:
        # Not just another script: another package. Rd examples of one package share data and objects, so
        # their numbers coincide for a real reason; across packages a match is chance or a shared dataset.
        pkg = script.split("__")[0]
        foreign = [p for members, p in pools if all(m.split("__")[0] != pkg for m in members)][:n_pools]
        hits = sum(fp.field_match(vals, p, rtol, atol) >= fp.MATCH_FRACTION for p in foreign)
        results.append((script, vals, hits / max(1, len(foreign))))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fields", default=str(ROOT / "work/census/fields.jsonl"))
    ap.add_argument("--target", type=float, default=1e-3)
    ap.add_argument("--pools", type=int, default=150)
    ap.add_argument("--pool-vars", type=int, default=10)
    args = ap.parse_args()

    from r2py.stage4.comparators import fingerprint as fp
    from r2py.stage4.comparators.data import _DEFAULT_ATOL, _DEFAULT_RTOL

    corpus = load(Path(args.fields))
    res = chance_rates(corpus, args.pools, args.pool_vars, _DEFAULT_RTOL, _DEFAULT_ATOL)
    print(f"{len(corpus)} scripts, {len(res)} numeric fields, each matched against {args.pools} foreign pools "
          f"of {args.pool_vars} variables\n")
    print("chance-match rate by field kind (all fields, before any informativeness rule):")
    by = collections.defaultdict(list)
    for _s, vals, rate in res:
        by[bucket(vals)].append(rate)
    for k in sorted(by):
        rates = by[k]
        print(f"  {k}  fields {len(rates):5d}   mean chance rate {sum(rates) / len(rates):.4f}   "
              f"fields that ever matched {sum(r > 0 for r in rates)}")

    def rate_of(min_non_int: int, min_distinct: int) -> tuple[float, int]:
        keep = [r for _s, vals, r in res if _admit(vals, min_non_int, min_distinct)]
        return (sum(keep) / len(keep) if keep else 0.0), len(keep)

    def _admit(vals, min_non_int, min_distinct) -> bool:
        non_int = sum(1 for v in vals if abs(v - round(v)) > 1e-9)
        return (non_int >= min(len(vals), min_non_int) and non_int > 0) or len({round(v) for v in vals}) >= min_distinct

    print("\nchance-match rate of the fields each rule admits (target {:.0e}):".format(args.target))
    best = None
    for mn, md in itertools.product((1, 2, 3), (6, 8, 12, 20, 10 ** 9)):
        rate, n = rate_of(mn, md)
        ok = rate < args.target
        print(f"  MIN_NON_INTEGERS={mn} MIN_DISTINCT_INTEGERS={md if md < 10 ** 9 else 'never':>5}: "
              f"{n:5d} fields admitted, chance rate {rate:.5f} {'ok' if ok else ''}")
        if ok and n and (best is None or n > best[2]):
            best = (mn, md, n)
    if best:
        print(f"\nloosest rule under the target: MIN_NON_INTEGERS={best[0]}, MIN_DISTINCT_INTEGERS={best[1]} "
              f"({best[2]} of {len(res)} fields admitted)")
    rate, n = rate_of(fp.MIN_NON_INTEGERS, fp.MIN_DISTINCT_INTEGERS)
    passed = rate < args.target
    print(f"\ncurrent constants (MIN_NON_INTEGERS={fp.MIN_NON_INTEGERS}, MIN_DISTINCT_INTEGERS={fp.MIN_DISTINCT_INTEGERS}): "
          f"{n} fields admitted, chance rate {rate:.5f} -> {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
