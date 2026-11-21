"""Move the gap ledger's source to default-2026-11-21-replay (2026-11-21): rows below 0.95 under the new finals keep
their class; leavers go, entrants come in as unknown. Prints the new rows and the summary by class."""
import json, re, sys
L = 'experiments/gap_ledger.md'
old = {json.loads(l)['stem']: json.loads(l)['aggregate'] for l in open('work/replay_default_e16/finals_epoch17.jsonl')}
new = {json.loads(l)['stem']: json.loads(l)['aggregate'] for l in open('work/replay_default_e17/finals_epoch17.jsonl')}
def name(s):
    pkg, _, rest = s.split('__', 2)
    return pkg + ' ' + re.sub(r'_Rd$', '', rest)
names = {name(s): s for s in new}
text = open(L, encoding='utf-8').read()
head, rows_part = text.split('## States', 1)
lines = rows_part.split('\n')
rows = {}
for l in lines:
    m = re.match(r'\| ([^|]+) \| ([0-9.]+) \| ([0-9.]+) \| ([^|]+) \| (.*) \| ([0-9-]+) \|$', l)
    if m and m.group(1).strip() in names:
        rows[m.group(1).strip()] = [m.group(4).strip(), m.group(5).strip(), m.group(6)]
out, cls = [], {}
for s in sorted(new, key=lambda s: new[s]):
    if new[s] >= 0.95: continue
    n = name(s)
    if n in rows:
        c, ev, st = rows[n]
        ev += f' default-2026-11-21-replay: {old[s]:.3f} -> {new[s]:.3f}.'
    else:
        c, ev, st = 'unknown', f'Enters with default-2026-11-21-replay ({new[s]:.3f}; {old[s]:.3f} in the 11-16 replay under epoch 17). Not read.', '2026-11-21'
    pts = (1 - new[s]) / 60
    key = c.split(' (')[0]
    cls.setdefault(key, []).append((n, pts))
    out.append(f'| {n} | {new[s]:.3f} | {pts:.4f} | {c} | {ev} | {st} |')
left = [n for n in rows if new[names[n]] >= 0.95]
print('\n'.join(out))
print('LEFT', [(n, f'{old[names[n]]:.3f}->{new[names[n]]:.3f}') for n in left])
print('ENTER', [n for n in (name(s) for s in new if new[s] < 0.95) if n not in rows])
for k, v in cls.items(): print(k, len(v), round(sum(p for _, p in v), 4), [n for n, _ in v])
hi = [s for s in new if new[s] >= 0.95]
print('>=0.95', len(hi), round(sum((1 - new[s]) / 60 for s in hi), 4), 'gap', round(1 - sum(new.values()) / 60, 4))
