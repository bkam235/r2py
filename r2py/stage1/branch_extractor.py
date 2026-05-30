"""Build runnable R slices for unevaluated branches (§3.4 step 3)."""
from __future__ import annotations

from ..types import EffectBundle, EntityId
from .entities import AstNode, Entity
from .runner import _py_to_r


def extract_branch(
    node: AstNode,
    parent_entities: dict[EntityId, Entity],
    parent_bundle: EffectBundle,
) -> str:
    """Build a runnable R script for an unevaluated branch node.

    Strategy:
    1. Collect the free variable names referenced in *node*'s source text.
    2. For each free variable found in *parent_bundle.data*, emit an R
       assignment statement to restore its value.
    3. Append the branch body source text.

    Returns a self-contained R script string.
    """
    body_source = node.text
    free_vars = _free_variables(node, parent_entities)

    preamble_lines: list[str] = []
    for var_name in free_vars:
        value = parent_bundle.data.get(var_name)
        if value is not None:
            r_lit = _py_to_r(value)
            if r_lit is not None:
                preamble_lines.append(f"{var_name} <- {r_lit}")

    if preamble_lines:
        return "\n".join(preamble_lines) + "\n\n" + body_source
    return body_source


def _free_variables(node: AstNode, parent_entities: dict[EntityId, Entity]) -> list[str]:
    """Return variable names used in *node* that are defined in *parent_entities*."""
    used: set[str] = set()
    _collect_identifiers(node, used)
    defined_names = {e.name for e in parent_entities.values()}
    return sorted(used & defined_names)


def extract_for_branch(
    node: AstNode,
    parent_entities: dict[EntityId, Entity],
    parent_bundle: EffectBundle,
) -> str | None:
    """Build a runnable R slice for one synthetic iteration of a for-loop body.

    Strategy:
    1. Find the loop variable name and sequence expression from the for_statement node.
    2. Look up the sequence value in parent_bundle.data.
    3. If it's a list/vector, take the first element as the iterator value.
    4. Restore free variables from parent_bundle.data as a preamble.
    5. Return: preamble + ``for (<var> in <value>) { <body> }``

    Returns None if the sequence value cannot be synthesized.
    """
    # tree-sitter-r fields: variable, sequence, body
    var_node = node.child_by_field("variable")
    seq_node = node.child_by_field("sequence")
    body_node = node.child_by_field("body")

    if var_node is None or body_node is None:
        return None

    loop_var = var_node.text
    body_text = body_node.text

    # Try to find the sequence value in parent bundle data
    seq_r_lit = "1"  # fallback: iterate over a single integer
    if seq_node is not None:
        seq_name = seq_node.text.strip()
        seq_val = parent_bundle.data.get(seq_name)
        if seq_val is not None:
            if isinstance(seq_val, list) and seq_val:
                first = _py_to_r(seq_val[0])
                if first:
                    seq_r_lit = first
            else:
                r_lit = _py_to_r(seq_val)
                if r_lit:
                    seq_r_lit = r_lit

    # Restore free variables (excluding the loop variable itself)
    free_vars = _free_variables(body_node, parent_entities)
    free_vars = [v for v in free_vars if v != loop_var]

    preamble_lines: list[str] = []
    for var_name in free_vars:
        value = parent_bundle.data.get(var_name)
        if value is not None:
            r_lit = _py_to_r(value)
            if r_lit is not None:
                preamble_lines.append(f"{var_name} <- {r_lit}")

    for_slice = f"for ({loop_var} in {seq_r_lit}) {body_text}"
    if preamble_lines:
        return "\n".join(preamble_lines) + "\n\n" + for_slice
    return for_slice


def _collect_identifiers(node: AstNode, out: set[str]) -> None:
    if node.kind == "identifier":
        out.add(node.text)
    for child in node.children:
        _collect_identifiers(child, out)


