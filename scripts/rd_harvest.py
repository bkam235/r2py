"""Yield probe: can a package's own Rd examples supply the test cases the runtime pilot lacks?

Half of the pilot's package-function attempts never got a verdict (`no_cases`: R accepted fewer than
three of the model's invented calls), and corpus mining cannot help because the functions that cost
us points appear in one or two scripts in the whole 3,988-script corpus. Every exported function,
though, ships an `\\examples` block. This runs that block with the function intercepted in its own
namespace and records each real call: the arguments as evaluated at the call site, and R's answer.

No model calls. The question is the yield: how many usable cases per function, against the three
`propose.attempt` needs before it will even try.

    python scripts/rd_harvest.py --top 15
    python scripts/rd_harvest.py --functions time_add@timechange createTimeSlices@caret
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "work" / "rd_harvest"

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

local({
  ns <- asNamespace(.r2py_pkg)
  orig <- get(.r2py_fname, envir = ns)
  w <- function(...) {
    a <- list(...)
    r <- orig(...)
    ok <- tryCatch({ .r2py_json_args(a); .r2py_serialize_var(r); TRUE }, error = function(e) FALSE)
    if (ok && length(.r2py_rec) < 60L) {
      .r2py_rec[[length(.r2py_rec) + 1L]] <<- list(
        args = .r2py_json_args(a), value = .r2py_serialize_var(r),
        rclass = class(r)[1],
        shown = paste(utils::head(tryCatch(capture.output(print(r)), error = function(e) ""), 12), collapse = "
"),
        call = paste(utils::head(deparse(sys.call(0)), 3), collapse = " "),
        nargs = length(a), names = if (is.null(names(a))) list() else as.list(names(a)))
    }
    r
  }
  # the examples call the exported binding, so replace it in the namespace AND in the attached
  # package environment; internal calls from other package functions are intercepted too.
  for (env in list(ns, tryCatch(as.environment(paste0("package:", .r2py_pkg)), error = function(e) NULL))) {
    if (is.null(env) || !exists(.r2py_fname, envir = env, inherits = FALSE)) next
    tryCatch({
      unlockBinding(.r2py_fname, env); assign(.r2py_fname, w, envir = env); lockBinding(.r2py_fname, env)
    }, error = function(e) NULL)
  }
})

.r2py_lines <- tryCatch(
  utils::example(.r2py_fname, package = .r2py_pkg, character.only = TRUE, give.lines = TRUE,
                 echo = FALSE, local = TRUE),
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
  list(status = .r2py_status, n_lines = length(.r2py_lines), cases = .r2py_rec),
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


def targets(top: int) -> list[str]:
    """The candidate functions that cost the held-out set the most, biggest first."""
    from collections import Counter

    from coverage_probe import heldout_entities
    from runtime_ceiling import PROBE, _classify, probe

    fns = {}
    for line in (PROBE / "heldout_functions.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if "error" in r:
            continue
        for e in r["entities"]:
            fns[(r["script"], e["id"])] = (e["fn"], e["package"])
    ents = heldout_entities("empty")
    specs = sorted({fns[k] for k in ents if k in fns and fns[k][0]})
    info = probe(specs)
    loss: Counter = Counter()
    for k, v in ents.items():
        pair = fns.get(k)
        if pair and pair[0] and _classify(info.get(pair), pair[1]) == "candidate" and pair[1]:
            loss[f"{pair[0]}@{pair[1]}"] += 1 - v["mean"]
    return [s for s, _ in loss.most_common(top)], loss


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=15, help="the N candidate functions with the most held-out loss")
    ap.add_argument("--functions", nargs="+", default=None, help="explicit name@package list instead")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    loss: dict = {}
    if args.functions:
        specs = args.functions
    else:
        specs, loss = targets(args.top)
    print(f"{len(specs)} functions: {', '.join(specs)}", flush=True)
    ctx = multiprocessing.get_context("spawn")
    rows = []
    with ctx.Pool(args.workers) as pool:
        for row in pool.imap_unordered(harvest, specs):
            rows.append(row)
            print(f"   {row['function'] + '@' + row['package']:<34}{str(row.get('status'))[:22]:<24}"
                  f"cases {row.get('n_cases', 0):>3} ({row.get('n_distinct', 0)} distinct)  "
                  f"{row['seconds']}s", flush=True)
    (OUT / "rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    usable = [r for r in rows if (r.get("n_distinct") or 0) >= 3]
    print(f"\n{len(usable)}/{len(rows)} functions reach the 3 distinct cases the pilot needs")
    if loss:
        got = sum(loss[f"{r['function']}@{r['package']}"] for r in usable)
        want = sum(loss[s] for s in specs)
        print(f"held-out loss on those functions: {got:.1f} of {want:.1f} points covered "
              f"({got / want:.0%} of the targeted loss)")
    print(f"status counts: {json.dumps({s: sum(1 for r in rows if str(r.get('status')).startswith(s)) for s in sorted({str(r.get('status'))[:14] for r in rows})})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
