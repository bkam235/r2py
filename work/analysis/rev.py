import json,glob,collections,os
fin={json.loads(l)['stem']:json.loads(l)['aggregate'] for l in open('work/dsflash_default/finals_epoch10.jsonl')}
lost=0
for f in sorted(glob.glob('work/dsflash_default/trajectories/*.jsonl')):
    stem=os.path.basename(f).split('.default')[0]
    for l in open(f,encoding='utf-8'):
        r=json.loads(l)
        if r['kind']=='step' and r['outcome']=='rewrite:review_rejected':
            ex=max(0,r['aggregate']-fin[stem])
            lost+=ex/60
            print(f"{stem[:45]:45} fin {fin[stem]:.3f} b{r['branch']} s{r['step']} best {r['best_score']:.3f} cand {r['aggregate']:.3f} above_final {ex:.3f} keys {[k for k in r if k not in ('source','per_entity')][-4:]}")
print('plateau pts if rejected candidates had been kept (upper bound, candidate over final):',round(lost,4))
