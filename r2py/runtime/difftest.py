"""Differential tests of a Python function against the R function it claims to reproduce.

A *case* is a call: ``{"call": "quantile(x, 0.9)", "args": [[name_or_null, json_value], ...], "expected": json}``.
The harness builds cases by running example calls in R (ground truth), then mutates the first argument (NA inserted,
ties, reversed, a single value) and re-asks R, so edge cases the model did not think of are tested against R as well.
The Python function is called with the same arguments -- vectors as numpy arrays, NA as NaN, data frames as pandas --
under R's own formal names (a dot becomes an underscore: ``na.rm`` -> ``na_rm``) and its result is compared with R's at
the data comparator's tolerance.  Nothing here asks a model anything.
"""
from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from ..stage0.effects import data as _data_effects
from ..stage0.effects import rng as _rng_effects
from ..stage4.comparators.data import _DEFAULT_ATOL, _DEFAULT_RTOL, _compare_pair
from ..types import EffectClass

MAX_CASES = 60


def py_name(r_name: str) -> str:
    """The Python identifier for an R name: dots become underscores."""
    return r_name.replace(".", "_")


# ----------------------------------------------------------------------------------------------------- R side

# Unlike the script-level capture (wrappers attached ahead of base), this rewrites the bindings in the base and stats
# namespaces themselves, so draws made from inside a package's own code (caret's resampling calls base::sample) are
# recorded too.  Only ever done in the throwaway R process that builds test cases.
_R_INTERCEPT_RNG = """
.r2py_rng_log <- list()
local({
  for (.n in c(%s)) {
    .env <- if (exists(.n, envir = baseenv(), inherits = FALSE)) baseenv() else asNamespace('stats')
    local({
      nm <- .n; orig <- get(.n, envir = .env); env <- .env
      w <- function(...) {
        r <- orig(...)
        if (length(r) <= 100000L) .r2py_rng_log[[length(.r2py_rng_log) + 1L]] <<- list(
          fn = if (nm == 'sample.int') 'sample' else nm, value = if (is.numeric(r)) as.numeric(r) else as.character(r))
        r
      }
      unlockBinding(nm, env); assign(nm, w, envir = env); lockBinding(nm, env)
    })
  }
})
""" % ", ".join(f"'{n}'" for n in _rng_effects.RNG_FUNCTIONS)

_R_CASES = r"""
.r2py_json_args <- function(args) {
  lapply(seq_along(args), function(i) list(if (is.null(names(args)) || !nzchar(names(args)[i])) NULL else names(args)[i],
                                           .r2py_serialize_var(args[[i]])))
}
.r2py_mutants <- function(x) {
  out <- list()
  if (is.atomic(x) && !is.null(x) && !is.factor(x) && length(x) >= 3 && !is.list(x)) {
    if (is.numeric(x)) { y <- x; y[2] <- NA; out[['an NA inserted']] <- y
                         y <- x; y[2] <- x[1]; out[['a tie']] <- y
                         out[['scaled']] <- x * 7.3 - 1.1 }
    out[['reversed']] <- rev(x)
    out[['a single value']] <- x[1]
  }
  out
}
.r2py_calls <- jsonlite::fromJSON(r"----(__CALLS__)----")
.r2py_fname <- "__FNAME__"
.r2py_fun <- get(.r2py_fname, mode = "function")
.r2py_cases <- list()
.r2py_add <- function(label, args) {
  .before <- length(.r2py_rng_log)
  res <- tryCatch(suppressWarnings(do.call(.r2py_fun, args)), error = function(e) NULL)
  if (is.null(res)) return(invisible())
  .draws <- if (length(.r2py_rng_log) > .before) .r2py_rng_log[(.before + 1L):length(.r2py_rng_log)] else list()
  ex <- tryCatch(.r2py_serialize_var(res), error = function(e) '__uncapturable__')
  if (is.null(ex) || identical(ex, '__uncapturable__')) return(invisible())
  .r2py_cases[[length(.r2py_cases) + 1L]] <<- list(call = label, args = .r2py_json_args(args), expected = ex, draws = .draws,
    first_class = if (length(args) >= 1) class(args[[1]])[1] else '')
}
.r2py_method_for <- function(fun, fname, first) {
  if (any(grepl("UseMethod", deparse(body(fun)), fixed = TRUE))) {
    for (cl in c(class(first), "default")) {
      meth <- tryCatch(utils::getS3method(fname, cl, optional = TRUE), error = function(e) NULL)
      if (!is.null(meth)) return(meth)
    }
  }
  fun
}
.r2py_shown <- .r2py_fun
for (cs in .r2py_calls) {
  e <- tryCatch(parse(text = cs, keep.source = FALSE)[[1]], error = function(e) NULL)
  if (is.null(e) || !is.call(e)) next
  m0 <- tryCatch(match.call(.r2py_fun, e, expand.dots = TRUE), error = function(e) NULL)
  if (is.null(m0) || length(m0) < 2) next
  first <- tryCatch(eval(as.list(m0)[[2]], envir = globalenv()), error = function(e) NULL)
  meth <- .r2py_method_for(.r2py_fun, .r2py_fname, first)    # an S3 generic is matched against the method that will run
  .r2py_shown <- meth
  m <- tryCatch(match.call(meth, e, expand.dots = TRUE), error = function(e) NULL)
  if (is.null(m)) next
  args <- tryCatch(lapply(as.list(m)[-1], eval, envir = globalenv()), error = function(e) NULL)
  if (is.null(args)) next
  .r2py_add(cs, args)
  if (length(args) >= 1) for (k in names(.r2py_mutants(args[[1]]))) {
    a2 <- args; a2[[1]] <- .r2py_mutants(args[[1]])[[k]]
    .r2py_add(paste0(cs, "  [first argument: ", k, "]"), a2)
  }
}
.r2py_src <- tryCatch(paste(utils::head(deparse(.r2py_shown), 400), collapse = "\n"), error = function(e) "")
.r2py_usage <- tryCatch({ d <- deparse(args(.r2py_shown)); paste(d[seq_len(max(1, length(d) - 1))], collapse = " ") }, error = function(e) "")
writeLines(jsonlite::toJSON(list(cases = .r2py_cases, source = .r2py_src, usage = .r2py_usage), auto_unbox = TRUE,
                            digits = NA, na = 'null', force = TRUE), '_r2py_cases.json')
"""


