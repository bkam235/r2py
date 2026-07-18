"""Stage 1 — Script analysis: AST walk, branch extraction, ScriptMap (§3)."""
from __future__ import annotations

import sys
from pathlib import Path

from ..types import CaptureSpec, EffectClass, EntityKind
from .ast import parse
from .branch_extractor import extract_branch, extract_for_branch
from .coverage import CoverageTracker
from .effects import SideEffect
from .entities import AstNode, Entity, FunctionMetadata
from .package_lookup import resolve_symbol
from .runner import DEFAULT_CAPTURE, run_script, run_script_checkpointed, run_slice, strip_r_guards
from .script_map import BranchAnalysis, ScriptMap
from .walker import walk

# Default max sandbox attempts to reach full branch coverage.
_MAX_COVERAGE_ATTEMPTS = 3


def analyze(
    r_path: Path,
    capture: CaptureSpec = DEFAULT_CAPTURE,
    timeout_s: float = 60,
    max_coverage_attempts: int = _MAX_COVERAGE_ATTEMPTS,
) -> ScriptMap:
    """Parse and analyze an R script, returning its populated ScriptMap.

    Analysis procedure (§3.4):
      1. Parse source with tree-sitter-r.
      2. Walk AST: classify entities, predict side-effects, §3.7 annotations.
      3. Run script via Stage 0 sandbox; attach actual EffectBundle to entities.
      4. For each unexecuted branch, build + run a slice; attach BranchAnalysis.
      5. Resolve library() / ExternalSymbol sources (package_lookup).
      6. Repeat step 4 until full coverage or budget exhausted.
      7. Return ScriptMap.
    """
    r_path = Path(r_path)
    source = r_path.read_text(encoding="utf-8")
    source_file = str(r_path)

    # ── Step 1: parse ────────────────────────────────────────────────────────
    ast_root = parse(source)

    # ── Step 2: static walk ──────────────────────────────────────────────────
    tracker = CoverageTracker()
    entities, predicted_effects = walk(ast_root, source_file, tracker)

    # ── Step 3: dynamic run with per-entity checkpoints ─────────────────────
    main_bundle, entity_bundles, entity_types = run_script_checkpointed(
        source, entities, capture=capture, timeout_s=timeout_s
    )
    for eid in entities:
        tracker.mark(eid, "dynamic")
        entities[eid].actual_bundle = main_bundle

    # ── Step 3b: probe for inherited free variables ──────────────────────────
    # R built-in datasets (volcano, iris, …) are accessed by bare name but live
    # in package:datasets — NOT in .GlobalEnv.  The main capture misses them.
    # Collect every free_variable_ref that wasn't captured, then run a small R
    # probe that pulls each one from the search path into .GlobalEnv so the
    # standard epilogue serialises it normally.
    _all_free_refs: set[str] = set()
    for _e in entities.values():
        _all_free_refs.update(_e.free_variable_refs)
    _uncaptured = _all_free_refs - set(main_bundle.data.keys())
    if _uncaptured:
        _imported_pkgs = [
            _e.package for _e in entities.values()
            if _e.kind == EntityKind.LIBRARY_IMPORT and _e.package
        ]
        _extra = _probe_inherited_vars(_uncaptured, timeout_s, packages=_imported_pkgs)
        main_bundle.data.update(_extra)

    # ── Step 4 + 6: branch extraction loop ──────────────────────────────────
    branches: dict[str, BranchAnalysis] = {}
    _extract_branches(ast_root, entities, main_bundle,
                      branches, tracker, capture, timeout_s,
                      max_coverage_attempts,
                      entity_bundles=entity_bundles,
                      source=source)

    # ── Step 5: resolve external sources ────────────────────────────────────
    external_sources = {}
    for eid, entity in entities.items():
        if entity.kind in (EntityKind.LIBRARY_IMPORT, EntityKind.EXTERNAL_SYMBOL):
            pkg = entity.package
            if pkg:
                loc = resolve_symbol(pkg, entity.name)
                if loc:
                    external_sources[eid] = loc

    # ── Step 5b: resolve positional arg bindings via match.call() ─────────
    _resolve_arg_bindings(source, entities, timeout_s)

    # ── Step 5c: probe function metadata (formals, methods, namespace) ───
    _probe_function_metadata(source, entities, timeout_s)

    # ── Step 5d: backfill entity.package from function_metadata.where ───
    _backfill_package_from_metadata(entities)

    # ── Step 7: build ScriptMap ──────────────────────────────────────────────
    all_effects = _merge_dynamic_effects(list(predicted_effects), main_bundle, entities)

    return ScriptMap(
        source=source,
        ast_root=ast_root,
        entities=entities,
        effects=all_effects,
        branches=branches,
        external_sources=external_sources,
        coverage=tracker.report(),
        entity_bundles=entity_bundles,
        entity_types=entity_types,
    )


