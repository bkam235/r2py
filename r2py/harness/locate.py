"""Locate where a translation first departs from R inside one entity (roadmap step 6).

The score says *which* entity is wrong; the agent has to guess *where* inside it, and a small model does not go
and look (739 rewrites against 10 R probes).  Here the harness looks.  Every call of the entity is wrapped in a
probe on both sides -- in R by rewriting the parse tree, in Python by rewriting the AST -- so each call is still
evaluated exactly once, in order, with its side effects and random draws untouched (the random draws are served to
Python the same way as in verification).  The probes record each call's value.  Aligned by *value* rather than by
name (``quantile`` and ``np.percentile`` have nothing in common but their result), the first R call whose value
Python never produces is where the translation departs, and its inputs, evaluated earlier, were reproduced.

    divergence = find_divergence(r_probes, py_probes)   # None if every R value has a Python counterpart
"""
from __future__ import annotations

import ast
import json
import math
from typing import Any

from ..stage4.comparators import fingerprint as _fp

MAX_PROBES = 400
RTOL = 1e-6
ATOL = 1e-9

# ---------------------------------------------------------------------------------------------- R side

R_PROBE_FUNCTIONS = r"""
.r2py_probes <- list()
.r2py_pid <- 0L
.r2py_probe <- function(id, label, value) {
  tryCatch({
    n <- sum(vapply(.r2py_probes, function(p) identical(p$id, id), logical(1)))
    if (n < 3 && length(.r2py_probes) < 400 && !is.function(value) && !is.environment(value) && length(value) <= 100000) {
      s <- .r2py_serialize_var(value)
      if (!is.null(s) && !identical(s, '__uncapturable__')) {
        .r2py_probes[[length(.r2py_probes) + 1L]] <<- list(id = id, expr = label, value = s)
      }
    }
  }, error = function(e) NULL)
  value
}
.r2py_structural <- c('{', '(', 'if', 'for', 'while', 'repeat')
.r2py_hands_off <- c('function', 'quote', '~', 'library', 'require', 'suppressWarnings', 'suppressMessages',
                     'suppressPackageStartupMessages', '::', ':::', 'return', 'break', 'next', 'bquote', 'substitute',
                     'missing', 'on.exit', 'UseMethod', 'NextMethod', 'switch')
.r2py_pipes <- c('%>%', '%<>%', '%T>%', '%$%')
.r2py_wrap <- function(e) {
  if (!is.call(e)) return(e)
  fn <- e[[1]]
  fname <- if (is.symbol(fn)) as.character(fn) else ''
  if (fname %in% .r2py_hands_off) return(e)
  label <- substr(paste(deparse(e), collapse = ' '), 1, 120)
  wrap_from <- function(e, idx) {
    for (i in idx) if (i <= length(e) && !identical(e[[i]], quote(expr = ))) e[[i]] <- .r2py_wrap(e[[i]])
    e
  }
  if (fname %in% c('<-', '=', '<<-')) return(wrap_from(e, 3L))
  if (fname %in% c('$', '@')) { e <- wrap_from(e, 2L); return(e) }
  if (fname %in% .r2py_pipes) e <- wrap_from(e, 2L)
  else e <- wrap_from(e, seq_len(length(e))[-1])
  if (fname %in% .r2py_structural) return(e)
  .r2py_pid <<- .r2py_pid + 1L
  id <- .r2py_pid
  as.call(list(as.name('.r2py_probe'), id, label, e))
}
"""


def r_locate_program(r_source: str, span: tuple[int, int]) -> str:
    """The script up to the entity, with the entity's own statements rewritten to probe every call.

    *span* is the entity's (start_line, end_line), 0-based inclusive, in *r_source*.  Everything after the
    entity is dropped: it cannot influence the entity's values.
    """
    lines = r_source.splitlines(keepends=True)
    start, end = span
    entity = "".join(lines[start:end + 1])
    delim = "-" * 6
    while f"){delim}\"" in entity:
        delim += "-"
    program = (
        "".join(lines[:start])
        + "\n"
        + f'.r2py_ent <- parse(text = r"{delim}({entity}){delim}", keep.source = FALSE)\n'
        + "tryCatch(for (.e in as.list(.r2py_ent)) eval(.r2py_wrap(.e), envir = .GlobalEnv), error = function(e) NULL)\n"
        + "writeLines(jsonlite::toJSON(.r2py_probes, auto_unbox = TRUE, digits = NA, na = 'null', force = TRUE), '_r2py_probes.json')\n"
    )
    return program


