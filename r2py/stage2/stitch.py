"""Data-loading shim and entity-sentinel utilities for Stage 2 (§5.5)."""
from __future__ import annotations

import ast as _ast
import keyword as _keyword
import re
from typing import TYPE_CHECKING

_SENTINEL_RE = re.compile(r"^# r2py:entity:(\S+)$")

# Data-loading shim sentinels (§ Option A in plans/i-go-with-option-melodic-dewdrop.md).
# Saved on disk in fully-commented form; the verifier un-comments at sandbox time.
DATA_SHIM_BEGIN = "# r2py:data_shim:begin"
DATA_SHIM_END = "# r2py:data_shim:end"
DATA_SHIM_RE = re.compile(
    r"(# r2py:data_shim:begin\n)(.*?)(# r2py:data_shim:end)",
    re.DOTALL,
)

SHIM_PLACEHOLDER = "# r2py:data_shim managed by the harness (loads R's input data) - do not write it"


def hide_data_shim(source: str) -> str:
    """The source as the model sees it: the data-shim block (harness code the model keeps rewriting or breaking: 24% of
    rewrites altered it) replaced by one comment line.  ``show_data_shim`` puts the real block back."""
    m = DATA_SHIM_RE.search(source)
    if not m:
        return source
    end = m.end() + (1 if source[m.end():m.end() + 1] == "\n" else 0)
    return source[:m.start()] + SHIM_PLACEHOLDER + "\n" + source[end:]


def show_data_shim(original: str, rewritten: str) -> str:
    """*rewritten* (written against ``hide_data_shim(original)``) with *original*'s data-shim block restored.

    The placeholder line is replaced by the block; if the model dropped the placeholder, the block goes where it stood in
    *original* (after the same leading comment lines).  A block the model wrote itself is left to ``restore_data_shim``.
    """
    block = DATA_SHIM_RE.search(original)
    if not block or DATA_SHIM_RE.search(rewritten):
        return rewritten
    text = block.group(0) + "\n"
    if SHIM_PLACEHOLDER in rewritten:
        return rewritten.replace(SHIM_PLACEHOLDER + "\n", text, 1) if SHIM_PLACEHOLDER + "\n" in rewritten else rewritten.replace(SHIM_PLACEHOLDER, text.rstrip("\n"), 1)
    lead = original[:block.start()].count("\n")
    lines = rewritten.splitlines(keepends=True)
    return "".join(lines[:lead]) + text + "".join(lines[lead:])


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
    "example", "demo",
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
        "        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]",
        # R data frames arrive as {column: [values]}; the translation was told they are data frames
        # (and writes `.iloc`, `.columns`, passes them to plotnine), so hand it a DataFrame. 19 of 255
        # logged seeds crashed on `'dict' object has no attribute ...` before this.
        "        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and "
        "all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and "
        "len({len(_c) for _c in _r2py_shim_v.values()}) == 1):",
        "            import pandas as _r2py_shim_pd",
        "            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)",
        "        globals()[_r2py_shim_n] = _r2py_shim_v",
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

    # (1) Free variable refs the script references but does not define. Judged per entity this let in names
    # the script computes before using them (lava `e <- estimate(...)`, then `e`): R's result was pre-loaded,
    # so code that never computed it still ran, and code that did got no credit (the verifier skips names bound
    # before the first entity). 36 names in 27 scripts, 2026-10-16. Only names used before any assignment count.
    first_assign, first_use = _first_assign_and_use(script_map)
    for e in entities.values():
        for ref in getattr(e, "free_variable_refs", []) or []:
            if ref in captured and (ref not in first_assign
                                    or (ref in first_use and first_use[ref] < first_assign[ref])):
                needed.add(ref)

    # (2) Names defined by RNG/read entities — overridden by R-captured
    # values at test time so equivalence doesn't fail on PRNG divergence.
    r_source = getattr(script_map, "source", "") or ""
    r_lines = r_source.splitlines() if r_source else []
    for e in entities.values():
        span = getattr(e, "source_span", None)
        if span is None or not r_lines:
            continue
        # SourceLocation uses 0-based tree-sitter rows; end+1 because slices
        # are exclusive.  Using 1-based math here would slice one line
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


