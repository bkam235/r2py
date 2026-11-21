"""threshold-095-e16 (2026-11-21): faithfulness audit (META_LOOP step 8) of the t95 finals that gained most over the
default's recorded finals, both pools: new numeric literals with >= 4 significant digits (not in the program the chain
continued from, nor in the start), the forging marker, and the program written out for reading."""
import json, re, sys
from pathlib import Path
sys.path[:0] = ['.', 'scripts']
import health_report as hr
import threshold95_continue as t


def lits(src):   # the literal rule of work/analysis/e16_replay_audit.py
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+\.\d+(?:[eE][-+]?\d+)?|(?<![\w.])\d{4,}(?![\w.])', src):
        digits = re.sub(r'[^0-9]', '', m.group().split('e')[0].split('E')[0]).lstrip('0').rstrip('0')
        if len(digits) >= 4:
            out.add(m.group())
    return out


OUTDIR = Path('work/analysis/t95_e16_finals')
OUTDIR.mkdir(exist_ok=True)
rows = []
for name in ('e16-training', 'e16-heldout'):
    t.SRC, t.POLICY, t.FINALS, t.POOL, t.OUT = t.SOURCES[name]
    fin, ch = t.finals(), t.chains()
    for l in (t.OUT / 'results.jsonl').open(encoding='utf-8'):
        r = json.loads(l)
        if r['policy'] != 't95_cont' or 'final_score' not in r or r['final_score'] <= fin[r['script']]:
            continue
        stem = Path(r['script']).stem
        recs = [json.loads(x) for x in (t.OUT / 'trajectories' / f"{stem}.t95_cont.{r['sample']}.jsonl").open(encoding='utf-8')]
        final = hr._final_program(recs) or ''
        b = r['sample'][1:]
        cont = ch[(r['script'], b if b.startswith('s') else int(b))]['source']
        start = (hr.SOURCES / f'{stem}.py').read_text(encoding='utf-8')
        rows.append((r['final_score'] - fin[r['script']], name, stem, r['sample'], fin[r['script']], r['final_score'],
                     sorted(lits(final) - lits(cont) - lits(start)), final.count('__r2py_fp__'), final))
best = {}
for row in sorted(rows, reverse=True):
    best.setdefault(row[2], row)
for g, pool, stem, smp, f0, f1, new, fp, src in sorted(best.values(), reverse=True)[:10]:
    (OUTDIR / f'{stem}.{smp}.py').write_text(src, encoding='utf-8')
    print(f'{pool:12} {stem[:44]:44} {smp:4} {f0:.3f} -> {f1:.3f} (+{g:.3f})  new literals {len(new)} {new[:6]}  fp {fp}')
