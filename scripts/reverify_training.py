"""Re-verify the saved translations of the first experiment's training run, per entity.

The training run recorded only each script's aggregate, so the library could learn only from the
85 scripts that scored >= 0.9 (`scripts/coverage_probe.py`: that gate, not the exact
(package, function) key, is what caps reachable loss at 22% instead of 52%). The translations
themselves are on disk with their entity sentinels intact, so every entity can be scored again
offline: attribution is read off the sentinels, which costs no model call, and `llm_calls` on each
row proves it (any non-zero value means a mapping fell back to the model and that row's
attribution is noisy).

    python scripts/reverify_training.py run --workers 5
    python scripts/reverify_training.py summary

Writes one row per script to work/reverify/rows.jsonl (resumable: finished scripts are skipped),
each carrying every entity's score and its (R snippet, Python snippet) pair -- the corpus a
per-entity harvest would have, and the material for the oracle-library replay.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "experiments" / "heldout" / "manifest.json"
TRANSLATIONS = ROOT / "work" / "heldout" / "train_outputs"
OUT = ROOT / "work" / "reverify"   # rows.jsonl; the v2 pass adds per-entity feedback
MAX_R, MAX_PY = 1000, 2000


def _script_map(name: str, manifest: dict):
    """The analysed script (runs R), cached on disk as in scripts/replay.py."""
    from r2py import heldout as ho
    from r2py.stage1 import analyze

    cache = OUT / "script_maps"
    f = cache / (Path(name).stem + ".pkl")
    if f.exists():
        return pickle.loads(f.read_bytes())
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    sm = analyze(next(pool.rglob(name)))
    sm.ast_root = None                     # a tree-sitter node: not picklable, only analysis reads it
    cache.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(f".{multiprocessing.current_process().pid}.tmp")
    tmp.write_bytes(pickle.dumps(sm))
    tmp.replace(f)
    return sm


def _snippets(sm, entity, source: str, ranges) -> tuple[str, str]:
    """The entity's R lines and the Python lines its sentinels enclose."""
    r_text = ""
    span = getattr(entity, "source_span", None)
    if span is not None and getattr(sm, "source", ""):
        lines = sm.source.splitlines()
        start = getattr(span, "start_line", 0)
        r_text = "\n".join(lines[start:min(len(lines), getattr(span, "end_line", start) + 1)])
    py_lines = source.splitlines()
    picked: list[str] = []
    for start, end in (ranges or []):
        picked += [l for l in py_lines[start:end + 1] if "r2py:entity:" not in l]
    return r_text[:MAX_R], "\n".join(picked).strip("\n")[:MAX_PY]


def one(script: str) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.stage2 import llm
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels

    calls = [0]
    real_call = llm.call

    def counted(*a, **k):                  # attribution must come from the sentinels, not the model
        calls[0] += 1
        return real_call(*a, **k)
    llm.call = counted

    manifest = ho.load_manifest(MANIFEST)
    cfg = manifest["protocol"]["translate"]
    stem = Path(script).stem
    row = {"script": script}
    started = time.monotonic()
    try:
        source = (TRANSLATIONS / f"{stem}.py").read_text(encoding="utf-8")
        sm = _script_map(script, manifest)
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            lib = PatternLibrary(OUT / "empty_lib")
            tools = HarnessTools(sm, lib, model=cfg["model"], data_compare=cfg["data_compare"],
                                 timeout_s=cfg["timeout_s"], sidecar_filename=f"{stem}.r2py_data.json")
            tools.note_reference(source)
            report = tools.verify(source)
        ranges = ranges_from_sentinels(source)
        ents = []
        for rec in ho._entity_records(sm, report):
            entity = sm.entities[rec["id"]]
            r_text, py_text = _snippets(sm, entity, source, ranges.get(rec["id"]))
            # Which comparison complained, and in which direction: the prompt-arms sweep found every
            # stdout/files/graphics complaint pointing one way (Python produced output R never did).
            fb = [f"{f.effect_class.value}: {f.message}"[:220]
                  for f in report.feedback if f.entity_id == rec["id"]][:4]
            ents.append({**rec, "r_snippet": r_text, "py_snippet": py_text, "feedback": fb})
        row.update(aggregate=round(report.aggregate, 4), py_exit=report.py_exit_code,
                   infra_crash=report.infra_crash, entities=ents,
                   by_effect={k.value if hasattr(k, "value") else str(k): v
                              for k, v in (report.by_effect or {}).items()})
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["llm_calls"] = calls[0]
    row["seconds"] = round(time.monotonic() - started, 1)
    llm.call = real_call
    return row


def run(workers: int) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scripts = [e["script"] for e in manifest["train"]
               if (TRANSLATIONS / f"{Path(e['script']).stem}.py").exists()]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "rows_v2.jsonl"
    done = {json.loads(l)["script"] for l in path.open(encoding="utf-8")} if path.exists() else set()
    todo = [s for s in scripts if s not in done]
    print(f"{len(scripts)} translations saved, {len(done)} done, {len(todo)} to go, {workers} workers",
          flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(workers) as pool, path.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(one, todo), start=1):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            mark = row["error"] if "error" in row else f"{row['aggregate']:.3f}"
            print(f"{i}/{len(todo)} {row['script'][:48]:<50} {mark}  "
                  f"{row['seconds']}s  llm={row['llm_calls']}", flush=True)


def summary() -> str:
    import statistics
    name = "rows_v2.jsonl" if (OUT / "rows_v2.jsonl").exists() else "rows.jsonl"
    rows = [json.loads(l) for l in (OUT / name).open(encoding="utf-8")]
    ok = [r for r in rows if "error" not in r]
    ents = [e for r in ok for e in r["entities"]]
    verified = [e for e in ents if e["score"] >= 0.9 and e["py_snippet"]]
    keys = {e["key"] for e in verified if e["key"]}
    good_scripts = [r for r in ok if r["aggregate"] >= 0.9]
    out = [f"{len(rows)} scripts re-verified ({len(rows) - len(ok)} errors), "
           f"{sum(r['llm_calls'] for r in rows)} model calls",
           f"aggregate: mean {statistics.mean(r['aggregate'] for r in ok):.3f}, "
           f">= 0.9: {len(good_scripts)}",
           f"entities: {len(ents)}, scoring >= 0.9 with a Python snippet: {len(verified)} "
           f"({len(verified) / max(1, len(ents)):.0%})",
           f"distinct keys among them: {len(keys)}",
           f"of those keys, only reachable per entity (not from a >= 0.9 script): "
           f"{len(keys - {e['key'] for r in good_scripts for e in r['entities'] if e['key']})}"]
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--limit", type=int, default=None, help="smoke test: only this many scripts")
    sub.add_parser("summary")
    args = ap.parse_args()
    if args.cmd == "run":
        if args.limit:
            import itertools
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            names = [e["script"] for e in manifest["train"]][:args.limit]
            OUT.mkdir(parents=True, exist_ok=True)
            with (OUT / "smoke.jsonl").open("w", encoding="utf-8") as fh:
                for n in names:
                    r = one(n)
                    print(json.dumps({k: v for k, v in r.items() if k != "entities"}), flush=True)
                    fh.write(json.dumps(r) + "\n")
        else:
            run(args.workers)
    else:
        text = summary()
        print(text)
        (OUT / "summary.txt").write_text(text + "\n", encoding="utf-8")
