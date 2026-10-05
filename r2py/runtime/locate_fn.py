"""Where inside an R function does a Python reimplementation first depart from R?  (roadmap step 7, repair feedback)

A failing case says *that* the Python differs, with the two outputs; the model has to guess where.  For a function like
caret's ``createDataPartition`` the outputs are index vectors drawn through ``sample`` and the model cannot see which
intermediate step went wrong.  This probes both sides, as ``harness.locate`` does for a translated entity: the body of the R
function is rewritten so that every call and operator reports its value (each still evaluated once, in order, with R's own
draws), the model's Python is instrumented the same way and run on the same case with R's draws replayed, and the first R
value Python never produces is reported with the nearest Python value.  The harness looks; the model reads.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from ..harness import locate as _loc
from ..stage0.effects import data as _data_effects
from ..types import EffectClass
from . import difftest

_R_TARGET = r"""
.r2py_method_for <- function(fun, fname, first) {
  if (any(grepl("UseMethod", deparse(body(fun)), fixed = TRUE))) {
    for (cl in c(class(first), "default")) {
      meth <- tryCatch(utils::getS3method(fname, cl, optional = TRUE), error = function(e) NULL)
      if (!is.null(meth)) return(list(fun = meth, name = paste(fname, cl, sep = ".")))
    }
  }
  list(fun = fun, name = fname)
}
.r2py_install <- function(name, fun, where) {
  for (env in where) {
    if (is.environment(env) && exists(name, envir = env, inherits = FALSE)) {
      tryCatch({ unlockBinding(name, env); assign(name, fun, envir = env); lockBinding(name, env) }, error = function(e) NULL)
    }
  }
}
.r2py_call <- parse(text = r"------(__CALL__)------", keep.source = FALSE)[[1]]
.r2py_fname <- "__FNAME__"
.r2py_fun <- get(.r2py_fname, mode = "function")
.r2py_first <- tryCatch(eval(as.list(match.call(.r2py_fun, .r2py_call, expand.dots = TRUE))[[2]], envir = globalenv()), error = function(e) NULL)
.r2py_t <- .r2py_method_for(.r2py_fun, .r2py_fname, .r2py_first)
.r2py_inst <- .r2py_t$fun
if (!is.primitive(.r2py_inst)) {
  body(.r2py_inst) <- .r2py_wrap(body(.r2py_inst))
  .r2py_where <- c(list(environment(.r2py_t$fun)), lapply(search(), as.environment))   # the namespace and every attached copy
  .r2py_install(.r2py_t$name, .r2py_inst, .r2py_where)
}
tryCatch(eval(.r2py_call, envir = globalenv()), error = function(e) NULL)
writeLines(jsonlite::toJSON(.r2py_probes, auto_unbox = TRUE, digits = NA, na = 'null', force = TRUE), '_r2py_probes.json')
"""


def r_probes(fname: str, package: str | None, case: dict, timeout_s: float = 120) -> list[dict]:
    """The values of every call inside the R function's body while it runs *case*'s call (R's own order and draws)."""
    from ..stage0.sandbox.r_sandbox import RSandbox

    call = case["call"].split(difftest.MUTANT)[0]
    if ")------\"" in call:
        return []
    program = f"suppressPackageStartupMessages(library({package}))\n" if package else ""
    program += difftest._R_INTERCEPT_RNG + (case.get("setup") or "") + "\n"
    program += _R_TARGET.replace("__CALL__", call).replace("__FNAME__", fname)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        try:
            RSandbox().run(program, workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}), timeout_s=timeout_s,
                           preamble=_data_effects.build_r_serializer_fn() + _loc.R_PROBE_FUNCTIONS)
        except Exception:
            return []
        f = Path(tmp) / "_r2py_probes.json"
        return _loc.load_probes(f.read_text(encoding="utf-8") if f.exists() else None)


def py_probes(code: str, fname: str, case: dict, timeout_s: float = 60) -> list[dict]:
    """The values of every call inside the model's Python while it runs the same case (R's draws replayed)."""
    from ..stage0.sandbox.base import ReplayLog
    from ..stage0.sandbox.py_sandbox import PySandbox

    instrumented = _loc.instrument_python(code, (1, 10 ** 6))
    if instrumented is None:
        return []
    source = instrumented + "\n" + difftest._PY_RUNNER.replace("__FUNC__", "r_" + difftest.py_name(fname))
    sidecar = {"_cases_in.json": json.dumps([{"args": case["args"], "draws": case.get("draws", []), "rclass": case.get("rclass", "")}])}
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        PySandbox().run(source, workdir=Path(tmp), capture=frozenset({EffectClass.DATA, EffectClass.RNG}), timeout_s=timeout_s,
                        preamble=_loc.PY_PROBE_PREAMBLE, replay=ReplayLog(rng_draws=[("rnorm", [], [0.0])]), sidecar_files=sidecar)
        f = Path(tmp) / "_r2py_probes.json"
        return _loc.load_probes(f.read_text(encoding="utf-8") if f.exists() else None)


def explain(fname: str, package: str | None, code: str, case: dict, cache: dict | None = None) -> str | None:
    """A sentence naming the first call inside the R function whose value the Python never produces, or None."""
    key = (fname, case["call"])
    r = cache.get(key) if cache is not None else None
    if r is None:
        r = r_probes(fname, package, case)
        if cache is not None:
            cache[key] = r
    if not r:
        return None
    py = py_probes(code, fname, case)
    d = _loc.find_divergence(r, py)
    if d is None:
        return (f"Inside R's `{fname}`, every value R computes for this call ({len(r)} of them) also appears among the {len(py)} "
                "values your Python computes; the difference is in how the final result is assembled or returned.")
    shown = _loc._preview(d["numbers"]) if d["numbers"] else repr(d["texts"][0][:100]) if d["texts"] else "(no value)"
    text = (f"Inside R's `{fname}`, the first step where your Python departs from R is `{d['expr']}`: R computes {shown} and no value of "
            "that kind occurs anywhere in your Python for this call (the steps before it were reproduced).")
    c = d.get("closest")
    if c:
        text += f" The nearest value your Python computes is {_loc._preview(c['numbers'])} from `{c['expr']}` (relative error {c['error']:.3g})."
    return text
