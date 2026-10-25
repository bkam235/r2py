"""Experiment registry for the meta-loop (2026-10-25): one structured record per experiment.

`experiments/registry.jsonl`, one JSON object per line, next to the prose log (`IMPROVEMENT_PLAN.md`, which keeps the
reasoning; the record's `plan` names its entry there). A record is written when the test is registered, before any
data, and completed when it is decided (`experiments/META_LOOP.md`, steps 4 and 6-9).

    python scripts/registry.py register spec.json     # step 4: the spec's fields below; refused if the id exists
    python scripts/registry.py result ID --run-dir work/two_step --estimate "+0.049 [-0.013, +0.116], P=0.93" \
        --decision adopted [--heldout pending] [--commit abc123] [--note "..."]
    python scripts/registry.py list                   # one line per experiment
    python scripts/registry.py show ID

Registered fields (required): id, question, track (harness | scorer), instrument, pool, arms, baseline, primary,
rule, est_cost (USD, or null), plan. Optional: option, samples, strata, run_dir, analysis, budget, note.
Added on register: registered (date and time), status "registered", scoring_version, commit_registered (HEAD).
Added on result: decided (date), status "decided", cost (from <run_dir>/run_manifest.json: the invocations that
started after the registration, since a run directory can hold several experiments; else --cost),
run_scoring_version (from the manifest), estimate, decision, heldout, commit, note.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
REGISTRY = ROOT / "experiments/registry.jsonl"
REQUIRED = ("id", "question", "track", "instrument", "pool", "arms", "baseline", "primary", "rule", "est_cost", "plan")
TRACKS = ("harness", "scorer")
DECISIONS = ("adopted", "not adopted", "extended", "descriptive")
HELDOUT = ("pending", "passed", "failed", "not possible", "not run")


def load(path: Path = REGISTRY) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def save(records: list[dict], path: Path = REGISTRY) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")


def _head() -> str:
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def register(spec: dict, path: Path = REGISTRY) -> dict:
    missing = [k for k in REQUIRED if k not in spec]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    if spec["track"] not in TRACKS:
        raise ValueError(f"track must be one of {TRACKS}")
    records = load(path)
    if any(r["id"] == spec["id"] for r in records):
        raise ValueError(f"id {spec['id']!r} is already registered")
    from r2py.scoring import scoring_version
    rec = {**spec, "registered": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "status": "registered",
           "scoring_version": scoring_version(), "commit_registered": _head()}
    save(records + [rec], path)
    return rec


def _manifest(run_dir: Path, since: str) -> tuple["float | None", "str | None"]:
    """Cost and scorer version(s) of the run guard's invocations that started after ``since``."""
    mf = run_dir / "run_manifest.json"
    if not mf.exists():
        return None, None
    ms = [m for m in json.loads(mf.read_text(encoding="utf-8")) if m["started"][:16] >= since]
    costs = [m.get("cost") for m in ms if m.get("cost") is not None]
    versions = sorted({m.get("scoring_version") for m in ms if m.get("scoring_version")})
    return (round(sum(costs), 2) if costs else None), (", ".join(versions) or None)


def result(rid: str, estimate: str, decision: str, run_dir: "str | None" = None, cost: "float | None" = None,
           heldout: "str | None" = None, commit: "str | None" = None, note: "str | None" = None,
           path: Path = REGISTRY) -> dict:
    if decision not in DECISIONS:
        raise ValueError(f"decision must be one of {DECISIONS}")
    if heldout is not None and heldout not in HELDOUT:
        raise ValueError(f"heldout must be one of {HELDOUT}")
    records = load(path)
    rec = next((r for r in records if r["id"] == rid), None)
    if rec is None:
        raise ValueError(f"no experiment {rid!r}; register it first")
    run_dir = run_dir or rec.get("run_dir")
    m_cost, m_version = _manifest(ROOT / run_dir, rec["registered"]) if run_dir else (None, None)
    rec.update(decided=dt.date.today().isoformat(), status="decided", estimate=estimate, decision=decision,
               cost=cost if cost is not None else m_cost)
    for k, v in (("run_dir", run_dir), ("run_scoring_version", m_version), ("heldout", heldout),
                 ("commit", commit), ("note", note)):
        if v is not None:
            rec[k] = v
    save(records, path)
    return rec


def listing(records: list[dict]) -> str:
    lines = [f"{'id':28s} {'registered':10s} {'status':10s} {'decision':12s} {'cost':>6s}  question"]
    for r in records:
        cost = f"${r['cost']:.2f}" if r.get("cost") is not None else "-"
        lines.append(f"{r['id'][:28]:28s} {r['registered'][:10]:10s} {r['status']:10s} {r.get('decision', '-')[:12]:12s} "
                     f"{cost:>6s}  {r['question'][:70]}")
    spent = sum(r.get("cost") or 0 for r in records)
    lines.append(f"{len(records)} experiments, ${spent:.2f} recorded spend")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("register")
    p.add_argument("spec", help="JSON file with the registered fields")
    p = sub.add_parser("result")
    p.add_argument("id")
    p.add_argument("--estimate", required=True, help="the primary estimate as the analysis reports it")
    p.add_argument("--decision", required=True, choices=DECISIONS)
    p.add_argument("--run-dir")
    p.add_argument("--cost", type=float, help="actual USD, when the run has no run_manifest.json")
    p.add_argument("--heldout", choices=HELDOUT)
    p.add_argument("--commit")
    p.add_argument("--note")
    sub.add_parser("list")
    p = sub.add_parser("show")
    p.add_argument("id")
    a = ap.parse_args()
    try:
        if a.cmd == "register":
            print(json.dumps(register(json.loads(Path(a.spec).read_text(encoding="utf-8"))), indent=1, ensure_ascii=False))
        elif a.cmd == "result":
            print(json.dumps(result(a.id, a.estimate, a.decision, a.run_dir, a.cost, a.heldout, a.commit, a.note),
                             indent=1, ensure_ascii=False))
        elif a.cmd == "list":
            print(listing(load()))
        else:
            rec = next((r for r in load() if r["id"] == a.id), None)
            if rec is None:
                raise ValueError(f"no experiment {a.id!r}")
            print(json.dumps(rec, indent=1, ensure_ascii=False))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
