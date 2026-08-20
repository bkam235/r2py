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
R_PREAMBLE_SIMPLE = """\
.r2py_warnings <- character(0)
.r2py_orig_warning <- getOption('warning.expression')
options(warning.expression = quote({
  .r2py_warnings <<- c(.r2py_warnings, tryCatch(conditionMessage(w), error=function(e) ''))
}))
"""

R_EPILOGUE_SIMPLE = """\
options(warning.expression = .r2py_orig_warning)
suppressWarnings(
  writeLines(jsonlite::toJSON(.r2py_warnings), '_r2py_warnings.json')
)
"""

PY_PREAMBLE = """\
import warnings as _r2py_warnings_mod
_r2py_warn_list = []
_r2py_orig_showwarning = _r2py_warnings_mod.showwarning
def _r2py_capture_warning(message, category, filename, lineno, file=None, line=None):
    if 'matplotlib' not in (filename or ''):
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
