"""Test cases from a package's own Rd examples: run the examples with the function intercepted.

Moved from scripts/rd_harvest.py and scripts/rd_pilot.py so the harness can use it (the on-demand
step, r2py/runtime/ondemand.py). The functions that cost the most appear in one or two scripts of
the whole corpus, so their cases cannot come from our corpus; every exported function ships an
Rd examples block. `harvest` records each real call (arguments as evaluated, R's answer, class and
printed form); `as_mined` turns a harvest row into cases `propose.attempt` takes as mined cases.
"""
from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

_R_HARVEST = r"""
.r2py_rec <- list()
.r2py_fname <- "__FNAME__"
.r2py_pkg <- "__PKG__"
suppressPackageStartupMessages(library(.r2py_pkg, character.only = TRUE))

.r2py_json_args <- function(args) {
  lapply(seq_along(args), function(i) list(
    if (is.null(names(args)) || !nzchar(names(args)[i])) NULL else names(args)[i],
    .r2py_serialize_var(args[[i]])))
}

# Counters that tell the failure modes apart: never intercepted (seen = 0) versus intercepted but not
# recordable (unserialisable > 0, e.g. data frames, tibbles, S4 objects).
.r2py_seen <- 0L; .r2py_unser <- 0L; .r2py_hooked <- character(0)
# The same first-argument variants difftest makes for invented calls, applied to each real call: R answers
# every variant, so a function with thin examples still gets enough cases, all from R itself.
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

local({
  ns <- asNamespace(.r2py_pkg)
  orig <- get(.r2py_fname, envir = ns)
  record <- function(a, r, label) {
    ok <- tryCatch({ .r2py_json_args(a); .r2py_serialize_var(r); TRUE }, error = function(e) FALSE)
    if (!ok) { .r2py_unser <<- .r2py_unser + 1L; return(invisible()) }
    if (length(.r2py_rec) >= 60L) return(invisible())
    .r2py_rec[[length(.r2py_rec) + 1L]] <<- list(
      args = .r2py_json_args(a), value = .r2py_serialize_var(r),
      rclass = class(r)[1],
      shown = paste(utils::head(tryCatch(capture.output(print(r)), error = function(e) ""), 12), collapse = " | "),
      call = label, nargs = length(a), names = if (is.null(names(a))) list() else as.list(names(a)))
  }
  w <- function(...) {
    # Call the real function FIRST, with the arguments as untouched promises. Forcing them before the call
    # (list(...) first) broke every function with unevaluated arguments - group_by(cyl): there is no variable
    # cyl - so the example statement failed, and the recorder destroyed the examples it was observing.
    r <- orig(...)
    .r2py_seen <<- .r2py_seen + 1L
    a <- tryCatch(list(...), error = function(e) NULL)
    if (is.null(a)) { .r2py_unser <<- .r2py_unser + 1L; return(r) }   # unevaluated (NSE) arguments: not recordable
    label <- paste(utils::head(deparse(sys.call(0)), 3), collapse = " ")
    record(a, r, label)
    if (length(a) >= 1 && length(.r2py_rec) < 60L) for (k in names(.r2py_mutants(a[[1]]))) {
      a2 <- a; a2[[1]] <- .r2py_mutants(a[[1]])[[k]]
      r2 <- tryCatch(suppressWarnings(do.call(orig, a2)), error = function(e) NULL)
      if (!is.null(r2)) record(a2, r2, paste0(label, "  [first argument: ", k, "]"))
    }
    r
  }
  # the examples call the exported binding, so replace it in the namespace AND in the attached
  # package environment; internal calls from other package functions are intercepted too.
  for (env in list(ns, tryCatch(as.environment(paste0("package:", .r2py_pkg)), error = function(e) NULL))) {
    if (is.null(env) || !exists(.r2py_fname, envir = env, inherits = FALSE)) next
    hooked <- tryCatch({
      unlockBinding(.r2py_fname, env); assign(.r2py_fname, w, envir = env); lockBinding(.r2py_fname, env); TRUE
    }, error = function(e) FALSE)
    if (hooked) .r2py_hooked <<- c(.r2py_hooked, environmentName(env))
  }
})

.r2py_lines <- tryCatch(
  # run.donttest: under Rscript it defaults to interactive() = FALSE, which comments out every \donttest{}
  # block (`##D`) - where packages put their slower examples, and where base R puts nearly all of them.
  # \dontrun{} stays off: it is for code that needs credentials or a network, or writes files.
  utils::example(.r2py_fname, package = .r2py_pkg, character.only = TRUE, give.lines = TRUE,
                 echo = FALSE, local = TRUE, run.donttest = TRUE, run.dontrun = FALSE),
  error = function(e) NULL)
.r2py_status <- if (is.null(.r2py_lines) || !length(.r2py_lines)) "no_examples" else "ok"
if (identical(.r2py_status, "ok")) {
  .r2py_exprs <- tryCatch(parse(text = paste(.r2py_lines, collapse = "\n")), error = function(e) NULL)
  if (is.null(.r2py_exprs)) {
    .r2py_status <- "unparsable_examples"
  } else {
    .r2py_dev <- tryCatch({ grDevices::pdf(NULL); TRUE }, error = function(e) FALSE)
    for (.e in as.list(.r2py_exprs)) {
      try(suppressWarnings(suppressMessages(eval(.e, envir = globalenv()))), silent = TRUE)
    }
    if (.r2py_dev) try(grDevices::dev.off(), silent = TRUE)
  }
}
writeLines(as.character(jsonlite::toJSON(
  list(status = .r2py_status, n_lines = length(.r2py_lines), cases = .r2py_rec,
       seen = .r2py_seen, unserialisable = .r2py_unser, hooked = as.list(.r2py_hooked),
       example_text = substr(paste(.r2py_lines, collapse = "
"), 1, 4000)),
  auto_unbox = TRUE, digits = NA, null = "null")), "_r2py_harvest.json")
"""


