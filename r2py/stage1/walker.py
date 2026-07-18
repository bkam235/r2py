"""Depth-first AST walker: entity classification + §3.7 R-semantic annotations."""
from __future__ import annotations

import keyword as _keyword
from collections import defaultdict

from ..types import EntityId, EntityKind, EffectClass
from .coverage import CoverageTracker
from .effects import SideEffect, STATIC_PREDICTIONS
from .entities import AstNode, Entity, EntityRef, SourceLocation


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def walk(
    ast_root: AstNode,
    source_file: str,
    tracker: CoverageTracker | None = None,
) -> tuple[dict[EntityId, Entity], list[SideEffect]]:
    """Walk the AST and return (entities, predicted_side_effects).

    All entities are registered with *tracker* if provided.
    """
    ctx = _WalkContext(source_file=source_file, tracker=tracker or CoverageTracker())
    _visit(ast_root, ctx)
    _annotate_r_semantics(ctx.entities, ast_root)
    return ctx.entities, ctx.effects


# ---------------------------------------------------------------------------
# Walk context
# ---------------------------------------------------------------------------

class _WalkContext:
    def __init__(self, source_file: str, tracker: CoverageTracker) -> None:
        self.source_file = source_file
        self.tracker = tracker
        self.entities: dict[EntityId, Entity] = {}
        self.effects: list[SideEffect] = []
        self._counters: dict[str, int] = {}

    def fresh_id(self, prefix: str) -> EntityId:
        n = self._counters.get(prefix, 0)
        self._counters[prefix] = n + 1
        return f"{prefix}_{n}" if n > 0 else prefix

    def add(self, entity: Entity) -> None:
        self.entities[entity.id] = entity
        self.tracker.register(entity.id)
        self.tracker.mark(entity.id, "analyzed")

    def add_effect(self, effect: SideEffect) -> None:
        self.effects.append(effect)


# ---------------------------------------------------------------------------
# AST visitor
# ---------------------------------------------------------------------------

# R node types that represent literal (constant) values.
_LITERAL_KINDS = frozenset({
    "integer", "float", "complex", "string", "logical",
    "na", "null", "inf", "nan",
})

# Assignment operators recognised as top-level assignments.
_ASSIGN_OPS = frozenset({"<-", "=", "<<-", "->", "->>"})


def _visit(node: AstNode, ctx: _WalkContext, *, is_statement: bool = False) -> None:
    """Dispatch on top-level node kinds; recurse into children for others."""
    kind = node.kind

    if kind == "program":
        for child in node.named_children():
            _visit(child, ctx, is_statement=True)

    elif kind == "binary_operator":
        _visit_binary_op(node, ctx)

    elif kind == "call":
        _visit_call(node, ctx)

    elif kind == "if_statement":
        _visit_if(node, ctx)

    elif kind == "for_statement":
        _visit_for(node, ctx)

    elif kind == "while_statement":
        _visit_while(node, ctx)

    elif kind == "braced_expression":
        for child in node.named_children():
            _visit(child, ctx, is_statement=True)

    elif kind == "identifier" and is_statement:
        _visit_bare_identifier(node, ctx)

    else:
        # Recurse for anything else (e.g. parenthesized expressions)
        for child in node.named_children():
            _visit(child, ctx)


def _visit_binary_op(node: AstNode, ctx: _WalkContext) -> None:
    """Handle assignment and non-assignment binary operators."""
    op_node = _find_op(node)
    op_text = op_node.text if op_node else ""

    if op_text in _ASSIGN_OPS:
        _visit_assignment(node, op_text, ctx)
    else:
        # Non-assignment binary op — recurse both sides.
        for child in node.named_children():
            _visit(child, ctx)


