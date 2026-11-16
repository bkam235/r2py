"""threshold-095 xml2 b1 (0.953 under epoch 13, no forged marker): its entity scores beside the default final's."""
import json, pickle, sys
from pathlib import Path
sys.path[:0] = ['.', 'scripts']
from dotenv import load_dotenv; load_dotenv('.env', override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
stem = 'xml2__rd_example__xml_attr_Rd'
sm = pickle.loads((hr.MAPS / f'{stem}.pkl').read_bytes())
start = (hr.SOURCES / f'{stem}.py').read_text(encoding='utf-8')
d = {r['stem']: r for r in map(json.loads, open('work/dsflash_default/finals_epoch13.jsonl', encoding='utf-8'))}[stem]
t = _tools(sm, stem); t.note_reference(start)
rep = t.verify(Path(f'work/threshold95/audit/{stem}.b1.py').read_text(encoding='utf-8'))
print('aggregate default', d['aggregate'], 'b1', round(rep.aggregate, 4))
for e, es in rep.by_entity.items():
    if not es.active_dims: continue
    a, b = d['ents'].get(e, {}).get('score'), round(entity_score(es), 3)
    if a != b: print(f'  {e:20s} default {a}  b1 {b}  dims {dict((k, round(getattr(es, k), 3)) for k in es.active_dims)}')