def harvest(spec: str, timeout_s: float = 240) -> dict:
    """Run one function's package examples with the function intercepted; return its recorded calls."""
    from r2py.stage0.effects import data as _data_effects
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    from r2py.types import EffectClass

    fname, pkg = spec.split("@", 1)
    row = {"function": fname, "package": pkg}
    started = time.monotonic()
    program = _R_HARVEST.replace("__FNAME__", fname).replace("__PKG__", pkg)
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            RSandbox().run(program, workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}),
                           timeout_s=timeout_s, preamble=_data_effects.build_r_serializer_fn())
            f = Path(tmp) / "_r2py_harvest.json"
            if not f.exists():
                row["status"] = "no_output"
            else:
                got = json.loads(f.read_text(encoding="utf-8"))
                cases = got.get("cases") or []
                cases = cases if isinstance(cases, list) else [cases]
                row["status"] = got.get("status")
                row["example_lines"] = got.get("n_lines")
                row["seen"] = got.get("seen")                       # calls intercepted (0: never hooked)
                row["unserialisable"] = got.get("unserialisable")   # intercepted, not recordable
                row["hooked"] = got.get("hooked") or []
                row["example_text"] = got.get("example_text") or ""
                # An argument the R serialiser could only fingerprint (`__r2py_fp__`) is a hash of an
                # object, not a value: a Python function handed that dict can "pass" vacuously, which
                # is exactly what happened to ggroc@pROC (7/7 on roc-object fingerprints).
                usable = [c for c in cases if "__r2py_fp__" not in json.dumps(c.get("args"))]
                row["n_fingerprint_args"] = len(cases) - len(usable)
                cases = usable
                row["cases"] = cases
                row["n_cases"] = len(cases)
                row["n_distinct"] = len({json.dumps(c.get("args"), sort_keys=True) for c in cases})
    except Exception as exc:
        row["status"] = f"error: {type(exc).__name__}: {exc}"[:160]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def as_mined(row: dict) -> list[dict]:
    """Harvested calls in the shape `difftest.run_python` and `propose` expect of mined cases."""
    cases = []
    for c in row.get("cases") or []:
        if c.get("value") is None:
            continue
        cases.append({
            "call": (c.get("call") or f"{row['function']}(...)") + "   [from the package's own examples]",
            "args": c["args"],
            "expected": c["value"],
            "rclass": c.get("rclass") or "",
            "shown": c.get("shown") or "",
            "mined": True,
            "core": True,
            "draws": [],
        })
    # the same arguments twice teaches nothing, and the budget is per function
    seen, out = set(), []
    for c in cases:
        k = json.dumps(c["args"], sort_keys=True)
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out[:20]
