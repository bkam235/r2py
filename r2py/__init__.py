"""r2py v0.2 — R-to-Python execution-verified translator."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import ScriptMap, TranslateResult

__version__ = "0.2.0"
__all__ = ["translate", "analyze", "review_library", "reset_library", "seed_from_translation"]


def translate(
    r_path: "str | Path",
    py_path: "str | Path",
    *,
    library=None,                    # inject a PatternLibrary (or _FrozenLibrary); None → get_library()
    model: "str | None" = None,      # cheap model for seed translation; None → _DEFAULT_MODEL
    escalation_model: "str | None" = None,  # stronger model for reasoning agent; None → model
    max_iters: int = 20,
    score_threshold: float = 0.85,
    use_judge: bool = False,         # D4: LLM judge off by default
    data_compare: str = "auto",      # "auto" | "exact" | "embedding"
    no_seeds: bool = False,          # ignore seed:true patterns (§6.7 transfer experiment)
    n_seeds: int = 3,                # cheap seeds to try before agent escalation (best-of-N)
    output_dir: "str | Path | None" = None,  # if set, write edits.log.jsonl + library_diff.json
    progress=None,                   # callable(ProgressEvent) for progress reporting; None = silent
    resume: bool = False,            # if True and py_path exists, continue improving it; if False and py_path exists, warn
    timeout_s: float = 60,           # per-execution timeout in seconds for sandbox runs
) -> "TranslateResult":
    """Translate an R script to Python via cheap path + reasoning agent escalation."""
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
        use_judge=use_judge,
        data_compare=data_compare,
        no_seeds=no_seeds,
        n_seeds=n_seeds,
        output_dir=Path(output_dir) if output_dir is not None else None,
        checkpoint_path=Path(py_path),
        model=model,
        escalation_model=escalation_model or model,
        progress=progress,
        seed_translation=seed_translation,
        timeout_s=timeout_s,
    )
    Path(py_path).write_text(result.python_source, encoding="utf-8")
    _write_translation_log(Path(py_path), script_map, result)
    _append_run_record(Path(r_path), result, model, escalation_model or model)
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


def seed_from_translation(
    r_path: "str | Path",
    py_path: "str | Path",
    *,
    library=None,
    script_id: str = "human-verified",
) -> list[str]:
    """Seed the Pattern Library with entity-level examples from a known-good Python file.

    For each entity in the R script whose Python translation in py_path is
    non-trivial (not a bare `pass` stub):
      - Finds the best-matching existing pattern and attaches a TranslationExample.
      - When no same-package pattern exists, creates a new seed pattern so the
        example is retrievable on the next run.

    Returns a list of pattern IDs that were created or updated.

    Use this after a successful translation run to permanently encode what worked
    into the library, so future translations of similar scripts benefit immediately
    from Stage 2 rather than having to rediscover the solution through editing.
    """
    import re
    from datetime import date
    from pathlib import Path
    from .stage1 import analyze as _analyze
    from .library import get_library
    from .library.pattern import Pattern, TranslationExample, r_snippet_hash
    from .library.writer import _add_translation_example
    from .stage2.stitch import rebuild_entity_line_map as _rebuild
    from .loop import _entity_r_snippet, _extract_entity_snippet

    from collections import defaultdict

    if library is None:
        library = get_library()

    script_map = _analyze(Path(r_path))
    py_source = Path(py_path).read_text(encoding="utf-8")
    elmap = _rebuild(py_source)
    entities = getattr(script_map, "entities", {})

    from .types import EntityKind as _EK

    # --- Pass 1: collect valid (eid, entity, r_snip, py_snip) tuples ----------
    valid: list[tuple] = []
    for eid, entity in entities.items():
        # LibraryImport entities are R-package loads with no meaningful Python
        # translation; skip them to avoid creating stub patterns like 'withr.withr'.
        if getattr(entity, "kind", None) == _EK.LIBRARY_IMPORT:
            continue
        r_snip = _entity_r_snippet(entity, script_map)
        py_snip = _extract_entity_snippet(py_source, elmap, eid)
        if not r_snip or not py_snip.strip():
            continue
        # Skip entities whose translation is substantively just `pass` (possibly
        # surrounded by comments) — they carry no useful Python example.
        code_lines = [l for l in py_snip.splitlines()
                      if l.strip() and not l.strip().startswith("#")]
        if not code_lines or all(l.strip() in ("pass", "pass  # untranslatable") or
                                  l.strip().startswith("pass  #") for l in code_lines):
            continue
        valid.append((eid, entity, r_snip, py_snip))

    # --- Pass 2: group by entity name ----------------------------------------
    # When multiple entities share the same name (e.g. 7× with_locale), we want
    # ONE pattern for the concept, not N patterns for N call sites.
    # Pick the "definer" — the entity whose py_snip contains `def <name>(` —
    # as the representative. Fall back to the first entity in declaration order.
    by_name: dict[str, list[tuple]] = defaultdict(list)
    for item in valid:
        eid, entity, r_snip, py_snip = item
        name = getattr(entity, "name", eid) or eid
        by_name[name].append(item)

    # Build the de-duplicated list: one representative per entity name.
    representatives: list[tuple] = []
    for name, group in by_name.items():
        if len(group) == 1:
            representatives.append(group[0])
        else:
            py_name = name.replace("::", ".").replace(".", "_")
            definer = next(
                (item for item in group if f"def {py_name}(" in item[3]),
                group[0],  # fallback: first entity in topological order
            )
            representatives.append(definer)

    # --- Pass 3: attach or create one pattern per representative --------------
    touched: list[str] = []
    created_ids: set[str] = set()

    for eid, entity, r_snip, py_snip in representatives:
        entity_pkg = getattr(entity, "package", "") or ""
        entity_name = getattr(entity, "name", eid) or eid

        ex = TranslationExample(
            r_hash=r_snippet_hash(r_snip),
            r_snippet=r_snip[:300],
            py_snippet=py_snip[:600],
            score=1.0,   # human-verified: full confidence
            script_id=script_id,
        )

        # Prefer an existing package-matched pattern.
        patterns = library.retrieve(entity, k=3)
        matched = next((p for p in patterns if p.package == entity_pkg), None)

        if matched:
            pat = library.store.get(matched.id)
            if pat is not None:
                _add_translation_example(pat, ex)
                library.store.save(pat)
                if matched.id not in touched:
                    touched.append(matched.id)
                continue

        # No package-matched pattern — create a seed (seed=True bypasses the
        # evidence-count gate so it is immediately retrievable).
        # Use entity_name (not eid) for the ID so the pattern is named after
        # the R concept, not the script-local entity numbering.
        raw_id = f"{entity_pkg}.{entity_name}" if entity_pkg else entity_name
        base_id = re.sub(r"[^a-z0-9.\-]", "-", raw_id.lower())[:60]
        pat_id = base_id
        suffix = 0
        while library.store.get(pat_id) is not None or pat_id in created_ids:
            suffix += 1
            pat_id = f"{base_id}-{suffix}"

        kind_str = getattr(getattr(entity, "kind", None), "value", "entity")
        pkg_display = entity_pkg or "base R"
        guidance = (
            f"Translate R `{entity_name}` ({kind_str} from {pkg_display}) to Python. "
            f"See verified example below — prefer it over guessing from the R source alone."
        )
        pat = Pattern(
            id=pat_id,
            package=entity_pkg,
            confidence="tentative",
            seed=True,
            guidance=guidance,
            created=date.today().isoformat(),
            last_review=date.today().isoformat(),
        )
        _add_translation_example(pat, ex)
        library.store.save(pat)
        created_ids.add(pat_id)
        touched.append(pat_id)

    if touched:
        library.index.rebuild(library.store)

    return touched


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


def _append_run_record(
    r_path: "Path",
    result: "TranslateResult",
    model: str,
    escalation_model: str,
) -> None:
    """Append a JSONL record to work/analysis/run_history.jsonl."""
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    history_path = Path(__file__).resolve().parent.parent / "work" / "analysis" / "run_history.jsonl"
    history_path.parent.mkdir(parents=True, exist_ok=True)

    report = result.final_score_report
    by_effect = {}
    if report is not None:
        from .types import EffectClass
        by_effect = {ec.value: score for ec, score in report.by_effect.items()}

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": r_path.stem,
        "final_score": result.final_score,
        "iterations": result.iterations,
        "exit_code": result.final_exit_code,
        "entity_count": len(report.by_entity) if report else 0,
        "by_effect": by_effect,
        "model": model,
        "escalation_model": escalation_model,
    }
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


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

    from .types import EffectClass
    data_score = report.by_effect.get(EffectClass.DATA) if report is not None else None
    files_score = report.by_effect.get(EffectClass.FILES) if report is not None else None

    lines: list[str] = [
        "Translation log",
        f"Final score: {result.final_score:.3f}",
        *([f"Data score:  {data_score:.3f}"] if data_score is not None else []),
        *([f"Files score: {files_score:.3f}"] if files_score is not None else []),
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