def _visit_assignment(node: AstNode, op: str, ctx: _WalkContext) -> None:
    """Classify an assignment node as Variable, Constant, FunctionDef, etc."""
    # lhs/rhs field names in tree-sitter-r grammar
    lhs = node.child_by_field("lhs")
    rhs = node.child_by_field("rhs")

    # ->  and ->> reverse the sides
    if op in {"->", "->>"}:
        lhs, rhs = rhs, lhs

    if lhs is None:
        return

    name = lhs.text.strip("`\"")
    loc = _span(node, ctx.source_file)

    if rhs is None:
        # Incomplete assignment — skip
        return

    if rhs.kind == "function_definition":
        kind = EntityKind.FUNCTION_DEF
    elif rhs.kind in _LITERAL_KINDS:
        kind = EntityKind.CONSTANT
    elif rhs.kind == "binary_operator" and _is_tilde_op(rhs):
        kind = EntityKind.FORMULA
    elif rhs.kind in {"setClass", "new"} or (
        rhs.kind == "call" and _call_name(rhs) in ("setClass", "new_class")
    ):
        kind = EntityKind.S4_CLASS
    elif rhs.kind == "call" and _call_name(rhs) == "R6Class":
        kind = EntityKind.R6_CLASS
    elif rhs.kind == "call" and _call_name(rhs) in ("new.env", "new_environment"):
        kind = EntityKind.ENVIRONMENT
    else:
        kind = EntityKind.VARIABLE

    entity_id = ctx.fresh_id(name)

    # Dependency edges: names used on the RHS
    deps: list[EntityRef] = []
    if rhs is not None:
        for used_name in _collect_identifiers(rhs):
            if used_name in ctx.entities:
                # Find the most-recently-defined entity with this name
                match = _latest_entity_for_name(used_name, ctx.entities)
                if match:
                    deps.append(EntityRef(entity_id=match.id, kind=match.kind))

    # Predicted effects: <<- creates a cross-scope write (ENV effect)
    predicted: list[EffectClass] = []
    if op in {"<<-", "->>"}:
        predicted.append(EffectClass.ENV)

    # Identifiers on the RHS that aren't defined in this script are free variable
    # refs (e.g. built-in R datasets).  We record all of them here; Stage 2 will
    # filter to those that actually appear in actual_bundle.data.
    free_refs: list[str] = []
    if rhs is not None:
        for used_name in _collect_identifiers(rhs):
            if used_name not in ctx.entities and used_name != name and used_name not in free_refs:
                free_refs.append(used_name)

    entity = Entity(
        id=entity_id,
        kind=kind,
        name=name,
        source_span=loc,
        dependencies=deps,
        predicted_effects=predicted,
        package=None,
        free_variable_refs=free_refs,
    )
    ctx.add(entity)

    # Do NOT recurse into function definition bodies.  The entire function
    # (body included) is one FUNCTION_DEF entity; local assignments and calls
    # inside it are not top-level effects and must not become separate entities.
    # free_variable_refs collected above already includes all identifiers inside
    # the body (via _collect_identifiers), so _lookup_free_ref_sources in
    # prompt.py can still fetch package sources for symbols used inside.
    if rhs.kind == "function_definition":
        pass
    elif rhs.kind == "call":
        # Call RHS: sub-calls are translated as part of their enclosing entity.
        # Scan for nested library/require imports and braced-expression arguments.
        args = rhs.child_by_field("arguments")
        if args:
            for child in args.named_children():
                if child.kind == "argument":
                    val = child.child_by_field("value")
                    if val is not None and val.kind == "call" and _call_name(val) in ("library", "require"):
                        _visit_library_call(val, _call_name(val), ctx)
                    elif val is not None and val.kind == "braced_expression":
                        for stmt in val.named_children():
                            _visit(stmt, ctx)
                elif child.kind == "call" and _call_name(child) in ("library", "require"):
                    _visit_library_call(child, _call_name(child), ctx)
                elif child.kind == "braced_expression":
                    for stmt in child.named_children():
                        _visit(stmt, ctx)
    else:
        # Recurse for braced_expression, if_statement, etc. — may contain
        # nested named definitions.
        for child in rhs.named_children():
            _visit(child, ctx)


