"""Compose per-entity Python snippets into one .py file (§5.5)."""
from __future__ import annotations

import ast as _ast
import re
from typing import TYPE_CHECKING

# R packages that have no Python equivalents and must never appear as imports.
# Entries here are bare package names (no dots/underscores disambiguation needed).
_R_ONLY_PACKAGES: frozenset[str] = frozenset({
    "withr", "dplyr", "ggplot2", "shiny", "magrittr", "tidyr", "purrr",
    "rlang", "tibble", "stringr", "forcats", "readr", "lubridate",
    "broom", "tidyverse", "devtools", "testthat", "usethis",
    "data.table", "caret", "mlr", "mlr3", "glue",
})

_SENTINEL_RE = re.compile(r"^# r2py:entity:(\S+)$")

# Data-loading shim sentinels (§ Option A in plans/i-go-with-option-melodic-dewdrop.md).
# Saved on disk in fully-commented form; the verifier un-comments at sandbox time.
DATA_SHIM_BEGIN = "# r2py:data_shim:begin"
DATA_SHIM_END = "# r2py:data_shim:end"
DATA_SHIM_RE = re.compile(
    r"(# r2py:data_shim:begin\n)(.*?)(# r2py:data_shim:end)",
    re.DOTALL,
)

# R call names whose results are non-deterministic from Python's PRNG (RNG)
# or environment-dependent (file reads, env vars).  Entities whose defining
# call is in this set are reclassified as "non-translatable sources" — their
# captured R values are loaded by the shim at test time even though they ARE
# defined in the script.  This is the only case where the shim overrides a
# name the translation also assigns; without it, the equivalence test would
# fail purely because the two PRNGs produced different draws.
_NON_TRANSLATABLE_SOURCE_CALLS: frozenset[str] = frozenset({
    "rnorm", "runif", "sample", "rbinom", "rpois", "rgamma", "rbeta", "rt",
    "rexp", "rchisq", "rlnorm", "rweibull", "rcauchy", "rf",
    "read.csv", "read.csv2", "read.table", "read.delim", "read.delim2",
    "readRDS", "readLines", "scan", "load",
    "Sys.getenv", "Sys.time", "Sys.Date", "Sys.timezone",
})

# Compile once: match the first call expression in an entity's R source.
# Captures the (possibly dotted) function name.
_R_CALL_RE = re.compile(r"\b([A-Za-z_][\w.]*)\s*\(")


_R_COMMENT_RE = re.compile(r"#[^\n]*")


def is_non_translatable_source_entity(entity_source: str) -> bool:
    """Return True if *entity_source* assigns from a non-translatable R source.

    Used by compose() to widen the shim's payload beyond pure free-variable
    refs.  Detection is intentionally simple: strip R comments first (so a
    name in a comment never triggers a false positive), then look at the first
    call expression in the code; if it's in the allowlist, the value must be
    loaded from the R-captured sidecar rather than recomputed.
    """
    if not entity_source:
        return False
    # Strip line comments first — a comment like ``# uses rnorm()`` must not
    # cause the classifier to mark an unrelated entity as a non-translatable
    # source.  R has no block comments, so a single-pass strip is sufficient.
    text = _R_COMMENT_RE.sub("", entity_source).strip()
    # Strip a leading assignment so we look at the RHS.
    text = re.sub(r"^[A-Za-z_.][\w.]*\s*(<-|=)\s*", "", text, count=1)
    m = _R_CALL_RE.search(text)
    if not m:
        return False
    return m.group(1) in _NON_TRANSLATABLE_SOURCE_CALLS