# ------------------------------------------------------------------------------------------ Python side

PY_PROBE_PREAMBLE = """\
import atexit as _r2py_atexit
import json as _r2py_json_pr

_r2py_probes = []
_r2py_probe_counts = {}


def _r2py_probe(i, label, value):
    n = _r2py_probe_counts.get(i, 0)
    if n < 3 and len(_r2py_probes) < 400:
        _r2py_probe_counts[i] = n + 1
        try:
            v, ok = _r2py_try_serialize(label, value)
        except Exception:
            ok = False
        if ok:
            _r2py_probes.append({'id': i, 'expr': label, 'value': v})
    return value


def _r2py_write_probes():
    try:
        with open('_r2py_probes.json', 'w', encoding='utf-8') as f:
            _r2py_json_pr.dump(_r2py_probes, f)
    except Exception:
        pass


_r2py_atexit.register(_r2py_write_probes)
"""


class _Prober(ast.NodeTransformer):
    """Wrap every call and operator whose first line lies in [lo, hi] in ``_r2py_probe(id, label, expr)``.

    R's operators (``+``, ``[``, ``==``) are calls and are probed on the R side, so their Python counterparts
    (binary and unary operations, comparisons, subscripts) are probed too.  Inner expressions are wrapped
    first, so they get the lower ids.
    """

    def __init__(self, lo: int, hi: int) -> None:
        self.lo, self.hi, self.n = lo, hi, 0

    def _label(self, node: ast.AST) -> str:
        try:
            return ast.unparse(node)[:120]
        except Exception:
            return "<expression>"

    def _wrap(self, node: ast.AST, label: str) -> ast.AST:
        if not (self.lo <= getattr(node, "lineno", 0) <= self.hi):
            return node
        self.n += 1
        wrapped = ast.Call(func=ast.Name("_r2py_probe", ast.Load()),
                           args=[ast.Constant(self.n), ast.Constant(label), node], keywords=[])
        return ast.copy_location(wrapped, node)

    def visit_Call(self, node):
        label = self._label(node)           # before the arguments are rewritten: the label is the original code
        self.generic_visit(node)
        return self._wrap(node, label)

    visit_BinOp = visit_UnaryOp = visit_Compare = visit_Call

    def visit_Subscript(self, node):
        label = self._label(node)
        self.generic_visit(node)
        return self._wrap(node, label) if isinstance(node.ctx, ast.Load) else node


