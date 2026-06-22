"""r2py CLI — §9.2"""
from __future__ import annotations

import argparse
import sys


def cmd_analyze(args: argparse.Namespace) -> int:
    from pathlib import Path
    from r2py import analyze
    from r2py.stage1.script_map import save, to_annotated_r

    r_path = Path(args.input)
    sm = analyze(r_path)

    map_path = r_path.with_suffix(".map.json")
    save(sm, map_path)

    ann_path = r_path.with_suffix(".annotated.R")
    ann_path.write_text(to_annotated_r(sm), encoding="utf-8")

    if not getattr(args, "quiet", False):
        print(f"ScriptMap   -> {map_path}")
        print(f"Annotated R -> {ann_path}")
        print(f"Entities: {len(sm.entities)}  "
              f"Effects: {len(sm.effects)}  "
              f"Coverage: {sm.coverage.fraction_analyzed:.0%}")
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    from r2py import translate
    result = translate(
        r_path=args.input,
        py_path=args.output,
        model=args.model,
        max_iters=args.max_iters,
        score_threshold=args.score_threshold,
        use_judge=args.use_judge,
        data_compare=args.data_compare,
        no_seeds=args.no_seeds,
        max_stalls=args.max_stalls,
    )
    print(f"Score: {result.final_score:.3f}  Iterations: {result.iterations}")
    if result.final_exit_code != 0:
        return 1
    return 0


def cmd_library(args: argparse.Namespace) -> int:
    sub = args.library_command
    if sub == "list":
        from r2py.library import get_library
        lib = get_library()
        patterns = list(lib.store.load_all().values())
        if args.package:
            patterns = [p for p in patterns if p.package == args.package]
        if args.confidence:
            patterns = [p for p in patterns if p.confidence == args.confidence]
        if args.kind == "mapping":
            patterns = [p for p in patterns if "→" in p.guidance]
        for p in sorted(patterns, key=lambda x: (x.package or "", x.id)):
            seed_flag = " [seed]" if p.seed else ""
            print(f"{p.id:<45s} {p.confidence:<12s} {p.package or '(none)'}{seed_flag}")
        print(f"\n{len(patterns)} pattern(s) shown.")
        return 0
    elif sub == "show":
        from r2py.library import get_library
        from r2py.library.pattern import to_markdown
        lib = get_library()
        p = lib.store.get(args.pattern_id)
        if p is None:
            print(f"Pattern '{args.pattern_id}' not found.", file=sys.stderr)
            return 1
        # Use buffer directly so non-ASCII characters (e.g. →) survive on
        # Windows terminals without cp1252 encoding errors. Tests that capture
        # this output must read sys.stdout.buffer, not sys.stdout.
        sys.stdout.buffer.write(to_markdown(p).encode("utf-8") + b"\n")
        return 0
    elif sub == "review":
        from r2py.library import get_library
        from r2py.library.epistemology import review
        lib = get_library()
        log = review(lib.store, lib.index)
        for line in log:
            print(line)
        print(f"Review complete: {len(log)} action(s).")
        return 0
    elif sub == "train-reranker":
        from r2py.library.reranker import train as _train
        rc = _train(
            out_dir=args.out,
            min_episodes=args.min_episodes,
        )
        return rc
    raise NotImplementedError(f"Unknown library command: {sub}")


def cmd_harvest(args: argparse.Namespace) -> int:
    from r2py.stage0.harvest.crawler import crawl
    paths = crawl(args.repo_or_url)
    print(f"Harvested {len(paths)} script(s)")
    return 0


def cmd_ablation(args: argparse.Namespace) -> int:
    from r2py.ablation import run_ablation
    summary = run_ablation(
        slice_path=args.slice,
        compare=args.compare,
    )
    print(
        f"n={summary['n_scripts']}  "
        f"mean_delta={summary['mean_delta']:+.3f}  "
        f"p={summary['p_value']:.3f} ({summary['test']})  "
        f"regressions={len(summary['regressions'])}"
    )
    return 0


def main() -> None:
    from r2py.stage2.llm import _DEFAULT_MODEL
    parser = argparse.ArgumentParser(prog="r2py", description="R-to-Python translator")
    parser.add_argument("--quiet", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = sub.add_parser("analyze", help="Analyze an R file and emit a ScriptMap (stage 1)")
    p_analyze.add_argument("input", help="Input .R file")

    # translate
    p_translate = sub.add_parser("translate", help="Translate an R file to Python (full pipeline)")
    p_translate.add_argument("input", help="Input .R file")
    p_translate.add_argument("output", help="Output .py file")
    p_translate.add_argument("--model", default=_DEFAULT_MODEL,
                             help="Model to use: Anthropic model ID or 'ollama:<name>' for local Ollama")
    p_translate.add_argument("--max-iters", type=int, default=8, dest="max_iters")
    p_translate.add_argument("--score-threshold", type=float, default=0.85, dest="score_threshold")
    p_translate.add_argument("--use-judge", action="store_true", dest="use_judge",
                             help="Enable LLM judge fallback (D4; off by default)")
    p_translate.add_argument("--data-compare", default="auto", dest="data_compare",
                             choices=["auto", "exact", "embedding"])
    p_translate.add_argument("--no-seeds", action="store_true", dest="no_seeds",
                             help="Ignore seed:true patterns (transfer experiment §6.7)")
    p_translate.add_argument("--max-stalls", type=int, default=3, dest="max_stalls",
                             help="Consecutive non-improving agent rewrites before stopping (default: 3)")

    # library
    p_lib = sub.add_parser("library", help="Pattern Library operations")
    lib_sub = p_lib.add_subparsers(dest="library_command", required=True)
    p_lib_list = lib_sub.add_parser("list", help="List patterns")
    p_lib_list.add_argument("--package", default=None)
    p_lib_list.add_argument("--confidence", default=None,
                            choices=["confirmed", "tentative", "contradicted"])
    p_lib_list.add_argument("--kind", default=None, choices=["mapping"],
                            help="'mapping' shows the emergent equivalence registry (§6.7)")
    p_lib_show = lib_sub.add_parser("show", help="Show a pattern")
    p_lib_show.add_argument("pattern_id")
    lib_sub.add_parser("review", help="Run epistemology pass")
    p_reranker = lib_sub.add_parser("train-reranker", help="Train offline retrieval reranker (§12.6 A)")
    p_reranker.add_argument("--min-episodes", type=int, default=500, dest="min_episodes")
    p_reranker.add_argument("--out", default="work/models/reranker/")

    # harvest
    p_harvest = sub.add_parser("harvest", help="Harvest R examples from a repo or URL (stage 0)")
    p_harvest.add_argument("repo_or_url")

    # ablation
    p_ablation = sub.add_parser("ablation", help="Run manual stratified ablation experiment (§12.4.1)")
    p_ablation.add_argument("--slice", default="work/inputs/ablation_slice.txt")
    p_ablation.add_argument("--compare", default="frozen-vs-learning",
                            choices=["frozen-vs-learning", "heuristic-vs-learned"])

    args = parser.parse_args()
    dispatch = {
        "analyze":   cmd_analyze,
        "translate": cmd_translate,
        "library":   cmd_library,
        "harvest":   cmd_harvest,
        "ablation":  cmd_ablation,
    }
    sys.exit(dispatch[args.command](args))


if __name__ == "__main__":
    main()