def build_data_shim(
    needed_names: list[str],
    sidecar_filename: str,
    script_relpath: str | None = None,
) -> str:
    """Return the commented-out data-loading shim block.

    Every body line is prefixed ``# `` so the saved .py is a no-op when run
    directly.  The verifier strips the prefix at sandbox time via
    ``DATA_SHIM_RE`` to activate the shim for the equivalence test.

    Body lines load *sidecar_filename* (which must sit next to ``__file__``)
    and bind any name in *needed_names* that is present in the captured data
    into module globals.  Names not in the captured data are silently skipped
    — the translation's natural assignment then takes over for them.

    *script_relpath* — when provided, the shim defines ``__file__`` as a
    fallback if it is not already bound (i.e. when the body is pasted into a
    REPL or executed without ``runpy.run_path``).  Use forward slashes for
    cross-platform compatibility; ``Path`` normalizes them on Windows.
    """
    if not needed_names or not sidecar_filename:
        return ""
    # Build the name list as a Python literal so it embeds cleanly in a comment.
    names_literal = "[" + ", ".join(repr(n) for n in sorted(needed_names)) + "]"
    body: list[str] = [
        "import json as _r2py_shim_json",
        "from pathlib import Path as _r2py_shim_Path",
    ]
    if script_relpath:
        # Normalize backslashes to forward slashes — works on every OS, dodges
        # the ``\n`` / ``\t`` escape-sequence pitfall in single-quoted strings.
        normalized = script_relpath.replace("\\", "/")
        body.append(
            f"if '__file__' not in globals(): __file__ = {normalized!r}"
        )
    body.extend([
        f"_r2py_shim_data = _r2py_shim_json.loads("
        f"(_r2py_shim_Path(__file__).parent / {sidecar_filename!r}).read_text(encoding='utf-8'))",
        f"for _r2py_shim_n in {names_literal}:",
        "    if _r2py_shim_n in _r2py_shim_data:",
        "        globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]",
    ])
    return (
        DATA_SHIM_BEGIN
        + "\n"
        + "\n".join("# " + line for line in body)
        + "\n"
        + DATA_SHIM_END
    )


def validate_data_shim(source: str, expected_names: list[str] | None = None) -> str | None:
    """Check data shim integrity in *source*. Return error message or None if OK.

    Checks:
      1. Completeness: if DATA_SHIM_BEGIN is present, DATA_SHIM_END must also be.
      2. Variable coverage: if *expected_names* is provided, the shim's name list
         must contain all of them.
    """
    has_begin = DATA_SHIM_BEGIN in source
    has_end = DATA_SHIM_END in source
    if has_begin and not has_end:
        return "data_shim is incomplete (begin marker without end marker)"
    if not has_begin:
        return None
    if expected_names:
        m = re.search(r"for _r2py_shim_n in (\[.*?\]):", source)
        if not m:
            return "data_shim is malformed (no for-loop over needed names)"
        try:
            shim_names = set(eval(m.group(1)))  # noqa: S307 — trusted source
        except Exception:
            return "data_shim is malformed (cannot parse name list)"
        missing = set(expected_names) - shim_names
        if missing:
            return f"data_shim missing variables: {sorted(missing)}"
    return None


def collect_shim_needed_names(script_map: "ScriptMap") -> list[str]:
    """Return names the data-loading shim should pre-bind for *script_map*.

    Two sources:
      1. Free-variable refs whose values were captured into ``actual_bundle.data``
         — these are R built-in datasets, package datasets, and other inherited
         values the script uses but does not define.
      2. Names defined by entities whose RHS is a non-translatable source call
         (RNG, file read, environment query) — see
         ``is_non_translatable_source_entity``.

    Empty list if no captured data is available — caller can then skip shim
    emission entirely.
    """
    entities = getattr(script_map, "entities", {}) or {}
    # Bundle data is shared across all entities (Stage 1 main run); grab any one.
    captured: dict = {}
    for e in entities.values():
        ab = getattr(e, "actual_bundle", None)
        if ab is not None and ab.data:
            captured = ab.data
            break
    if not captured:
        return []

    needed: set[str] = set()

    # (1) Free variable refs the script references but does not define.
    for e in entities.values():
        for ref in getattr(e, "free_variable_refs", []) or []:
            if ref in captured:
                needed.add(ref)

    # (2) Names defined by RNG/read entities — overridden by R-captured values
    # at test time so equivalence doesn't fail on PRNG divergence.
    r_source = getattr(script_map, "source", "") or ""
    r_lines = r_source.splitlines() if r_source else []
    for e in entities.values():
        span = getattr(e, "source_span", None)
        if span is None or not r_lines:
            continue
        # SourceLocation uses 0-based tree-sitter rows; end+1 because slices
        # are exclusive.  Matches the convention used in stage2/prompt.py
        # (_entity_source).  Using 1-based math here would slice one line
        # too early and miss single-line entities at row 0 entirely
        # (lines[-1:0] returns []).
        try:
            start = max(0, span.start_line)
            end = min(len(r_lines), span.end_line + 1)
            seg = "\n".join(r_lines[start:end])
        except Exception:
            continue
        if is_non_translatable_source_entity(seg):
            name = getattr(e, "name", None)
            if name and name in captured:
                needed.add(name)

    return sorted(needed)