def _entities_in_node(node: AstNode, entities: dict[str, Entity]) -> list[str]:
    """Return entity ids whose source spans are strictly inside *node*'s span."""
    ns_row, ns_col = node.start
    ne_row, ne_col = node.end
    result = []
    for eid, entity in entities.items():
        sp = entity.source_span
        starts_inside = (sp.start_line > ns_row or
                         (sp.start_line == ns_row and sp.start_col >= ns_col))
        ends_inside = (sp.end_line < ne_row or
                       (sp.end_line == ne_row and sp.end_col <= ne_col))
        if starts_inside and ends_inside:
            result.append(eid)
    return result


def _build_lib_preamble(entities: dict[str, Entity], source: str) -> str:
    """Build R preamble that loads libraries from LIBRARY_IMPORT entities."""
    lines = source.splitlines()
    lib_lines: list[str] = []
    for entity in entities.values():
        if entity.kind == EntityKind.LIBRARY_IMPORT:
            sp = entity.source_span
            lib_call = "\n".join(lines[sp.start_line:sp.end_line + 1]).strip()
            if lib_call:
                lib_lines.append(f"suppressPackageStartupMessages({lib_call})")
    if lib_lines:
        return "\n".join(lib_lines) + "\n\n"
    return ""


def _extract_branches(
    ast_root: AstNode,
    entities: dict[str, Entity],
    main_bundle,
    branches: dict[str, BranchAnalysis],
    tracker: CoverageTracker,
    capture: CaptureSpec,
    timeout_s: float,
    max_attempts: int,
    entity_bundles: dict[str, "EffectBundle"] | None = None,
    source: str = "",
) -> None:
    """Find if/else and loop branches; force-execute untaken ones as slices.

    When *entity_bundles* is provided, infers which branches were actually
    taken during the main run (any contained entity with a checkpoint →
    branch was taken).  Untaken branches are force-executed via ``run_slice``
    and their effects are merged into *entity_bundles* so Stage 4 scores
    against real effects instead of empty-vs-empty.
    """
    branch_nodes = _collect_branch_nodes(ast_root, entities)

    # Detect which branches were actually executed from entity checkpoint data.
    if entity_bundles:
        resolved = []
        for branch_id, branch_node, parent_eid, cond_text, was_executed in branch_nodes:
            if not was_executed:
                contained = _entities_in_node(branch_node, entities)
                if any(eid in entity_bundles for eid in contained):
                    was_executed = True
            resolved.append((branch_id, branch_node, parent_eid, cond_text, was_executed))
        branch_nodes = resolved

    lib_preamble = _build_lib_preamble(entities, source) if source else ""

    attempt = 0
    pending = branch_nodes

    while pending and attempt < max_attempts:
        attempt += 1
        still_pending = []
        for branch_id, branch_node, parent_entity_id, condition_text, was_executed in pending:
            if was_executed:
                tracker.mark(branch_id, "dynamic")
                continue

            # Choose extractor based on node kind.
            if branch_node.kind == "for_statement":
                slice_source = extract_for_branch(branch_node, entities, main_bundle)
            else:
                slice_source = extract_branch(branch_node, entities, main_bundle)
            if slice_source is None:
                # Cannot synthesize a slice for this node; mark unreachable.
                tracker.mark(branch_id, "unreachable")
                branches[branch_id] = BranchAnalysis(
                    branch_id=branch_id,
                    parent_entity_id=parent_entity_id,
                    condition_text=condition_text,
                    was_executed=False,
                    runnable_slice=None,
                    bundle=None,
                )
                continue

            # Wrap in invisible() to prevent auto-printing of objects
            # that start blocking operations (e.g. shinyApp → runApp).
            wrapped_source = f"invisible({{\n{slice_source}\n}})"
            full_slice = lib_preamble + wrapped_source if lib_preamble else wrapped_source

            bundle = None
            try:
                bundle = run_slice(
                    full_slice,
                    capture=capture,
                    timeout_s=min(timeout_s, 30),
                )
                tracker.mark(branch_id, "branch-extracted")

                # Merge branch effects into entity_bundles for entities inside
                # this branch that had no checkpoint during the main run.
                if entity_bundles is not None:
                    contained = _entities_in_node(branch_node, entities)
                    for eid in contained:
                        if eid not in entity_bundles:
                            entity_bundles[eid] = bundle
            except Exception:
                tracker.mark(branch_id, "unreachable")

            branches[branch_id] = BranchAnalysis(
                branch_id=branch_id,
                parent_entity_id=parent_entity_id,
                condition_text=condition_text,
                was_executed=was_executed,
                runnable_slice=slice_source,
                bundle=bundle,
            )
        pending = still_pending


