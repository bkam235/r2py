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
   CRITICAL: Any package loaded via library() or require() in the R source is an R package,
   NOT a Python module. Never emit "import <r-package-name>" for any package that appeared
   in a library()/require() call — doing so will crash the script. If no Python equivalent
   exists, omit the import entirely and translate the entity as pass.
6. CRITICAL Windows locale: POSIX locale strings ("es_ES", "it_IT", "fr_FR", "en_GB",
   etc.) are INVALID on Windows Python. NEVER call locale.setlocale() directly with such
   strings — it will raise locale.Error and crash the script. When the Pattern Library
   provides a _with_locale helper, use it. Otherwise, wrap every locale.setlocale() call
   in try/except locale.Error and silently skip unsupported locales.
7. Declare which effect classes your translation will produce.
8. If you cannot translate an entity, output:
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
    prior_failures: list[str] | None = None,
) -> list[dict]:
    """Build a messages list for translating one entity.

    Returns a single-turn user message. The static SYSTEM_PROMPT is passed
    separately to llm.call() so it can be cached.
    """
    r_source = _entity_source(entity, script_map)
    annotations = _entity_annotations(entity, script_map)
    pattern_block = _format_patterns(patterns)
    dep_block = _format_dependencies(entity, prior_translations)
    free_var_block = _format_free_variables(entity)

    # For unattributed function calls, try to resolve the actual package and
    # fetch the R source so the LLM can translate the real implementation
    # rather than guessing based on the function name alone.
    resolved_pkg, pkg_fn_source = _lookup_package_source(entity, script_map)
    pkg_display = entity.package or resolved_pkg or "base R"

    parts: list[str] = []

    parts.append(f"## Entity to translate\n"
                 f"Kind: {_kind_str(entity)}\n"
                 f"Name: {entity.name}\n"
                 f"Package: {pkg_display}\n"
                 f"R-semantic flags: {', '.join(entity.r_semantic_flags) or 'none'}\n"
                 f"Predicted effects: {_effects_str(entity)}")

    parts.append(f"## R source\n```r\n{r_source}\n```")

    if annotations:
        parts.append(f"## Stage 1 annotations\n{annotations}")

    if free_var_block:
        parts.append(f"## Implicit R environment variables\n{free_var_block}")

    if pattern_block:
        parts.append(f"## Pattern Library guidance\n{pattern_block}")

    if dep_block:
        parts.append(f"## Previously translated dependencies\n{dep_block}")

    if prior_failures:
        failure_lines = "\n".join(f"- {f}" for f in prior_failures)
        parts.append(
            f"## Previous translation failures\n"
            f"The prior attempt produced these errors. Fix them in your new translation:\n"
            f"{failure_lines}"
        )

    if pkg_fn_source:
        parts.append(
            f"## R source of `{entity.name}` (from package `{resolved_pkg}`)\n"
            f"This is the actual implementation — translate it to Python rather than "
            f"marking it untranslatable:\n"
            f"```r\n{pkg_fn_source}\n```"
        )

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


def _lookup_package_source(
    entity: "Entity",
    script_map: "ScriptMap",
) -> tuple[str | None, str | None]:
    """Try to find the R source of *entity.name* from packages imported in the script.

    Returns ``(package_name, r_source)`` if the function is found in an installed
    package's R/ directory, otherwise ``(None, None)``.

    Only runs for FUNCTION_CALL entities with no package already attributed —
    i.e. bare calls like ``graycol(10)`` that lack a ``pkg::fn()`` qualifier.
    Silently returns ``(None, None)`` on any lookup error.
    """
    from ..types import EntityKind

    # Only attempt for unattributed function calls.
    if getattr(entity, "kind", None) != EntityKind.FUNCTION_CALL:
        return None, None
    if entity.package:
        return None, None

    # Collect packages loaded via library()/require() in this script.
    imported_pkgs: list[str] = [
        e.package
        for e in script_map.entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]
    if not imported_pkgs:
        return None, None

    try:
        from ..stage1.package_lookup import get_function_source
    except ImportError:
        return None, None

    fn_name = entity.name
    for pkg in imported_pkgs:
        try:
            source = get_function_source(pkg, fn_name)
        except Exception:
            source = None
        if source:
            return pkg, source

    return None, None


def _format_free_variables(entity: "Entity") -> str:
    """Describe variables used by this entity that were not defined in the script.

    Only surfaces names whose values were actually captured in actual_bundle.data —
    this naturally filters out base-R function names (c, mean, …) which are never
    captured as data variables, leaving only genuine dataset / object references.
    """
    refs = getattr(entity, "free_variable_refs", [])
    if not refs:
        return ""
    bundle = getattr(entity, "actual_bundle", None)
    bundle_data: dict = bundle.data if bundle is not None else {}
    lines: list[str] = []
    for name in refs:
        if name not in bundle_data:
            continue
        lines.append(f"- `{name}`: {_summarise_value(bundle_data[name])}")
    if not lines:
        return ""
    header = (
        "The following names are used in this entity but were NOT defined in this script.\n"
        "They were present in R's execution environment (built-in datasets, lazy-loaded objects, etc.).\n"
        "Use the shape/range info below to find an equivalent Python source — do NOT "
        "reconstruct or approximate the values from this description:"
    )
    return header + "\n" + "\n".join(lines)


def _summarise_value(val: object) -> str:
    """Return a shape/range description of a captured R value — no raw data.

    Deliberately omits actual values so the LLM cannot partially reconstruct
    the data from the summary (e.g. copy 3 sample rows of an 87-row matrix).
    """
    try:
        import numpy as np  # type: ignore[import]
        if isinstance(val, np.ndarray):
            shape = "×".join(str(d) for d in val.shape)
            lo, hi = float(np.nanmin(val)), float(np.nanmax(val))
            return f"numpy array [{shape}], values {lo:.4g}–{hi:.4g}"
    except Exception:
        pass
    try:
        import pandas as pd  # type: ignore[import]
        if isinstance(val, pd.DataFrame):
            cols = list(val.columns)[:5]
            return f"DataFrame [{val.shape[0]}×{val.shape[1]}], cols: {cols}"
    except Exception:
        pass
    if isinstance(val, list):
        # Detect matrix (list-of-equal-length-lists) and report as rows×cols.
        if val and isinstance(val[0], list):
            nrows = len(val)
            ncols = len(val[0])
            flat = [x for row in val for x in row if isinstance(x, (int, float))]
            if flat:
                lo, hi = min(flat), max(flat)
                return f"matrix [{nrows} rows × {ncols} cols], values {lo:.4g}–{hi:.4g}"
            return f"matrix [{nrows} rows × {ncols} cols]"
        lo_hi = ""
        nums = [x for x in val if isinstance(x, (int, float))]
        if nums:
            lo_hi = f", values {min(nums):.4g}–{max(nums):.4g}"
        return f"vector of {len(val)}{lo_hi}"
    if isinstance(val, (int, float)):
        return repr(val)
    return f"{type(val).__name__} (length {len(val)})" if hasattr(val, "__len__") else type(val).__name__
