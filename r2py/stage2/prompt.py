"""Per-entity LLM prompt construction for Stage 2 translation (§5.3)."""
from __future__ import annotations

import ast as _ast
import re
from typing import TYPE_CHECKING

from .stitch import is_non_translatable_source_entity as _is_non_translatable_source

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
8. Do not redefine names that are already defined by earlier entities in this script.
   If a helper function or constant you need was already generated, call it directly.
9. If you cannot translate an entity, output:
   <python>pass  # untranslatable: <brief reason></python>
   Do NOT write explanatory prose outside the XML tags.



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
    already_defined: set[str] | None = None,
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
    # Skip when the function is already defined by a prior entity — the LLM
    # should call the existing definition, not re-translate from R source.
    _defined = already_defined or set()
    if entity.name in _defined:
        resolved_pkg, pkg_fn_source = None, None
    else:
        resolved_pkg, pkg_fn_source = _lookup_package_source(entity, script_map)
    pkg_display = entity.package or resolved_pkg or "base R"

    # Resolve free variable refs that are functions from imported packages.
    # These are symbols used in this entity (e.g. passed by reference as
    # arguments) but not defined in the script — the per-entity translator
    # needs their R source to translate correctly rather than guessing.
    free_ref_sources = _lookup_free_ref_sources(entity, script_map)

    parts: list[str] = []

    parts.append(f"## Entity to translate\n"
                 f"Kind: {_kind_str(entity)}\n"
                 f"Name: {entity.name}\n"
                 f"Package: {pkg_display}\n"
                 f"R-semantic flags: {', '.join(entity.r_semantic_flags) or 'none'}\n"
                 f"Predicted effects: {_effects_str(entity)}")

    parts.append(f"## R source\n```r\n{r_source}\n```")

    _resolved = getattr(entity, "resolved_call", None)
    if _resolved:
        parts.append(
            f"## R positional arg binding (from match.call)\n"
            f"R resolves this call to: `{_resolved}`\n"
            "Positional arguments are bound to formals in this order. "
            "Unmatched positional args go to `...` (dots). "
            "Your Python translation MUST bind arguments accordingly."
        )

    _fm = getattr(entity, "function_metadata", None)
    if _fm is not None:
        fm_parts = ["## Function metadata (from R introspection)"]
        if _fm.formals:
            formals_str = ", ".join(f"{k}={v}" if v else k for k, v in _fm.formals.items())
            fm_parts.append(f"Formals: {formals_str}")
        if _fm.methods:
            fm_parts.append(f"S3 methods: {', '.join(_fm.methods)}")
        if _fm.where:
            fm_parts.append(f"Defined in: {', '.join(_fm.where)}")
        parts.append("\n".join(fm_parts))

    # If R produced output when this entity was evaluated, show it so the LLM
    # knows the output format to reproduce.  When R library source is available,
    # redact data values to prevent the LLM from hardcoding them instead of
    # implementing the actual computation.
    _has_r_source = bool(pkg_fn_source or free_ref_sources)
    _entity_bundles = getattr(script_map, "entity_bundles", {})
    _r_entity_bundle = _entity_bundles.get(entity.id)
    if _r_entity_bundle is not None:
        _r_stdout = (_r_entity_bundle.stdout or "").strip()
        if _r_stdout:
            _stdout_lines = _r_stdout.splitlines()
            if len(_stdout_lines) > 50:
                _r_stdout = "\n".join(_stdout_lines[:50]) + f"\n... ({len(_stdout_lines) - 50} more lines truncated)"
            if _has_r_source:
                _r_stdout_fmt = _redact_data_values(_r_stdout)
                parts.append(
                    "## Expected R output format\n"
                    "R produced output in the format shown below (data values replaced "
                    "with «…»). Your Python translation MUST implement the R source "
                    "code provided and produce output that matches this FORMAT exactly "
                    "WITHOUT hardcoding values — compute them from the data:\n"
                    f"```\n{_r_stdout_fmt}\n```"
                )
            else:
                parts.append(
                    "## Expected R output\n"
                    "R produced the following output when this entity was evaluated. "
                    "Your Python translation MUST produce output that matches this "
                    "format exactly:\n"
                    f"```\n{_r_stdout}\n```"
                )

    if annotations:
        parts.append(f"## Stage 1 annotations\n{annotations}")

    if free_var_block:
        parts.append(f"## Implicit R environment variables\n{free_var_block}")

    # Phase 3b: RNG / file-read / env-query entities are loaded from R-captured
    # values at test time by the data-loading shim — emitting the natural
    # Python translation is still desired (it's what the saved .py shows the
    # reader), but the LLM should know its output value will be overridden so
    # PRNG / file-content divergence doesn't surface as a translation error.
    if _is_non_translatable_source(r_source):
        parts.append(
            "## Test-harness note: pre-loaded entity\n"
            "This entity's defining call is a non-deterministic source (RNG draw, "
            "file read, or environment query). At equivalence-test time, the test "
            "harness pre-loads this entity's output from the R-captured value, so "
            "it will overwrite whatever your translation assigns. Emit the natural, "
            "idiomatic Python translation anyway (it is preserved in the saved "
            ".py for the reader) — do NOT try to match R's PRNG, encode the file "
            "contents inline, or otherwise short-circuit the call."
        )

    example_block = _format_translation_examples(patterns)
    if example_block:
        parts.append(f"## Verified Translation Example\n{example_block}")

    if pattern_block:
        parts.append(f"## Pattern Library guidance\n{pattern_block}")

    if dep_block:
        parts.append(f"## Previously translated dependencies\n{dep_block}")

    already_defined_block = _format_already_defined(already_defined)
    if already_defined_block:
        parts.append(f"## Already defined in this script\n{already_defined_block}")

    repeated_block = _repeated_call_hint(entity, script_map, already_defined)
    if repeated_block:
        parts.append(repeated_block)

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
            f"You MUST implement Python code that produces the same output as "
            f"this R code. Translate the logic — do NOT hardcode return values "
            f"or output strings:\n"
            f"```r\n{pkg_fn_source}\n```"
        )

    if free_ref_sources:
        ref_parts: list[str] = []
        for ref_name, ref_pkg, ref_source in free_ref_sources:
            ref_parts.append(
                f"### `{ref_name}` (from package `{ref_pkg}`)\n"
                f"```r\n{ref_source}\n```"
            )
        parts.append(
            "## Library functions referenced by this entity\n"
            "This entity uses the following function(s) from loaded R packages. "
            "You MUST translate the R source below into working Python functions "
            "that compute correct results — do NOT hardcode return values or "
            "output strings. "
            "Define ONLY these listed functions as Python functions above the usage "
            "so this entity's behaviour matches R. Later entities that call the "
            "same function will reuse your definition.\n\n"
            "CRITICAL: Do NOT define, assign, or fabricate any OTHER names "
            "(variables, datasets, arrays) — especially not names listed in the "
            "\"Implicit R environment variables\" section above. Those are pre-loaded "
            "by the test harness and must be used as-is.\n\n"
            + "\n\n".join(ref_parts)
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

def _redact_data_values(stdout: str) -> str:
    """Replace data values in R output with ``<values>``, preserving format.

    Keeps tibble headers ("# A tibble: ..."), column names, type annotations
    (<dbl>, <chr>, etc.), and row numbers.  Replaces the actual data cells
    so the LLM can see the output format without being tempted to hardcode values.
    """
    import re

    lines = stdout.splitlines()
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Preserve blank lines
        if not stripped:
            result.append(line)
            continue
        # Preserve tibble/data-frame headers
        if stripped.startswith("#"):
            result.append(line)
            continue
        # Preserve type annotation rows: lines consisting of <type> tokens
        if re.match(r'^[\s<>a-z/]+$', stripped):
            result.append(line)
            continue
        # Preserve column-name header rows: no standalone numbers
        if not re.search(r'(?<!\w)\d+\.?\d*(?!\w)', stripped):
            result.append(line)
            continue
        # Data row: replace values after the row number or [n] prefix
        m = re.match(r'^(\s*\d+\s+)', line) or re.match(r'^(\s*\[\d+\]\s*)', line)
        if m:
            result.append(m.group(1) + "<values>")
        else:
            result.append("<values>")
    return "\n".join(result)


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


def _format_translation_examples(patterns: list["Pattern"]) -> str:
    """Return a prompt block showing the best verified translation example across patterns.

    Shows the highest-quality TranslationExample from the first pattern that has one.
    Prefers examples that define a Python callable (contain 'def ') over call-site
    snippets, then breaks ties by score.  Returns "" when no examples exist yet.
    """
    for pat in patterns:
        examples = getattr(pat, "translation_examples", [])
        if examples:
            ex = max(
                examples,
                key=lambda e: (1 if "def " in e.py_snippet else 0, e.score),
            )
            return (
                f"From pattern `{pat.id}` (score {ex.score:.2f}):\n"
                f"R:\n```r\n{ex.r_snippet}\n```\n"
                f"Python:\n```python\n{ex.py_snippet}\n```"
            )
    return ""


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

    For S3 generics (tidy, glance, augment, etc.), the bare name often resolves
    to just ``UseMethod("name")`` or isn't directly findable.  When entity_types
    is available from the sandbox run, we use the runtime class of the first
    argument to construct the S3 method name (e.g. ``tidy.durbinWatsonTest``)
    and look that up instead.
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
        from ..stage1.package_lookup import get_function_source_recursive
    except ImportError:
        return None, None

    fn_name = entity.name

    # Try S3 method name first when we have runtime class information.
    s3_source = _try_s3_method_lookup(entity, script_map, imported_pkgs)
    if s3_source:
        source, found_pkg = s3_source
        return found_pkg, source

    # Fall back to bare name lookup.
    try:
        source = get_function_source_recursive(imported_pkgs, fn_name)
    except Exception:
        source = None
    if source:
        from ..stage1.package_lookup import get_function_source as _gfs
        found_pkg = next(
            (p for p in imported_pkgs if _gfs(p, fn_name, max_lines=1) is not None),
            imported_pkgs[0],
        )
        return found_pkg, source

    return None, None


def _try_s3_method_lookup(
    entity: "Entity",
    script_map: "ScriptMap",
    imported_pkgs: list[str],
) -> tuple[str, str] | None:
    """Try to resolve an S3 method using runtime class info from entity_types.

    Extracts the first argument name from the entity's R source, finds its
    runtime class in entity_types, and looks up ``fn_name.class_name`` in the
    imported packages.  Returns ``(r_source, package_name)`` or None.
    """
    import re

    entity_types = getattr(script_map, "entity_types", {})
    if not entity_types:
        return None

    # Extract first argument name from R source: fn_name(arg, ...)
    r_source = _entity_source(entity, script_map)
    m = re.match(r'\s*\w[\w.]*\s*\(\s*([a-zA-Z.][a-zA-Z0-9._]*)', r_source)
    if not m:
        return None
    first_arg = m.group(1)

    # Find which entity defined this variable and get its class from entity_types.
    arg_classes: list[str] = []
    for eid, types_dict in entity_types.items():
        if first_arg in types_dict:
            cls = types_dict[first_arg].get("class", "")
            if cls:
                arg_classes = [c.strip() for c in cls.split(",")]
            break

    if not arg_classes:
        return None

    from ..stage1.package_lookup import get_function_source_recursive, get_function_source

    # Try each class in the S3 method resolution order.
    fn_name = entity.name
    for cls in arg_classes:
        method_name = f"{fn_name}.{cls}"
        try:
            source = get_function_source_recursive(imported_pkgs, method_name)
        except Exception:
            continue
        if source:
            found_pkg = next(
                (p for p in imported_pkgs if get_function_source(p, method_name, max_lines=1) is not None),
                imported_pkgs[0],
            )
            return source, found_pkg

    return None


def _lookup_free_ref_sources(
    entity: "Entity",
    script_map: "ScriptMap",
) -> list[tuple[str, str, str]]:
    """Find R source for free variable refs that are functions from imported packages.

    Returns a list of ``(symbol_name, package_name, r_source)`` tuples for each
    free variable ref that resolves to a function in one of the script's loaded
    packages.  Skips refs that are already defined by prior entities in the
    script (those are handled by the dependency/already-defined mechanism).
    """
    from ..types import EntityKind

    refs = getattr(entity, "free_variable_refs", [])
    if not refs:
        return []

    # Refs already in actual_bundle.data are data values handled by the shim.
    bundle = getattr(entity, "actual_bundle", None)
    bundle_data: dict = bundle.data if bundle is not None else {}

    # Names already defined by prior entities — no need to look them up.
    defined_names: set[str] = set()
    for e in script_map.entities.values():
        if e.source_span.start_line < entity.source_span.start_line:
            defined_names.add(e.name)

    imported_pkgs: list[str] = [
        e.package
        for e in script_map.entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]
    if not imported_pkgs:
        return []

    try:
        from ..stage1.package_lookup import get_function_source_recursive, get_function_source
    except ImportError:
        return []

    results: list[tuple[str, str, str]] = []
    for ref_name in refs:
        if ref_name in bundle_data:
            continue
        if ref_name in defined_names:
            continue
        try:
            source = get_function_source_recursive(imported_pkgs, ref_name)
        except Exception:
            source = None
        if not source:
            continue
        found_pkg = next(
            (p for p in imported_pkgs if get_function_source(p, ref_name, max_lines=1) is not None),
            imported_pkgs[0],
        )
        results.append((ref_name, found_pkg, source))

    return results


def _format_already_defined(names: set[str] | None) -> str:
    """Format the set of already-defined helper names for display in the prompt."""
    if not names:
        return ""
    sorted_names = sorted(names)
    listing = ", ".join(f"`{n}`" for n in sorted_names)
    return (
        "The following names were defined by earlier entities in this translation. "
        "Do NOT redefine them — call them directly.\n"
        "You MUST still translate this entity's R code into Python — just use the "
        "existing definitions instead of re-implementing them:\n"
        + listing
    )


def _repeated_call_hint(
    entity: "Entity",
    script_map: "ScriptMap",
    already_defined: set[str] | None,
) -> str:
    """Return a prompt section when an entity name appears more than once in the script.

    Two cases:
    - First occurrence (name not yet in already_defined): tell the LLM to define
      a reusable Python construct rather than inlining the logic.
    - Later occurrence (name already defined by a prior entity): tell the LLM to
      use the existing definition directly and NOT redefine it.

    Applies to: FunctionCall, ExternalSymbol, FunctionDef, S4Class, R6Class, Formula.
    Excluded: Variable, Constant, LibraryImport — for those, repeated names mean
    intentional reassignment or duplicate imports, not re-use of the same definition.
    """
    from ..types import EntityKind

    _REUSE_KINDS = (
        EntityKind.FUNCTION_CALL,
        EntityKind.EXTERNAL_SYMBOL,
        EntityKind.FUNCTION_DEF,
        EntityKind.S4_CLASS,
        EntityKind.R6_CLASS,
        EntityKind.FORMULA,
    )
    _CLASS_KINDS = (EntityKind.S4_CLASS, EntityKind.R6_CLASS)

    kind = getattr(entity, "kind", None)
    if kind not in _REUSE_KINDS:
        return ""

    name = getattr(entity, "name", "") or ""
    if not name:
        return ""

    entities = getattr(script_map, "entities", {})
    count = sum(1 for e in entities.values() if getattr(e, "name", "") == name)
    if count < 2:
        return ""

    construct = "class" if kind in _CLASS_KINDS else "function/callable"
    defined = already_defined or set()

    if name in defined:
        # Check whether this entity has per-entity R stdout (meaning R produced
        # a specific output format that must be matched, not just auto-print).
        _entity_bundles = getattr(script_map, "entity_bundles", {})
        _r_eb = _entity_bundles.get(entity.id)
        _has_custom_output = (
            _r_eb is not None
            and (_r_eb.stdout or "").strip()
        )
        if _has_custom_output:
            print_hint = (
                f"The 'Expected R output' section above shows the exact output this "
                f"entity must produce. Do NOT use `print({name}(...))` alone — the raw "
                f"Python repr will NOT match R's format. Use the same output-formatting "
                f"approach that produced the first `{name}` entity's output."
            )
        else:
            print_hint = (
                f"If the R code is a bare call like `{name}(...)` at the top level, "
                f"translate it as `print({name}(...))` to match R's auto-print behaviour."
            )
        return (
            f"## Use existing definition — do NOT redefine\n"
            f"`{name}` was already translated as a Python {construct} by an earlier "
            f"entity in this script. Do NOT redefine or re-implement it here. "
            f"You MUST still translate this entity's R code — call `{name}` with the "
            f"appropriate arguments. {print_hint}"
        )
    else:
        return (
            f"## Define a reusable {construct} ({count} uses in this script)\n"
            f"`{name}` appears {count} times in this script. "
            f"In your translation of THIS entity, define a reusable Python {construct} "
            f"`{name}` that captures the full logic, then use it for this specific call. "
            f"Later entities will reuse your definition directly — do not inline the "
            f"logic separately for each occurrence."
        )


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
        "They were captured from R's execution environment (built-in datasets, RNG draws,\n"
        "file reads, etc.) and will be PRE-LOADED into Python globals by an external test\n"
        "harness BEFORE this code runs.\n"
        "\n"
        "Use each name AS-IS. Do NOT emit code to load, import, read, sample, or otherwise\n"
        "reconstruct these values — any such code will run AFTER the pre-loaded value is\n"
        "already bound and may overwrite it with a divergent value, breaking the equivalence\n"
        "test. The shape/range info below is for type-aware reference only:"
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