def _first_assign_and_use(script_map: "ScriptMap") -> tuple[dict[str, int], dict[str, int]]:
    """Per name, the first R source line that assigns it and the first that uses it (entity granularity).

    An entity assigns its name when its R code is an assignment to that name; a bare `storms` printing a
    package dataset is a use, not a definition (it is named after the variable all the same)."""
    entities = getattr(script_map, "entities", {}) or {}
    lines = (getattr(script_map, "source", "") or "").splitlines()
    first_assign: dict[str, int] = {}
    first_use: dict[str, int] = {}
    for e in sorted(entities.values(), key=lambda x: getattr(getattr(x, "source_span", None), "start_line", 0)):
        span = getattr(e, "source_span", None)
        if span is None:
            continue
        seg = _R_COMMENT_RE.sub("", "\n".join(lines[max(0, span.start_line):span.end_line + 1]))
        name = getattr(e, "name", None) or ""
        assigns = bool(name) and re.search(rf"(^|\n)\s*`?{re.escape(name)}`?\s*(<<-|<-|=)", seg) is not None
        if assigns:
            first_assign.setdefault(name, span.start_line)
        elif name:
            first_use.setdefault(name, span.start_line)
        for ref in getattr(e, "free_variable_refs", []) or []:
            first_use.setdefault(ref, span.start_line)
    return first_assign, first_use


def shim_input_names(script_map: "ScriptMap") -> list[str]:
    """Shim names the R script never assigns: the ones a translation must use as they are and never overwrite."""
    first_assign, _ = _first_assign_and_use(script_map)
    return [n for n in collect_shim_needed_names(script_map) if n not in first_assign]


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


if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import EntityId


