"""default-e16-replay (2026-11-16): faithfulness audit of the finals that moved most (step 8's reading, descriptive
here): numeric literals with >= 4 significant digits new in the final (not in the start program), and the
forging marker. Also broom augment_felm, whose final still writes `__r2py_fp__`."""
import json, re, sys
sys.path[:0] = ['.', 'scripts']
import health_report as hr

def lits(src):
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+\.\d+(?:[eE][-+]?\d+)?|(?<![\w.])\d{4,}(?![\w.])', src):
        digits = re.sub(r'[^0-9]', '', m.group().split('e')[0].split('E')[0]).lstrip('0').rstrip('0')
        if len(digits) >= 4:
            out.add(m.group())
    return out

a = {json.loads(l)['stem']: json.loads(l)['aggregate'] for l in open('work/dsflash_default/finals_epoch16.jsonl')}
b = {json.loads(l)['stem']: json.loads(l)['aggregate'] for l in open('work/replay_default_e16/finals_epoch16.jsonl')}
movers = sorted(b, key=lambda s: a[s] - b[s])[:12] + ['broom__rd_example__augment_felm_Rd']
for stem in movers:
    recs = [json.loads(l) for l in open(f'work/replay_default_e16/trajectories/{stem}.default_2026_11_12.0.jsonl', encoding='utf-8')]
    final = hr._final_program(recs) or ''
    start = (hr.SOURCES / f'{stem}.py').read_text(encoding='utf-8')
    new = sorted(lits(final) - lits(start))
    print(f'{stem[:45]:45} {a[stem]:.3f} -> {b[stem]:.3f}  new 4+digit literals {len(new):3d} {new[:8]}  fp-marker {final.count("__r2py_fp__")}')