def _visit_call(node: AstNode, ctx: _WalkContext) -> None:
    """Classify a bare function call (not on the LHS of an assignment)."""
    fn_name = _call_name(node)
    if fn_name is None:
        return

    # library() / require() — special handling
    if fn_name in ("library", "require"):
        _visit_library_call(node, fn_name, ctx)
        return

    # Transparent wrapper detection: if any argument is a braced expression,
    # this call is a wrapper (withAutoprint, local, suppressWarnings, etc.).
    # Walk the braced-expression children as top-level statements and skip
    # creating an entity for the wrapper itself — it has no translatable
    # semantics beyond its children.
    if _has_braced_arg(node):
        args = node.child_by_field("arguments")
        if args:
            for child in args.named_children():
                if child.kind == "argument":
                    val = child.child_by_field("value")
                    if val is not None and val.kind == "braced_expression":
                        for stmt in val.named_children():
                            _visit(stmt, ctx)
                    elif val is not None and val.kind == "call" and _call_name(val) in ("library", "require"):
                        _visit_library_call(val, _call_name(val), ctx)
                elif child.kind == "braced_expression":
                    for stmt in child.named_children():
                        _visit(stmt, ctx)
                elif child.kind == "call" and _call_name(child) in ("library", "require"):
                    _visit_library_call(child, _call_name(child), ctx)
        return

    # Detect pkg::fn() or pkg:::fn() — EXTERNAL_SYMBOL
    fn_node = node.child_by_field("function")
    pkg_name: str | None = None
    if fn_node is not None and fn_node.kind == "namespace_operator":
        kind = EntityKind.EXTERNAL_SYMBOL
        # LHS of the namespace_operator is the package identifier
        pkg_name = fn_node.text.split("::")[0].strip("`\"")
    else:
        kind = EntityKind.FUNCTION_CALL

    entity_id = ctx.fresh_id(fn_name)
    loc = _span(node, ctx.source_file)
    predicted = list(STATIC_PREDICTIONS.get(fn_name, []))

    # Collect identifiers from argument *values* (not keyword names) that aren't
    # defined in this script.  These may be R built-in datasets or other implicit
    # environment objects.  We record everything; Stage 2 filters against
    # actual_bundle.data so base-R function names (c, mean, …) are suppressed.
    free_refs: list[str] = []
    _args_node = node.child_by_field("arguments")
    if _args_node:
        for _child in _args_node.named_children():
            if _child.kind == "argument":
                _val = _child.child_by_field("value")
                _targets = [_val] if _val is not None else []
            else:
                _targets = [_child]
            for _target in _targets:
                for _ident in _collect_identifiers(_target):
                    if _ident not in ctx.entities and _ident not in free_refs:
                        free_refs.append(_ident)

    entity = Entity(
        id=entity_id,
        kind=kind,
        name=fn_name,
        source_span=loc,
        predicted_effects=predicted,
        package=pkg_name,
        free_variable_refs=free_refs,
    )
    ctx.add(entity)

    # Add corresponding SideEffect entries
    for ec in predicted:
        ctx.add_effect(SideEffect(kind=ec, entity_id=entity_id, is_predicted=True))

    # Scan arguments for nested library/require imports only.
    # Generic sub-calls (c(), as.Date(), etc.) are NOT extracted as separate
    # entities — they are translated as part of their enclosing statement.
    args = node.child_by_field("arguments")
    if args:
        for child in args.named_children():
            if child.kind == "argument":
                val = child.child_by_field("value")
                if val is not None and val.kind == "call" and _call_name(val) in ("library", "require"):
                    _visit_library_call(val, _call_name(val), ctx)
            elif child.kind == "call" and _call_name(child) in ("library", "require"):
                _visit_library_call(child, _call_name(child), ctx)


def _visit_bare_identifier(node: AstNode, ctx: _WalkContext) -> None:
    """Handle a bare identifier at the top level (e.g. `storms`, `mtcars`).

    In R, a bare name as a statement prints the object.  This creates an
    entity so the data-shim mechanism can capture the value and the
    translation reproduces the print.
    """
    name = node.text.strip("`\"")
    if not name:
        return
    entity_id = ctx.fresh_id(name)
    loc = _span(node, ctx.source_file)
    free_refs = [name]
    entity = Entity(
        id=entity_id,
        kind=EntityKind.VARIABLE,
        name=name,
        source_span=loc,
        free_variable_refs=free_refs,
    )
    ctx.add(entity)


