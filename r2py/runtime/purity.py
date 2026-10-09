"""Can an R function be a runtime function at all? Found, a closure with a walkable body, no impure call.

Moved from scripts/runtime_ceiling.py so the harness can use it (the on-demand step,
r2py/runtime/ondemand.py). Unlike difftest.impure_calls this keeps "not found" apart from "pure" and
keys results by (function, package).

  candidate   found, a closure with a walkable body, no impure/lazy call in it
  impure      found, but its body uses one of difftest.IMPURE (IO, environment, NSE, error handling)
  graphics    a plotting/device function (its effect is a drawing, not a value)
  primitive   found but has no R body (builtin/internal); pure, yet nothing to read a spec from
  not_found   R could not find it (package not installed, S4/R5 method, local helper)
"""
from __future__ import annotations

import json
from pathlib import Path

GRAPHICS_PACKAGES = {"graphics", "grdevices", "grid", "ggplot2", "lattice", "diagram", "shape", "plotrix"}

_R_PROBE = r"""
fns <- jsonlite::fromJSON(r"----(__SPECS__)----", simplifyVector = FALSE)
res <- lapply(fns, function(sp) {
  if (!is.null(sp$pkg) && nzchar(sp$pkg)) {
    try(suppressPackageStartupMessages(library(sp$pkg, character.only = TRUE)), silent = TRUE)
  }
  f <- tryCatch(get(sp$name, mode = "function"), error = function(e) NULL)
  if (is.null(f)) return(list(name = sp$name, pkg = sp$pkg, found = FALSE, kind = "not_found", impure = list()))
  meth <- tryCatch(utils::getS3method(sp$name, "default", optional = TRUE), error = function(e) NULL)
  if (is.primitive(f) && is.null(meth)) {
    return(list(name = sp$name, pkg = sp$pkg, found = TRUE, kind = "primitive", impure = list()))
  }
  bodies <- list(body(f)); if (!is.null(meth)) bodies[[2]] <- body(meth)
  cond <- c("stop", "warning", "message", "stopifnot", "gettextf", "gettext", ".Deprecated", ".Defunct",
            "packageStartupMessage")
  walk <- function(e) {
    if (is.call(e)) {
      h <- e[[1]]
      hn <- if (is.symbol(h)) as.character(h) else ""
      if (hn %in% cond) return(character(0))
      return(c(hn, unlist(lapply(as.list(e)[-1],
        function(a) if (identical(a, quote(expr = ))) character(0) else walk(a))),
        if (!is.symbol(h)) walk(h)))
    }
    if (is.symbol(e)) return(as.character(e))
    character(0)
  }
  used <- unique(unlist(lapply(bodies, walk)))
  list(name = sp$name, pkg = sp$pkg, found = TRUE, kind = "closure",
       impure = as.list(intersect(used, unlist(IMPURE))))
})
cat("@@", as.character(jsonlite::toJSON(res, auto_unbox = TRUE)), "@@")
"""


def probe(specs: list[tuple[str, str]], timeout_s: float = 600) -> dict[tuple[str, str], dict]:
    """(function, package) -> {found, kind, impure}. Keyed by the pair, unlike difftest.impure_calls."""
    import tempfile

    from r2py.runtime.difftest import IMPURE
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    from r2py.types import EffectClass

    program = ("IMPURE <- c(" + ", ".join(json.dumps(x) for x in IMPURE) + ")\n"
               + _R_PROBE.replace("__SPECS__", json.dumps([{"name": n, "pkg": p} for n, p in specs])))
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        out = RSandbox().run(program, workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}),
                             timeout_s=timeout_s).stdout
    try:
        rows = json.loads(out.split("@@")[1])
    except (IndexError, json.JSONDecodeError):
        return {}
    return {(r["name"], r.get("pkg") or ""): r for r in rows}


def classify(info: dict | None, package: str) -> str:
    if package.lower() in GRAPHICS_PACKAGES:
        return "graphics"
    if info is None or not info.get("found"):
        return "not_found"
    if info["kind"] == "primitive":
        return "primitive"
    return "impure" if info.get("impure") else "candidate"
