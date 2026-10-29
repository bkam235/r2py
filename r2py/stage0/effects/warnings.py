"""Warning / message / error capture for R and Python (§2.2)."""
from __future__ import annotations

import json
from pathlib import Path


R_PREAMBLE = """\
# r2py warnings capture
.r2py_warnings <- character(0)
withCallingHandlers(
"""

# The R preamble wraps the script body: the sandbox must close the handler after
# the user script runs.  The epilogue below closes the withCallingHandlers call
# and writes the captured list.
R_EPILOGUE = """\
, warning = function(w) {
    .r2py_warnings <<- c(.r2py_warnings, conditionMessage(w))
    invokeRestart('muffleWarning')
  },
  message = function(m) {
    .r2py_warnings <<- c(.r2py_warnings, conditionMessage(m))
    invokeRestart('muffleMessage')
  }
)
writeLines(jsonlite::toJSON(.r2py_warnings), '_r2py_warnings.json')
"""

# NOTE: The withCallingHandlers wrapping requires the preamble to open the
# expression and the epilogue to close it.  The sandbox joins them as:
#   preamble + "{" + source + "}" + epilogue
# The R_PREAMBLE ends with the opening brace of the expression argument.


# Simpler preamble/epilogue that doesn't require wrapping (used by r_sandbox):
# warning.expression runs once per warning that reaches the default handling, but has no condition in scope
# (2026-10-29: every warning was stored as ''), so a global calling handler keeps the latest message for it.
# The handler alone would count rlang's warnings twice (it signals the condition, then calls warning()).
# "package 'x' was built under R version y" comes from the harness's R install, not from the script.
R_PREAMBLE_SIMPLE = """\
.r2py_warnings <- character(0)
.r2py_last_warning <- ''
.r2py_orig_warning <- getOption('warning.expression')
globalCallingHandlers(warning = function(w) .r2py_last_warning <<- conditionMessage(w))
options(warning.expression = quote({
  if (!grepl('was built under R version', .r2py_last_warning, fixed = TRUE))
    .r2py_warnings <<- c(.r2py_warnings, .r2py_last_warning)
}))
"""

R_EPILOGUE_SIMPLE = """\
options(warning.expression = .r2py_orig_warning)
globalCallingHandlers(NULL)
suppressWarnings(
  writeLines(jsonlite::toJSON(.r2py_warnings), '_r2py_warnings.json')
)
"""

PY_PREAMBLE = """\
import warnings as _r2py_warnings_mod
_r2py_warn_list = []
_r2py_orig_showwarning = _r2py_warnings_mod.showwarning
def _r2py_capture_warning(message, category, filename, lineno, file=None, line=None):
    # plt.show() under the sandbox's Agg backend warns from the script's own line, not from matplotlib
    if 'matplotlib' not in (filename or '') and 'is non-interactive, and thus cannot be shown' not in str(message):
        _r2py_warn_list.append(str(message))
_r2py_warnings_mod.showwarning = _r2py_capture_warning
"""

PY_EPILOGUE = """\
try:
    import json as _r2py_json_warn
    _r2py_warnings_mod.showwarning = _r2py_orig_showwarning
    with open('_r2py_warnings.json', 'w', encoding='utf-8') as _f:
        _r2py_json_warn.dump(_r2py_warn_list, _f)
except Exception:
    pass
"""


def collect(workdir: Path) -> dict:
    """Read _r2py_warnings.json → EffectBundle.warnings list."""
    warn_file = workdir / "_r2py_warnings.json"
    if not warn_file.exists():
        return {"warnings": []}
    try:
        return {"warnings": json.loads(warn_file.read_text(encoding="utf-8"))}
    except Exception:
        return {"warnings": []}
