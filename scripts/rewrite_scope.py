"""Which entities does a rewrite touch? (offline, no model calls; reads saved trajectories only)

Hypothesis (a), 2026-11-12: GLM rewrites parts of the program that it should leave alone more often than DeepSeek.
For every rewrite candidate the base is the chain's best program at that step (`best_hash`). Base and candidate are
diffed line by line (sentinel, blank and comment-only lines dropped); a changed line belongs to the entity whose
`# r2py:entity:<id>` range holds it (base side: the base's sentinels; candidate side: the candidate's, with dropped
ones restored as the harness does). An entity is *verified* if the base scores it 1.0.

Per rewrite: verified entities touched (count, share of the verified ones), whether a failing entity was touched at
all, share of the changed lines inside verified entities, and for verified candidates how many verified entities
dropped below 1.0; also the harness's outcome (catastrophic = crash or a large drop, improved) and whether a verified
candidate crashed. Breadth (entities touched, share of the base's lines changed) needs no scores and is reported for
every rewrite; the verified/failing split only where the base's per-entity scores were logged (a frozen start that
no chain re-verified has none).

    python scripts/rewrite_scope.py screen     # model screen: GLM 5.3 Flash vs DeepSeek Flash, same stall-2 chains
    python scripts/rewrite_scope.py full       # full runs: GLM 5.3 (ceiling_glm53) vs DeepSeek Flash (dsflash_default)
"""
from __future__ import annotations

import collections
import difflib
import json
import random
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from r2py.harness import trajectory  # noqa: E402
from r2py.stage2.sentinel_mapper import _SENTINEL_ID_RE, restore_sentinels  # noqa: E402

PRE = "_preamble"
METRICS = ("entities_touched_share", "base_lines_changed_share", "sentinels_lost", "verified_touched", "verified_touched_share", "any_verified_touched", "failing_touched",
           "no_failing_touched", "lines_changed", "lines_in_verified_share", "verified_broken", "any_verified_broken",
           "catastrophic", "crashed", "improved")


def owned_lines(source: str) -> list[tuple[str, str]]:
    """(owner entity, line) for every non-blank, non-sentinel line; the data shim block is skipped."""
    out, owner, shim = [], PRE, False
    for line in source.splitlines():
        if "r2py:data_shim:begin" in line:
            shim = True
        if shim:
            shim = "r2py:data_shim:end" not in line
            continue
        m = _SENTINEL_ID_RE.match(line)
        if m:
            owner = m.group(1)
        elif line.strip() and not line.lstrip().startswith("#"):
            out.append((owner, line.rstrip()))
    return out


def scope(base: str, cand: str, base_scores: dict | None, cand_scores: dict | None) -> dict | None:
    a = owned_lines(base)
    b = owned_lines(restore_sentinels(base, cand))
    ents = {o for o, _ in a} - {PRE}
    lines, base_changed = collections.Counter(), 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [l for _, l in a], [l for _, l in b],
                                                       autojunk=False).get_opcodes():
        if tag != "equal":
            lines.update(o for o, _ in a[i1:i2])
            lines.update(o for o, _ in b[j1:j2])
            base_changed += i2 - i1
    n = sum(lines.values())
    if not n or not ents:
        return None
    breadth = dict(entities_touched_share=sum(1 for e in ents if lines[e]) / len(ents),
                   base_lines_changed_share=base_changed / len(a),
                   sentinels_lost=float(bool(ents - {o for o, _ in b})))
    verified = {e for e in ents if (base_scores or {}).get(e) == 1.0}
    failing = {e for e in ents if e in (base_scores or {}) and base_scores[e] < 1.0}
    if not verified or not failing:
        return breadth
    tv = [e for e in verified if lines[e]]
    tf = [e for e in failing if lines[e]]
    row = dict(breadth, verified_touched=len(tv), verified_touched_share=len(tv) / len(verified),
               any_verified_touched=float(bool(tv)), failing_touched=len(tf), no_failing_touched=float(not tf),
               lines_changed=n, lines_in_verified_share=sum(lines[e] for e in verified) / n)
    if cand_scores is not None:
        broken = [e for e in verified if cand_scores.get(e, 0.0) < 1.0]
        row.update(verified_broken=len(broken), any_verified_broken=float(bool(broken)))
    return row


