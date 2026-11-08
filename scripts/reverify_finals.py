"""Re-verify the final programs of one replay sample under the current scorer (no model calls), 2026-11-08.

Per program: aggregate, exit code, every entity's score and dimensions, and the feedback items. Used for the gap
table under epoch 9 and as the baseline of the GLM ceiling run (`glm53-ceiling`).

    python scripts/reverify_finals.py <run_dir> <policy> <out.jsonl> [sample]
"""
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score

MAPS, SRC = hr.MAPS, hr.SOURCES
rd, pol, out = ROOT / sys.argv[1], sys.argv[2], open(sys.argv[3], "w", encoding="utf-8")
sample = sys.argv[4] if len(sys.argv) > 4 else "0"
stems = sorted({Path(json.loads(l)["script"]).stem for l in open(rd / "results.jsonl", encoding="utf-8")})
for stem in stems:
    start = (SRC / f"{stem}.py").read_text(encoding="utf-8")
    sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
    tf = rd / "trajectories" / f"{stem}.{pol}.{sample}.jsonl"
    recs = [json.loads(l) for l in open(tf, encoding="utf-8")] if tf.exists() else []
    src = hr._final_program(recs) or start
    try:
        t = _tools(sm, stem); t.note_reference(start)
        rep = t.verify(src)
    except Exception as ex:
        out.write(json.dumps(dict(stem=stem, error=str(ex)[:200])) + "\n"); out.flush(); continue
    ents = {}
    for e, es in rep.by_entity.items():
        if not es.active_dims:
            continue
        ents[e] = dict(score=round(entity_score(es), 3), ran=es.executed_ok,
                       dims={d: round(getattr(es, d), 3) for d in es.active_dims})
    fb = [dict(e=f.entity_id, cls=str(f.effect_class), msg=f.message[:300], score=round(f.score, 3))
          for f in (getattr(rep, "feedback", None) or [])]
    out.write(json.dumps(dict(stem=stem, aggregate=round(rep.aggregate, 4), exit=rep.py_exit_code,
                              ents=ents, feedback=fb)) + "\n"); out.flush()
    print(stem, round(rep.aggregate, 3), flush=True)
