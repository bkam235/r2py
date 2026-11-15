import json, glob, os, sys
sys.path[:0] = ['.', 'scripts']
import health_report as hr
for d in ['work/dsflash_default', 'work/dsflash_heldout', 'work/threshold95']:
    for f in sorted(glob.glob(d + '/trajectories/*.jsonl')):
        recs = [json.loads(l) for l in open(f, encoding='utf-8')]
        src = hr._final_program(recs) or ''
        acc = sum('__r2py_fp__' in (str(r.get('source') or r.get('program') or '')) for r in recs if r['kind'] == 'accepted')
        if '__r2py_fp__' in src or acc:
            n = src.count('__r2py_fp__')
            print(d, os.path.basename(f)[:60], 'in final:', n, 'accepted programs with it:', acc)