def _visit_library_call(node: AstNode, fn_name: str, ctx: _WalkContext) -> None:
    """Handle library(pkg) / require(pkg) — creates a LIBRARY_IMPORT entity."""
    pkg_name = _first_arg_text(node)
    if pkg_name is None:
        return
    pkg_name = pkg_name.strip('"\'`')

    entity_id = ctx.fresh_id(f"import_{pkg_name}")
    loc = _span(node, ctx.source_file)

    entity = Entity(
        id=entity_id,
        kind=EntityKind.LIBRARY_IMPORT,
        name=pkg_name,
        source_span=loc,
        predicted_effects=[EffectClass.ENV],
        package=pkg_name,
    )
    ctx.add(entity)
    ctx.add_effect(SideEffect(kind=EffectClass.ENV, entity_id=entity_id, is_predicted=True))


def _visit_if(node: AstNode, ctx: _WalkContext) -> None:
    """Visit if/else — recurse into all named children (condition, consequence, alternative)."""
    for child in node.named_children():
        _visit(child, ctx)


def _visit_for(node: AstNode, ctx: _WalkContext) -> None:
    body = node.child_by_field("body")
    if body:
        _visit(body, ctx)


def _visit_while(node: AstNode, ctx: _WalkContext) -> None:
    body = node.child_by_field("body")
    if body:
        _visit(body, ctx)


# ---------------------------------------------------------------------------
# §3.7 R-semantic annotation pass
# ---------------------------------------------------------------------------

# Platform-specific functions whose behaviour differs on Windows vs POSIX.
_PLATFORM_SPECIFIC_FUNCTIONS = frozenset({
    "Sys.setlocale", "Sys.getlocale", "Sys.setenv", "Sys.getenv",
    "with_locale", "local_locale", "with_envvar", "local_envvar",
    "Sys.time", "proc.time", "system", "system2",
})

# Known NSE (non-standard evaluation) function names.
_NSE_FUNCTIONS = frozenset({
    "filter", "select", "mutate", "arrange", "group_by", "summarise", "summarize",
    "rename", "transmute", "across", "where", "starts_with", "ends_with",
    "subset", "transform", "with", "within",
    "aes", "aes_string", "vars",
    "quote", "substitute", "bquote",
    "eval", "parse", "deparse",
})

# Names that trigger S3/S4/R6 dispatch annotation.
_DISPATCH_FUNCTIONS = frozenset({
    "UseMethod", "setGeneric", "setMethod", "setClass", "R6Class",
    "is", "inherits", "class",
})

# R vector constructor functions: called with a single integer argument n they create
# a vector of length n — NOT a type conversion.  Annotated so Stage 2 translates them
# as np.zeros / bytes / list-of-empty rather than the Python scalar equivalents.
_R_VECTOR_CONSTRUCTORS = frozenset({
    "complex", "raw", "logical", "integer", "character",
    "numeric", "double", "single",
})

# Python keywords that cannot be used as argument names in Python but are valid
# R parameter names.  Detected by Stage 1 so the translator can rename them.
_PYTHON_KEYWORDS = frozenset(_keyword.kwlist) - {"True", "False", "None"}