def last_run(path: Path) -> list[dict]:
    recs = trajectory.read(path)
    starts = [i for i, r in enumerate(recs) if r["kind"] == "run_start"]
    return recs[starts[-1]:]


def rewrites(recs: list[dict], sources: dict, scores: dict) -> tuple[list[dict], collections.Counter]:
    """One row per rewrite step of a run (keyed by branch and step), with its place in the chain.

    The base is looked up by `best_hash`; the harness re-annotates an accepted candidate that lost sentinels, so its
    hash can be unknown: then the base is the branch's last accepted candidate (sentinels restored from its own base).
    """
    steps, accepted, skipped = collections.OrderedDict(), {}, collections.Counter()
    outcomes, crashes = collections.defaultdict(set), {}
    for r in recs:
        if r["kind"] == "step" and r.get("action") == "rewrite" and r.get("exit_code"):
            crashes.setdefault((r.get("branch"), r["step"]), r.get("crash") or "")
        if r["kind"] == "accepted" and r.get("source"):
            accepted[(r.get("branch"), r["step"])] = r
        if r["kind"] in ("step", "accepted") and r.get("source_hash") and "per_entity" in r:
            scores[r["source_hash"]] = (r["per_entity"], r.get("exit_code"))
        if r["kind"] == "step" and r.get("action") == "rewrite" and r.get("source"):
            steps.setdefault((r.get("branch"), r["step"]), r)
            outcomes[(r.get("branch"), r["step"])].add(r["outcome"])
    rows, seen, last = [], collections.Counter(), {}
    for (branch, step), r in steps.items():
        seen[branch] += 1
        base, base_scores = sources.get(r["best_hash"]), scores.get(r["best_hash"], (None,))[0]
        if base is None and branch in last:
            base, base_scores = last[branch]
        if (branch, step) in accepted and base is not None:
            acc = accepted[(branch, step)]
            last[branch] = (restore_sentinels(base, acc["source"]), acc.get("per_entity"))
        if base is None:
            skipped["base source unknown"] += 1
            continue
        cand = scores.get(r["source_hash"])
        row = scope(base, r["source"], base_scores, cand[0] if cand and cand[1] == 0 else None)
        if row is None:
            skipped["no entity or no change"] += 1
            continue
        if "verified_touched" not in row:
            skipped["breadth only (base scores unknown, or no verified/failing entity)"] += 1
        row.update(catastrophic=float("rewrite:catastrophic" in outcomes[(branch, step)]),
                   improved=float("rewrite:improved" in outcomes[(branch, step)]))
        if cand:
            row["crashed"] = float(cand[1] != 0)
        rows.append(dict(row, first=seen[branch] == 1, base=r["best_hash"], base_src=base, cand_src=r["source"],
                         crash=crashes.get((branch, step)), branch=branch, step=step))
    return rows, skipped


def boot(by_state: dict, seed: int = 0, n: int = 4000) -> tuple[float, float, float]:
    """Mean over states of a per-state value, with a 95% bootstrap interval over states."""
    vals = list(by_state.values())
    rng = random.Random(seed)
    draws = sorted(st.mean(rng.choices(vals, k=len(vals))) for _ in range(n))
    return st.mean(vals), draws[int(0.025 * n)], draws[int(0.975 * n)]


