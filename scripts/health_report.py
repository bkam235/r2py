"""Health report of a replay run: the diagnoses that found the October fixes, produced after every run (2026-10-24).

Reads a replay output directory (results.jsonl, trajectories/, run_manifest.json) and writes health_report.md:
  - per arm: runs, start and final, improved, reaching the threshold, ending in a running program, model calls,
    stop reasons, review rejections, conversation turns;
  - score gap: 1 - mean final split exactly by outcome (never improved, improved below 0.9, at 0.9 or above, ending
    in a crash) and start stratum, and the states that hold the most of it;
  - attribution paths: how often a verification needed a model mapping (the one remaining scoring noise);
  - crashes: exception types of the crashing candidates, and the runs that end with a crashing program;
  - never-improving states: states where no run improved on its start (14 of 40 such states found the checkpoint,
    tag, temp-path and shim faults on 2026-10-17). With --deep each one's start is re-verified (no model calls) and
    its losing entities are listed with their verifier messages and whether R and Python had per-entity results;
  - pasting: the deterministic paste check on every changed final program (a measuring instrument, not a gate);
  - the run's scorer version(s), invalid rows and cost.

    python scripts/health_report.py work/replay_default            # cheap: no verification
    python scripts/health_report.py work/replay_default --deep     # also re-verify the never-improving starts
"""
from __future__ import annotations

import argparse
import json
import pickle
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
SOURCES = ROOT / "work/heldout/train_outputs"
MAPS = ROOT / "work/reverify/script_maps"
EXC_RE = re.compile(r"\b([A-Z][A-Za-z]*(?:Error|Exception|Warning)|KeyboardInterrupt|StopIteration|TimeoutExpired)\b")


def _calls(agent: dict) -> int:
    n = sum((agent.get("action") or {}).values())
    for k, v in (agent.get("guided_width") or {}).items():
        n += (int(k.split("_")[0]) - 1) * v
    return n


def _trajectory(run_dir: Path, r: dict) -> list[dict]:
    f = run_dir / "trajectories" / f"{Path(r['script']).stem}.{r['policy']}.{r['sample']}.jsonl"
    return [json.loads(l) for l in f.open(encoding="utf-8")] if f.exists() else []


def _final_program(recs: list[dict]) -> "str | None":
    best, src = None, None
    for x in recs:
        if x["kind"] == "accepted" and x.get("source"):
            key = (x.get("exit_code") == 0, x.get("aggregate", 0.0))
            if best is None or key > best:
                best, src = key, x.get("scored_source") or x["source"]
    return src


def _deep(name: str) -> list[str]:
    """Losing entities of a start program, with their verifier messages (no model calls)."""
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from prompt_load import _tools
    from r2py.harness.objective import entity_score
    stem = Path(name).stem
    src = (SOURCES / f"{stem}.py").read_text(encoding="utf-8")
    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    t = _tools(sm, stem)
    t.note_reference(src)
    rep = t.verify(src)
    rb, pb = sm.entity_bundles or {}, getattr(rep, "py_entity_bundles", None) or {}
    lines = []
    losing = sorted(((entity_score(es), e) for e, es in rep.by_entity.items() if es.active_dims and entity_score(es) < 0.95))
    for score, e in losing[:6]:
        msgs = [f"[{f.effect_class.value}] {f.message[:140]}".replace("\n", " ").replace("|", "/")
                for f in rep.feedback if f.entity_id == e][:2]
        where = ("R" if e in rb else "no R bundle") + ", " + ("Py" if e in pb else "no Py bundle")
        lines.append(f"    - `{e}` {score:.2f} ({where}): " + ("; ".join(msgs) or "no message"))
    if not rb:
        lines.insert(0, "    - **no per-entity R results for this script** (every entity scored on script-wide fallbacks)")
    return lines


