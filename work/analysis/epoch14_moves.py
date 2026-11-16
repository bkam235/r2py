"""Epoch-14 check: what R holds and what the Python capture now gives for the entities that moved (purrr attr_getter x,
openssl certificates cert_data, recipes step_kpca kpca_estimates)."""
import json, pickle, sys
from pathlib import Path
sys.path[:0] = ['.', 'scripts']
from dotenv import load_dotenv; load_dotenv('.env', override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
for prog, stem, ents in [('final_default_purrr__rd_example__attr_getter_Rd', 'purrr__rd_example__attr_getter_Rd', ['x']),
                         ('start_openssl__rd_example__certificates_Rd', 'openssl__rd_example__certificates_Rd', ['cert_data']),
                         ('final_default_recipes__rd_example__step_kpca_Rd', 'recipes__rd_example__step_kpca_Rd', ['kpca_estimates', 'ggplot'])]:
    src = Path(f'work/scoring/programs/{prog}.py').read_text(encoding='utf-8')
    sm = pickle.loads((hr.MAPS / f'{stem}.pkl').read_bytes())
    t = _tools(sm, stem); t.note_reference(src)
    rep = t.verify(src)
    print('=====', prog, round(rep.aggregate, 4))
    for f in getattr(rep, 'feedback', None) or []:
        if f.entity_id in ents:
            print(f'  [{f.entity_id}] {f.score:.3f} {f.message[:700]}')
