"""Did the model use what it was shown? (Behaviour, not score.)

Three knowledge-injection mechanisms are null (pattern library, lesson store, oracle library), which
raises the prior question: does a 31B model's rewrite change at all when a verified example sits in
its prompt? The oracle replay already contains the controlled comparison -- identical frozen states,
the same agent loop, the example present in one arm and absent in the other -- so imitation can be
measured without new runs.

For every entity that had an example in the oracle arm, this takes the identifiers that are
distinctive to the example (present in its Python, absent from the entity's R source, not Python
keywords or builtins) and asks what share of them appear in the entity's final Python. The same
measurement in the arm that never saw the example is the chance rate: the model reaches for `np.` and
`pd.` on its own. The difference between the arms is imitation.

    python scripts/imitation_probe.py
"""
from __future__ import annotations

import json
import keyword
import pickle
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TRAJ = ROOT / "work" / "replay_oracle" / "trajectories"
LIBS = ROOT / "work" / "oracle" / "libs"
MAPS = ROOT / "work" / "replay" / "script_maps"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
COMMON = set(keyword.kwlist) | set(dir(__builtins__)) | {
    "np", "pd", "self", "x", "i", "n", "r", "df", "s", "f", "e", "result", "out", "data", "value",
    "import", "numpy", "pandas", "None", "True", "False",
}


def best_source(path: Path) -> tuple[str, dict] | None:
    """The run's winning source and its per-entity scores."""
    from r2py.harness import trajectory

    best, score = None, -1.0
    for rec in trajectory.read(path):
        if rec["kind"] in ("step", "accepted") and rec.get("source") and float(rec.get("aggregate", -1)) > score:
            best, score = (rec["source"], rec.get("per_entity") or {}), float(rec["aggregate"])
    return best


def examples_for(stem: str) -> dict[str, list[tuple[str, str]]]:
    """pattern id -> the (R, Python) snippet pairs of its examples, as the prompt shows them."""
    from r2py.library.pattern import from_markdown

    out: dict[str, list[tuple[str, str]]] = {}
    for f in (LIBS / stem / "patterns").glob("*.md"):
        pat = from_markdown(f.read_text(encoding="utf-8"))
        out[pat.id] = [(ex.r_snippet, ex.py_snippet) for ex in pat.translation_examples]
    return out


def relatedness(entity_r: str, example_r: str) -> float:
    """Jaccard overlap of the identifiers of two R statements: both sides are R, so this measures
    whether the example is the same kind of statement or merely shares a function name."""
    a = {t for t in IDENT.findall(entity_r.lower()) if len(t) > 2}
    b = {t for t in IDENT.findall(example_r.lower()) if len(t) > 2}
    return len(a & b) / len(a | b) if a and b else 0.0


def entity_keys_and_r(stem: str) -> dict[str, tuple[str, set[str], str]]:
    """entity id -> (its own pattern key or "", the keys of the base-R calls inside it, its R source)."""
    from r2py.library.pattern import correction_functions, pattern_id, pattern_key

    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    src = (getattr(sm, "source", "") or "").splitlines()
    out = {}
    for eid, e in sm.entities.items():
        k = pattern_key(e)
        own = pattern_id(*k) if k else ""
        calls = {pattern_id(*q.split("::")) for q in correction_functions(e.base_r_calls or [])} - {own}
        span = getattr(e, "source_span", None)
        start = getattr(span, "start_line", 0) if span else 0
        r_text = "\n".join(src[start:min(len(src), getattr(span, "end_line", start) + 1)]) if span else ""
        out[eid] = (own, calls, r_text)
    return out


def distinctive(py_snippets: list[str], r_text: str) -> set[str]:
    r_tokens = set(IDENT.findall(r_text.lower()))
    toks: set[str] = set()
    for s in py_snippets:
        toks |= set(IDENT.findall(s))
    return {t for t in toks if len(t) > 2 and t not in COMMON and t.lower() not in r_tokens}


