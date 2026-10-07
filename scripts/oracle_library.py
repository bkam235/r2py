"""Build a per-script *oracle* pattern library: a verified example for every function the script calls.

An upper bound on retrieval-based learning. The real library reached 17% of the held-out loss and
recovered none of it (`scripts/coverage_probe.py`); a general RAG over past translations could at best
reach 52%. Rather than build that first, give one script a library that already holds a verified
example of *exactly* the functions it uses -- perfect coverage, perfect retrieval -- and see whether
the agent loop does any better with it (`scripts/replay.py --policies rewrite_w3 rewrite_w3_oracle`).

Examples come from the re-verified training translations (`scripts/reverify_training.py`): every entity
that scored >= THRESHOLD, keyed by its own (package, function) and by each base-R function it calls.
Training scripts only, so a target script never sees an example derived from itself.

    python scripts/oracle_library.py build
    python scripts/oracle_library.py build --targets dplyr__vignette__colwise_chunk17.R
"""
from __future__ import annotations

import argparse
import json
import pickle
import shutil
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ROWS = ROOT / "work" / "reverify" / "rows.jsonl"
MAPS = ROOT / "work" / "replay" / "script_maps"
OUT = ROOT / "work" / "oracle" / "libs"
THRESHOLD = 0.9
MAX_EXAMPLES = 3


def candidates() -> dict[str, list[dict]]:
    """pattern id -> verified examples for it, best first."""
    from r2py.library.pattern import pattern_id

    by_key: dict[str, list[dict]] = defaultdict(list)
    for line in ROWS.open(encoding="utf-8"):
        row = json.loads(line)
        if "error" in row:
            continue
        for e in row["entities"]:
            if e["score"] < THRESHOLD or not e["py_snippet"].strip() or not e["r_snippet"].strip():
                continue
            ex = {"r": e["r_snippet"], "py": e["py_snippet"], "score": e["score"],
                  "script": row["script"], "n_calls": len(e["calls"])}
            for key in filter(None, [e["key"], *e["calls"]]):
                by_key[key].append({**ex, "package": key.split(".", 1)[0], "fn": key.split(".", 1)[1]})
    for key, exs in by_key.items():
        exs.sort(key=lambda x: (-x["score"], x["n_calls"], x["script"]))
    return by_key


def script_keys(stem: str) -> set[str]:
    """Every pattern id the script's entities would look up: own keys and base-R calls."""
    from r2py.library.pattern import correction_functions, pattern_id, pattern_key

    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    keys: set[str] = set()
    for e in sm.entities.values():
        k = pattern_key(e)
        if k:
            keys.add(pattern_id(*k))
        keys.update(pattern_id(*q.split("::")) for q in correction_functions(e.base_r_calls or []))
    return keys


def build_one(stem: str, pool: dict[str, list[dict]]) -> dict:
    from r2py.library import PatternLibrary
    from r2py.library.pattern import MAX_PY_SNIPPET, MAX_R_SNIPPET, Pattern, TranslationExample, clip_snippet, r_snippet_hash
    from r2py.library.writer import _add_translation_example

    out = OUT / stem
    if out.exists():
        shutil.rmtree(out)
    lib = PatternLibrary(out)
    needed = script_keys(stem)
    written = 0
    for key in sorted(needed):
        exs = [e for e in pool.get(key, []) if Path(e["script"]).stem != stem][:MAX_EXAMPLES]
        if not exs:
            continue
        package, fn = key.split(".", 1)
        pat = Pattern(id=key, package=package, confidence="tentative", seed=True,
                      guidance=(f"Translate R `{fn}` from {package} to Python. The verified example "
                                f"below comes from another script that used it."),
                      created=date.today().isoformat(), last_review=date.today().isoformat())
        for e in exs:
            _add_translation_example(pat, TranslationExample(
                r_hash=r_snippet_hash(e["r"]), r_snippet=clip_snippet(e["r"], MAX_R_SNIPPET),
                py_snippet=clip_snippet(e["py"], MAX_PY_SNIPPET), score=e["score"],
                script_id=e["script"], n_calls=e["n_calls"]))
        lib.store.save(pat)
        written += 1
    lib.index.rebuild(lib.store)
    return {"script": stem, "keys_needed": len(needed), "patterns": written}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--targets", nargs="+", default=None, help="script names (default: every cached script map)")
    args = ap.parse_args()

    pool = candidates()
    print(f"{sum(len(v) for v in pool.values())} verified examples over {len(pool)} keys "
          f"(threshold {THRESHOLD})")
    stems = [Path(t).stem for t in args.targets] if args.targets else sorted(p.stem for p in MAPS.glob("*.pkl"))
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [build_one(s, pool) for s in stems]
    rows.sort(key=lambda r: r["patterns"] / max(1, r["keys_needed"]))
    covered = sum(r["patterns"] for r in rows)
    need = sum(r["keys_needed"] for r in rows)
    print(f"{len(rows)} libraries in {OUT}: {covered} patterns for {need} keys needed "
          f"({covered / max(1, need):.0%} of lookups answered)")
    for r in (rows[:5] + rows[-3:] if len(rows) > 8 else rows):
        print(f"   {r['patterns']:>3}/{r['keys_needed']:<3} {r['script']}")
    (OUT.parent / "build.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
