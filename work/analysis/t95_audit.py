"""threshold-095: re-verify every chain's final under the open epoch (offline) and dump the best t95 finals for audit."""
import json, pickle, sys, glob, collections
from pathlib import Path
ROOT = Path(r"C:\Users\bened\Desktop\r2py_v0.3"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
RD = ROOT / "work/threshold95"; OUT = RD / "finals_reverified.jsonl"; DUMP = RD / "audit"; DUMP.mkdir(exist_ok=True)
rows = [json.loads(l) for l in open(RD / "results.jsonl", encoding="utf-8")]
with open(OUT, "w", encoding="utf-8") as out:
    for r in rows:
        stem = Path(r["script"]).stem
        start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
        sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
        tf = RD / "trajectories" / f"{stem}.{r['policy']}.{r['sample']}.jsonl"
        src = hr._final_program([json.loads(l) for l in open(tf, encoding="utf-8")])
        if src is None:
            agg = None
        else:
            t = _tools(sm, stem); t.note_reference(start); rep = t.verify(src); agg = round(rep.aggregate, 4)
            low = {e: round(entity_score(es), 3) for e, es in rep.by_entity.items() if es.active_dims and entity_score(es) < 0.999}
            if r["policy"] == "t95_cont" and agg >= 0.95:
                (DUMP / f"{stem}.{r['sample']}.py").write_text(src, encoding="utf-8")
        out.write(json.dumps(dict(script=r["script"], policy=r["policy"], sample=r["sample"], inloop=r["final_score"],
                                  start=r["start_score"], reverified=agg)) + "\n"); out.flush()
        print(f"{stem[:40]:40s} {r['policy']:9s} {r['sample']} in-loop {r['final_score']:.3f} re-verified {agg}", flush=True)
