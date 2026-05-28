"""Stage 1 — Script analysis: AST walk, branch extraction, ScriptMap (§3)."""
from __future__ import annotations

import sys
from pathlib import Path

from ..types import CaptureSpec, EffectClass, EntityKind
from .ast import parse
from .branch_extractor import extract_branch
from .coverage import CoverageTracker
from .effects import SideEffect
from .entities import AstNode, Entity
from .package_lookup import resolve_symbol
from .runner import DEFAULT_CAPTURE, run_script, run_slice
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

    # ── Step 3: dynamic run ──────────────────────────────────────────────────
    main_bundle = None
    try:
        main_bundle = run_script(r_path, capture=capture, timeout_s=timeout_s)
        # Mark all known entities as dynamically confirmed.
        for eid in entities:
            tracker.mark(eid, "dynamic")
            entities[eid].actual_bundle = main_bundle
    except Exception as exc:
        # Sandbox unavailable or script crashed — static analysis only.
        print(f"r2py: sandbox run failed, using static analysis only: {exc}", file=sys.stderr)

    # ── Step 4 + 6: branch extraction loop ──────────────────────────────────
    branches: dict[str, BranchAnalysis] = {}
    if main_bundle is not None:
        _extract_branches(ast_root, entities, main_bundle,
                          branches, tracker, capture, timeout_s,
                          max_coverage_attempts)

    # ── Step 5: resolve external sources ────────────────────────────────────
    external_sources = {}
    for eid, entity in entities.items():
        if entity.kind in (EntityKind.LIBRARY_IMPORT, EntityKind.EXTERNAL_SYMBOL):
            pkg = entity.package
            if pkg:
                loc = resolve_symbol(pkg, entity.name)
                if loc:
                    external_sources[eid] = loc

    # ── Step 7: build ScriptMap ──────────────────────────────────────────────
    # Merge actual effect bundles into the effects list.
    all_effects = list(predicted_effects)
    if main_bundle is not None:
        all_effects = _merge_dynamic_effects(all_effects, main_bundle, entities)

    return ScriptMap(
        source=source,
        ast_root=ast_root,
        entities=entities,
        effects=all_effects,
        branches=branches,
        external_sources=external_sources,
        coverage=tracker.report(),
    )


def _extract_branches(
    ast_root: AstNode,
    entities: dict[str, Entity],
    main_bundle,
    branches: dict[str, BranchAnalysis],
    tracker: CoverageTracker,
    capture: CaptureSpec,
    timeout_s: float,
    max_attempts: int,
) -> None:
    """Find if/else alternative branches and run each as a slice."""
    branch_nodes = _collect_branch_nodes(ast_root, entities)
    attempt = 0
    pending = branch_nodes

    while pending and attempt < max_attempts:
        attempt += 1
        still_pending = []
        for branch_id, branch_node, parent_entity_id, condition_text, was_executed in pending:
            if was_executed:
                tracker.mark(branch_id, "dynamic")
                continue

            slice_source = extract_branch(branch_node, entities, main_bundle)
            bundle = None
            try:
                bundle = run_slice(
                    slice_source,
                    capture=capture,
                    timeout_s=min(timeout_s, 30),
                )
                tracker.mark(branch_id, "branch-extracted")
            except Exception:
                still_pending.append(
                    (branch_id, branch_node, parent_entity_id, condition_text, was_executed)
                )

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

    Currently collects `else` branches of `if_statement` nodes.
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
        # consequence is always executed when condition is true — we focus on
        # the alternative (else) branch, which may not be executed.
        alt_node = node.child_by_field("alternative")
        if alt_node is not None:
            branch_id = f"branch_{counter[0]}"
            counter[0] += 1
            # Find the enclosing entity (the one whose span contains this if_statement).
            row = node.start[0]
            parent_eid = ""
            for eid, entity in entities.items():
                sp = entity.source_span
                if sp.start_line <= row <= sp.end_line:
                    parent_eid = eid
                    break
            # We conservatively mark else-branches as not-executed; Stage 0's
            # EffectBundle does not tell us which branches ran, so we run them all.
            out.append((branch_id, alt_node, parent_eid, condition_text, False))

    for child in node.children:
        _collect_branch_nodes_rec(child, out, counter, entities)


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
