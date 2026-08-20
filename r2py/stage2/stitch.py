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
