"""How much of the loss could a verified runtime ever reach? (Step 1 of the runtime pilot.)

The same discipline as `scripts/coverage_probe.py`, applied before building the growth loop: bound the
prize offline, with no model calls, so we cannot repeat the pattern library's course of building a
mechanism whose ceiling was 17%.

A runtime function can only replace an R function that is *value-returning and inspectable*: a plot,
a file write or an environment manipulation cannot be pasted in as `r_f(...)`. So each entity's loss
is attributed to the function that would have to be implemented (the right-hand call of an
assignment, else the entity's own call) and that function is classified in R:

  candidate   -- found, a closure with a walkable body, no impure/lazy call in it
  impure      -- found, but its body uses one of difftest.IMPURE (IO, environment, NSE, error handling)
  graphics    -- a plotting/device function (its effect is a drawing, not a value)
  primitive   -- found but has no R body (builtin/internal); pure, yet nothing to read a spec from
  not_found   -- R could not find it (package not installed, S4/R5 method, local helper)

`impure_calls()` cannot tell `not_found` from pure (it returns an empty list for both), so this
script runs its own probe and keeps the two apart.

    python scripts/runtime_ceiling.py inventory --set heldout
    python scripts/runtime_ceiling.py report
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROBE = ROOT / "work" / "coverage_probe"
MANIFEST = ROOT / "experiments" / "heldout" / "manifest.json"
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


# ----------------------------------------------------------------------------- inventory (runs R)

def _one(script: str) -> dict:
    """Which function each entity of this script would need implemented."""
    from r2py import stage1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pool = Path(manifest["pool_dir"])
    if not pool.is_absolute():
        pool = ROOT / pool
    try:
        sm = stage1.analyze(next(pool.rglob(script)))
    except Exception as exc:
        return {"script": script, "error": f"{type(exc).__name__}: {exc}"[:200]}
    ents = []
    for eid, e in sm.entities.items():
        rhs = getattr(e, "rhs_call_name", None)
        ents.append({"id": eid, "name": getattr(e, "name", ""),
                     "fn": rhs or getattr(e, "name", ""),
                     "package": ((getattr(e, "rhs_call_package", None) if rhs else None)
                                 or getattr(e, "package", "") or "")})
    return {"script": script, "entities": ents}


def inventory(which: str, workers: int) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scripts = [e["script"] for e in manifest[which]]
    out = PROBE / f"{which}_functions.jsonl"
    done = {json.loads(l)["script"] for l in out.open(encoding="utf-8")} if out.exists() else set()
    todo = [s for s in scripts if s not in done]
    print(f"{which}: {len(done)} done, {len(todo)} to go", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(workers) as pool, out.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(_one, todo), start=1):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            if i % 10 == 0:
                print(f"{i}/{len(todo)}", flush=True)


# ----------------------------------------------------------------------------- report

def _classify(info: dict | None, package: str) -> str:
    if package.lower() in GRAPHICS_PACKAGES:
        return "graphics"
    if info is None or not info.get("found"):
        return "not_found"
    if info["kind"] == "primitive":
        return "primitive"
    return "impure" if info.get("impure") else "candidate"


def report() -> str:
    import sys as _s
    _s.path.insert(0, str(ROOT / "scripts"))
    from coverage_probe import heldout_entities

    fns = {}
    for line in (PROBE / "heldout_functions.jsonl").open(encoding="utf-8"):
        row = json.loads(line)
        if "error" in row:
            continue
        for e in row["entities"]:
            fns[(row["script"], e["id"])] = (e["fn"], e["package"])

    ents = heldout_entities("empty")
    total = sum(1 - v["mean"] for v in ents.values())
    specs = sorted({fns[k] for k in ents if k in fns and fns[k][0]})
    info = probe(specs)

    loss: Counter = Counter()
    count: Counter = Counter()
    worst: dict = defaultdict(Counter)
    unmapped = 0.0
    for key, v in ents.items():
        l = 1 - v["mean"]
        pair = fns.get(key)
        if not pair or not pair[0]:
            unmapped += l
            count["(no function identified)"] += 1
            continue
        cls = _classify(info.get(pair), pair[1])
        loss[cls] += l
        count[cls] += 1
        worst[cls][f"{pair[0]}@{pair[1] or '-'}"] += l

    lines = [f"held-out entities {len(ents)}, lost points {total:.1f}; "
             f"{len(specs)} distinct (function, package) pairs probed in R",
             f"{'class':<14}{'entities':>10}{'lost points':>14}{'share':>8}"]
    for cls, l in loss.most_common():
        lines.append(f"{cls:<14}{count[cls]:>10}{l:>14.1f}{l / total:>8.0%}")
    if unmapped:
        lines.append(f"{'(unmapped)':<14}{count['(no function identified)']:>10}{unmapped:>14.1f}"
                     f"{unmapped / total:>8.0%}")
    lines.append("")
    lines.append("biggest losses among the candidates (what a runtime would have to implement):")
    for name, l in worst["candidate"].most_common(12):
        lines.append(f"  {l:6.2f}  {name}")
    lines.append("")
    lines.append("biggest losses ruled out (graphics / impure / primitive / not found):")
    ruled: Counter = Counter()
    for cls in ("graphics", "impure", "primitive", "not_found"):
        ruled.update(worst[cls])
    for name, l in ruled.most_common(8):
        lines.append(f"  {l:6.2f}  {name}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("inventory")
    p.add_argument("--set", dest="which", default="heldout", choices=["heldout", "train"])
    p.add_argument("--workers", type=int, default=5)
    sub.add_parser("report")
    args = ap.parse_args()
    if args.cmd == "inventory":
        inventory(args.which, args.workers)
    else:
        text = report()
        print(text)
        (PROBE / "runtime_ceiling.txt").write_text(text + "\n", encoding="utf-8")
