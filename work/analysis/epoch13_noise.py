"""Re-score the two reference programs without a forged marker that moved in the epoch-13 check, 4 times each."""
import pickle, sys
from pathlib import Path
sys.path[:0] = ['.', 'scripts']
from dotenv import load_dotenv; load_dotenv('.env', override=True)
import health_report as hr
from prompt_load import _tools
for prog, stem in [('final_default_openssl__rd_example__ec_dh_Rd', 'openssl__rd_example__ec_dh_Rd'),
                   ('final_w3_textshaping__rd_example__lorem_text_Rd', 'textshaping__rd_example__lorem_text_Rd')]:
    src = Path(f'work/scoring/programs/{prog}.py').read_text(encoding='utf-8')
    start = (hr.SOURCES / f'{stem}.py').read_text(encoding='utf-8')
    sm = pickle.loads((hr.MAPS / f'{stem}.pkl').read_bytes())
    scores = []
    for _ in range(4):
        t = _tools(sm, stem); t.note_reference(src)   # as scoring_epoch.verify_one
        scores.append(round(t.verify(src).aggregate, 4))
    print(prog, scores, flush=True)