def instrument_python(source: str, line_range: tuple[int, int]) -> str | None:
    """*source* with every call in the (1-based, inclusive) line range wrapped in a probe; None if it cannot be parsed."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    prober = _Prober(*line_range)
    tree = prober.visit(tree)
    ast.fix_missing_locations(tree)
    try:
        return ast.unparse(tree)
    except Exception:
        return None


# ----------------------------------------------------------------------------------------------- matching

def _numbers(value: Any) -> list[float]:
    return [x for _p, vec in _fp.numeric_fields(value) for x in vec]


def _reproduced(r_probe: dict, py_numbers: list[float], py_texts: set[str]) -> bool | None:
    """Does Python produce this R value somewhere in the entity?  None when the value carries nothing to compare."""
    nums = _numbers(r_probe["value"])
    if nums:
        pool = sorted(py_numbers)
        return _fp.field_match(nums, pool, RTOL, ATOL) >= 0.99
    texts = [_fp.canonical_text(t) for t in _fp.texts(r_probe["value"])]
    texts = [t for t in texts if t]
    if texts:
        return any(t in py_texts for t in texts)
    return None


def _preview(nums: list[float], n: int = 6) -> str:
    shown = ", ".join(f"{x:.6g}" for x in nums[:n])
    return f"[{shown}{', ...' if len(nums) > n else ''}] (length {len(nums)})"


def find_divergence(r_probes: list[dict], py_probes: list[dict]) -> dict | None:
    """The first R call (in evaluation order) whose value has no counterpart among Python's, or None.

    Python's values are pooled, so the match does not depend on call names, argument order or how many helper
    calls the translation needs.  Calls whose values are trivial constants of one or two digits are skipped: they
    appear everywhere and say nothing.
    """
    py_numbers = [x for p in py_probes for x in _numbers(p["value"])]
    py_texts = {_fp.canonical_text(t) for p in py_probes for t in _fp.texts(p["value"])}
    py_vectors = [vec for p in py_probes for _path, vec in _fp.numeric_fields(p["value"])]
    for p in r_probes:
        nums = _numbers(p["value"])
        if nums and len(nums) <= 2 and all(_fp.significant_digits(x) <= 2 for x in nums):
            continue
        if len(nums) >= 2:
            # A vector is reproduced only as the same sequence: pooled values would match any index vector made of small
            # integers (they occur everywhere), and the order of a result is part of the result.
            if any(_same_sequence(nums, v) for v in py_vectors):
                continue
            kind = "order" if any(len(v) == len(nums) and _same_sequence(sorted(nums), sorted(v)) for v in py_vectors) else "missing"
            return {"expr": p["expr"], "numbers": nums, "texts": _fp.texts(p["value"]), "kind": kind,
                    "closest": _closest(nums, py_probes) if kind == "missing" else _same_values(nums, py_probes)}
        ok = _reproduced(p, py_numbers, py_texts)
        if ok is False:
            return {"expr": p["expr"], "numbers": nums, "texts": _fp.texts(p["value"]), "kind": "missing",
                    "closest": _closest(nums, py_probes)}
    return None


def _same_sequence(a: list[float], b: list[float]) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= ATOL + RTOL * abs(y) for x, y in zip(a, b))


def _same_values(nums: list[float], py_probes: list[dict]) -> dict | None:
    """The Python vector holding the same values as R's in another order (for the 'order' divergence)."""
    for p in py_probes:
        for _path, vec in _fp.numeric_fields(p["value"]):
            if len(vec) == len(nums) and _same_sequence(sorted(nums), sorted(vec)):
                return {"expr": p["expr"], "numbers": vec, "error": 0.0}
    return None


def _closest(nums: list[float], py_probes: list[dict]) -> dict | None:
    """The Python value of the same length nearest to R's, to show how far off it is."""
    if not nums:
        return None
    best = None
    for p in py_probes:
        for _path, vec in _fp.numeric_fields(p["value"]):
            if len(vec) != len(nums):
                continue
            err = max(abs(a - b) / max(abs(b), 1e-12) if b else abs(a) for a, b in zip(vec, nums))
            if math.isfinite(err) and (best is None or err < best["error"]):
                best = {"expr": p["expr"], "numbers": vec, "error": err}
    return best


def format_divergence(entity: str, d: dict | None, n_r: int, n_py: int) -> str:
    if d is None:
        return (f"Entity {entity}: every value R computes inside it ({n_r} calls) also appears among the {n_py} values your Python "
                "computes; the difference is in what the entity finally assigns or prints, not in an intermediate step.")
    shown = _preview(d["numbers"]) if d["numbers"] else repr(d["texts"][0][:100]) if d["texts"] else "(no value)"
    text = (f"Entity {entity}: the first call where your Python departs from R is `{d['expr']}`. R computes {shown}, and no "
            f"value of that kind occurs anywhere in your Python for this entity (the calls before it were reproduced).")
    c = d.get("closest")
    if c and d.get("kind") == "order":
        text = (f"Entity {entity}: the first call where your Python departs from R is `{d['expr']}`. R computes {shown}; your Python computes "
                f"the same values in a different order: {_preview(c['numbers'])} from `{c['expr']}`.")
    elif c:
        text += f" The nearest Python value is {_preview(c['numbers'])} from `{c['expr']}` (relative error {c['error']:.3g})."
    return text


def load_probes(text: str | None) -> list[dict]:
    try:
        raw = json.loads(text) if text else []
    except json.JSONDecodeError:
        return []
    return [p for p in raw if isinstance(p, dict) and "value" in p and "expr" in p]
