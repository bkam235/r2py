"""probe_r in the script's own state (2026-11-08): the expression is evaluated after the R script has run, with
its variables and packages in place.

The harness's probe (``HarnessTools.probe_r``) runs the expression in a bare R session, so a probe that names a
script variable or calls an unloaded package fails (9 of 18 probes in `free-probe-stall2`). Here the script runs
first, statement by statement (a failing statement is skipped, as in ``harness.locate``), with its own output,
messages and plots discarded; then the expression is evaluated like a console line: each visible value is printed,
and an error prints its message. The harness's 10-probe limit and probe history are shared.
"""
from __future__ import annotations

import tempfile
from pathlib import Path


def _raw(text: str) -> str:
    """*text* as an R raw string literal."""
    delim = "-" * 6
    while f"){delim}\"" in text:
        delim += "-"
    return f'r"{delim}({text}){delim}"'


def program(r_source: str, expression: str) -> str:
    return (
        ".r2py_null <- file(nullfile(), open = 'wt')\n"
        "sink(.r2py_null); sink(.r2py_null, type = 'message')\n"
        "grDevices::pdf(NULL)\n"
        f".r2py_script <- parse(text = {_raw(r_source)}, keep.source = FALSE)\n"
        "for (.r2py_e in as.list(.r2py_script)) tryCatch(eval(.r2py_e, envir = .GlobalEnv), error = function(e) NULL)\n"
        "sink(type = 'message'); sink()\n"
        "tryCatch(for (.r2py_e in as.list(parse(text = " + _raw(expression) + ", keep.source = FALSE))) {\n"
        "  .r2py_v <- withVisible(eval(.r2py_e, envir = .GlobalEnv))\n"
        "  if (.r2py_v$visible) print(.r2py_v$value)\n"
        "}, error = function(e) cat('Error:', conditionMessage(e), '\\n'))\n"
    )


def probe(harness, script_map, expression: str) -> str:
    """The probe's printed output, or "(probe limit reached)" past the harness's 10 probes."""
    if harness._probe_count >= 10:
        return "(probe limit reached)"
    harness._probe_count += 1

    from ..stage0.sandbox.r_sandbox import RSandbox
    from ..stage1.runner import _CRAWLER_PKG_RE, strip_r_guards
    from ..types import EffectClass

    r_source = getattr(script_map, "source", "") or ""
    src = strip_r_guards(r_source)
    m = _CRAWLER_PKG_RE.search(r_source)
    if m:
        src = f"suppressPackageStartupMessages(library({m.group(1)}))\n" + src
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        bundle = RSandbox().run(program(src, expression), workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}),
                                timeout_s=min(harness._timeout_s, 60))
    result = (bundle.stdout or "").strip()
    harness._probe_history.append((expression, result))
    return result
