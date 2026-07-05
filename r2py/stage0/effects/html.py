"""HTML / widget render-to-string capture (§2.2)."""
from __future__ import annotations

import json
from pathlib import Path


R_EPILOGUE = """\
# r2py HTML capture: render any htmltools/shiny/htmlwidgets objects to string
.r2py_html_list <- list()
for (.r2py_v in ls(envir = .GlobalEnv)) {
  if (startsWith(.r2py_v, ".r2py_")) next
  .r2py_obj <- get(.r2py_v, envir = .GlobalEnv)
  if (inherits(.r2py_obj, 'shiny.tag') || inherits(.r2py_obj, 'shiny.tag.list') || inherits(.r2py_obj, 'htmltools_tag')) {
    tryCatch({
      .r2py_html_list[[.r2py_v]] <- as.character(
        htmltools::renderTags(.r2py_obj)$html
      )
    }, error = function(e) NULL)
  } else if (inherits(.r2py_obj, 'htmlwidget')) {
    tryCatch({
      tmp <- tempfile(fileext = '.html')
      htmlwidgets::saveWidget(.r2py_obj, tmp, selfcontained = TRUE)
      .r2py_html_list[[.r2py_v]] <- paste(readLines(tmp), collapse = '\\n')
      unlink(tmp)
    }, error = function(e) NULL)
  }
}
if (length(.r2py_html_list) > 0) {
  writeLines(jsonlite::toJSON(.r2py_html_list, auto_unbox = TRUE), '_r2py_html.json')
}
"""

PY_EPILOGUE = """\
try:
    import json as _r2py_json_html
    _r2py_html_out = {}
    for _r2py_hk, _r2py_hv in list(globals().items()):
        if _r2py_hk.startswith('_r2py_') or _r2py_hk.startswith('__'):
            continue
        # plotly figures
        try:
            import plotly.graph_objects as _r2py_go
            if isinstance(_r2py_hv, _r2py_go.Figure):
                _r2py_html_out[_r2py_hk] = _r2py_hv.to_html(full_html=False)
                continue
        except ImportError:
            pass
        # htmltools Tag / TagList (shiny UI objects)
        try:
            from htmltools._core import Tag as _r2py_Tag, TagList as _r2py_TagList
            if isinstance(_r2py_hv, (_r2py_Tag, _r2py_TagList)):
                _r2py_html_out[_r2py_hk] = str(_r2py_hv)
                continue
        except ImportError:
            pass
    if _r2py_html_out:
        with open('_r2py_html.json', 'w', encoding='utf-8') as _f:
            _r2py_json_html.dump(_r2py_html_out, _f)
except Exception:
    pass
"""


def collect(workdir: Path) -> dict:
    """Read _r2py_html.json → EffectBundle.html list."""
    html_file = workdir / "_r2py_html.json"
    if not html_file.exists():
        return {"html": []}
    try:
        raw = json.loads(html_file.read_text(encoding="utf-8"))
        return {"html": list(raw.values())}
    except Exception:
        return {"html": []}