def _annotate_r_semantics(entities: dict[EntityId, Entity], ast_root: AstNode) -> None:
    """Scan AST and attach §3.7 semantic flags to relevant entities.

    This pass adds tags to already-classified entities based on AST patterns
    that are language-level invariants (not learnable per-package signals).
    """
    # Build a flat list of all nodes for scanning.
    all_nodes: list[AstNode] = []
    _collect_all_nodes(ast_root, all_nodes)

    # Build line → [Entity] index so _flag_enclosing is O(1) per node instead of O(entities).
    entities_by_line: dict[int, list[Entity]] = defaultdict(list)
    for entity in entities.values():
        sp = entity.source_span
        for line in range(sp.start_line, sp.end_line + 1):
            entities_by_line[line].append(entity)

    for node in all_nodes:
        kind = node.kind

        # 1-based indexing: subscript `[` calls
        if kind == "subset" or (kind == "call" and node.text.startswith("[")):
            _flag_enclosing(node, entities_by_line,"indexing_1based")

        # super-assignment <<- or ->>
        if kind == "binary_operator":
            op = _find_op(node)
            if op and op.text in {"<<-", "->>"}:
                _flag_enclosing(node, entities_by_line,"super_assign")

        # NA semantics
        if kind == "na":
            _flag_enclosing(node, entities_by_line,"na_semantics")
        if kind == "identifier" and node.text in (
            "NA", "NA_integer_", "NA_real_", "NA_complex_", "NA_character_",
            "is.na", "na.rm",
        ):
            _flag_enclosing(node, entities_by_line,"na_semantics")

        # NSE: known non-standard evaluation function calls
        if kind == "call":
            fn = _call_name(node)
            if fn in _NSE_FUNCTIONS:
                _flag_enclosing(node, entities_by_line,"nse")

        # Vector recycling: binary arithmetic on named identifiers
        if kind == "binary_operator":
            op = _find_op(node)
            if op and op.text in ("+", "-", "*", "/", "%%", "%/%"):
                lhs = node.child_by_field("lhs")
                rhs_node = node.child_by_field("rhs")
                if (lhs and lhs.kind == "identifier" and
                        rhs_node and rhs_node.kind == "identifier"):
                    _flag_enclosing(node, entities_by_line,"vector_recycling")

        # Copy-on-modify: any assignment where RHS is also an identifier
        if kind == "binary_operator":
            op = _find_op(node)
            if op and op.text in {"<-", "="}:
                rhs_node = node.child_by_field("rhs")
                if rhs_node and rhs_node.kind == "identifier":
                    _flag_enclosing(node, entities_by_line,"copy_on_modify")

        # Platform-specific calls (locale, OS-level functions)
        if kind == "call":
            fn = _call_name(node)
            if fn in _PLATFORM_SPECIFIC_FUNCTIONS:
                _flag_enclosing(node, entities_by_line, "platform_specific")

        # S3/S4/R6 dispatch
        if kind == "call":
            fn = _call_name(node)
            if fn in _DISPATCH_FUNCTIONS:
                _flag_enclosing(node, entities_by_line,"dispatch_s3s4r6")

        # Formula: ~ operator (tree-sitter-r represents y ~ x as binary_operator with ~)
        if kind == "binary_operator" and _is_tilde_op(node):
            _flag_enclosing(node, entities_by_line,"nse")

        # Scalar vs vector: length() comparisons
        if kind == "call":
            fn = _call_name(node)
            if fn == "length":
                _flag_enclosing(node, entities_by_line,"scalar_vs_vector")

        # R vector constructors: complex(n), raw(n), logical(n), integer(n), etc.
        # Called with a single numeric argument they create a length-n vector, NOT a
        # type conversion. Flag so Stage 2 knows to use np.zeros / bytes / [] not
        # Python's scalar-producing equivalents.
        if kind == "call":
            fn = _call_name(node)
            if fn in _R_VECTOR_CONSTRUCTORS:
                args = node.child_by_field("arguments")
                if args:
                    arg_children = [c for c in args.named_children()
                                    if c.kind in ("argument", "float", "integer",
                                                  "identifier", "call", "binary_operator")]
                    # Heuristic: single positional argument that looks numeric (no keyword =)
                    if len(arg_children) == 1:
                        child = arg_children[0]
                        if child.kind == "argument":
                            # argument node: check it has no keyword label (positional)
                            key = child.child_by_field("name")
                            if key is None or key.text in ("length.out", "n", ""):
                                _flag_enclosing(node, entities_by_line, "vector_constructor")
                        elif child.kind in ("float", "integer", "identifier", "call"):
                            _flag_enclosing(node, entities_by_line, "vector_constructor")

        # Python keyword as argument name: R uses identifiers like `from`, `in`,
        # `as` as parameter names; these are Python reserved keywords and cause
        # SyntaxError in the generated Python. Flag each offending keyword so the
        # translator knows which names to rename consistently.
        if kind == "argument":
            name_node = node.child_by_field("name")
            if name_node and name_node.text in _PYTHON_KEYWORDS:
                # Flag with a per-keyword tag so the prompt can be specific.
                _flag_enclosing(node, entities_by_line,
                                f"python_keyword_arg:{name_node.text}")