from .. import __version__ as _r2py_version


def get_toplevel_def_names(text: str) -> set[str]:
    """Return names of top-level ``def``/``class`` blocks and ``_``-prefixed assignments.

    These are the shared helpers that, when duplicated across entity translations,
    should be deduplicated rather than renamed.
    """
    try:
        tree = _ast.parse(text)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, _ast.Assign):
            for t in node.targets:
                if isinstance(t, _ast.Name) and t.id.startswith("_"):
                    names.add(t.id)
    return names


def remove_shim_overrides(text: str, shim_names: set[str]) -> str:
    """Strip top-level assignments whose target is a name pre-loaded by the shim.

    The data-loading shim (Option A) binds R-captured values into module
    globals BEFORE the translated body runs.  Any later top-level assignment
    to the same name overwrites the authoritative R value with whatever the
    LLM produced — typically a truncated stub when the data is large
    (the LLM token budget can't reproduce ``volcano``'s 87×61 elevation
    matrix faithfully, so it hallucinates a few rows of plausible values).

    Stripping these assignments at compose time is a structural guarantee
    that complements the LLM-facing prompt instruction (which the LLM may
    ignore).  Side-effecting RHS expressions are converted to bare
    expression statements so the side effects, if any, are preserved.
    """
    if not shim_names:
        return text
    try:
        tree = _ast.parse(text)
    except SyntaxError:
        return text

    lines = text.splitlines()
    # Map line index → replacement text (None = delete line).
    line_edits: dict[int, str | None] = {}

    for node in tree.body:
        if not isinstance(node, _ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, _ast.Name):
            continue
        if target.id not in shim_names:
            continue

        # The assignment may span several lines (e.g. multi-line np.array).
        # Mark the whole node range for removal.
        start = node.lineno - 1
        end = node.end_lineno - 1 if node.end_lineno else start
        for i in range(start, end + 1):
            line_edits[i] = None

    if not line_edits:
        return text

    result = [
        line for i, line in enumerate(lines)
        if line_edits.get(i, line) is not None
    ]
    # Tidy trailing/leading blank lines created by the removal.
    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    return "\n".join(result)


def remove_prior_definitions(text: str, defined: set[str]) -> str:
    """Strip top-level definitions whose names are already in *defined*.

    Removes entire ``def``/``class`` blocks and ``_``-prefixed constant
    assignments that duplicate code already generated by an earlier entity.
    Regular (non-``_``) variable assignments are left untouched so that
    ``_resolve_collisions`` can rename them in the usual way.
    """
    if not defined:
        return text
    try:
        tree = _ast.parse(text)
    except SyntaxError:
        return text

    lines = text.splitlines()
    remove_lines: set[int] = set()  # 0-indexed

    for node in tree.body:
        name: str | None = None
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
            name = node.name
        elif isinstance(node, _ast.Assign):
            if (len(node.targets) == 1
                    and isinstance(node.targets[0], _ast.Name)
                    and node.targets[0].id.startswith("_")):
                name = node.targets[0].id

        if name and name in defined:
            for i in range(node.lineno - 1, node.end_lineno):
                remove_lines.add(i)

    if not remove_lines:
        return text

    result = [line for i, line in enumerate(lines) if i not in remove_lines]
    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    return "\n".join(result)

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import EntityId


