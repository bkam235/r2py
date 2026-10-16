"""The translation manual: a stable design for the Python program (experiments/TRANSLATION_MANUAL_PLAN.md).

Stage 1 (2026-10-16) freezes only the helper interfaces of the best program for a step. 52% of agent rewrites
changed them (rename, drop, add, re-parameterise), and an improvement written against one design does not survive
in another. Text alone is not followed by the model, so the harness enforces it: a frozen helper the candidate
dropped, renamed away from or re-parameterised gets the best program's definition back. Bodies with an unchanged
interface, and new helpers, are free.
"""
from __future__ import annotations

import ast

_ENTITY_MARK = "# r2py:entity:"


def _top_level_defs(src: str) -> dict[str, ast.stmt] | None:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def _signature(node: ast.stmt) -> tuple:
    if isinstance(node, ast.ClassDef):
        return ("class",)
    a = node.args
    return tuple(x.arg for x in a.posonlyargs + a.args + a.kwonlyargs) + \
        ((("*" + a.vararg.arg),) if a.vararg else ()) + ((("**" + a.kwarg.arg),) if a.kwarg else ())


def helper_interfaces(src: str) -> dict[str, tuple]:
    """Name -> parameter names of the top-level functions (("class",) for classes); {} if src does not parse."""
    defs = _top_level_defs(src)
    return {name: _signature(node) for name, node in (defs or {}).items()}


def _span(node: ast.stmt) -> tuple[int, int]:
    """1-based first and last line of a definition, decorators included."""
    first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return first, node.end_lineno


def enforce_interfaces(best: str, candidate: str) -> tuple[str, dict]:
    """``candidate`` with the best program's definition put back for every helper whose interface it changed.

    Returns (source, info) with info["changed"] (helpers the candidate dropped or re-parameterised) and
    info["restored"]; info["unparsable"] when either side does not parse (the candidate is returned unchanged).
    """
    best_defs, cand_defs = _top_level_defs(best), _top_level_defs(candidate)
    if best_defs is None or cand_defs is None:
        return candidate, {"changed": [], "restored": [], "unparsable": True}
    changed = sorted(n for n, node in best_defs.items()
                     if n not in cand_defs or _signature(cand_defs[n]) != _signature(node))
    if not changed:
        return candidate, {"changed": [], "restored": []}
    best_lines = best.splitlines()
    lines = candidate.splitlines()

    def best_text(name):
        a, b = _span(best_defs[name])
        return best_lines[a - 1:b]

    # replace re-parameterised definitions in place, bottom-up so earlier line numbers stay valid
    for name in sorted((n for n in changed if n in cand_defs), key=lambda n: -_span(cand_defs[n])[0]):
        a, b = _span(cand_defs[name])
        lines[a - 1:b] = best_text(name)
    # put dropped ones back before the first entity, in the best program's order
    missing = sorted((n for n in changed if n not in cand_defs), key=lambda n: _span(best_defs[n])[0])
    if missing:
        at = next((i for i, l in enumerate(lines) if l.startswith(_ENTITY_MARK)), len(lines))
        # The first marker can sit inside a function body (hms: right after `def hms(...):`); insert at the
        # top-level statement that contains or follows it, which is always a statement boundary.
        try:
            nodes = ast.parse("\n".join(lines)).body
            node = next((n for n in nodes if n.end_lineno - 1 >= at), None)
            if node is not None:
                at = min(at, _span(node)[0] - 1)
        except SyntaxError:
            pass
        block = []
        for name in missing:
            block += best_text(name) + ["", ""]
        lines[at:at] = block
    out = "\n".join(lines) + ("\n" if candidate.endswith("\n") else "")
    return out, {"changed": changed, "restored": changed}


def interface_note(best: str) -> str:
    """The turn's statement of the frozen interfaces ("" when the program has no helpers)."""
    ifs = helper_interfaces(best)
    if not ifs:
        return ""
    items = [f"- class {n}" if sig == ("class",) else f"- {n}({', '.join(sig)})" for n, sig in ifs.items()]
    return ("### Fixed helper functions\n"
            "These helpers are the program's design and stay fixed in this step: call them, keep their names and "
            "parameters (you may change their bodies). New helpers are allowed.\n" + "\n".join(items))