def _flag_enclosing(
    node: AstNode,
    entities_by_line: dict[int, list[Entity]],
    flag: str,
) -> None:
    """Add *flag* to entities whose span contains this node's row.

    Uses the pre-built line index for O(1) lookup instead of scanning all entities.
    """
    row = node.start[0]
    for entity in entities_by_line.get(row, []):
        if flag not in entity.r_semantic_flags:
            entity.r_semantic_flags.append(flag)


# ---------------------------------------------------------------------------
# Small AST helper utilities
# ---------------------------------------------------------------------------

def _collect_all_nodes(node: AstNode, out: list[AstNode]) -> None:
    out.append(node)
    for child in node.children:
        _collect_all_nodes(child, out)


def _has_braced_arg(node: AstNode) -> bool:
    """Return True if a call node has a braced_expression among its arguments."""
    args = node.child_by_field("arguments")
    if args is None:
        return False
    for child in args.named_children():
        if child.kind == "braced_expression":
            return True
        if child.kind == "argument":
            val = child.child_by_field("value")
            if val is not None and val.kind == "braced_expression":
                return True
    return False


def _find_op(node: AstNode) -> AstNode | None:
    """Find the operator child of a binary_operator node."""
    for child in node.children:
        if not child.is_named:
            # Punctuation/operator tokens are unnamed in tree-sitter-r
            return child
    return None


def _is_tilde_op(node: AstNode) -> bool:
    """Return True if *node* is a binary_operator whose operator is `~` (formula)."""
    op = _find_op(node)
    return op is not None and op.text == "~"


def _call_name(node: AstNode) -> str | None:
    """Return the function name of a call node, or None."""
    fn_node = node.child_by_field("function")
    if fn_node is None:
        # Fallback: first named child
        nc = node.named_children()
        fn_node = nc[0] if nc else None
    if fn_node is None:
        return None
    # Handle package::name or package:::name
    if "::" in fn_node.text or ":::" in fn_node.text:
        return fn_node.text.split(":")[-1]
    return fn_node.text.strip("`\"")



def _first_arg_text(node: AstNode) -> str | None:
    """Return the text of the first argument to a call node."""
    args = node.child_by_field("arguments")
    if args is None:
        return None
    for child in args.named_children():
        if child.kind == "argument":
            val = child.child_by_field("value")
            if val:
                return val.text
            return child.text
    return None


def _collect_identifiers(node: AstNode) -> list[str]:
    """Return all identifier texts within *node* (for dependency tracking)."""
    results: list[str] = []
    _collect_identifiers_rec(node, results)
    return results


def _collect_identifiers_rec(node: AstNode, out: list[str]) -> None:
    if node.kind == "identifier":
        out.append(node.text)
    for child in node.children:
        _collect_identifiers_rec(child, out)


def _latest_entity_for_name(name: str, entities: dict[EntityId, Entity]) -> Entity | None:
    """Return the most recently defined entity with the given *name*."""
    matches = [e for e in entities.values() if e.name == name]
    if not matches:
        return None
    return max(matches, key=lambda e: (e.source_span.start_line, e.source_span.start_col))


def _span(node: AstNode, file: str) -> SourceLocation:
    return SourceLocation(
        file=file,
        start_line=node.start[0],
        start_col=node.start[1],
        end_line=node.end[0],
        end_col=node.end[1],
    )