def _collect_branch_nodes(
    ast_root: AstNode,
    entities: dict[str, Entity],
) -> list[tuple[str, AstNode, str, str, bool]]:
    """Walk the AST and collect (branch_id, node, parent_eid, condition, was_executed) tuples.

    Collects both if-body (consequence) and else-body (alternative) branches
    of ``if_statement`` nodes, plus for and while loop bodies.
    """
    results: list[tuple[str, AstNode, str, str, bool]] = []
    _collect_branch_nodes_rec(ast_root, results, counter=[0], entities=entities)
    return results


def _collect_branch_nodes_rec(
    node: AstNode,
    out: list,
    counter: list[int],
    entities: dict[str, Entity],
) -> None:
    if node.kind == "if_statement":
        condition_node = node.child_by_field("condition")
        condition_text = condition_node.text if condition_node else ""

        row = node.start[0]
        parent_eid = ""
        for eid, entity in entities.items():
            sp = entity.source_span
            if sp.start_line <= row <= sp.end_line:
                parent_eid = eid
                break

        # Collect consequence (if-body) — not executed when condition is FALSE.
        consequence_node = node.child_by_field("consequence")
        if consequence_node is not None:
            branch_id = f"if_branch_{counter[0]}"
            counter[0] += 1
            out.append((branch_id, consequence_node, parent_eid, condition_text, False))

        # Collect alternative (else-body) — not executed when condition is TRUE.
        alt_node = node.child_by_field("alternative")
        if alt_node is not None:
            branch_id = f"branch_{counter[0]}"
            counter[0] += 1
            out.append((branch_id, alt_node, parent_eid, condition_text, False))

    if node.kind == "for_statement":
        body_node = node.child_by_field("body")
        if body_node is not None:
            branch_id = f"for_branch_{counter[0]}"
            counter[0] += 1
            row = node.start[0]
            parent_eid = ""
            for eid, entity in entities.items():
                sp = entity.source_span
                if sp.start_line <= row <= sp.end_line:
                    parent_eid = eid
                    break
            # was_executed=False so the extractor always runs a synthetic slice.
            # condition_text uses the for header as the "condition".
            seq_node = node.child_by_field("sequence")
            condition_text = f"for ({node.child_by_field('variable').text if node.child_by_field('variable') else '?'} in {seq_node.text if seq_node else '?'})"
            out.append((branch_id, node, parent_eid, condition_text, False))

    if node.kind == "while_statement":
        body_node = node.child_by_field("body")
        if body_node is not None:
            branch_id = f"while_branch_{counter[0]}"
            counter[0] += 1
            row = node.start[0]
            parent_eid = ""
            for eid, entity in entities.items():
                sp = entity.source_span
                if sp.start_line <= row <= sp.end_line:
                    parent_eid = eid
                    break
            condition_node = node.child_by_field("condition")
            condition_text = f"while({condition_node.text if condition_node else '...'})"
            out.append((branch_id, body_node, parent_eid, condition_text, False))

    for child in node.children:
        _collect_branch_nodes_rec(child, out, counter, entities)


