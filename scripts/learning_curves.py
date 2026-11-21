"""In-loop learning curves: the mean score of the best program after each agent step (2026-10-20).

Rebuilds the chart "In-Loop Score Curves" (experiments/figures/) from the saved replay runs, all on the same 60
training-pool states:

  work/replay_k3                width-3 and 3-per-step runs of 2026-10-17 (6 single chains per state -> width 1, 3,
                                and the width-6 estimate; 3 per step)
  work/continue_plateau         restart / accept-equal continuations of running plateaus (2026-10-18)
  work/continue_stalled         patience continuations of chains that stalled while crashing (2026-10-18)
  work/replay_crash6p5_b2       crash default: width 6, patience 5, doubled time limit (2026-10-19)
  work/replay_default           the production default with conversation mode (2026-10-20)
  work/replay_default_e8        the production default of 2026-11-01 (entity feedback), replayed 2026-11-05
  work/dsflash_default          the production default of 2026-11-12 (agent on DeepSeek V4.1 Flash), run 2026-11-12
  work/replay_default_e16       the same default replayed 2026-11-16 under epoch 16 (after the feedback corrections of
                                epochs 10-16; test default-e16-replay)
  work/replay_default_e17       the production default of 2026-11-21 (stop threshold 0.95), run 2026-11-21 under
                                epoch 17 (test default-2026-11-21-replay)

The scores of the programs the curves use (the starting programs and every program a chain accepted) are cached in
work/curves/rescored.json with the scorer version. When the scorer has changed, the next call re-scores only the live
programs: the 60 starting programs and those of the production default's replay (LIVE_RUNS; the person's decision of
2026-11-16, before which all ~2,100 were re-scored). Every other line keeps its programs' scores from the epoch in which
they were last re-scored (`frozen_version` in the cache, epoch 14) and is labelled so; `--all` re-scores everything
again. `scripts/scoring_epoch.py accept` calls this script, so a new epoch rebuilds the curves by default. A state's
stratum is its re-scored start: running or crashing.

    python scripts/learning_curves.py             # data, PNG and HTML (re-scores the live programs if the scorer changed)
    python scripts/learning_curves.py --rescore   # re-score the live programs even if the scorer is unchanged
    python scripts/learning_curves.py --all       # re-score every program (all lines in one epoch again)
    python scripts/learning_curves.py --extract   # refresh work/curves/inputs.json.gz from the full run logs

The full trajectories (~48 MB) are not in the repository. What the curves need from them (per step: kind, chain,
step, exit code, score, and a hash of each accepted program) is extracted into work/curves/inputs.json.gz, which is;
without the full logs the script reads that file.

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
INPUTS = ROOT / "work/curves/inputs.json.gz"
RUNS = ("work/replay_k3", "work/continue_plateau", "work/continue_stalled", "work/replay_crash6p5_b2", "work/replay_default",
        "work/replay_default_e8", "work/dsflash_default", "work/replay_default_e16", "work/replay_default_e17")
# re-scored in every new epoch (both measured runs of the production default); the others are frozen
LIVE_RUNS = ("work/dsflash_default", "work/replay_default_e16", "work/replay_default_e17")
LIVE_LINES = ("default 2026-11-12, DeepSeek agent (measured)", "default 2026-11-12, replayed 2026-11-16 (measured)",
              "default 2026-11-21, threshold 0.95 (measured)")
_inputs: dict | None = None
N_SHOWN = 14          # steps drawn; every curve is flat well before
N_LONG = 20           # steps followed for the runs with patience 5

H = lambda s: hashlib.sha1(s.encode("utf-8")).hexdigest()   # noqa: E731


def _minimal(r: dict) -> dict:
    out = {k: r[k] for k in ("kind", "branch", "step", "exit_code", "aggregate") if k in r}
    if r.get("source"):
        out["source_hash"] = H(r["source"])
    return out


def _stored(rel: str):
    global _inputs
    if _inputs is None:
        import gzip
        _inputs = json.loads(gzip.decompress(INPUTS.read_bytes()).decode("utf-8")) if INPUTS.exists() else {}
    return _inputs.get(rel)


def _jsonl(path: Path) -> list[dict]:
    if not path.exists():   # results files of runs whose logs are not in the repository
        return _stored(path.relative_to(ROOT).as_posix())
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def _traj(run: str, script: str, policy: str, sample) -> list[dict]:
    path = ROOT / run / "trajectories" / f"{Path(script).stem}.{policy}.{sample}.jsonl"
    if not path.exists():
        return _stored(path.relative_to(ROOT).as_posix())
    return [_minimal(json.loads(line)) for line in path.open(encoding="utf-8")]


def extract() -> None:
    """Write work/curves/inputs.json.gz: every results file and trajectory the curves read, reduced to what they use."""
    import gzip
    out = {}
    for run in RUNS:
        res = ROOT / run / "results.jsonl"
        out[res.relative_to(ROOT).as_posix()] = [json.loads(line) for line in res.open(encoding="utf-8")]
        for f in sorted((ROOT / run / "trajectories").glob("*.jsonl")):
            out[f.relative_to(ROOT).as_posix()] = [_minimal(json.loads(line)) for line in f.open(encoding="utf-8")]
    INPUTS.parent.mkdir(parents=True, exist_ok=True)
    INPUTS.write_bytes(gzip.compress(json.dumps(out, separators=(",", ":")).encode("utf-8")))
    print(f"{len(out)} files -> {INPUTS} ({INPUTS.stat().st_size / 1e6:.1f} MB)")


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
                cur = value(acc[(b, k)].get("source_hash"), ver[(b, k)]) if value else ver[(b, k)]
            s.append(cur)
        out[b] = s
    return out


# ---------------------------------------------------------------------------------------------- re-scoring

def logs_available() -> bool:
    return all((ROOT / run / "trajectories").is_dir() for run in RUNS)


def all_programs(runs=RUNS) -> dict:
    """script -> {hash: source}: the starting programs and the accepted programs of *runs*."""
    import replay
    progs = defaultdict(dict)
    for name, st_ in replay.training_states().items():
        progs[name][H(st_["source"])] = st_["source"]
    for run in runs:
        for f in (ROOT / run / "trajectories").glob("*.jsonl"):
            name = f.name.split(".")[0] + ".R"
            for line in f.open(encoding="utf-8"):
                r = json.loads(line)
                if r["kind"] == "accepted" and r.get("source"):
                    progs[name][H(r["source"])] = r["source"]
    return progs


def _rescore_one(item):
    name, progs = item
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from prompt_load import _tools
    stem = Path(name).stem
    sm = pickle.loads((ROOT / "work/reverify/script_maps" / f"{stem}.pkl").read_bytes())
    out = {}
    for h, src in progs.items():
        t = _tools(sm, stem)
        t.note_reference(src)   # as the loop does: attribution read off the sentinels, no model call
        try:
            rep = t.verify(src)
            out[h] = [rep.py_exit_code == 0, rep.aggregate]
        except Exception:
            out[h] = None
    return name, out


def rescore(old: dict, everything: bool) -> dict:
    """Re-score the live programs (or all), keeping the cached scores of the others; returns the new cache."""
    from r2py.scoring import scoring_version
    progs = all_programs(RUNS if everything else LIVE_RUNS)
    print(f"re-scoring {sum(len(v) for v in progs.values())} programs of {len(progs)} states with the current scorer"
          + ("" if everything else " (live lines only)"), flush=True)
    with ProcessPoolExecutor(8) as ex:
        new = dict(ex.map(_rescore_one, sorted(progs.items())))
    res = {} if everything else {s: dict(v) for s, v in old.get("values", {}).items()}
    for s, v in new.items():
        res.setdefault(s, {}).update(v)
    frozen = None if everything else old.get("frozen_version") or old.get("scoring_version")
    cache = {"scoring_version": scoring_version(), "frozen_version": frozen, "values": res}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache


# ---------------------------------------------------------------------------------------------- curves

def compute(res: dict) -> dict:
    import replay
    starts = replay.training_states()

    def val(script, src_hash, fallback):
        if script in res and src_hash is not None:
            v = res[script].get(src_hash)
            if v:
                return (v[0], v[1])
        return fallback

    rows = {(r["script"], r["policy"], r["sample"]): r for r in _jsonl(ROOT / "work/replay_k3/results.jsonl")}
    single, k3, crash, w3runs = defaultdict(list), defaultdict(list), {}, {}
    start_of = lambda s, r: val(s, H(starts[s]["source"]), (r["start_exit"] == 0, r["start_score"]))   # noqa: E731
    for (s, pol, smp), row in rows.items():
        start = start_of(s, row)
        crash[s] = not start[0]                 # the stratum is the re-scored start
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
            v = lambda src, fb, s=s: val(s, src, fb)   # noqa: E731
            cs = series(_traj("work/continue_plateau", s, pol, smp), final, (None,), k, v)[None]   # starts where the run stopped
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
                v = lambda src, fb, s=s: val(s, src, fb)   # noqa: E731
                cs = series(_traj("work/continue_stalled", s, "continue2", f"{smp}.{b}"), c[-1], (None,), 2, v)[None]
                cols.append([max(c[-1], x) for x in cs])
        per[s].append([max(col[i] for col in cols)[1] for i in range(3)])
    ext["patience 5"] = per

    def best_of(run: str, policy: str, n_chains: int) -> dict:
        out = {}
        for r in _jsonl(ROOT / run / "results.jsonl"):
            recs = _traj(run, r["script"], policy, r["sample"])
            branches = sorted({x.get("branch") for x in recs if x["kind"] == "step"}, key=lambda b: (b is None, b))
            v = lambda src, fb, s=r["script"]: val(s, src, fb)   # noqa: E731
            chs = list(series(recs, start_of(r["script"], r), branches or [None], N_LONG, v).values())
            out[r["script"]] = [max(c[k] for c in chs)[1] for k in range(N_LONG + 1)]
        return out
    crash6 = best_of("work/replay_crash6p5_b2", "rewrite_w3_crash6p5", 6)
    measured = best_of("work/replay_default", "default_2026_10_20", 3)
    later = {"default 2026-11-01 (measured)": best_of("work/replay_default_e8", "default_2026_11_01", 3),
             "default 2026-11-12, DeepSeek agent (measured)": best_of("work/dsflash_default", "default_2026_11_01_dsflash", 3),
             "default 2026-11-12, replayed 2026-11-16 (measured)": best_of("work/replay_default_e16", "default_2026_11_12", 3),
             "default 2026-11-21, threshold 0.95 (measured)": best_of("work/replay_default_e17", "default_2026_11_21", 3)}

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
        for name, m in later.items():
            lines[name] = r4(mean_over(m, [s for s in m if sel(s)], N_LONG))[:N_SHOWN + 1]
        data["strata"][label] = {"n": len(ss), "lines": lines, "w3_runs_end": round(w3_end, 4), "ext": exts}
    cr = data["strata"]["crashing"]
    cr["lines"].pop("width 6 (estimated)")
    cr["lines"]["width 6 + patience 5"] = r4(mean_over(crash6, [s for s in states if crash[s]], N_LONG))[:N_SHOWN + 1]
    run, nr, nc = data["strata"]["running"], data["strata"]["running"]["n"], cr["n"]
    data["strata"]["all"]["lines"]["default without conversation"] = [
        round((nr * a + nc * b) / (nr + nc), 4) for a, b in zip(run["lines"]["width 3"], cr["lines"]["width 6 + patience 5"])]
    return data


# ---------------------------------------------------------------------------------------------- outputs

STYLE = {"default 2026-11-21, threshold 0.95 (measured)": ("#15803d", "-", 3.2),
         "default 2026-11-12, replayed 2026-11-16 (measured)": ("#ca8a04", "-", 3.0),
         "default 2026-11-12, DeepSeek agent (measured)": ("#be123c", "-", 3.0),
         "default 2026-11-01 (measured)": ("#475569", "-", 2.6),
         "default with conversation (measured)": ("#111827", "-", 2.8), "width 1": ("#8a93a3", "--", 1.8),
         "width 3": ("#2f6fd1", "-", 2.2), "width 6 (estimated)": ("#0f766e", ":", 1.6),
         "width 6 + patience 5": ("#0f766e", "-", 2.2), "default without conversation": ("#0f766e", "-", 2.2),
         "3 per step": ("#d9731a", "-", 2.2)}
EXT_STYLE = {"restart": "#7c3aed", "accept equal": "#c026d3", "patience 5": "#b91c1c"}


def _epoch_of(version) -> str:
    """'epoch N (date)' of a scorer version, from work/scoring/epochs.json."""
    for e in json.loads((ROOT / "work/scoring/epochs.json").read_text(encoding="utf-8")):
        if version and e.get("scoring_version") == version:
            return f"epoch {e['epoch']} ({str(e.get('date', ''))[:10]})"
    return f"scorer {version}"


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
            frozen = data.get("frozen_version") and name not in LIVE_LINES
            ax.plot(data["steps"], ys, ls, color=c, lw=lw, alpha=0.55 if frozen else 1.0,
                    label=f"{name}, {_epoch_of(data['frozen_version']).split(' (')[0]}" if frozen else name)
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
    fig.suptitle("In-loop score curves: mean best score after each agent step, same 60 training states; "
                 + data.get("scoring_note", ""), fontsize=10)
    fig.tight_layout(rect=(0, 0.1, 1, 0.95))
    fig.savefig(path, dpi=130)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rescore", action="store_true", help="re-score the live programs even if the scorer is unchanged")
    ap.add_argument("--all", action="store_true", help="re-score every program, the frozen lines too")
    ap.add_argument("--extract", action="store_true", help="refresh work/curves/inputs.json.gz from the full run logs")
    a = ap.parse_args()
    if a.extract:
        extract()
    from r2py.scoring import scoring_version
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    current = scoring_version()
    if a.rescore or a.all or cache.get("scoring_version") != current:
        if logs_available():
            cache = rescore(cache, a.all)
        else:
            print(f"WARNING: the curves were scored with {cache.get('scoring_version', 'an older scorer')}; the current "
                  f"scorer is {current}, and re-scoring needs the full run logs in work/")
    data = compute(cache.get("values", {}))
    data["scoring_version"] = cache.get("scoring_version")
    data["frozen_version"] = cache.get("frozen_version")
    live, frozen = _epoch_of(data["scoring_version"]), _epoch_of(data["frozen_version"])
    if data["frozen_version"]:
        data["scoring_note"] = (f"the starting programs and the DeepSeek default re-scored with the scorer of {live}; "
                                f"the other lines frozen at {frozen}")
        rescored = (f"the starting programs and every program of the DeepSeek default with the scorer of {live}; the "
                    f"other lines keep their scores from {frozen}, when they were last re-scored (from 2026-11-16 a new "
                    f"epoch re-scores only the production default's line).")
    else:
        data["scoring_note"] = f"re-scored with the scorer of {live}"
        rescored = f"all of them with the scorer of {live}, so all lines are in one scoring epoch."
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "inloop_curves.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    plot(data, FIG / "inloop_curves.png")
    tpl = (FIG / "inloop_curves_template.html").read_text(encoding="utf-8")
    tpl = tpl.replace("__SCORING__", data["scoring_note"]).replace("__RESCORED__", rescored)
    (FIG / "inloop_curves.html").write_text(tpl.replace("__DATA__", json.dumps(data, separators=(",", ":"))), encoding="utf-8")
    for k, s in data["strata"].items():
        print(k, s["n"], {n: (v[0], v[-1]) for n, v in s["lines"].items()})


if __name__ == "__main__":
    main()
