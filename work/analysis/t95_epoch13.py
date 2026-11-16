"""threshold-095 under epoch 13 (forged fingerprints refused), offline: re-verify every chain's final and redo the
analysis of threshold95_continue.py against the default's finals re-verified under epoch 13.

A chain with no accepted program ends at its start: for t95_cont the continued chain's best (which may itself be
forged), for t90_chain the frozen start; both are re-verified, not taken from the log.

    python work/analysis/t95_epoch13.py            # re-verify (writes work/threshold95/finals_epoch13.jsonl), then analyze
    python work/analysis/t95_epoch13.py analyze    # analyze only
    python work/analysis/t95_epoch13.py analyze xml2   # analyze without the states matching xml2
"""
import collections, json, pickle, random, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
RD = ROOT / "work/threshold95"; OUT = RD / "finals_epoch13.jsonl"
ARMS = ("t95_cont", "t90_chain")


def reverify():
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
    import health_report as hr
    import threshold95_continue as tc
    from prompt_load import _tools
    starts = {(t["script"], t["policy"], t["sample"]): t["source"] for t in tc.tasks()}
    with open(OUT, "w", encoding="utf-8") as out:
        for r in map(json.loads, open(RD / "results.jsonl", encoding="utf-8")):
            if not tc._valid(r):
                continue
            stem = Path(r["script"]).stem
            sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
            tf = RD / "trajectories" / f"{stem}.{r['policy']}.{r['sample']}.jsonl"
            src = hr._final_program([json.loads(l) for l in open(tf, encoding="utf-8")]) or starts[(r["script"], r["policy"], r["sample"])]
            t = _tools(sm, stem); t.note_reference((hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8"))
            agg = round(t.verify(src).aggregate, 4)
            out.write(json.dumps(dict(script=r["script"], policy=r["policy"], sample=r["sample"], inloop=r["final_score"],
                                      calls=r["llm_steps"], epoch13=agg)) + "\n"); out.flush()
            print(f"{stem[:44]:44s} {r['policy']:9s} {r['sample']} in-loop {r['final_score']:.3f} epoch 13 {agg:.3f}", flush=True)


def analyze(without=()):
    fin = {f"{r['stem']}.R": r["aggregate"]
           for r in map(json.loads, open(ROOT / "work/dsflash_default/finals_epoch13.jsonl", encoding="utf-8"))}
    rows = collections.defaultdict(list)
    for r in map(json.loads, open(OUT, encoding="utf-8")):
        rows[(r["script"], r["policy"])].append(r)
    states = sorted({s for s, _ in rows if not any(w in s for w in without)})
    gain, flip, calls = ({a: {} for a in ARMS} for _ in range(3))
    for a in ARMS:
        for s in states:
            new = max([fin[s]] + [r["epoch13"] for r in rows[(s, a)]])
            gain[a][s], flip[a][s] = new - fin[s], float(new >= 0.95 > fin[s])
            calls[a][s] = sum(r["calls"] for r in rows[(s, a)])

    def stats(smp):
        g = {a: sum(gain[a][s] for s in smp) for a in ARMS}
        f = {a: sum(flip[a][s] for s in smp) for a in ARMS}
        n = {a: sum(calls[a][s] for s in smp) or 1 for a in ARMS}
        return (g["t95_cont"] / 60, g["t90_chain"] / 60, g["t95_cont"] / n["t95_cont"] - g["t90_chain"] / n["t90_chain"],
                f["t95_cont"] / 60, f["t90_chain"] / 60, f["t95_cont"] / n["t95_cont"] - f["t90_chain"] / n["t90_chain"])

    point = stats(states)
    rng = random.Random(0)
    boots = [stats([rng.choice(states) for _ in states]) for _ in range(10000)]
    print(f"states {len(states)}; baseline: the default's finals under epoch 13")
    for i, name in enumerate(("t95: gain on the plateau", "t90: gain on the plateau", "plateau gain per call, t95 - t90",
                              "t95: share gain", "t90: share gain", "flipped per call, t95 - t90")):
        c = sorted(b[i] for b in boots)
        print(f"{name:34s} {point[i]:+.5f} [{c[250]:+.5f}, {c[9749]:+.5f}]  P(> 0) {sum(x > 0 for x in c) / len(c):.3f}")
    for s in states:
        print(f"  {s[:46]:46s} {fin[s]:.3f}  t95 {gain['t95_cont'][s]:+.3f} ({calls['t95_cont'][s]} calls)"
              f"  t90 {gain['t90_chain'][s]:+.3f} ({calls['t90_chain'][s]} calls)")


if __name__ == "__main__":
    if sys.argv[1:2] != ["analyze"]:
        reverify()
    analyze(tuple(sys.argv[2:]))
