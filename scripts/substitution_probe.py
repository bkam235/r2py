"""If the harness pastes a verified example straight into its entity, does the score rise?

The imitation probe showed the model does not read the examples it is shown
(`scripts/imitation_probe.py`: 6.3% of an example's distinctive identifiers appear in the output when
it is in the prompt, 6.6% when it is not). That leaves two possibilities, and they lead opposite ways:
the examples are useless, or the content is fine and only the behaviour is broken. This separates them
without a model in the loop -- each example replaces its entity's Python in the frozen start state and
the result is verified.

Substituted verbatim, an example also carries its original script's variable names, so a drop here is
not proof that the content is worthless: the failure mode matters, and the outcomes are broken down by
whether the entity still ran.

    python scripts/substitution_probe.py
"""
from __future__ import annotations

import json
import pickle
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

ARMS = [f"work/smoke/{a}" for a in ("20261001_112951", "20261001_140509", "20261001_165951")]
LIBS = ROOT / "work" / "oracle" / "libs"
MAPS = ROOT / "work" / "replay" / "script_maps"
OUT = ROOT / "work" / "replay_oracle" / "substitution.jsonl"


def reindent(snippet: str, indent: str) -> str:
    lines = [l for l in snippet.splitlines() if l.strip()]
    if not lines:
        return ""
    base = min(len(l) - len(l.lstrip()) for l in lines)
    return "\n".join(indent + l[base:] if l.strip() else l for l in snippet.splitlines())


def substitute(source: str, ranges: list[tuple[int, int]], snippet: str) -> str:
    """Replace the entity's lines with the example, keeping its sentinel comments so that
    attribution is still read off them and not resampled by a model."""
    lines = source.splitlines()
    drop = {i for a, b in ranges for i in range(a, b + 1)}
    first = min(drop)
    body = [lines[i] for i in sorted(drop) if "r2py:entity:" in lines[i]]
    code = next((lines[i] for i in sorted(drop) if lines[i].strip() and "r2py:entity:" not in lines[i]), "")
    indent = code[:len(code) - len(code.lstrip())]
    body += reindent(snippet, indent).splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        if i == first:
            out += body
        if i not in drop:
            out.append(line)
    return "\n".join(out) + "\n"


def main() -> int:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import replay
    from r2py import heldout as ho
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.library.pattern import correction_functions, from_markdown, pattern_id, pattern_key
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels

    manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
    cfg = manifest["protocol"]["translate"]
    states = replay.best_states(ARMS, 0.9)
    empty = PatternLibrary(ROOT / "work/dev_run/checkpoints/empty")
    rows = []
    outcomes: Counter = Counter()
    for name, state in sorted(states.items()):
        stem = Path(name).stem
        pats = {}
        for f in (LIBS / stem / "patterns").glob("*.md"):
            pat = from_markdown(f.read_text(encoding="utf-8"))
            pats[pat.id] = [ex.py_snippet for ex in pat.translation_examples]
        if not pats:
            continue
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        tools = HarnessTools(sm, empty, model=cfg["model"], data_compare=cfg["data_compare"],
                             timeout_s=cfg["timeout_s"], sidecar_filename=f"{stem}.r2py_data.json")
        tools.note_reference(state["source"])
        base = tools.verify(state["source"])
        ranges = ranges_from_sentinels(state["source"])
        for eid, entity in sm.entities.items():
            k = pattern_key(entity)
            keys = ({pattern_id(*k)} if k else set()) | {
                pattern_id(*q.split("::")) for q in correction_functions(entity.base_r_calls or [])}
            snippets = [s for key in keys & set(pats) for s in pats[key]]
            if not snippets or eid not in ranges:
                continue
            before = base.by_entity.get(eid)
            before_score = ho.entity_score(before) if before else None
            try:
                new_source = substitute(state["source"], ranges[eid], snippets[0])
                rep = tools.verify(new_source)
            except Exception as exc:
                rows.append({"script": stem, "entity": eid, "error": f"{type(exc).__name__}: {exc}"[:200]})
                outcomes["harness error"] += 1
                continue
            after = rep.by_entity.get(eid)
            after_score = ho.entity_score(after) if after else None
            row = {"script": stem, "entity": eid, "before": before_score, "after": after_score,
                   "aggregate_before": round(base.aggregate, 4), "aggregate_after": round(rep.aggregate, 4),
                   "exit_before": base.py_exit_code, "exit_after": rep.py_exit_code,
                   "ran_before": bool(before and before.executed_ok), "ran_after": bool(after and after.executed_ok)}
            rows.append(row)
            if after_score is None or before_score is None:
                outcomes["not scored"] += 1
            elif after_score > before_score + 0.01:
                outcomes["entity better"] += 1
            elif after_score < before_score - 0.01:
                outcomes["entity worse" + (" (stopped running)" if row["ran_before"] and not row["ran_after"] else "")] += 1
            else:
                outcomes["entity unchanged"] += 1
            print(f"  {stem[:34]:<36}{eid[:20]:<22} {before_score} -> {after_score}   "
                  f"aggregate {base.aggregate:.3f} -> {rep.aggregate:.3f}", flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    scored = [r for r in rows if r.get("before") is not None and r.get("after") is not None]
    print(f"\n{len(rows)} substitutions over {len({r['script'] for r in rows})} states")
    for k, v in outcomes.most_common():
        print(f"   {k:<34}{v:>4}")
    if scored:
        import statistics as st
        print(f"   mean entity score {st.mean(r['before'] for r in scored):.3f} -> "
              f"{st.mean(r['after'] for r in scored):.3f}")
        print(f"   mean script aggregate {st.mean(r['aggregate_before'] for r in scored):.3f} -> "
              f"{st.mean(r['aggregate_after'] for r in scored):.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