def _probe_inherited_vars(
    names: set[str], timeout_s: float, *, packages: list[str] | None = None,
) -> dict:
    """Capture R values that exist on the search path but not in .GlobalEnv.

    For each name in *names*, if R can find it via ``exists(name, inherits=TRUE)``
    (i.e. it's a lazy-loaded built-in dataset, an object from an attached package,
    etc.) and it is not a function or environment, assign it into .GlobalEnv so
    the standard Stage 0 data-capture epilogue picks it up.

    *packages* are loaded first so package-exported datasets (e.g. dplyr::storms)
    are on the search path.

    Returns a dict of name → captured value (same format as EffectBundle.data).
    """
    if not names:
        return {}

    lib_lines = ""
    for pkg in (packages or []):
        lib_lines += f'suppressPackageStartupMessages(library({pkg}))\n'

    r_names = "c(" + ", ".join(f'"{n}"' for n in sorted(names)) + ")"
    probe_source = f"""\
{lib_lines}for (.r2py_v in {r_names}) {{
  if (exists(.r2py_v, inherits = TRUE) && !.r2py_v %in% ls(envir = .GlobalEnv)) {{
    .r2py_obj <- get(.r2py_v, inherits = TRUE)
    if (!is.function(.r2py_obj) && !is.environment(.r2py_obj)) {{
      assign(.r2py_v, .r2py_obj, envir = .GlobalEnv)
    }}
  }}
}}
"""
    probe_capture: CaptureSpec = frozenset({EffectClass.DATA})
    try:
        bundle = run_slice(probe_source, capture=probe_capture, timeout_s=timeout_s)
        return bundle.data
    except Exception:
        return {}