def main() -> int:
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels

    per: dict = defaultdict(dict)                      # (stem, eid) -> policy -> [recall, ...]
    scores: dict = defaultdict(dict)
    kind: dict = {}                                    # (stem, eid) -> ("own key"|"base call only", relatedness)
    for f in sorted(TRAJ.glob("*.jsonl")):
        stem, policy, _sample = f.stem.rsplit(".", 2)
        got = best_source(f)
        if not got:
            continue
        source, per_entity = got
        ex = examples_for(stem)
        info = entity_keys_and_r(stem)
        ranges = ranges_from_sentinels(source)
        lines = source.splitlines()
        for eid, (own, calls, r_text) in info.items():
            # the examples the prompt shows for this entity, with where each one came from
            pool = [(own, r, p) for r, p in ex.get(own, [])] + \
                   [(k, r, p) for k in sorted(calls & set(ex)) for r, p in ex[k]]
            if not pool or eid not in ranges:
                continue
            want = distinctive([p for _, _, p in pool], r_text)
            if not want:
                continue
            got_text = "\n".join(l for a, b in ranges[eid] for l in lines[a:b + 1])
            present = set(IDENT.findall(got_text))
            per[(stem, eid)].setdefault(policy, []).append(len(want & present) / len(want))
            scores[(stem, eid)].setdefault(policy, []).append(float(per_entity.get(eid, 0.0)))
            kind[(stem, eid)] = ("own key" if own and ex.get(own) else "base call only",
                                 max(relatedness(r_text, r) for _, r, _ in pool))

    paired = [(k, v) for k, v in per.items() if len(v) == 2]
    print(f"{len(paired)} entities had an example and a sentinel in both arms "
          f"(of {len(per)} with an example)")
    if not paired:
        return 0

    def report(label: str, sel: list) -> None:
        if not sel:
            print(f"   {label:<38} none")
            return
        shown = [st.mean(v["rewrite_w3_oracle"]) for _, v in sel]
        blind = [st.mean(v["rewrite_w3"]) for _, v in sel]
        print(f"   {label:<38} n={len(sel):>3}   shown {st.mean(shown):>5.1%}   "
              f"not shown {st.mean(blind):>5.1%}   difference {st.mean(shown) - st.mean(blind):>+5.1%}")

    print("\nshare of the example's distinctive identifiers that appear in the entity's final Python:")
    report("all entities", paired)
    for label, test in (("example for the entity's own function", lambda k: kind[k][0] == "own key"),
                        ("example only for a base-R call inside", lambda k: kind[k][0] != "own key"),
                        ("R statements related (Jaccard >= 0.3)", lambda k: kind[k][1] >= 0.3),
                        ("R statements unrelated (< 0.3)", lambda k: kind[k][1] < 0.3),
                        ("own function AND related", lambda k: kind[k][0] == "own key" and kind[k][1] >= 0.3)):
        report(label, [(k, v) for k, v in paired if test(k)])

    rel = [kind[k][1] for k, _ in paired]
    own = sum(1 for k, _ in paired if kind[k][0] == "own key")
    print(f"\nretrieval quality: {own}/{len(paired)} entities got an example of their own function; "
          f"median R-statement relatedness {st.median(rel):.2f}, "
          f"{sum(1 for r in rel if r >= 0.3)}/{len(rel)} at or above 0.3")
    print("\nentities where the example was clearly adopted (recall >= 0.5 when shown, < 0.5 when not):")
    for (stem, eid), v in paired:
        s, b = st.mean(v["rewrite_w3_oracle"]), st.mean(v["rewrite_w3"])
        if s >= 0.5 > b:
            sc = scores[(stem, eid)]
            print(f"   {stem[:40]:<42}{eid[:22]:<24} recall {b:.0%} -> {s:.0%}   "
                  f"score {st.mean(sc['rewrite_w3']):.2f} -> {st.mean(sc['rewrite_w3_oracle']):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
