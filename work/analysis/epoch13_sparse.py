"""Why sparsevctrs sparse_logical crashes under epoch 13: verify its held-out final (= its start) and show stderr."""
import pickle, sys
sys.path[:0] = ['.', 'scripts']
from dotenv import load_dotenv; load_dotenv('.env', override=True)
import health_report as hr
from prompt_load import _tools
stem = 'sparsevctrs__rd_example__sparse_logical_Rd'
src = (hr.SOURCES / f'{stem}.py').read_text(encoding='utf-8')
t = _tools(pickle.loads((hr.MAPS / f'{stem}.pkl').read_bytes()), stem); t.note_reference(src)
rep = t.verify(src)
print('aggregate', rep.aggregate, 'exit', rep.py_exit_code)
for a in ('py_stderr', 'stderr'):
    if getattr(rep, a, None):
        print(getattr(rep, a)[-1500:])