def build_cases(fname: str, calls: list[str], package: str | None = None, timeout_s: float = 90) -> dict:
    """Run *calls* (R code strings calling *fname*) and their first-argument mutants in R.

    Returns ``{"cases": [...], "source": R source of the function, "usage": its argument list}``; cases whose call
    errors in R are dropped.
    """
    from ..stage0.sandbox.r_sandbox import RSandbox

    program = ""
    if package:
        program += f"suppressPackageStartupMessages(library({package}))\n"
    program += _R_INTERCEPT_RNG                    # the draws a function makes are recorded per case, replayed to Python
    program += _R_CASES.replace("__CALLS__", json.dumps(calls)).replace("__FNAME__", fname)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        RSandbox().run(program, workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}), timeout_s=timeout_s,
                       preamble=_data_effects.build_r_serializer_fn())
        f = Path(tmp) / "_r2py_cases.json"
        if not f.exists():
            return {"cases": [], "source": "", "usage": ""}
        out = json.loads(f.read_text(encoding="utf-8"))
    out["cases"] = label_core(out.get("cases", [])[:MAX_CASES])
    return out


MUTANT = "  [first argument:"


def label_core(cases: list[dict]) -> list[dict]:
    """Mark each case ``core`` or exotic.  The model's example calls disagree with each other about what the first
    argument of an R function is (``tolower(data.frame(...))`` next to seven calls with character vectors) and R's
    behaviour on the odd one is idiosyncratic, so the most common first-argument class among the example calls defines
    the function's ordinary use: calls of another class, and the mutants made from them, are reported but do not
    decide acceptance."""
    import collections

    classes = collections.Counter(c.get("first_class", "") for c in cases if MUTANT not in c["call"])
    mode = classes.most_common(1)[0][0] if classes else ""
    parent = {c["call"]: c.get("first_class", "") for c in cases if MUTANT not in c["call"]}
    for c in cases:
        root = c["call"].split(MUTANT)[0]
        c["core"] = parent.get(root, c.get("first_class", "")) == mode
    return cases


# ------------------------------------------------------------------------------------------------- Python side

