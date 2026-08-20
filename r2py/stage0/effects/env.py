"""R/Python environment diff capture (§2.2).

Captures changes to options, env vars, working directory, and sys.path.
"""
from __future__ import annotations

import json
from pathlib import Path


R_PREAMBLE = """\
# r2py env capture: snapshot session state before script
.r2py_env_before <- list(
  options  = options(),
  envvars  = as.list(Sys.getenv()),
  wd       = getwd()
)
"""

R_EPILOGUE = """\
# r2py env capture: diff against before-snapshot
.r2py_env_after <- list(
  options = options(),
  envvars = as.list(Sys.getenv()),
  wd      = getwd()
)
.r2py_env_diff <- list()
for (.k in union(names(.r2py_env_before$options), names(.r2py_env_after$options))) {
  .before_v <- .r2py_env_before$options[[.k]]
  .after_v  <- .r2py_env_after$options[[.k]]
  if (!identical(.before_v, .after_v)) {
    .r2py_env_diff[[paste0('option:', .k)]] <- .after_v
  }
}
for (.k in union(names(.r2py_env_before$envvars), names(.r2py_env_after$envvars))) {
  .before_v <- .r2py_env_before$envvars[[.k]]
  .after_v  <- .r2py_env_after$envvars[[.k]]
  if (!identical(.before_v, .after_v)) {
    .r2py_env_diff[[paste0('envvar:', .k)]] <- if (is.null(.after_v)) NA_character_ else .after_v
  }
}
if (!identical(.r2py_env_before$wd, .r2py_env_after$wd)) {
  .r2py_env_diff[['wd']] <- .r2py_env_after$wd
}
if (length(.r2py_env_diff) > 0) {
  writeLines(jsonlite::toJSON(.r2py_env_diff, auto_unbox=TRUE, na='null'), '_r2py_env.json')
}
"""

PY_PREAMBLE = """\
import os as _r2py_os
import sys as _r2py_sys
_r2py_env_before = {
    'environ': dict(_r2py_os.environ),
    'cwd': _r2py_os.getcwd(),
    'sys_path': list(_r2py_sys.path),
}
"""

PY_EPILOGUE = """\
try:
    import os as _r2py_os2
    import sys as _r2py_sys2
    import json as _r2py_json_env
    _r2py_env_diff = {}
    _after_env = dict(_r2py_os2.environ)
    for _k in set(list(_r2py_env_before['environ']) + list(_after_env)):
        _bv = _r2py_env_before['environ'].get(_k)
        _av = _after_env.get(_k)
        if _bv != _av:
            _r2py_env_diff[f'envvar:{_k}'] = _av
    _after_cwd = _r2py_os2.getcwd()
    if _r2py_env_before['cwd'] != _after_cwd:
        _r2py_env_diff['cwd'] = _after_cwd
    _after_path = list(_r2py_sys2.path)
    if _r2py_env_before['sys_path'] != _after_path:
        _r2py_env_diff['sys_path'] = _after_path
    if _r2py_env_diff:
        with open('_r2py_env.json', 'w', encoding='utf-8') as _f:
            _r2py_json_env.dump(_r2py_env_diff, _f)
except Exception:
    pass
"""


def collect(workdir: Path) -> dict:
    """Read _r2py_env.json → EffectBundle.env dict."""
    env_file = workdir / "_r2py_env.json"
    if not env_file.exists():
        return {"env": {}}
    try:
        return {"env": json.loads(env_file.read_text(encoding="utf-8"))}
    except Exception:
        return {"env": {}}