def report(run_dir: Path, deep: bool = False) -> str:
    from paste_check import check as paste_check
    rows = [json.loads(l) for l in (run_dir / "results.jsonl").open(encoding="utf-8")]
    invalid = [r for r in rows if r.get("invalid") or "error" in r]
    rows = [r for r in rows if not (r.get("invalid") or "error" in r) and "final_score" in r]
    out = [f"# Health report: `{run_dir.relative_to(ROOT).as_posix()}`", ""]
    versions = Counter(r.get("scoring_version", "unrecorded") for r in rows)
    out.append(f"- Valid runs {len(rows)}, invalid or failed {len(invalid)}; scorer version(s): "
               + ", ".join(f"`{v}` ({n})" for v, n in versions.items()))
    mf = run_dir / "run_manifest.json"
    if mf.exists():
        ms = json.loads(mf.read_text(encoding="utf-8"))
        out.append(f"- Cost ${sum(m.get('cost') or 0 for m in ms):.2f} over {len(ms)} invocation(s); stop reasons: "
                   + ", ".join(m["stop_reason"] for m in ms) + "; sleep gaps: " + str(sum(len(m["sleep_gaps"]) for m in ms)))
    trajs = {id(r): _trajectory(run_dir, r) for r in rows}

    # per arm
    out += ["", "## Arms", "", "| arm | runs | start | final | improved | final >= 0.9 | ends running | calls/run | stops | review rejections | conversation turns |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    by_arm = defaultdict(list)
    for r in rows:
        by_arm[r["policy"]].append(r)
    for arm, rs in sorted(by_arm.items()):
        stops = Counter()
        for r in rs:
            stops.update(r["agent"].get("stop") or {})
        rej = sum(v for r in rs for k, v in (r["agent"].get("outcome") or {}).items() if k.endswith("review_rejected"))
        conv = sum((r["agent"].get("outcome") or {}).get("conversation_turn", 0) for r in rs)
        out.append(f"| {arm} | {len(rs)} | {st.mean(r['start_score'] for r in rs):.3f} | {st.mean(r['final_score'] for r in rs):.3f} "
                   f"| {st.mean(r['final_score'] > r['start_score'] + 1e-9 for r in rs):.2f} | {st.mean(r['final_score'] >= 0.9 for r in rs):.2f} "
                   f"| {sum(r['final_exit'] == 0 for r in rs)}/{len(rs)} | {st.mean(_calls(r['agent']) for r in rs):.1f} "
                   f"| {', '.join(f'{k} {v}' for k, v in stops.most_common())} | {rej} | {conv} |")

    # where the remaining score sits (exact: the parts add up to 1 - mean final)
    def group(r):
        if r["final_exit"] != 0:
            return "ends crashing"
        if r["final_score"] >= 0.9:
            return "final >= 0.9"
        return "improved, final < 0.9" if r["final_score"] > r["start_score"] + 1e-9 else "never improved"
    out += ["", f"## Score gap (1 - mean final = {st.mean(1 - r['final_score'] for r in rows):.3f})", "",
            "Points of the gap by outcome and start stratum (each run's 1 - final, divided by all runs; the cells add up "
            "to the gap). Questions are worth what share of it they can reach.", "",
            "| outcome | runs | start runs | start crashes | total | share |", "|---|---|---|---|---|---|"]
    gap_total = sum(1 - r["final_score"] for r in rows) or 1.0
    for g in ("never improved", "improved, final < 0.9", "final >= 0.9", "ends crashing"):
        rs = [r for r in rows if group(r) == g]
        pts = [sum(1 - r["final_score"] for r in rs if bool(r["start_exit"]) == c) / len(rows) for c in (False, True)]
        out.append(f"| {g} | {len(rs)} | {pts[0]:.3f} | {pts[1]:.3f} | {sum(pts):.3f} | "
                   f"{sum(1 - r['final_score'] for r in rs) / gap_total:.0%} |")
    lost = defaultdict(list)
    for r in rows:
        lost[r["script"]].append(r)
    top = sorted(lost.items(), key=lambda kv: -sum(1 - r["final_score"] for r in kv[1]))[:10]
    out += ["", "States holding the most of the gap: " + ", ".join(
        f"`{Path(s).stem}` {sum(1 - r['final_score'] for r in rs) / len(rows):.3f} ({group(rs[0])})" for s, rs in top)]

    # attribution paths
    paths = Counter()
    for r in rows:
        paths.update({k: v for k, v in (r.get("verify_paths") or {}).items() if k != "hit"})
    misses = paths.get("miss", 0)
    out += ["", "## Attribution", "",
            f"- Verifications {misses}: sentinels read {paths.get('sentinel_reuse', 0)}, restored {paths.get('sentinel_restored', 0)}, "
            f"**model mapping {paths.get('mapping_ok', 0)}** ({paths.get('mapping_ok', 0) / max(misses, 1):.0%}), "
            f"mapping failed {paths.get('mapping_failed', 0)}." if misses else "- No attribution statistics recorded."]

    # crashes
    exc, ending = Counter(), []
    for r in rows:
        for x in trajs[id(r)]:
            if x["kind"] == "step" and x.get("exit_code") not in (0, None) and x.get("crash"):
                m = EXC_RE.search(x["crash"])
                # trajectories before 2026-10-25 kept only 600 characters, which cut off the exception line
                exc[m.group(1) if m else "truncated" if len(x["crash"]) == 600 else "unclassified"] += 1
        if r["final_exit"] != 0:
            ending.append(f"{Path(r['script']).stem} ({r['policy']} s{r['sample']})")
    out += ["", "## Crashes", "",
            "- Crashing candidates by exception: " + (", ".join(f"{k} {v}" for k, v in exc.most_common(10)) or "none"),
            f"- Runs ending with a crashing program ({len(ending)}): " + (", ".join(ending) or "none")]

    # never-improving states
    per_state = defaultdict(list)
    for r in rows:
        per_state[r["script"]].append(r)
    stuck = sorted(s for s, rs in per_state.items() if all(r["final_score"] <= r["start_score"] + 1e-9 for r in rs)
                   and st.mean(r["start_score"] for r in rs) < 0.9)
    out += ["", f"## Never-improving states ({len(stuck)} of {len(per_state)})", ""]
    for s in stuck:
        rs = per_state[s]
        out.append(f"- `{Path(s).stem}`: start {rs[0]['start_score']:.3f}, start {'crashes' if rs[0]['start_exit'] else 'runs'}, "
                   f"{len(rs)} run(s)")
        if deep:
            try:
                out += _deep(s)
            except Exception as exc_:
                out.append(f"    - re-verification failed: {type(exc_).__name__}: {exc_}"[:200])
    if stuck and not deep:
        out.append("\n(`--deep` re-verifies these starts and lists their losing entities.)")

    # pasting
    flagged, n = [], 0
    for r in rows:
        src = _final_program(trajs[id(r)])
        if not src:
            continue
        stem = Path(r["script"]).stem
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        res = paste_check(src, (SOURCES / f"{stem}.py").read_text(encoding="utf-8"), sm.source or "", getattr(sm, "entity_bundles", {}) or {})
        n += 1
        if res.get("pasted"):
            flagged.append(f"`{stem}` ({r['policy']}): {str(res.get('examples'))[:120]}")
    out += ["", "## Pasting (deterministic check on changed final programs)", "",
            f"- Flagged {len(flagged)} of {n} ({len(flagged) / max(n, 1):.0%}). The check over-flags print labels and class "
            "names; read the examples."]
    out += [f"  - {f}" for f in flagged]
    if invalid:
        out += ["", "## Invalid or failed runs", ""] + [f"- `{Path(r['script']).stem}` {r.get('policy')} s{r.get('sample')}: "
                                                         f"{r.get('invalid') or r.get('error', '')[:120]}" for r in invalid]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--deep", action="store_true", help="re-verify never-improving starts (no model calls)")
    a = ap.parse_args()
    run_dir = Path(a.run_dir).resolve()
    text = report(run_dir, a.deep)
    (run_dir / "health_report.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
