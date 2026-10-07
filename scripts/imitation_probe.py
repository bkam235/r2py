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


def examples_for(stem: str) -> dict[str, list[str]]:
    """pattern id -> the Python snippets of its examples, as the prompt shows them."""
    from r2py.library.pattern import from_markdown

    out: dict[str, list[str]] = {}
    for f in (LIBS / stem / "patterns").glob("*.md"):
        pat = from_markdown(f.read_text(encoding="utf-8"))
        out[pat.id] = [ex.py_snippet for ex in pat.translation_examples]
    return out


def entity_keys_and_r(stem: str) -> dict[str, tuple[set[str], str]]:
    from r2py.library.pattern import correction_functions, pattern_id, pattern_key

    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    src = (getattr(sm, "source", "") or "").splitlines()
    out = {}
    for eid, e in sm.entities.items():
        k = pattern_key(e)
        keys = {pattern_id(*k)} if k else set()
        keys |= {pattern_id(*q.split("::")) for q in correction_functions(e.base_r_calls or [])}
        span = getattr(e, "source_span", None)
        start = getattr(span, "start_line", 0) if span else 0
        r_text = "\n".join(src[start:min(len(src), getattr(span, "end_line", start) + 1)]) if span else ""
        out[eid] = (keys, r_text)
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
        for eid, (keys, r_text) in info.items():
            snippets = [s for k in keys & set(ex) for s in ex[k]]
            if not snippets or eid not in ranges:
                continue
            want = distinctive(snippets, r_text)
            if not want:
                continue
            got_text = "\n".join(l for a, b in ranges[eid] for l in lines[a:b + 1])
            present = set(IDENT.findall(got_text))
            per[(stem, eid)].setdefault(policy, []).append(len(want & present) / len(want))
            scores[(stem, eid)].setdefault(policy, []).append(float(per_entity.get(eid, 0.0)))

    paired = [(k, v) for k, v in per.items() if len(v) == 2]
    print(f"{len(paired)} entities had an example and a sentinel in both arms "
          f"(of {len(per)} with an example)")
    if not paired:
        return 0
    shown = [st.mean(v["rewrite_w3_oracle"]) for _, v in paired]
    blind = [st.mean(v["rewrite_w3"]) for _, v in paired]
    print(f"distinctive identifiers of the example that appear in the entity's final Python:")
    print(f"   example in the prompt : {st.mean(shown):.1%}")
    print(f"   example never shown   : {st.mean(blind):.1%}   (chance rate)")
    print(f"   difference            : {st.mean(shown) - st.mean(blind):+.1%}")
    gained = sum(1 for s, b in zip(shown, blind) if s > b + 0.05)
    lost = sum(1 for s, b in zip(shown, blind) if b > s + 0.05)
    print(f"   entities more like the example: {gained}, less like it: {lost}, "
          f"unchanged: {len(paired) - gained - lost}")
    print()
    print("entities where the example was clearly adopted (recall >= 0.5 when shown, < 0.5 when not):")
    for (stem, eid), v in paired:
        s, b = st.mean(v["rewrite_w3_oracle"]), st.mean(v["rewrite_w3"])
        if s >= 0.5 > b:
            sc = scores[(stem, eid)]
            print(f"   {stem[:40]:<42}{eid[:22]:<24} recall {b:.0%} -> {s:.0%}   "
                  f"score {st.mean(sc['rewrite_w3']):.2f} -> {st.mean(sc['rewrite_w3_oracle']):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
