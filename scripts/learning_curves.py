"""In-loop learning curves: the mean score of the best program after each agent step (2026-10-20).

Rebuilds the chart "In-Loop Score Curves" (experiments/figures/) from the saved replay runs, all on the same 60
training-pool states:

  work/replay_k3                width-3 and 3-per-step runs of 2026-10-17 (6 single chains per state -> width 1, 3,
                                and the width-6 estimate; 3 per step)
  work/continue_plateau         restart / accept-equal continuations of running plateaus (2026-10-18)
  work/continue_stalled         patience continuations of chains that stalled while crashing (2026-10-18)
  work/replay_crash6p5_b2       crash default: width 6, patience 5, doubled time limit (2026-10-19)
  work/replay_default           the production default with conversation mode (2026-10-20)

The programs of the 2026-10-17 runs are re-scored with the harness of 2026-10-18 for the 10 states its fixes touch
(tag lists, temp paths, session reports); that needs verification runs and is cached in work/curves/rescored.json.

    python scripts/learning_curves.py             # data, PNG and HTML (re-scoring only if the cache is missing)
    python scripts/learning_curves.py --rescore   # redo the re-scoring first

Writes experiments/figures/inloop_curves.json, inloop_curves.png and inloop_curves.html (from
inloop_curves_template.html).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pickle
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
FIG = ROOT / "experiments/figures"
CACHE = ROOT / "work/curves/rescored.json"
N_SHOWN = 14          # steps drawn; every curve is flat well before
N_LONG = 20           # steps followed for the runs with patience 5

H = lambda s: hashlib.sha1(s.encode("utf-8")).hexdigest()   # noqa: E731


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def _traj(run: str, script: str, policy: str, sample) -> list[dict]:
    return _jsonl(ROOT / run / "trajectories" / f"{Path(script).stem}.{policy}.{sample}.jsonl")


def series(recs: list[dict], start: tuple, branches, n: int, value=None) -> dict:
    """Per chain: (runs, score) of its current best program after 0..n steps (a stopped chain keeps its last)."""
    acc = {(r.get("branch"), r["step"]): r for r in recs if r["kind"] == "accepted"}
    ver = {(r.get("branch"), r.get("step")): (r.get("exit_code") == 0, r["aggregate"])
           for r in recs if r["kind"] == "step" and "aggregate" in r}
    out = {}
    for b in branches:
        cur, s = start, []
        for k in range(n + 1):
            if k and (b, k) in acc and (b, k) in ver:
                cur = value(acc[(b, k)].get("source"), ver[(b, k)]) if value else ver[(b, k)]
            s.append(cur)
        out[b] = s
    return out


# ---------------------------------------------------------------------------------------------- re-scoring

def affected_states() -> list[str]:
    """Training-pool states the harness fixes of 2026-10-18 change: tag lists, temp paths, session reports."""
    import replay
    from r2py.stage4.verifier import _environment_report_entities
    out = []
    for name in sorted(replay.training_states()):
        sm = pickle.loads((ROOT / "work/reverify/script_maps" / f"{Path(name).stem}.pkl").read_bytes())
        tag = any("shiny.tag" in i.get("class", "") for t in (sm.entity_types or {}).values() for i in t.values())
        if tag or "tempfile" in (sm.source or "") or _environment_report_entities(sm):
            out.append(name)
    return out


def _rescore_one(name: str):
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import replay
    from prompt_load import _tools
    stem = Path(name).stem
    srcs = {}
    start = replay.training_states()[name]["source"]
    srcs[H(start)] = start
    for f in (ROOT / "work/replay_k3/trajectories").glob(f"{stem}.*.jsonl"):
        for r in _jsonl(f):
            if r["kind"] == "accepted" and r.get("source"):
                srcs[H(r["source"])] = r["source"]
    sm = pickle.loads((ROOT / "work/reverify/script_maps" / f"{stem}.pkl").read_bytes())
    out = {}
    for h, src in srcs.items():
        t = _tools(sm, stem)
        t.note_reference(src)   # as the loop does: attribution read off the sentinels, no model call
        try:
            rep = t.verify(src)
            out[h] = [rep.py_exit_code == 0, rep.aggregate]
        except Exception:
            out[h] = None
    return name, out


def rescore() -> dict:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(8) as ex:
        res = dict(ex.map(_rescore_one, affected_states()))
    CACHE.write_text(json.dumps(res), encoding="utf-8")
    return res


# ---------------------------------------------------------------------------------------------- curves

def compute(res: dict) -> dict:
    import replay
    starts = replay.training_states()

    def val(script, src, fallback):
        if script in res and src is not None:
            v = res[script].get(H(src))
            if v:
                return (v[0], v[1])
        return fallback

    rows = {(r["script"], r["policy"], r["sample"]): r for r in _jsonl(ROOT / "work/replay_k3/results.jsonl")}
    single, k3, crash, w3runs = defaultdict(list), defaultdict(list), {}, {}
    for (s, pol, smp), row in rows.items():
        crash[s] = row["start_exit"] != 0
        start = val(s, starts[s]["source"], (row["start_exit"] == 0, row["start_score"]))
        recs = _traj("work/replay_k3", s, pol, smp)
        v = lambda src, fb, s=s: val(s, src, fb)   # noqa: E731
        if pol == "rewrite_w3":
            ch = series(recs, start, (0, 1, 2), N_SHOWN, v)
            single[s] += list(ch.values())
            w3runs[(s, smp)] = ch
        else:
            k3[s].append(series(recs, start, (None,), N_SHOWN, v)[None])
    states = sorted(single)

    # plateau continuations: the run-level final after k more steps (the run keeps the best of its chains)
    ext = {}
    for name, pol, k in (("restart", "continue3", 3), ("accept equal", "continue3_eq", 3)):
        done = {(r["script"], r["sample"]): r for r in _jsonl(ROOT / "work/continue_plateau/results.jsonl")
                if r["policy"] == pol and "final_score" in r}
        per = defaultdict(list)
        for (s, smp), ch in w3runs.items():
            final = max(c[-1] for c in ch.values())
            r = done.get((s, smp))
            if r is None:
                per[s].append([final[1]] * (k + 1))
                continue
            cs = series(_traj("work/continue_plateau", s, pol, smp), (r["start_exit"] == 0, r["start_score"]), (None,), k)[None]
            per[s].append([max(final, c)[1] for c in cs])
        ext[name] = per
    done = {(r["script"], r["sample"]): r for r in _jsonl(ROOT / "work/continue_stalled/results.jsonl") if "final_score" in r}
    per = defaultdict(list)
    for (s, smp), ch in w3runs.items():
        cols = []
        for b, c in ch.items():
            r = done.get((s, f"{smp}.{b}"))
            if r is None:
                cols.append([c[-1]] * 3)
            else:
                cs = series(_traj("work/continue_stalled", s, "continue2", f"{smp}.{b}"),
                            (r["start_exit"] == 0, r["start_score"]), (None,), 2)[None]
                cols.append([max(c[-1], x) for x in cs])
        per[s].append([max(col[i] for col in cols)[1] for i in range(3)])
    ext["patience 5"] = per

    def best_of(run: str, policy: str, n_chains: int) -> dict:
        out = {}
        for r in _jsonl(ROOT / run / "results.jsonl"):
            recs = _traj(run, r["script"], policy, r["sample"])
            branches = sorted({x.get("branch") for x in recs if x["kind"] == "step"}, key=lambda b: (b is None, b))
            chs = list(series(recs, (r["start_exit"] == 0, r["start_score"]), branches or [None], N_LONG).values())
            out[r["script"]] = [max(c[k] for c in chs)[1] for k in range(N_LONG + 1)]
        return out
    crash6 = best_of("work/replay_crash6p5_b2", "rewrite_w3_crash6p5", 6)
    measured = best_of("work/replay_default", "default_2026_10_20", 3)

    def width_curve(s, k):
        subs = list(itertools.combinations(single[s], k))
        return [st.mean(max(c[n] for c in sub)[1] for sub in subs) for n in range(N_SHOWN + 1)]
    r4 = lambda xs: [round(x, 4) for x in xs]   # noqa: E731
    mean_over = lambda curves, ss, n: [st.mean(curves[s][i] for s in ss) for i in range(n + 1)]   # noqa: E731
    data = {"steps": list(range(N_SHOWN + 1)), "strata": {}}
    for label, sel in (("all", lambda s: True), ("running", lambda s: not crash[s]), ("crashing", lambda s: crash[s])):
        ss = [s for s in states if sel(s)]
        lines = {"width 1": [st.mean(width_curve(s, 1)[n] for s in ss) for n in range(N_SHOWN + 1)],
                 "width 3": [st.mean(width_curve(s, 3)[n] for s in ss) for n in range(N_SHOWN + 1)],
                 "width 6 (estimated)": [st.mean(width_curve(s, 6)[n] for s in ss) for n in range(N_SHOWN + 1)],
                 "3 per step": [st.mean(st.mean(c[n][1] for c in k3[s]) for s in ss) for n in range(N_SHOWN + 1)]}
        w3_end = st.mean(st.mean(max(c[-1] for c in w3runs[(s, smp)].values())[1] for smp in (0, 1)) for s in ss)
        exts = {name: [round(lines["width 3"][-1] + st.mean(st.mean(r[i] for r in p[s]) for s in ss) - w3_end, 4)
                       for i in range(len(next(iter(p.values()))[0]))] for name, p in ext.items()}
        lines = {k: r4(v) for k, v in lines.items()}
        lines["default with conversation (measured)"] = r4(mean_over(measured, [s for s in measured if sel(s)], N_LONG))[:N_SHOWN + 1]
        data["strata"][label] = {"n": len(ss), "lines": lines, "w3_runs_end": round(w3_end, 4), "ext": exts}
    cr = data["strata"]["crashing"]
    cr["lines"].pop("width 6 (estimated)")
    cr["lines"]["width 6 + patience 5"] = r4(mean_over(crash6, [s for s in states if crash[s]], N_LONG))[:N_SHOWN + 1]
    run, nr, nc = data["strata"]["running"], data["strata"]["running"]["n"], cr["n"]
    data["strata"]["all"]["lines"]["default without conversation"] = [
        round((nr * a + nc * b) / (nr + nc), 4) for a, b in zip(run["lines"]["width 3"], cr["lines"]["width 6 + patience 5"])]
    return data


# ---------------------------------------------------------------------------------------------- outputs

STYLE = {"default with conversation (measured)": ("#111827", "-", 2.8), "width 1": ("#8a93a3", "--", 1.8),
         "width 3": ("#2f6fd1", "-", 2.2), "width 6 (estimated)": ("#0f766e", ":", 1.6),
         "width 6 + patience 5": ("#0f766e", "-", 2.2), "default without conversation": ("#0f766e", "-", 2.2),
         "3 per step": ("#d9731a", "-", 2.2)}
EXT_STYLE = {"restart": "#7c3aed", "accept equal": "#c026d3", "patience 5": "#b91c1c"}


def plot(data: dict, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    titles = {"all": "All starts", "running": "Starts that run", "crashing": "Starts that crash"}
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), sharey=False)
    for ax, (k, st_) in zip(axes, data["strata"].items()):
        last = data["steps"][-1]
        ax.axvspan(last + 0.3, last + 3.6, color="#eef1f5", zorder=0)
        for name, ys in st_["lines"].items():
            c, ls, lw = STYLE.get(name, ("#555555", "-", 2))
            ax.plot(data["steps"], ys, ls, color=c, lw=lw, label=name)
        for name, ys in st_["ext"].items():
            ax.plot([last + i for i in range(len(ys))], ys, "--", color=EXT_STYLE[name], lw=1.8, label=f"then {name}")
        ax.set_title(f"{titles[k]} ({st_['n']} states)")
        ax.set_xlabel("agent step (0 = starting translation; shaded: after the width-3 plateau)")
        ax.set_xticks(list(range(0, last + 1, 2)) + [last + 1, last + 2, last + 3])
        ax.set_xticklabels([str(i) for i in range(0, last + 1, 2)] + ["+1", "+2", "+3"])
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("mean score of the best program")
    handles, labels = [], []
    for ax in axes:
        for h, lab in zip(*ax.get_legend_handles_labels()):
            if lab not in labels:
                handles.append(h); labels.append(lab)
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False, fontsize=9)
    fig.suptitle("In-loop score curves: mean best score after each agent step, same 60 training states")
    fig.tight_layout(rect=(0, 0.1, 1, 0.95))
    fig.savefig(path, dpi=130)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rescore", action="store_true", help="redo the re-scoring of the affected states")
    a = ap.parse_args()
    res = rescore() if (a.rescore or not CACHE.exists()) else json.loads(CACHE.read_text(encoding="utf-8"))
    data = compute(res)
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "inloop_curves.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    plot(data, FIG / "inloop_curves.png")
    tpl = (FIG / "inloop_curves_template.html").read_text(encoding="utf-8")
    (FIG / "inloop_curves.html").write_text(tpl.replace("__DATA__", json.dumps(data, separators=(",", ":"))), encoding="utf-8")
    for k, s in data["strata"].items():
        print(k, s["n"], {n: (v[0], v[-1]) for n, v in s["lines"].items()})


if __name__ == "__main__":
    main()
