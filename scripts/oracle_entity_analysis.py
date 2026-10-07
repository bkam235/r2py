"""Entity-level reading of the oracle-library replay (`work/replay_oracle/`).

The planned comparison is script-level and is reported by `replay.py` itself. It is blunt: a script
mean averages over entities the oracle library said nothing about, and state-level noise is large
(the no-pattern control states swing by up to 0.33 with identical arms). This script asks the
sharper question the same runs already answer -- did the entities that actually *got* a verified
example score better? -- by reading the `per_entity` scores the trajectory log records for every
accepted step. No re-verification and no model calls.

Diagnostic, computed after seeing the script-level result.

    python scripts/oracle_entity_analysis.py
"""
from __future__ import annotations

import json
import pickle
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TRAJ = ROOT / "work" / "replay_oracle" / "trajectories"
LIBS = ROOT / "work" / "oracle" / "libs"
MAPS = ROOT / "work" / "replay" / "script_maps"
BOILERPLATE = "suppressPackageStartupMessages"


def final_per_entity(path: Path) -> dict[str, float] | None:
    """The per-entity scores of the run's best accepted source (the branch that won)."""
    from r2py.harness import trajectory

    best, best_score = None, -1.0
    for r in trajectory.read(path):
        if r["kind"] in ("step", "accepted") and r.get("per_entity") is not None:
            if float(r.get("aggregate", -1)) > best_score:
                best, best_score = r["per_entity"], float(r["aggregate"])
    return best


def informed_keys(stem: str) -> set[str]:
    return {p.stem for p in (LIBS / stem / "patterns").glob("*.md")}


def entity_keys(stem: str) -> dict[str, set[str]]:
    """entity id -> the pattern ids that would inform it (its own key and its base-R calls)."""
    from r2py.library.pattern import correction_functions, pattern_id, pattern_key

    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    out = {}
    for eid, e in sm.entities.items():
        k = pattern_key(e)
        keys = {pattern_id(*k)} if k else set()
        keys |= {pattern_id(*q.split("::")) for q in correction_functions(e.base_r_calls or [])}
        out[eid] = keys
    return out


def main() -> int:
    runs: dict = defaultdict(dict)                     # (stem, eid) -> policy -> [scores]
    for f in sorted(TRAJ.glob("*.jsonl")):
        stem, policy, sample = f.stem.rsplit(".", 2)
        per = final_per_entity(f)
        if not per:
            continue
        for eid, score in per.items():
            if eid == BOILERPLATE:
                continue
            runs[(stem, eid)].setdefault(policy, []).append(float(score))

    rows = []
    for (stem, eid), by_policy in runs.items():
        if len(by_policy) < 2:
            continue
        keys = entity_keys(stem).get(eid, set())
        rows.append({"stem": stem, "eid": eid,
                     "informed": bool(keys & informed_keys(stem)),
                     "w3": st.mean(by_policy["rewrite_w3"]),
                     "oracle": st.mean(by_policy["rewrite_w3_oracle"])})

    def block(label: str, sel) -> str:
        sub = [r for r in sel if True]
        if not sub:
            return f"{label}: none"
        d = [r["oracle"] - r["w3"] for r in sub]
        lost = sum(1 - r["w3"] for r in sub)
        rec = sum(r["oracle"] - r["w3"] for r in sub)
        # cluster bootstrap over scripts: entities of one script are not independent
        by_script = defaultdict(list)
        for r in sub:
            by_script[r["stem"]].append(r["oracle"] - r["w3"])
        scripts = list(by_script)
        rng = random.Random(7)
        boot = []
        for _ in range(2000):
            pick = [x for s in (rng.choice(scripts) for _ in scripts) for x in by_script[s]]
            boot.append(st.mean(pick))
        boot.sort()
        lo, hi = boot[int(.025 * len(boot))], boot[int(.975 * len(boot))]
        return (f"{label:<34} entities {len(sub):>4}  mean {st.mean(r['w3'] for r in sub):.3f} -> "
                f"{st.mean(r['oracle'] for r in sub):.3f}   diff {st.mean(d):+.3f} "
                f"[{lo:+.3f}, {hi:+.3f}]   lost {lost:.1f}, recovered {rec:+.1f} "
                f"({100 * rec / lost if lost else 0:+.0f}%)")

    print(f"{len(rows)} entities paired across both arms, from {len({r['stem'] for r in rows})} states")
    print(block("entities with an example", [r for r in rows if r["informed"]]))
    print(block("entities without one", [r for r in rows if not r["informed"]]))
    print(block("all entities", rows))
    failing = [r for r in rows if r["w3"] < 0.999]
    print(block("failing + example", [r for r in failing if r["informed"]]))
    print(block("failing, no example", [r for r in failing if not r["informed"]]))
    out = ROOT / "work" / "replay_oracle" / "entity_analysis.json"
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