_PY_RUNNER = """
import json as _rt_json
import math as _rt_math

try:
    import numpy as _rt_np
except ImportError:
    _rt_np = None


def _rt_conv(v):
    if isinstance(v, list):
        if v and all(isinstance(x, bool) for x in v) and _rt_np is not None:
            return _rt_np.array(v, dtype=bool)
        if all((x is None) or (isinstance(x, (int, float)) and not isinstance(x, bool)) for x in v):
            return _rt_np.array([_rt_math.nan if x is None else x for x in v], dtype=float) if _rt_np is not None else v
        return [_rt_conv(x) for x in v]
    if isinstance(v, dict):
        try:
            import pandas as _rt_pd
            if v and all(isinstance(x, list) for x in v.values()) and len({len(x) for x in v.values()}) == 1:
                return _rt_pd.DataFrame({k: _rt_conv(x) for k, x in v.items()})
        except ImportError:
            pass
        return {k: _rt_conv(x) for k, x in v.items()}
    return v


_rt_cases = _rt_json.load(open('_cases_in.json', encoding='utf-8'))
_rt_out = []
for _c in _rt_cases:
    try:
        _pos, _kw = [], {}
        for _name, _val in _c['args']:
            if _name:
                _kw[_name.replace('.', '_')] = _rt_conv(_val)
            else:
                _pos.append(_rt_conv(_val))
        _r2py_draws.clear()
        for _d in _c.get('draws') or []:
            _r2py_draws.setdefault(_d['fn'], []).append(_d['value'] if isinstance(_d['value'], list) else [_d['value']])
        _res = __FUNC__(*_pos, **_kw)
        _v, _ok = _r2py_try_serialize('r', _res)
        _rt_out.append({'value': _v} if _ok else {'error': 'result of type ' + type(_res).__name__ + ' is not serialisable'})
    except BaseException as _e:
        _rt_out.append({'error': (type(_e).__name__ + ': ' + str(_e))[:240]})
with open('_cases_out.json', 'w', encoding='utf-8') as _f:
    _rt_json.dump(_rt_out, _f)
"""


@dataclass
class Result:
    passed: int = 0
    total: int = 0
    core_passed: int = 0
    core_total: int = 0
    failures: list[dict] = field(default_factory=list)       # {"call", "expected", "got" | "error", "core"}

    @property
    def ok(self) -> bool:
        return self.total > 0 and self.passed == self.total

    @property
    def ok_core(self) -> bool:
        """Every ordinary-use case passes (see ``label_core``): the acceptance criterion."""
        return self.core_total > 0 and self.core_passed == self.core_total


def _unwrap(v):
    while isinstance(v, list) and len(v) == 1:
        v = v[0]
    return v


def run_python(code: str, fname: str, cases: list[dict], timeout_s: float = 60) -> Result:
    """Run the Python implementation (``def r_<fname>(...)``) on every case in the sandbox and compare with R."""
    from ..stage0.sandbox.base import ReplayLog
    from ..stage0.sandbox.py_sandbox import PySandbox

    func ="r_" + py_name(fname)
    source = code + "\n" + _PY_RUNNER.replace("__FUNC__", func)
    res = Result(total=len(cases), core_total=sum(1 for c in cases if c.get("core", True)))
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        wd = Path(tmp)
        bundle = PySandbox().run(
            source, workdir=wd, capture=frozenset({EffectClass.DATA, EffectClass.RNG}), timeout_s=timeout_s,
            replay=ReplayLog(rng_draws=[("rnorm", [], [0.0])]),          # installs the hooks; the real draws are set per case
            sidecar_files={"_cases_in.json": json.dumps([{"args": c["args"], "draws": c.get("draws", [])} for c in cases])})
        f = wd / "_cases_out.json"
        outs = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    if len(outs) != len(cases):
        tail = " ".join((bundle.stderr or "").strip().splitlines()[-4:])[-400:]
        res.failures.append({"call": "(the whole file)", "error": "the function file did not run to completion; define `"
                             + func + "` and import what it needs. Python said: " + tail})
        return res
    for c, o in zip(cases, outs):
        core = c.get("core", True)
        if "error" in o:
            res.failures.append({"call": c["call"], "expected": _unwrap(c["expected"]), "error": o["error"], "core": core})
            continue
        _score, verdict, _tag, _why = _compare_pair(c["call"], _unwrap(c["expected"]), _unwrap(o["value"]),
                                                    _DEFAULT_RTOL, _DEFAULT_ATOL)
        if verdict == "pass":
            res.passed += 1
            res.core_passed += core
        else:
            res.failures.append({"call": c["call"], "expected": _unwrap(c["expected"]), "got": _unwrap(o["value"]), "core": core})
    return res