def compose(
    per_entity: dict[str, str],
    per_entity_imports: dict[str, list[str]],
    order: list[str],
    script_map: "ScriptMap",
    model: str,
    r_path: str = "",
    sidecar_filename: str | None = None,
    script_relpath: str | None = None,
) -> tuple[str, dict[str, tuple[int, int]]]:
    """Compose ordered snippets into a single Python source string.

    Returns:
        (source, entity_line_map) where entity_line_map maps each EntityId to
        the (start_line, end_line) range (1-indexed, inclusive) of its body
        snippet in the assembled source.

    Steps:
    1. Collect all import lines (from snippets + per_entity_imports), deduplicate, sort.
    2. Collect body snippets in topological order, tracking per-entity line ranges.
    3. Resolve name collisions (suffix _1, _2, ...).
    4. Prepend header comment.
    """
    all_imports: list[str] = []
    body_items: list[tuple[str, str]] = []   # (eid, body_text)
    defined_names: dict[str, str] = {}  # python_name → entity_id that defined it
    already_defined_defs: set[str] = set()  # def/class names + _-prefixed consts already emitted

    # Compute shim payload up front so we can strip body-level reassignments
    # to those names (the shim is authoritative — see remove_shim_overrides).
    shim_needed_names: list[str] = (
        collect_shim_needed_names(script_map) if sidecar_filename else []
    )
    shim_names_set: set[str] = set(shim_needed_names)

    for eid in order:
        snippet = per_entity.get(eid, "")
        # Collect explicit imports registered by the translator
        for imp in per_entity_imports.get(eid, []):
            imp = imp.strip()
            if imp and _is_import_line(imp):
                all_imports.append(imp)

        # Split snippet into import lines vs body lines
        imp_lines, body_lines = _split_imports(snippet)
        all_imports.extend(imp_lines)

        if body_lines:
            body_text = "\n".join(body_lines)
            # Remove def/class blocks and _-prefixed constants already emitted by a
            # prior entity — these are shared helpers, not entity-specific state.
            body_text = remove_prior_definitions(body_text, already_defined_defs)
            # Strip top-level assignments to names the shim pre-loads.  The LLM
            # sometimes hallucinates a truncated literal (e.g. a 2-row stub of
            # the 87-row ``volcano`` matrix) when told the value is pre-bound;
            # removing the assignment guarantees the shim's authoritative value
            # survives into the body.
            body_text = remove_shim_overrides(body_text, shim_names_set)
            if not body_text.strip():
                continue  # entity was nothing but a shim-overridden assignment
            body_text = _resolve_collisions(body_text, eid, defined_names)
            # Track all helpers newly defined by this entity for subsequent entities.
            already_defined_defs.update(get_toplevel_def_names(body_text))
            body_text = f"# r2py:entity:{eid}\n" + body_text
            body_items.append((eid, body_text))

    # Deduplicate, filter R-only packages, and sort imports
    seen: set[str] = set()
    deduped_imports: list[str] = []
    for imp in all_imports:
        if imp not in seen and not _is_r_only_import(imp):
            seen.add(imp)
            deduped_imports.append(imp)
    deduped_imports = _remove_module_shadows(deduped_imports)
    deduped_imports.sort(key=_import_sort_key)

    # Build header
    n_entities = len(script_map.entities) if hasattr(script_map, "entities") else 0
    r_label = r_path or getattr(script_map, "source_file", "<R script>")
    header = (
        f"# Translated from {r_label} by r2py v{_r2py_version}\n"
        f"# Model: {model}  ScriptMap entities: {n_entities}"
    )

    # Build commented-out data-loading shim (§ Option A).  Empty string when
    # there is nothing to pre-load — keeps the saved .py minimal.
    shim_text = (
        build_data_shim(shim_needed_names, sidecar_filename,
                        script_relpath=script_relpath)
        if (sidecar_filename and shim_needed_names) else ""
    )

    # Build source string first, then derive line ranges by scanning sentinels.
    parts: list[str] = [header]
    if deduped_imports:
        parts.append("\n".join(deduped_imports))
    if shim_text:
        parts.append(shim_text)
    if body_items:
        parts.append("\n\n".join(bt for _, bt in body_items))

    source = "\n\n".join(parts) + "\n"

    # Rebuild entity_line_map from sentinels — simpler and less error-prone than
    # accumulating line counts while inserting a variable-length shim block.
    entity_line_map = rebuild_entity_line_map(source)

    # Hoist any top-level function defs called before they are defined
    # (entity-by-entity LLM translation can produce helper functions in a later
    # entity that an earlier entity calls — _hoist_function_defs fixes the order).
    hoisted = _hoist_function_defs(source)
    if hoisted != source:
        source = hoisted
        entity_line_map = rebuild_entity_line_map(source)

    return source, entity_line_map


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_IMPORT_RE = re.compile(r"^\s*(import |from \S+ import )")
_IMPORT_PKG_RE = re.compile(r"^\s*(?:import|from)\s+(\w[\w.]*)")


