"""Entities outside the frozen start's sentinels (2026-11-13): for each state whose final loses on such an entity,
verify the default's final program (raw, as logged) with a fresh harness twice: reference = frozen start (as the
loop scores it) and reference = the program itself (its own sentinels trusted). No agent calls.

    python work/patience_dsflash/trace_unmapped.py
"""
import json, pickle, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr, replay
from prompt_load import _tools
from r2py.harness import tools as T
from r2py.harness.objective import entity_score
from r2py.stage2.sentinel_mapper import ranges_from_sentinels

RUN = ROOT / "work/dsflash_default"
states = replay.training_states()
for stem in ["farver__rd_example__convert_colour_Rd", "shape__rd_example__Arrows_Rd", "lubridate__rd_example__period_Rd",
             "gtable__rd_example__gtable_add_cols_Rd", "purrr__rd_example__invoke_Rd"]:
    start = states[stem + ".R"]["source"]
    recs = [json.loads(l) for l in open(RUN / "trajectories" / f"{stem}.default_2026_11_01_dsflash.0.jsonl", encoding="utf-8")]
    src = hr._final_program(recs) or start
    sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
    s0, s1 = set(ranges_from_sentinels(start)), set(ranges_from_sentinels(src))
    print(f"## {stem}: sentinels added by the program {sorted(s1 - s0)}, dropped {sorted(s0 - s1)}", flush=True)
    res = {}
    for name, ref in (("start", start), ("self", src)):
        b = dict(T.cache_stats); t = _tools(sm, stem); t.note_reference(ref); rep = t.verify(src)
        path = {k: T.cache_stats[k] - b.get(k, 0) for k in T.cache_stats if T.cache_stats[k] != b.get(k, 0)}
        res[name] = ({e: round(entity_score(es), 3) for e, es in rep.by_entity.items() if es.active_dims}, rep.aggregate, path)
    diff = {e: (res["start"][0].get(e), res["self"][0].get(e)) for e in set(res["start"][0]) | set(res["self"][0])
            if res["start"][0].get(e) != res["self"][0].get(e)}
    print(f"   ref start {res['start'][1]:.4f} {res['start'][2]}  ref self {res['self'][1]:.4f} {res['self'][2]}  differ {diff}", flush=True)
