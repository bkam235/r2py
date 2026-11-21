"""default-2026-11-21-replay and -heldout (2026-11-21): the registered secondary readings, descriptive. Share >= 0.95,
the baseline's [0.9, 0.95) band apart from the rest, calls and cost per run, stops, the forging marker, and new
numeric literals with >= 4 significant digits in the 12 largest gains' finals (as in e16_replay_audit.py)."""
import json, random, re, sys
from collections import Counter
sys.path[:0] = ['.', 'scripts']
import health_report as hr

POOLS = {'training': ('work/replay_default_e16', 'work/replay_default_e17'),
         'heldout': ('work/replay_default_e16_heldout', 'work/replay_default_e17_heldout')}


def lits(src):
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+\.\d+(?:[eE][-+]?\d+)?|(?<![\w.])\d{4,}(?![\w.])', src):
        digits = re.sub(r'[^0-9]', '', m.group().split('e')[0].split('E')[0]).lstrip('0').rstrip('0')
        if len(digits) >= 4:
            out.add(m.group())
    return out


def finals(d):
    return {json.loads(l)['stem']: json.loads(l)['aggregate'] for l in open(f'{d}/finals_epoch17.jsonl')}


def rows(d):
    return {json.loads(l)['script'][:-2]: json.loads(l) for l in open(f'{d}/results.jsonl', encoding='utf-8')}


def boot(diffs, n=10000, seed=0):
    rng = random.Random(seed)
    m = [sum(rng.choice(diffs) for _ in diffs) / len(diffs) for _ in range(n)]
    m.sort()
    return m[int(.025 * n)], m[int(.975 * n)]


def per_run(r):
    calls = sum(u['calls'] for u in r['usage'].values())
    cost = sum(u['cost'] for u in r['usage'].values())
    return calls, cost


for pool, (bd, nd) in POOLS.items():
    a, b = finals(bd), finals(nd)
    ra, rb = rows(bd), rows(nd)
    stems = sorted(a)
    print(f'===== {pool} (n={len(stems)})')
    for name, f in (('baseline', a), ('new', b)):
        print(f'  {name:8} plateau {sum(f[s] for s in stems) / len(stems):.4f}  share>=0.95 '
              f'{sum(f[s] >= 0.95 for s in stems) / len(stems):.3f}  >=0.9 {sum(f[s] >= 0.9 for s in stems)}')
    d = [b[s] - a[s] for s in stems]
    sh = [(b[s] >= 0.95) - (a[s] >= 0.95) for s in stems]
    print(f'  diff plateau {sum(d) / len(d):+.4f} {boot(d)}  share {sum(sh) / len(sh):+.3f} {boot(sh)}')
    for label, sel in (('band [0.9,0.95)', lambda s: 0.9 <= a[s] < 0.95), ('rest', lambda s: not 0.9 <= a[s] < 0.95)):
        ss = [s for s in stems if sel(s)]
        dd = [b[s] - a[s] for s in ss]
        print(f'  {label:16} n={len(ss):2d} baseline {sum(a[s] for s in ss) / len(ss):.4f} new '
              f'{sum(b[s] for s in ss) / len(ss):.4f} diff {sum(dd) / len(dd):+.4f}  now >=0.95 '
              f'{sum(b[s] >= 0.95 for s in ss)}  better {sum(x > 0.001 for x in dd)} worse {sum(x < -0.001 for x in dd)}')
    for name, r in (('baseline', ra), ('new', rb)):
        c = [per_run(r[s]) for s in stems]
        print(f'  {name:8} calls/run {sum(x for x, _ in c) / len(c):.1f}  cost/run ${sum(y for _, y in c) / len(c):.4f}'
              f'  llm_steps/run {sum(r[s]["llm_steps"] for s in stems) / len(stems):.1f}')
    stops = Counter()
    fp = []
    for s in stems:
        recs = [json.loads(l) for l in open(f'{nd}/trajectories/{s}.default_2026_11_21.0.jsonl', encoding='utf-8')]
        for k, v in rb[s]['agent']['stop'].items():
            stops[k] += v
        final = hr._final_program(recs) or ''
        raw = open(f'{nd}/trajectories/{s}.default_2026_11_21.0.jsonl', encoding='utf-8').read()
        if '__r2py_fp__' in raw:
            fp.append((s, final.count('__r2py_fp__'), raw.count('__r2py_fp__')))
    print(f'  stops {dict(stops)}')
    print(f'  forging marker (final count, trajectory count): {fp}')
    print('  12 largest gains, new 4+digit literals in the final (not in the start program):')
    for s in sorted(stems, key=lambda s: a[s] - b[s])[:12]:
        recs = [json.loads(l) for l in open(f'{nd}/trajectories/{s}.default_2026_11_21.0.jsonl', encoding='utf-8')]
        final = hr._final_program(recs) or ''
        start = (hr.SOURCES / f'{s}.py').read_text(encoding='utf-8')
        new = sorted(lits(final) - lits(start))
        print(f'    {s[:45]:45} {a[s]:.3f} -> {b[s]:.3f}  new {len(new):3d} {new[:8]}  fp {final.count("__r2py_fp__")}')
