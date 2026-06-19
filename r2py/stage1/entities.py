"""Stage 1 entity types: AstNode, Entity, EntityRef, SourceLocation."""
from __future__ import annotations

from dataclasses import dataclass, field

from ..types import EntityId, EntityKind, EffectClass, EffectBundle


@dataclass
class SourceLocation:
    file: str
    start_line: int
    start_col: int
    end_line: int
    end_col: int


@dataclass
class AstNode:
    """Lightweight wrapper around a tree-sitter-language-pack Node."""
    kind: str                          # tree-sitter node type, e.g. "binary_operator"
    text: str                          # source text of this node
    start: tuple[int, int]             # (row, col), 0-based
    end: tuple[int, int]
    start_byte: int
    end_byte: int
    is_named: bool
    children: list[AstNode] = field(default_factory=list)
    # Raw tree-sitter node kept for field-name queries (not serialized).
    _ts_node: object = field(default=None, repr=False, compare=False)

    def child_by_field(self, name: str) -> AstNode | None:
        """Return the first named child with the given field name."""
        if self._ts_node is None:
            return None
        ts_child = self._ts_node.child_by_field_name(name)
        if ts_child is None:
            return None
        # Find the matching wrapper in children by byte offset.
        for c in self.children:
            if c.start_byte == ts_child.start_byte() and c.end_byte == ts_child.end_byte():
                return c
        return None

    def named_children(self) -> list[AstNode]:
        return [c for c in self.children if c.is_named]


@dataclass
class FunctionMetadata:
    """R introspection results for a function: formals, S3 methods, namespace location."""
    formals: dict[str, str] = field(default_factory=dict)
    methods: list[str] = field(default_factory=list)
    where: list[str] = field(default_factory=list)


@dataclass
class EntityRef:
    """A directed dependency edge from one entity to another."""
    entity_id: EntityId
    kind: EntityKind


@dataclass
class Entity:
    id: EntityId
    kind: EntityKind
    name: str
    source_span: SourceLocation
    dependencies: list[EntityRef] = field(default_factory=list)
    predicted_effects: list[EffectClass] = field(default_factory=list)
    actual_bundle: EffectBundle | None = None
    # §3.7 R-semantic annotation tags, e.g. "na_semantics", "super_assign"
    r_semantic_flags: list[str] = field(default_factory=list)
    # Set for LIBRARY_IMPORT and EXTERNAL_SYMBOL entities.
    package: str | None = None
    # Identifiers referenced in this entity's source that are not defined anywhere
    # in the script (i.e. free variables — R built-in datasets, lazy-loaded objects,
    # etc.).  Populated by the walker; Stage 2 surfaces observed values to the LLM.
    free_variable_refs: list[str] = field(default_factory=list)
    # R match.call() resolution for FUNCTION_CALL entities, e.g. "chunk(x = 1, 100, 10)".
    resolved_call: str | None = None
    # R introspection: formals, S3 methods, namespace location.
    function_metadata: FunctionMetadata | None = None
