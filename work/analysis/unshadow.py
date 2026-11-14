import json,pickle,sys,glob,re
from pathlib import Path
ROOT=Path(r"C:\Users\bened\Desktop\r2py_v0.3"); sys.path[:0]=[str(ROOT),str(ROOT/"scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT/".env",override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
for stem in sys.argv[1:]:
    start=(hr.SOURCES/f"{stem}.py").read_text(encoding="utf-8")
    sm=pickle.loads((hr.MAPS/f"{stem}.pkl").read_bytes())
    f=glob.glob(str(ROOT/f"work/dsflash_default/trajectories/{stem}.*"))[0]
    src=hr._final_program([json.loads(l) for l in open(f,encoding='utf-8')]) or start
    # rename the module binding only: 'from shiny import ..., ui, ...' -> import shiny.ui as _ui; module uses ui.X( -> _ui.X(
    v=re.sub(r'(from shiny import [^\n]*?)\bui\b,?\s*', r'\1', src)
    v=v.replace("from shiny import ", "import shiny.ui as _ui\nfrom shiny import ",1)
    v=re.sub(r'(?<![\w.])ui\.(\w+)', r'_ui.\1', v)
    v=re.sub(r'from shiny import\s*\n','\n',v)
    for name,s in [("final",src),("unshadowed",v)]:
        t=_tools(sm,stem); t.note_reference(start); rep=t.verify(s)
        u=rep.by_entity.get('ui')
        print(stem[:40],name,round(rep.aggregate,3),"exit",rep.py_exit_code,"ui",u and round(entity_score(u),2), u and {d:round(getattr(u,d),2) for d in u.active_dims})
        if rep.py_exit_code: print(rep.py_stderr[-300:] if hasattr(rep,'py_stderr') else '')
