"""The reference program decides which entities are attributed (2026-11-13). Verifies one chain-best program
with a fresh harness per reference: the frozen start, the program itself; prints per-entity scores and the path
verify took (sentinels read, restored, or model-mapped).

    python work/patience_dsflash/trace_reference.py <script.R> <branch>
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import replay, patience_continue as p
from prompt_load import _tools
from r2py.harness import tools as T
from r2py.harness.objective import entity_score
from r2py.stage2.sentinel_mapper import ranges_from_sentinels

script, b = sys.argv[1], int(sys.argv[2])
stem = Path(script).stem
sm = replay._script_map(script, None, replay.TRAIN_MAPS)
src = p.chains()[(script, b)]["source"]
start = replay.training_states()[script]["source"]
print("script map entities:", [e.id if hasattr(e, "id") else e for e in getattr(sm, "entities", [])][:30])
print("sentinels: start", sorted(ranges_from_sentinels(start)), " program", sorted(ranges_from_sentinels(src)))
for ref_name, ref in (("frozen start", start), ("program itself", src)):
    h = _tools(sm, stem); h.note_reference(ref)
    before = dict(T.cache_stats) if hasattr(T, "cache_stats") else {}
    rep = h.verify(src)
    after = dict(T.cache_stats) if hasattr(T, "cache_stats") else {}
    path = {k: after[k] - before.get(k, 0) for k in after if after[k] != before.get(k, 0)}
    ents = {e: round(entity_score(es), 3) for e, es in rep.by_entity.items() if es.active_dims}
    print(f"== reference = {ref_name}: aggregate {rep.aggregate:.4f}  path {path}\n   {ents}", flush=True)
