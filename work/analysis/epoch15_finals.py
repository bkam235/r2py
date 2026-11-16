"""The default's finals, epoch 14 vs epoch 15 (graphics pages attributed as R's), training and held-out."""
import json
for d in ['work/dsflash_default', 'work/dsflash_heldout']:
    a = {r['stem']: r for r in map(json.loads, open(f'{d}/finals_epoch14.jsonl', encoding='utf-8'))}
    b = {r['stem']: r for r in map(json.loads, open(f'{d}/finals_epoch15.jsonl', encoding='utf-8'))}
    err = [s for s in b if 'aggregate' not in b[s]] + [s for s in a if 'aggregate' not in a[s]]
    s = sorted(set(a) & set(b) - set(err))
    ma, mb = sum(a[x]['aggregate'] for x in s) / len(s), sum(b[x]['aggregate'] for x in s) / len(s)
    sa = sum(a[x]['aggregate'] >= 0.95 for x in s) / len(s); sb = sum(b[x]['aggregate'] >= 0.95 for x in s) / len(s)
    print(f'{d}: n {len(s)} errors {err}  plateau {ma:.4f} -> {mb:.4f} ({mb - ma:+.4f})  share>=0.95 {sa:.3f} -> {sb:.3f}')
    for x in s:
        if abs(b[x]['aggregate'] - a[x]['aggregate']) > 0.005:
            print(f'   {x[:58]:58s} {a[x]["aggregate"]:.3f} -> {b[x]["aggregate"]:.3f}')
