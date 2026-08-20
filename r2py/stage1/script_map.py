"""Full ScriptMap (§3.3), BranchAnalysis, and serialization helpers."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from ..types import (
    BranchId, EffectBundle, EntityId,
    ScriptMap as _BaseScriptMap,
)
from ..stage0.effects.bundle import to_json as _bundle_to_json, from_json as _bundle_from_json
from .coverage import CoverageReport
from .effects import SideEffect
from .entities import AstNode, Entity, EntityRef, SourceLocation


@dataclass
class BranchAnalysis:
    branch_id: BranchId
    parent_entity_id: EntityId
    condition_text: str
    was_executed: bool
    runnable_slice: str | None = None       # slice source built by branch_extractor
    bundle: EffectBundle | None = None      # sandbox result of running the slice


@dataclass
class ScriptMap(_BaseScriptMap):
    """Full ScriptMap produced by Stage 1.  Extends the minimal placeholder in types.py."""
    ast_root:         AstNode | None                     = None
    entities:         dict[EntityId, Entity]             = field(default_factory=dict)
    effects:          list[SideEffect]                   = field(default_factory=list)
    branches:         dict[BranchId, BranchAnalysis]     = field(default_factory=dict)
    external_sources: dict[EntityId, SourceLocation]     = field(default_factory=dict)
    coverage:         CoverageReport | None              = None
    # Per-entity EffectBundle deltas from the checkpointed R run (§ Option-2 scoring).
    # Maps entity_id → EffectBundle containing only what that entity added to the
    # namespace/stdout/graphics.  Empty dict when checkpointing is unavailable.
    entity_bundles:   dict[EntityId, EffectBundle]       = field(default_factory=dict)
    # Per-entity R type info: entity_id → {var_name: {"class": "...", "typeof": "..."}}.
    entity_types:     dict[EntityId, dict]               = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def to_json(sm: ScriptMap) -> dict:
    """Return a JSON-serializable dict for a ScriptMap."""
    return {
        "source": sm.source,
        "ast_root": _ast_to_dict(sm.ast_root) if sm.ast_root else None,
        "entities": {eid: _entity_to_dict(e) for eid, e in sm.entities.items()},
        "effects": [_effect_to_dict(e) for e in sm.effects],
        "branches": {bid: _branch_to_dict(b) for bid, b in sm.branches.items()},
        "external_sources": {
            eid: _loc_to_dict(loc) for eid, loc in sm.external_sources.items()
        },
        "coverage": _coverage_to_dict(sm.coverage) if sm.coverage else None,
        "entity_bundles": {
            eid: _bundle_to_json(eb) for eid, eb in sm.entity_bundles.items()
        },
        "entity_types": sm.entity_types,
    }


def save(sm: ScriptMap, path: Path) -> None:
    path.write_text(json.dumps(to_json(sm), indent=2), encoding="utf-8")


def from_json(d: dict) -> ScriptMap:
    return ScriptMap(
        source=d.get("source", ""),
        ast_root=_ast_from_dict(d["ast_root"]) if d.get("ast_root") else None,
        entities={
            eid: _entity_from_dict(e) for eid, e in d.get("entities", {}).items()
        },
        effects=[_effect_from_dict(e) for e in d.get("effects", [])],
        branches={
            bid: _branch_from_dict(b) for bid, b in d.get("branches", {}).items()
        },
        external_sources={
            eid: _loc_from_dict(loc) for eid, loc in d.get("external_sources", {}).items()
        },
        coverage=_coverage_from_dict(d["coverage"]) if d.get("coverage") else None,
        entity_bundles={
            eid: _bundle_from_json(eb)
            for eid, eb in d.get("entity_bundles", {}).items()
        },
        entity_types=d.get("entity_types", {}),
    )


def load(path: Path) -> ScriptMap:
    return from_json(json.loads(path.read_text(encoding="utf-8")))


def to_annotated_r(sm: ScriptMap) -> str:
    """Return the original R source with `# r2py: <entity_id>` inserted after each entity."""
    lines = sm.source.splitlines(keepends=True)
    # Collect annotation insertions: line_number (0-based) → list of tags to append.
    insertions: dict[int, list[str]] = {}
    for eid, entity in sm.entities.items():
        end_line = entity.source_span.end_line
        insertions.setdefault(end_line, []).append(eid)
    # Rebuild output line by line.
    out: list[str] = []
    for i, line in enumerate(lines):
        out.append(line)
        if i in insertions:
            for eid in insertions[i]:
                stripped = line.rstrip("\n\r")
                indent = " " * (len(stripped) - len(stripped.lstrip()))
                out.append(f"{indent}# r2py: {eid}\n")
    return "".join(out)


# ---------------------------------------------------------------------------
# Private conversion helpers
# ---------------------------------------------------------------------------

def _loc_to_dict(loc: SourceLocation) -> dict:
    return {
        "file": loc.file,
        "start_line": loc.start_line, "start_col": loc.start_col,
        "end_line": loc.end_line, "end_col": loc.end_col,
    }


def _loc_from_dict(d: dict) -> SourceLocation:
    return SourceLocation(
        file=d["file"],
        start_line=d["start_line"], start_col=d["start_col"],
        end_line=d["end_line"], end_col=d["end_col"],
    )


def _entity_to_dict(e: Entity) -> dict:
    return {
        "id": e.id,
        "kind": e.kind.value,
        "name": e.name,
        "source_span": _loc_to_dict(e.source_span),
        "dependencies": [{"entity_id": r.entity_id, "kind": r.kind.value} for r in e.dependencies],
        "predicted_effects": [ef.value for ef in e.predicted_effects],
        "actual_bundle": _bundle_to_json(e.actual_bundle) if e.actual_bundle else None,
        "r_semantic_flags": e.r_semantic_flags,
        "package": e.package,
        "free_variable_refs": e.free_variable_refs,
        "resolved_call": e.resolved_call,
    }


def _entity_from_dict(d: dict) -> Entity:
    from ..types import EntityKind, EffectClass
    return Entity(
        id=d["id"],
        kind=EntityKind(d["kind"]),
        name=d["name"],
        source_span=_loc_from_dict(d["source_span"]),
        dependencies=[
            EntityRef(entity_id=r["entity_id"], kind=EntityKind(r["kind"]))
            for r in d.get("dependencies", [])
        ],
        predicted_effects=[EffectClass(v) for v in d.get("predicted_effects", [])],
        actual_bundle=_bundle_from_json(d["actual_bundle"]) if d.get("actual_bundle") else None,
        r_semantic_flags=d.get("r_semantic_flags", []),
        package=d.get("package"),
        free_variable_refs=d.get("free_variable_refs", []),
        resolved_call=d.get("resolved_call"),
    )


def _effect_to_dict(e: SideEffect) -> dict:
    return {
        "kind": e.kind.value,
        "entity_id": e.entity_id,
        "is_predicted": e.is_predicted,
        "actual_bundle": _bundle_to_json(e.actual_bundle) if e.actual_bundle else None,
    }


def _effect_from_dict(d: dict) -> SideEffect:
    from ..types import EffectClass
    return SideEffect(
        kind=EffectClass(d["kind"]),
        entity_id=d["entity_id"],
        is_predicted=d["is_predicted"],
        actual_bundle=_bundle_from_json(d["actual_bundle"]) if d.get("actual_bundle") else None,
    )


def _branch_to_dict(b: BranchAnalysis) -> dict:
    return {
        "branch_id": b.branch_id,
        "parent_entity_id": b.parent_entity_id,
        "condition_text": b.condition_text,
        "was_executed": b.was_executed,
        "runnable_slice": b.runnable_slice,
        "bundle": _bundle_to_json(b.bundle) if b.bundle else None,
    }


def _branch_from_dict(d: dict) -> BranchAnalysis:
    return BranchAnalysis(
        branch_id=d["branch_id"],
        parent_entity_id=d["parent_entity_id"],
        condition_text=d["condition_text"],
        was_executed=d["was_executed"],
        runnable_slice=d.get("runnable_slice"),
        bundle=_bundle_from_json(d["bundle"]) if d.get("bundle") else None,
    )


def _coverage_to_dict(c: CoverageReport) -> dict:
    return {
        "total_nodes": c.total_nodes,
        "by_status": c.by_status,
        "fraction_analyzed": c.fraction_analyzed,
    }


def _coverage_from_dict(d: dict) -> CoverageReport:
    return CoverageReport(
        total_nodes=d["total_nodes"],
        by_status=d["by_status"],
        fraction_analyzed=d["fraction_analyzed"],
    )


def _ast_to_dict(node: AstNode) -> dict:
    return {
        "kind": node.kind,
        "text": node.text,
        "start": list(node.start),
        "end": list(node.end),
        "start_byte": node.start_byte,
        "end_byte": node.end_byte,
        "is_named": node.is_named,
        "children": [_ast_to_dict(c) for c in node.children],
    }


def _ast_from_dict(d: dict) -> AstNode:
    node = AstNode(
        kind=d["kind"],
        text=d["text"],
        start=tuple(d["start"]),
        end=tuple(d["end"]),
        start_byte=d["start_byte"],
        end_byte=d["end_byte"],
        is_named=d["is_named"],
    )
    node.children = [_ast_from_dict(c) for c in d.get("children", [])]
    return node
