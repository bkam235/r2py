"""r2py v0.2 — R-to-Python execution-verified translator."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import ScriptMap, TranslateResult

__version__ = "0.2.0"
__all__ = ["translate", "analyze", "review_library", "reset_library"]


def translate(
    r_path: "str | Path",
    py_path: "str | Path",
    *,
    library=None,                    # inject a PatternLibrary (or _FrozenLibrary); None → get_library()
    model: "str | None" = None,  # Anthropic model ID, or "ollama:<name>" for local Ollama; None → _DEFAULT_MODEL
    max_iters: int = 8,
    score_threshold: float = 0.85,
    beam_width: int = 4,
    use_judge: bool = False,         # D4: LLM judge off by default
    learned_retrieval: bool = False, # D6: learned reranker (§12.6 A); off by default
    learned_policy: bool = False,    # D6: learned edit policy (§12.6 B); off by default
    data_compare: str = "auto",      # "auto" | "exact" | "embedding"
    sandbox: str = "subprocess",
    no_seeds: bool = False,          # ignore seed:true patterns (§6.7 transfer experiment)
    output_dir: "str | Path | None" = None,  # if set, write edits.log.jsonl + library_diff.json
    progress=None,                   # callable(ProgressEvent) for progress reporting; None = silent
    retranslation_patience: int = 3, # retranslate from scratch after this many stalled iterations (0 = disabled)
    resume: bool = False,            # if True and py_path exists, continue improving it; if False and py_path exists, warn
) -> "TranslateResult":
    """Translate an R script to Python via the beam/strict-improvement loop (§4.1)."""
    import sys
    from pathlib import Path
    from .stage1 import analyze as _analyze
    from .library import get_library
    from .loop import run_loop, _emit
    from .stage2.llm import _DEFAULT_MODEL
    if model is None:
        model = _DEFAULT_MODEL

    if library is None:
        library = get_library()

    _py_path = Path(py_path)
    seed_translation: "str | None" = None
    if resume and _py_path.exists():
        seed_translation = _py_path.read_text(encoding="utf-8")
    elif not resume and _py_path.exists():
        print(
            f"r2py: warning: {py_path} already exists and will be overwritten "
            f"(pass resume=True to continue improving it instead).",
            file=sys.stderr,
        )

    script_map = _analyze(Path(r_path))
    _emit(progress, kind="analysis_done",
          entity_count=len(getattr(script_map, "entities", None) or {}))

    result = run_loop(
        script_map,
        library,
        max_iters=max_iters,
        score_threshold=score_threshold,
        beam_width=beam_width,
        use_judge=use_judge,
        data_compare=data_compare,
        no_seeds=no_seeds,
        learned_retrieval=learned_retrieval,
        learned_policy=learned_policy,
        output_dir=Path(output_dir) if output_dir is not None else None,
        checkpoint_path=Path(py_path),
        model=model,
        progress=progress,
        retranslation_patience=retranslation_patience,
        seed_translation=seed_translation,
    )
    Path(py_path).write_text(result.python_source, encoding="utf-8")
    _write_translation_log(Path(py_path), script_map, result)
    if result.final_exit_code != 0:
        print(
            f"r2py: warning: final Python translation crashed "
            f"(exit {result.final_exit_code}); output written to {py_path} "
            f"but may not run correctly. Score: {result.final_score:.3f}",
            file=sys.stderr,
        )
    return result


def analyze(r_path: "str | Path") -> "ScriptMap":
    """Analyze an R script and return its ScriptMap (§3)."""
    from pathlib import Path
    from .stage1 import analyze as _analyze
    return _analyze(Path(r_path))


def reset_library(library=None, keep_seeds: bool = True) -> int:
    """Delete all learned patterns from the library and rebuild the index.

    Args:
        keep_seeds: If True (default), seed patterns are preserved.
                    If False, every pattern including seeds is removed.
    Returns:
        Number of patterns removed.
    """
    from .library import get_library
    if library is None:
        library = get_library()

    store = library.store
    index = library.index

    patterns = store.load_all()
    removed = 0
    for pid, pat in patterns.items():
        if keep_seeds and pat.seed:
            continue
        # Delete the markdown file from disk
        path = store._path(pid)
        if path.exists():
            path.unlink()
        removed += 1

    # Rebuild the index from whatever files remain, and reset the run counter
    index.rebuild(store)
    index._data["total_runs"] = 0
    index._save()

    return removed


def _write_translation_log(
    py_path: "Path",
    script_map: "ScriptMap",
    result: "TranslateResult",
) -> None:
    """Write a human-readable comparison log next to the output .py file."""
    log_path = py_path.with_suffix(".log")
    report = result.final_score_report
    entities = getattr(script_map, "entities", {}) or {}

    # Build entity_line_map from the final Python source to extract py snippets.
    try:
        from .stage2.stitch import rebuild_entity_line_map as _rebuild
        elmap = _rebuild(result.python_source)
    except Exception:
        elmap = {}

    lines: list[str] = [
        "Translation log",
        f"Final score: {result.final_score:.3f}",
        f"Iterations:  {result.iterations}",
        "",
    ]

    for eid, entity in entities.items():
        kind = getattr(getattr(entity, "kind", None), "value", "unknown")
        name = getattr(entity, "name", eid)

        # R source snippet
        r_snippet = ""
        span = getattr(entity, "source_span", None)
        if span is not None and script_map.source:
            src_lines = script_map.source.splitlines()
            start = getattr(span, "start_line", 0)
            end = min(len(src_lines), getattr(span, "end_line", start) + 1)
            r_snippet = "\n".join(src_lines[start:end])

        # Python snippet
        py_snippet = ""
        if eid in elmap:
            py_start, py_end = elmap[eid]
            py_lines = result.python_source.splitlines()
            py_snippet = "\n".join(py_lines[py_start:py_end])

        # Per-entity score (average of the six EntityScore fields)
        score = None
        if report is not None:
            es = report.by_entity.get(eid)
            if es is not None:
                score = (
                    es.type_match + es.control_flow_match + es.data_output
                    + es.variable_output + es.callable_output + es.side_effects
                ) / 6

        lines.append("=" * 60)
        lines.append(f"Entity: {eid}")
        lines.append(f"  Name:  {name}")
        lines.append(f"  Kind:  {kind}")
        if score is not None:
            lines.append(f"  Score: {score:.3f}")
        lines.append("")
        if r_snippet:
            lines.append("  R:")
            for ln in r_snippet.splitlines():
                lines.append(f"    {ln}")
        if py_snippet:
            lines.append("  Python:")
            for ln in py_snippet.splitlines():
                lines.append(f"    {ln}")
        lines.append("")

    log_path.write_text("\n".join(lines), encoding="utf-8")


def review_library(library=None, prune_unimproved: bool = False) -> list[str]:
    """Manually trigger a library epistemology review.

    Set prune_unimproved=True to immediately archive all patterns that have
    zero real improvement evidence regardless of run count (Fix D cleanup).
    """
    from .library import get_library
    from .library import epistemology as _epi
    if library is None:
        library = get_library()
    if prune_unimproved:
        return _epi.prune_unimproved(library.store, library.index)
    return _epi.review(library.store, library.index)
