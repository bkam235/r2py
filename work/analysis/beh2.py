import json,glob,collections,os
fin={json.loads(l)['stem']:json.loads(l)['aggregate'] for l in open('work/dsflash_default/finals_epoch10.jsonl')}
seq=collections.Counter(); agg=collections.defaultdict(list)
succ=collections.defaultdict(lambda:[0,0])
for f in glob.glob('work/dsflash_default/trajectories/*.jsonl'):
    stem=os.path.basename(f).split('.default')[0]; low=fin.get(stem,1)<0.9
    steps=collections.OrderedDict()
    for l in open(f,encoding='utf-8'):
        r=json.loads(l)
        if r['kind']!='step' or not r['outcome'].startswith('rewrite'): continue
        steps.setdefault((r['branch'],r['step']),[]).append(r)
    fails=collections.Counter()
    for (b,s),rs in sorted(steps.items()):
        seq[tuple(x['outcome'].split(':')[1] for x in rs)]+=1
        for x in rs:
            if 'aggregate' in x: agg[x['outcome']].append(x['aggregate']-x['best_score'])
        ok=any(x['outcome']=='rewrite:improved' for x in rs)
        k=min(fails[b],3); succ[(low,k)][1]+=1; succ[(low,k)][0]+=ok
        fails[b]=0 if ok else fails[b]+1
for k,v in seq.most_common(15): print(v,k)
for k,v in agg.items(): print(k,len(v),'mean delta',round(sum(v)/len(v),3),'pos',sum(d>0 for d in v))
for k in sorted(succ): print('final<0.9' if k[0] else 'final>=0.9','after',k[1],'fails',succ[k], round(succ[k][0]/max(1,succ[k][1]),2))