def _resolve_arg_bindings(
    source: str,
    entities: dict[str, Entity],
    timeout_s: float,
) -> None:
    """Use R's match.call() to resolve positional args to formal names.

    For each FUNCTION_CALL / EXTERNAL_SYMBOL entity, runs match.call(fn, quote(call))
    in R and stores the deparsed result on entity.resolved_call.  Modifies entities
    in place.  Degrades gracefully: on any failure, entities keep resolved_call=None.
    """
    import re

    targets: list[tuple[str, Entity, str]] = []
    for eid, entity in entities.items():
        if entity.kind not in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            continue
        span = entity.source_span
        r_lines = source.splitlines()[span.start_line:span.end_line + 1]
        r_call = " ".join(l.strip() for l in r_lines)
        if not r_call or "(" not in r_call:
            continue
        targets.append((eid, entity, r_call))

    if not targets:
        return

    # Extract library() calls to load packages before match.call.
    lib_lines: list[str] = []
    for eid, entity in entities.items():
        if entity.kind == EntityKind.LIBRARY_IMPORT:
            span = entity.source_span
            lib_lines.append(
                " ".join(source.splitlines()[span.start_line:span.end_line + 1])
            )

    # Build the probe script.
    parts: list[str] = []
    for lib_call in lib_lines:
        parts.append(f"tryCatch(suppressPackageStartupMessages({lib_call}), error=function(e) NULL)")

    # Also source function definitions from the script so match.call works for
    # in-script functions.  Extract only FUNCTION_DEF entities.
    for eid, entity in entities.items():
        if entity.kind == EntityKind.FUNCTION_DEF:
            span = entity.source_span
            fn_lines = source.splitlines()[span.start_line:span.end_line + 1]
            fn_src = "\n".join(fn_lines)
            parts.append(f"tryCatch({{\n{fn_src}\n}}, error=function(e) NULL)")

    for eid, entity, r_call in targets:
        fn_name = entity.name
        safe_eid = eid.replace('"', '\\"')
        # Try method-level match.call first (e.g. chunk.default for S3 dispatch),
        # then fall back to the generic.  Method-level resolution is more informative
        # because it resolves positional args against the full method signature
        # (including args that the generic hides behind ...).
        parts.append(
            f'tryCatch({{\n'
            f'  .r2py_method <- tryCatch(getS3method("{fn_name}", "default"), error=function(e) NULL)\n'
            f'  if (!is.null(.r2py_method)) {{\n'
            f'    .r2py_mcall <- quote({r_call})\n'
            f'    .r2py_mcall[[1]] <- as.name("{fn_name}.default")\n'
            f'    .r2py_resolved <- deparse(match.call(.r2py_method, .r2py_mcall))\n'
            f'  }} else {{\n'
            f'    .r2py_resolved <- deparse(match.call({fn_name}, quote({r_call})))\n'
            f'  }}\n'
            f'  cat(paste0("__R2PY_MATCH__{safe_eid}__", paste(.r2py_resolved, collapse=" "), "\\n"))\n'
            f'}}, error=function(e) NULL)'
        )

    probe_source = "\n".join(parts)

    try:
        bundle = run_slice(probe_source, capture=frozenset({EffectClass.STDOUT}),
                           timeout_s=min(timeout_s, 15))
        stdout = getattr(bundle, "stdout", "") or ""
    except Exception:
        return

    marker = "__R2PY_MATCH__"
    for line in stdout.splitlines():
        if not line.startswith(marker):
            continue
        rest = line[len(marker):]
        sep_idx = rest.find("__")
        if sep_idx < 0:
            continue
        eid = rest[:sep_idx]
        resolved = rest[sep_idx + 2:].strip()
        if not resolved:
            continue
        # Strip .default/.numeric/etc. suffix from the function name so the
        # LLM sees the generic name it needs to call in Python.
        for target_eid, entity, _ in targets:
            if target_eid == eid:
                import re as _re
                resolved = _re.sub(
                    r'^(\w+)\.\w+\(', lambda m: m.group(1) + '(', resolved
                )
                entity.resolved_call = resolved
                break