def rebuild_entity_line_map(source: str) -> dict[str, list[tuple[int, int]]]:
    """Rebuild entity_line_map by scanning for sentinel comments in *source*.

    Callers (seed.py's sentinel injection, apply_edit, the reasoning agent's
    rewrites) prepend or preserve ``# r2py:entity:<eid>`` markers; this
    function finds those sentinels and re-derives the (start, end) ranges after
    any edits that shift line numbers.

    An entity may have multiple sentinels (e.g. a function definition and its
    call site), producing multiple ranges per entity.

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

    result: dict[str, list[tuple[int, int]]] = {}
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
        result.setdefault(eid, []).append((start, end))
    return result


def self_contained(snippet: str, source: str) -> str:
    """*snippet* preceded by the top-level functions, classes and imports of *source* it uses (transitively).

    Guidance cut from one program and shown for another must run on its own: donor snippets that called
    `format_hms` or `year_month_day`, defined elsewhere in the donor's program, moved the crash into the
    target entity (prompt-load runs, 2026-10-11). Script variables are not carried - the target script has
    its own data. Returns *snippet* unchanged when either side does not parse.
    """
    import builtins
    import textwrap

    try:
        tree = _ast.parse(source)
        snip = _ast.parse(textwrap.dedent(snippet))
    except SyntaxError:
        return snippet

    def bound_and_loaded(node):
        bound, loaded = set(), set()
        for n in _ast.walk(node):
            if isinstance(n, _ast.Name):
                (loaded if isinstance(n.ctx, _ast.Load) else bound).add(n.id)
            elif isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
                bound.add(n.name)
            elif isinstance(n, _ast.arg):
                bound.add(n.arg)
            elif isinstance(n, (_ast.Import, _ast.ImportFrom)):
                bound |= {(a.asname or a.name).split(".")[0] for a in n.names}
        return bound, loaded

    defs: dict[str, _ast.stmt] = {}
    for node in tree.body:
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, (_ast.Import, _ast.ImportFrom)):
            for a in node.names:
                defs[(a.asname or a.name).split(".")[0]] = node
    bound, loaded = bound_and_loaded(snip)
    todo = [n for n in loaded - bound - set(dir(builtins)) if n in defs]
    needed: dict[int, _ast.stmt] = {}
    while todo:
        node = defs[todo.pop()]
        if id(node) in needed:
            continue
        needed[id(node)] = node
        b, l = bound_and_loaded(node)
        todo += [n for n in l - b - bound - set(dir(builtins)) if n in defs and id(defs[n]) not in needed]
    if not needed:
        return snippet
    parts = [_ast.get_source_segment(source, n) for n in sorted(needed.values(), key=lambda n: n.lineno)]
    return "\n\n".join(p for p in parts if p) + "\n\n" + snippet


def splice_entity(source: str, eid: str, body: str) -> tuple[str | None, str]:
    """Replace one entity's body in *source*, leaving every other line untouched.

    The entity's own ``# r2py:entity:<eid>`` sentinel line is kept; lines after it up to
    the entity's end are replaced by *body*.  Returns ``(new_source, "")`` or
    ``(None, reason)``.  An entity with several sentinels (a definition and its call
    sites) is refused: which span to replace would be a guess.
    """
    spans = rebuild_entity_line_map(source).get(eid)
    if not spans:
        return None, f"unknown entity {eid!r} (no '# r2py:entity:{eid}' line in the current translation)"
    if len(spans) > 1:
        return None, f"entity {eid!r} has {len(spans)} separate spans; use a full rewrite for it"
    start, end = spans[0]
    lines = source.splitlines()
    # The model writes the fragment at column 0; if the entity sits inside a block (a function body,
    # an `if`), splicing it unindented is an "unexpected indent" syntax error. Re-indent it to the
    # indentation of the code it replaces, keeping its own relative indentation.
    existing = next((l for l in lines[start:end] if l.strip()), "")
    prefix = existing[:len(existing) - len(existing.lstrip())]
    import textwrap
    kept = [l for l in body.splitlines() if not _SENTINEL_RE.match(l)]
    fragment = textwrap.indent(textwrap.dedent("\n".join(kept)), prefix).splitlines() if prefix else kept
    return "\n".join(lines[:start] + fragment + lines[end:]) + "\n", ""


# ---------------------------------------------------------------------------
# Python reserved-keyword sanitisation (§3.7 language-level invariant)
# ---------------------------------------------------------------------------

# Pre-compiled patterns: match `kw=` (but not `kw==`) for each Python keyword.
# Built lazily on first call; shared across all calls in a process.
_KW_KWARG_PATTERNS: dict[str, re.Pattern] = {}


def sanitize_keyword_args(python_code: str) -> tuple[str, list[str]]:
    """Rename Python reserved keywords used as function parameter/argument names.

    R functions commonly use ``from``, ``in``, ``as``, ``class`` etc. as
    parameter names (e.g. ``chunk(from=1, to=100, by=10)``,
    ``seq(from=1, to=10)``).  In Python these are reserved keywords and
    produce a ``SyntaxError`` when used on the left side of ``=`` in a
    function call or definition.

    This function renames offending keywords consistently throughout the
    code: ``from=`` → ``from_val=``, ``in=`` → ``in_val=``, etc., covering
    both function definitions (``def f(from=default)``) and call sites
    (``f(from=value)``).

    Returns ``(fixed_code, renamed_keywords)``.  ``renamed_keywords`` is the
    sorted list of keywords that were replaced (empty when nothing changed).
    """
    # Skip constants that can legitimately appear as default values.
    _SKIP = frozenset({"True", "False", "None"})

    fixed = python_code
    renamed: list[str] = []

    for kw in sorted(_keyword.kwlist):
        if kw in _SKIP:
            continue
        if kw not in _KW_KWARG_PATTERNS:
            _KW_KWARG_PATTERNS[kw] = re.compile(
                rf'\b{re.escape(kw)}\s*=(?!=)'
            )
        pat = _KW_KWARG_PATTERNS[kw]
        if pat.search(fixed):
            new_name = f"{kw}_val"
            fixed = pat.sub(f"{new_name}=", fixed)
            renamed.append(kw)

    return fixed, renamed


def reorder_positional_before_kwargs(code: str) -> tuple[str, bool]:
    """Move keyword args (name=value) after positional args in function calls.

    R allows mixed named/unnamed argument ordering; Python requires all
    positional arguments before keyword arguments.  Applied as a deterministic
    post-processor on all LLM outputs (alongside ``sanitize_keyword_args``).

    Iterates until stable so nested violations are fixed from inside out.
    Returns ``(fixed_code, was_changed)``.
    """
    import io
    import tokenize as _tk

    _WS = frozenset({_tk.NEWLINE, _tk.NL, _tk.INDENT, _tk.DEDENT, _tk.COMMENT})

    def _one_pass(src: str) -> tuple[str, bool]:
        lines = src.splitlines(True)
        cum = [0]
        for ln in lines:
            cum.append(cum[-1] + len(ln))

        def to_off(row: int, col: int) -> int:
            return cum[row - 1] + col

        try:
            toks = [
                (t.type, t.string, to_off(*t.start), to_off(*t.end))
                for t in _tk.generate_tokens(io.StringIO(src).readline)
                if t.type not in (_tk.ENCODING, _tk.ENDMARKER)
            ]
        except (_tk.TokenError, IndentationError):
            return src, False

        n = len(toks)

        def prev_sig(i: int) -> int:
            j = i - 1
            while j >= 0 and toks[j][0] in _WS:
                j -= 1
            return j

        def close_of(oi: int) -> int:
            d = 0
            for k in range(oi, n):
                if toks[k][0] == _tk.OP:
                    if toks[k][1] in ('(', '[', '{'):
                        d += 1
                    elif toks[k][1] in (')', ']', '}'):
                        d -= 1
                        if d == 0:
                            return k
            return -1

        def top_commas(a: int, b: int) -> list:
            d, result = 0, []
            for k in range(a + 1, b):
                if toks[k][0] == _tk.OP:
                    if toks[k][1] in ('(', '[', '{'):
                        d += 1
                    elif toks[k][1] in (')', ']', '}'):
                        d -= 1
                    elif toks[k][1] == ',' and d == 0:
                        result.append(k)
            return result

        problems: list = []

        for i in range(n):
            if not (toks[i][0] == _tk.OP and toks[i][1] == '('):
                continue
            pi = prev_sig(i)
            if pi < 0:
                continue
            pt, ps = toks[pi][0], toks[pi][1]
            if not (pt == _tk.NAME or (pt == _tk.OP and ps in (')', ']'))):
                continue

            ci = close_of(i)
            if ci < 0:
                continue

            commas = top_commas(i, ci)
            if not commas:
                continue

            seps = [i] + commas + [ci]
            ng = len(seps) - 1

            def is_kw(b: int, _seps: list = seps) -> bool:
                mv = [k for k in range(_seps[b] + 1, _seps[b + 1])
                      if toks[k][0] not in _WS]
                if len(mv) >= 2:
                    t0, t1 = toks[mv[0]], toks[mv[1]]
                    if (t0[0] == _tk.NAME and t1[0] == _tk.OP and t1[1] == '='
                            and (len(mv) < 3 or toks[mv[2]][1] != '=')):
                        return True
                return False

            flags = [is_kw(b) for b in range(ng)]

            saw, needs = False, False
            for f in flags:
                if f:
                    saw = True
                elif saw:
                    needs = True
                    break
            if not needs:
                continue

            pos_bs = [b for b, f in enumerate(flags) if not f]
            kw_bs  = [b for b, f in enumerate(flags) if f]
            order  = pos_bs + kw_bs

            def arg_src(b: int, _seps: list = seps) -> str:
                return src[toks[_seps[b]][3]:toks[_seps[b + 1]][2]].strip()

            new_args = ', '.join(arg_src(b) for b in order)
            open_off  = toks[i][2]
            close_off = toks[ci][3]
            problems.append((open_off, close_off, '(' + new_args + ')'))

        if not problems:
            return src, False

        # Fix only innermost violations (not nested inside another problem).
        # Outer calls are fixed in subsequent iterations.
        innermost = [
            (ps, pe, pt)
            for ps, pe, pt in problems
            if not any(qs < ps and pe < qe
                       for qs, qe, _ in problems
                       if (qs, qe) != (ps, pe))
        ]

        result = src
        for start, end, txt in sorted(innermost, key=lambda r: -r[0]):
            result = result[:start] + txt + result[end:]
        return result, True

    changed_overall = False
    for _ in range(50):
        code, changed = _one_pass(code)
        if not changed:
            break
        changed_overall = True
    return code, changed_overall


shadow_log: list[dict] = []


def _parses(code: str) -> bool:
    try:
        _ast.parse("\n".join(l for l in code.splitlines() if not l.lstrip().startswith("# r2py:")))
        return True
    except SyntaxError:
        return False


def shadow_autofix(code: str, site: str) -> None:
    """Observe what the auto-fixers WOULD do, without applying them.

    Runs each fixer on a copy and records into ``shadow_log`` whether it turned invalid
    source valid (a genuine save), left valid source valid (unnecessary), broke valid
    source, or left invalid source invalid.  The caller keeps the original source.
    """
    before_ok = _parses(code)
    # Only the keyword-rename fixer is still watched: argument order is now repaired for real by
    # stage2/argorder.py, so shadowing the old text-surgery version only added noise.
    for name, fixer in (("sanitize_keyword_args", sanitize_keyword_args),):
        try:
            fixed, changed = fixer(code)
            if not changed:
                continue
            after_ok = _parses(fixed)
        except Exception:
            continue
        bucket = f"{'valid' if before_ok else 'invalid'}->{'valid' if after_ok else 'invalid'}"
        shadow_log.append({"fixer": name, "site": site, "bucket": bucket})


def drain_shadow_log() -> list[dict]:
    out = list(shadow_log)
    shadow_log.clear()
    return out
