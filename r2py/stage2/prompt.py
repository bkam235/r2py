"""Per-entity LLM prompt construction for Stage 2 translation (§5.3)."""
from __future__ import annotations

import ast as _ast
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stage1.entities import Entity
    from ..stage1.script_map import ScriptMap
    from ..library.pattern import Pattern
    from ..types import EntityId

# ---------------------------------------------------------------------------
# Static system prompt — version-controlled, never mutated at runtime (§5.7).
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a precise R-to-Python translator operating entity-by-entity.
For each R entity you receive, produce equivalent Python code.

Rules:
1. Translate ONLY the given entity's source span — not the whole script.
2. Preserve all observable behaviour: values, side effects, output format.
3. When Pattern Library guidance is provided, follow it exactly.
4. Honour all Stage 1 semantic annotations (1-based indexing, NA semantics,
   NSE, vector recycling, copy-on-modify, super-assign, dispatch flags).
5. List required imports separately; do not embed import statements in the snippet.
6. Declare which effect classes your translation will produce.
7. If you cannot translate an entity, output:
   <python>pass  # untranslatable: <brief reason></python>
   Do NOT write explanatory prose outside the XML tags.

R-to-Python semantic notes (always apply):
- R vectors are 1-indexed; Python lists/arrays are 0-indexed.
- R NA is NOT Python None or float('nan'); use pandas.NA or numpy.nan as appropriate.
- R's x:y produces an inclusive range; use range(x, y+1) in Python.
- Negative R indices exclude elements, not index from the end.
- R has no scalars; length-1 vectors should stay as length-1 arrays where behaviour differs.
- <<- super-assignment escapes the local scope; model with nonlocal or a mutable container.
- NSE (non-standard eval) in dplyr/ggplot2 must be rewritten as explicit Python equivalents.

Output format (use these exact XML tags — no other text outside the tags):
<python>
...the Python snippet for this entity only...
</python>
<imports>import statement 1, import statement 2, ...</imports>
<effects>STDOUT,DATA,FILES,GRAPHICS,HTML,ENV,WARNINGS</effects>
"""


def build_entity_prompt(
    entity: "Entity",
    script_map: "ScriptMap",
    patterns: list["Pattern"],
    prior_translations: dict[str, str],
) -> list[dict]:
    """Build a messages list for translating one entity.

    Returns a single-turn user message. The static SYSTEM_PROMPT is passed
    separately to llm.call() so it can be cached.
    """
    r_source = _entity_source(entity, script_map)
    annotations = _entity_annotations(entity, script_map)
    pattern_block = _format_patterns(patterns)
    dep_block = _format_dependencies(entity, prior_translations)

    parts: list[str] = []

    parts.append(f"## Entity to translate\n"
                 f"Kind: {_kind_str(entity)}\n"
                 f"Name: {entity.name}\n"
                 f"Package: {entity.package or 'base R'}\n"
                 f"R-semantic flags: {', '.join(entity.r_semantic_flags) or 'none'}\n"
                 f"Predicted effects: {_effects_str(entity)}")

    parts.append(f"## R source\n```r\n{r_source}\n```")

    if annotations:
        parts.append(f"## Stage 1 annotations\n{annotations}")

    if pattern_block:
        parts.append(f"## Pattern Library guidance\n{pattern_block}")

    if dep_block:
        parts.append(f"## Previously translated dependencies\n{dep_block}")

    parts.append("Translate this entity to Python. Use the XML output format specified in the system prompt.")

    user_content = "\n\n".join(parts)
    return [{"role": "user", "content": user_content}]


def parse_entity_response(raw: str) -> tuple[str, list[str], list[str]]:
    """Parse LLM response into (python_snippet, imports, effects).

    Falls back to treating the full response as the python snippet on parse failure.
    """
    python = _extract_tag(raw, "python")
    imports_raw = _extract_tag(raw, "imports")
    effects_raw = _extract_tag(raw, "effects")

    if python is None:
        # Fallback: strip fences and use the whole response.
        python = _strip_fences(raw)

    imports: list[str] = []
    if imports_raw:
        imports = [s.strip() for s in imports_raw.split(",") if s.strip()]

    effects: list[str] = []
    if effects_raw:
        effects = [s.strip() for s in effects_raw.split(",") if s.strip()]

    python = python.strip()

    # Validate: if the extracted snippet is not parseable Python, replace it
    # with a no-op stub so the assembled script stays syntactically valid.
    try:
        _ast.parse(python)
    except SyntaxError:
        python = "pass  # r2py: translation failed for entity (LLM response not valid Python)"

    return python, imports, effects


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _entity_source(entity: "Entity", script_map: "ScriptMap") -> str:
    """Extract the R source text for the entity's span."""
    sp = entity.source_span
    if not sp or not script_map.source:
        return entity.name
    lines = script_map.source.splitlines()
    # source_span uses 0-based line numbers (tree-sitter rows); end+1 because
    # Python list slices are exclusive on the right.
    start = sp.start_line
    end = min(len(lines), sp.end_line + 1)
    return "\n".join(lines[start:end])


def _entity_annotations(entity: "Entity", script_map: "ScriptMap") -> str:
    """Pull the # r2py: annotation lines near this entity from annotated R."""
    annotated = getattr(script_map, "_annotated_r_cache", None)
    if annotated is None:
        try:
            annotated = script_map.to_annotated_r()
            # Cache so subsequent entity calls reuse the same string.
            try:
                script_map._annotated_r_cache = annotated
            except AttributeError:
                pass  # frozen dataclass — caching not possible, accept the cost
        except Exception:
            return ""
    sp = entity.source_span
    if not sp:
        return ""
    lines = annotated.splitlines()
    # 0-based rows; +1 for exclusive slice, +2 lookahead for trailing annotation lines
    start = sp.start_line
    end = min(len(lines), sp.end_line + 3)
    relevant = [ln for ln in lines[start:end] if "# r2py:" in ln]
    return "\n".join(relevant)


def _format_patterns(patterns: list["Pattern"]) -> str:
    if not patterns:
        return ""
    parts: list[str] = []
    for i, pat in enumerate(patterns, 1):
        ev_count = len(pat.evidence)
        parts.append(
            f"**Pattern {i}** ({pat.id}, confidence: {pat.confidence}, evidence: {ev_count} scripts)\n"
            f"{pat.guidance.strip()}"
        )
    return "\n\n".join(parts)


def _format_dependencies(entity: "Entity", prior: dict[str, str]) -> str:
    if not entity.dependencies:
        return ""
    parts: list[str] = []
    for ref in entity.dependencies:
        snippet = prior.get(ref.entity_id)
        if snippet:
            parts.append(f"# {ref.entity_id}\n{snippet.strip()}")
    return "\n\n".join(parts)


def _kind_str(entity: "Entity") -> str:
    kind = getattr(entity, "kind", None)
    if kind is None:
        return "unknown"
    return getattr(kind, "value", str(kind))


def _effects_str(entity: "Entity") -> str:
    if not entity.predicted_effects:
        return "none"
    return ", ".join(getattr(e, "value", str(e)) for e in entity.predicted_effects)


def _extract_tag(text: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return m.group(1) if m else None


def _strip_fences(text: str) -> str:
    # Require the 'python' language label to avoid extracting R code or prose
    # that happens to be inside a generic ``` fence.
    m = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1)
    return text