def _is_import_line(line: str) -> bool:
    return bool(_IMPORT_RE.match(line))


def _is_r_only_import(imp: str) -> bool:
    """Return True if *imp* imports a known R-only package with no Python equivalent."""
    m = _IMPORT_PKG_RE.match(imp)
    if not m:
        return False
    pkg = m.group(1).split(".")[0]  # top-level package name
    return pkg in _R_ONLY_PACKAGES


def _split_imports(snippet: str) -> tuple[list[str], list[str]]:
    """Split a snippet into (import lines, non-import lines)."""
    imports: list[str] = []
    body: list[str] = []
    for line in snippet.splitlines():
        if _is_import_line(line):
            imports.append(line.strip())
        else:
            body.append(line)
    # Strip leading/trailing blank lines from body
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return imports, body


def _import_sort_key(imp: str) -> tuple[int, str]:
    """Sort: bare 'import X' before 'from X import Y', then alphabetically."""
    is_from = imp.startswith("from ")
    return (int(is_from), imp.lower())


def _remove_module_shadows(imports: list[str]) -> list[str]:
    """Remove 'from X import Y' when Y is already bound by a bare 'import Y'.

    Handles: import datetime + from datetime import datetime → second shadows module.
    Any code using datetime.date(...) would fail because 'datetime' becomes the class.
    Keep only the bare module import so X.Y attribute access works.
    """
    # Collect names bound by bare 'import X' or 'import X as Y'
    bare_bound: set[str] = set()
    for imp in imports:
        if not imp.startswith("from ") and imp.startswith("import "):
            mod_part = imp[len("import "):].strip()
            for segment in mod_part.split(","):
                segment = segment.strip()
                if " as " in segment:
                    bare_bound.add(segment.split(" as ")[1].strip())
                else:
                    bare_bound.add(segment.split(".")[0].strip())

    result = []
    for imp in imports:
        if imp.startswith("from "):
            m = re.match(r"^from\s+\S+\s+import\s+(\S+)(?:\s+as\s+(\S+))?", imp)
            if m:
                sym = m.group(1)
                alias = m.group(2)
                bound = alias if alias else sym
                if bound in bare_bound:
                    continue  # shadows a bare module import → drop
        result.append(imp)
    return result


_ASSIGN_RE = re.compile(r"^(\s*)([A-Za-z_]\w*)\s*=(?!=)")


def _resolve_collisions(
    body: str,
    eid: str,
    defined_names: dict[str, str],
) -> str:
    """Suffix top-level assigned names that clash with already-defined ones."""
    lines = body.splitlines()
    renames: dict[str, str] = {}

    for line in lines:
        m = _ASSIGN_RE.match(line)
        if not m:
            continue
        indent, name = m.group(1), m.group(2)
        if indent:  # only top-level (no indentation)
            continue
        if name in defined_names and defined_names[name] != eid:
            suffix = 1
            new_name = f"{name}_{suffix}"
            while new_name in defined_names:
                suffix += 1
                new_name = f"{name}_{suffix}"
            renames[name] = new_name
        else:
            defined_names[name] = eid

    if not renames:
        return body

    # Apply renames as whole-word replacements
    result = body
    for old, new in renames.items():
        result = re.sub(rf"\b{re.escape(old)}\b", new, result)
        defined_names[new] = eid
    return result


_DEF_RE = re.compile(r"^def\s+(\w+)\s*\(")
_SENTINEL_COMMENT_RE = re.compile(r"^# r2py:entity:")