def _probe_function_metadata(
    source: str,
    entities: dict[str, Entity],
    timeout_s: float,
) -> None:
    """Probe formals(), methods(), and getAnywhere()$where for function-call entities.

    Populates entity.function_metadata in place.  Degrades gracefully: on any
    failure the entity keeps function_metadata=None.
    """
    import json as _json

    targets: list[tuple[str, Entity]] = []
    for eid, entity in entities.items():
        if entity.kind not in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            continue
        targets.append((eid, entity))

    if not targets:
        return

    # Load packages so probed functions are available.
    parts: list[str] = []
    for eid, entity in entities.items():
        if entity.kind == EntityKind.LIBRARY_IMPORT:
            span = entity.source_span
            lib_call = " ".join(source.splitlines()[span.start_line:span.end_line + 1])
            parts.append(f"tryCatch(suppressPackageStartupMessages({lib_call}), error=function(e) NULL)")

    # Source function definitions from the script.
    for eid, entity in entities.items():
        if entity.kind == EntityKind.FUNCTION_DEF:
            span = entity.source_span
            fn_lines = source.splitlines()[span.start_line:span.end_line + 1]
            parts.append(f"tryCatch({{\n{chr(10).join(fn_lines)}\n}}, error=function(e) NULL)")

    seen_names: set[str] = set()
    for eid, entity in targets:
        fn_name = entity.name
        if fn_name in seen_names:
            continue
        seen_names.add(fn_name)
        safe_eid = eid.replace('"', '\\"')
        parts.append(
            f'tryCatch({{\n'
            f'  .r2py_fm <- list()\n'
            f'  .r2py_f <- tryCatch(formals({fn_name}), error=function(e) NULL)\n'
            f'  if (!is.null(.r2py_f)) .r2py_fm$formals <- lapply(.r2py_f, function(x) if(missing(x)) "" else deparse(x))\n'
            f'  .r2py_m <- tryCatch(as.character(methods({fn_name})), error=function(e) character(0))\n'
            f'  .r2py_fm$methods <- .r2py_m\n'
            f'  .r2py_w <- tryCatch(getAnywhere("{fn_name}")$where, error=function(e) character(0))\n'
            f'  .r2py_fm$where <- .r2py_w\n'
            f'  cat(paste0("__R2PY_META__{safe_eid}__", '
            f'jsonlite::toJSON(.r2py_fm, auto_unbox=TRUE), "\\n"))\n'
            f'}}, error=function(e) NULL)'
        )

    probe_source = "\n".join(parts)

    try:
        bundle = run_slice(probe_source, capture=frozenset({EffectClass.STDOUT}),
                           timeout_s=min(timeout_s, 15))
        stdout = getattr(bundle, "stdout", "") or ""
    except Exception:
        return

    marker = "__R2PY_META__"
    # Build eid→FunctionMetadata, then assign to all entities with the same function name.
    name_to_meta: dict[str, FunctionMetadata] = {}
    for line in stdout.splitlines():
        if not line.startswith(marker):
            continue
        rest = line[len(marker):]
        sep_idx = rest.find("__")
        if sep_idx < 0:
            continue
        eid = rest[:sep_idx]
        json_str = rest[sep_idx + 2:].strip()
        if not json_str:
            continue
        try:
            data = _json.loads(json_str)
        except _json.JSONDecodeError:
            continue
        formals_raw = data.get("formals", {})
        formals = {k: (v if isinstance(v, str) else str(v)) for k, v in formals_raw.items()}
        methods = data.get("methods", [])
        where = data.get("where", [])
        if isinstance(methods, str):
            methods = [methods]
        if isinstance(where, str):
            where = [where]
        fm = FunctionMetadata(formals=formals, methods=methods, where=where)
        # Find the function name for this eid and store by name.
        for target_eid, entity in targets:
            if target_eid == eid:
                name_to_meta[entity.name] = fm
                break

    # Assign to all matching entities (multiple call sites for the same function).
    for eid, entity in targets:
        if entity.name in name_to_meta:
            entity.function_metadata = name_to_meta[entity.name]


def _backfill_package_from_metadata(entities: dict[str, Entity]) -> None:
    """Set entity.package from function_metadata.where when still None.

    The walker only sets package for pkg::fn() calls.  For bare calls like
    which(), the R probe already collected getAnywhere()$where — e.g.
    ["package:base", "namespace:base"].  Extract the first "package:X" entry
    and use it.  Skip ".GlobalEnv" (user-defined functions).
    """
    for entity in entities.values():
        if entity.package is not None:
            continue
        fm = entity.function_metadata
        if fm is None or not fm.where:
            continue
        for w in fm.where:
            if w.startswith("package:"):
                entity.package = w[len("package:"):]
                break


def _merge_dynamic_effects(
    predicted: list[SideEffect],
    main_bundle,
    entities: dict[str, Entity],
) -> list[SideEffect]:
    """Attach main_bundle to every predicted SideEffect; add DATA if variables captured."""
    updated: list[SideEffect] = []
    for ef in predicted:
        updated.append(SideEffect(
            kind=ef.kind,
            entity_id=ef.entity_id,
            is_predicted=ef.is_predicted,
            actual_bundle=main_bundle,
        ))
    # If the sandbox captured data variables, add a DATA side-effect on the program.
    if main_bundle.data:
        # Attribute to the first entity (the program-level proxy) if any.
        first_eid = next(iter(entities), "program")
        updated.append(SideEffect(
            kind=EffectClass.DATA,
            entity_id=first_eid,
            is_predicted=False,
            actual_bundle=main_bundle,
        ))
    return updated
