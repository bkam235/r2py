import json,pickle,sys,glob
from pathlib import Path
ROOT=Path(r"C:\Users\bened\Desktop\r2py_v0.3"); sys.path[:0]=[str(ROOT),str(ROOT/"scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT/".env",override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
stem="shiny__rd_example__updateRadioButtons_Rd"
start=(hr.SOURCES/f"{stem}.py").read_text(encoding="utf-8")
sm=pickle.loads((hr.MAPS/f"{stem}.pkl").read_bytes())
f=glob.glob(str(ROOT/f"work/dsflash_default/trajectories/{stem}.*"))[0]
low=[json.loads(l) for l in open(f,encoding='utf-8')]
low=[r for r in low if r['kind']=='step' and r['outcome'].startswith('rewrite')][0]['source']
f2=glob.glob(str(ROOT/f"work/feedback_e10/trajectories/{stem}.*"))[0]
hi=[json.loads(l) for l in open(f2,encoding='utf-8') if '"accepted"' in l][-1]['source']
# variant A: low program with shiny.ui-style rename only (ui module alias), to isolate the shadowing
varA=low.replace("from shiny import App, ui, reactive","from shiny import App, reactive\nimport shiny.ui as _ui").replace("ui = ui.page_fluid","ui = _ui.page_fluid")
import re
varA=re.sub(r"(?<![\w.])ui\.(p|input_radio_buttons|update_radio_buttons)\(", r"_ui.\1(", varA)
for name,src in [("start",start),("low",low),("hi",hi),("low_unshadowed",varA)]:
    t=_tools(sm,stem); t.note_reference(start); rep=t.verify(src)
    print("==",name,round(rep.aggregate,3),"exit",rep.py_exit_code)
    for e,es in rep.by_entity.items():
        if es.active_dims: print("   ",e,round(entity_score(es),2),{d:round(getattr(es,d),2) for d in es.active_dims})
    for fb in (rep.feedback or []): print("   fb",fb.entity_id,fb.message[:220])
