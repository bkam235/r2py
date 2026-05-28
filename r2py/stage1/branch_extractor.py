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


def _collect_identifiers(node: AstNode, out: set[str]) -> None:
    if node.kind == "identifier":
        out.add(node.text)
    for child in node.children:
        _collect_identifiers(child, out)