def _hoist_function_defs(source: str) -> str:
    """Move top-level function definitions before their first call sites.

    When entity-by-entity LLM translation places a helper (e.g. ``_with_locale``)
    in entity B but entity A (earlier in the file) calls it, the assembled source
    crashes with ``NameError``.  This pass detects such forward references and moves
    the entire def block (plus any immediately preceding constant assignments) to
    just before the first call.
    """
    lines = source.splitlines()
    n = len(lines)

    # Collect top-level def blocks: {fname: (block_start, block_end)} (0-indexed, inclusive)
    def_blocks: dict[str, tuple[int, int]] = {}
    i = 0
    while i < n:
        m = _DEF_RE.match(lines[i])
        if m:
            fname = m.group(1)
            if fname not in def_blocks:
                start = i
                i += 1
                while i < n and (not lines[i] or lines[i][0] in (" ", "\t")):
                    i += 1
                def_blocks[fname] = (start, i - 1)
                continue
        i += 1

    if not def_blocks:
        return source

    # For each def, find first call before the def start
    call_re_cache: dict[str, re.Pattern] = {}
    hoists: list[tuple[int, int, int]] = []  # (call_line, hoist_start, def_end)

    for fname, (def_start, def_end) in def_blocks.items():
        pat = call_re_cache.setdefault(
            fname, re.compile(r"\b" + re.escape(fname) + r"\s*\(")
        )
        first_call = next(
            (j for j in range(def_start) if pat.search(lines[j])),
            None,
        )
        if first_call is None:
            continue

        # Extend the hoist range backward to the entity sentinel boundary.
        # The sentinel ``# r2py:entity:<eid>`` marks the start of the entity
        # block; everything from sentinel+1 up to the def (inclusive) is the
        # entity's setup code (constants, _LOCALE_MAP dicts, etc.) and must
        # travel with the def when hoisted.
        hoist_start = def_start
        j = def_start - 1
        while j >= 0:
            if _SENTINEL_COMMENT_RE.match(lines[j]):
                candidate = j + 1
                while candidate < def_start and not lines[candidate].strip():
                    candidate += 1
                hoist_start = candidate
                break
            j -= 1

        hoists.append((first_call, hoist_start, def_end))

    if not hoists:
        return source

    # Apply hoists from largest hoist_start to smallest to keep indices valid.
    hoists.sort(key=lambda h: h[1], reverse=True)
    lines = list(lines)
    for call_line, hoist_start, def_end in hoists:
        block = lines[hoist_start : def_end + 1]
        del lines[hoist_start : def_end + 1]

        # Adjust call_line for the deletion above.
        if call_line > hoist_start:
            call_line -= def_end - hoist_start + 1

        # Insert block before the call, with a trailing blank line.
        lines[call_line:call_line] = block + [""]

    return "\n".join(lines)


def rebuild_entity_line_map(source: str) -> dict[str, tuple[int, int]]:
    """Rebuild entity_line_map by scanning for sentinel comments in *source*.

    compose() prepends ``# r2py:entity:<eid>`` to each entity block; this
    function finds those sentinels and re-derives the (start, end) ranges after
    any edits that shift line numbers (apply_edit, coherence.review, etc.).

    Returns {} if no sentinels are present.
    """
    lines = source.splitlines()
    sentinels: list[tuple[int, str]] = []  # (1-indexed line number, entity_id)
    for i, line in enumerate(lines, start=1):
        m = _SENTINEL_RE.match(line)
        if m:
            sentinels.append((i, m.group(1)))

    if not sentinels:
        return {}

    result: dict[str, tuple[int, int]] = {}
    total_lines = len(lines)
    for idx, (sentinel_line, eid) in enumerate(sentinels):
        start = sentinel_line  # sentinel is the first line of the entity range
        if idx + 1 < len(sentinels):
            next_sentinel_line = sentinels[idx + 1][0]
            # end is the last non-blank line before the next sentinel
            end = next_sentinel_line - 1
            while end >= start and not lines[end - 1].strip():
                end -= 1
        else:
            end = total_lines
            while end >= start and not lines[end - 1].strip():
                end -= 1
        result[eid] = (start, end)
    return result