def report(title: str, data: dict, arms: tuple[str, str]) -> None:
    """data: arm -> state -> rows. Per-state means, then mean over states; difference on the common states."""
    print(f"\n{title}")
    for arm in arms:
        print(f"  {arm}: {sum(map(len, data[arm].values()))} rewrites in {len(data[arm])} states")
    print(f"  {'':26s}{arms[0]:>12s}{arms[1]:>12s}   difference [95% over states]")
    for m in METRICS:
        per = {arm: {s: st.mean(r[m] for r in rows if m in r) for s, rows in data[arm].items()
                     if any(m in r for r in rows)} for arm in arms}
        common = sorted(set(per[arms[0]]) & set(per[arms[1]]))
        if not common:
            continue
        d, lo, hi = boot({s: per[arms[0]][s] - per[arms[1]][s] for s in common})
        print(f"  {m:26s}{st.mean(per[arms[0]][s] for s in common):12.3f}{st.mean(per[arms[1]][s] for s in common):12.3f}"
              f"   {d:+.3f} [{lo:+.3f}, {hi:+.3f}]  ({len(common)} states)")


def index(dirs) -> tuple[dict, dict]:
    """hash -> source and hash -> (per-entity scores, exit code) from every record of the given run dirs."""
    sources, scores = {}, {}
    for d in dirs:
        for f in sorted((ROOT / d / "trajectories").glob("*.jsonl")):
            for r in trajectory.read(f):
                if r.get("source") and r.get("source_hash"):
                    sources.setdefault(r["source_hash"], r["source"])
                    if "per_entity" in r:
                        scores.setdefault(r["source_hash"], (r["per_entity"], r.get("exit_code")))
    return sources, scores


def screen() -> None:
    import stall2_continue as s2
    arms = ("stall2_ps_glmflash", "stall2_ps_dsflash")
    sources, scores = index(("work/replay_default_e8", "work/replay_default_e8_s1"))
    data = {arm: collections.defaultdict(list) for arm in arms}
    first = {arm: {} for arm in arms}
    skipped = collections.Counter()
    for (script, run, b), c in sorted(s2.chains().items()):
        if not c["reached"]:
            continue
        sources[c["hash"]] = c["source"]
        for arm in arms:
            f = ROOT / "work/model_screen/trajectories" / f"{Path(script).stem}.{arm}.{run}.{b}.jsonl"
            if not f.exists():
                skipped[f"{arm}: no trajectory"] += 1
                continue
            rows, sk = rewrites(last_run(f), dict(sources), scores)
            skipped.update({f"{arm}: {k}": v for k, v in sk.items()})
            data[arm][script] += rows
            if rows and rows[0]["first"] and rows[0]["base"] == c["hash"]:
                first[arm][(script, run, b)] = rows[0]
    print("skipped:", dict(skipped))
    report("Model screen, all rewrites (GLM 5.3 Flash vs DeepSeek V4.1 Flash)", data, arms)
    pairs = sorted(set(first[arms[0]]) & set(first[arms[1]]))
    paired = {arm: collections.defaultdict(list) for arm in arms}
    for k in pairs:
        for arm in arms:
            paired[arm][k[0]].append(first[arm][k])
    report(f"Model screen, first rewrite of each chain, same base program ({len(pairs)} chains)", paired, arms)
    return data, paired


def full() -> None:
    import replay
    runs = {"glm53": ("work/ceiling_glm53", "default_2026_11_01_glm53_r8k"),
            "dsflash": ("work/dsflash_default", "default_2026_11_01_dsflash")}
    starts = {trajectory.source_hash(s["source"]): s["source"] for s in replay.training_states().values()}
    data = {arm: collections.defaultdict(list) for arm in runs}
    skipped = collections.Counter()
    for arm, (d, _policy) in runs.items():
        _, scores = index((d,))
        for f in sorted((ROOT / d / "trajectories").glob("*.jsonl")):
            recs = last_run(f)
            rows, sk = rewrites(recs, dict(starts), scores)
            skipped.update({f"{arm}: {k}": v for k, v in sk.items()})
            data[arm][recs[0]["script"]] += rows
    print("skipped:", dict(skipped))
    report("Full default runs, all rewrites (GLM 5.3 vs DeepSeek V4.1 Flash)", data, tuple(runs))
    return data


if __name__ == "__main__":
    {"screen": screen, "full": full}[sys.argv[1]]()
