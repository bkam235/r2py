"""Plot capture for R and Python (§2.2): every page as a PNG, plus a content fingerprint.

A *fingerprint* describes what a page plots, not how it renders: the data behind its
points/lines/bars, and its text.  Rendered PNGs from R and matplotlib differ in fonts and
styling, so image similarity cannot tell a right plot from a wrong one (measured: an empty
axis scored higher than the correct plot).  The fingerprint is what
``stage4.comparators.graphics`` compares.

Fingerprint schema (one dict per page; ``None`` when extraction was impossible)::

    {"src": "base" | "ggplot" | "mpl",
     "title": str, "xlab": str, "ylab": str, "texts": [str],
     "px": [float], "py": [float],   # vertices of points / lines
     "seg": [int],                   # length of each series within px/py
     "bars": [float],                # signed bar / histogram heights
     "n_polys": int, "n_segs": int, "n_img": int}
"""
from __future__ import annotations

import json
from pathlib import Path

MAX_POINTS = 5000


# ---------------------------------------------------------------------------
# R
# ---------------------------------------------------------------------------

R_PREAMBLE = """\
# r2py graphics capture: PNG device writing EVERY page (%03d), plus a per-page fingerprint.
.r2py_seg <- 0L
.r2py_open_device <- function() {
  .r2py_seg <<- .r2py_seg + 1L
  png(
    filename = file.path(getwd(), sprintf("_r2py_plot_s%03d_%%03d.png", .r2py_seg)),
    width = 800, height = 600
  )
  # Without this recordPlot() returns an empty display list.
  dev.control("enable")
}
.r2py_open_device()

.r2py_fp_num <- function(x) {
  x <- suppressWarnings(as.numeric(x)); x[is.finite(x)]
}
.r2py_fp_chr <- function(x) {
  if (is.null(x)) return(character(0))
  x <- tryCatch(as.character(x), error = function(e) character(0))
  x[!is.na(x) & nzchar(x)]
}

# Fingerprint of the page currently on the device (base graphics via the display list).
.r2py_fp_base <- function() {
  dl <- recordPlot()[[1]]
  fp <- list(src = "base", title = "", xlab = "", ylab = "", texts = character(0),
             px = numeric(0), py = numeric(0), seg = integer(0), bars = numeric(0),
             n_polys = 0L, n_segs = 0L, n_img = 0L)
  seen <- FALSE
  for (e in dl) {
    cl <- e[[2]]
    nm <- tryCatch(cl[[1]]$name, error = function(err) NULL)
    if (is.null(nm)) next
    a <- as.list(cl)[-1]
    if (nm == "C_plotXY") {
      type <- tryCatch(as.character(a[[2]]), error = function(err) "p")
      if (!identical(type, "n")) {
        xy <- a[[1]]
        x <- .r2py_fp_num(xy$x); y <- .r2py_fp_num(xy$y)
        n <- min(length(x), length(y))
        fp$px <- c(fp$px, x[seq_len(n)]); fp$py <- c(fp$py, y[seq_len(n)])
        fp$seg <- c(fp$seg, n)
        seen <- TRUE
      }
    } else if (nm == "C_rect") {
      yb <- .r2py_fp_num(a[[2]]); yt <- .r2py_fp_num(a[[4]])
      n <- max(length(yb), length(yt))
      if (n > 0L) fp$bars <- c(fp$bars, rep_len(yt, n) - rep_len(yb, n))
      seen <- TRUE
    } else if (nm == "C_polygon") {
      fp$n_polys <- fp$n_polys + 1L; seen <- TRUE
    } else if (nm == "C_segments") {
      fp$n_segs <- fp$n_segs + length(a[[1]]); seen <- TRUE
    } else if (nm == "C_image") {
      fp$n_img <- fp$n_img + 1L; seen <- TRUE
    } else if (nm == "C_text") {
      fp$texts <- c(fp$texts, .r2py_fp_chr(a[[2]]))
    } else if (nm == "C_mtext") {
      fp$texts <- c(fp$texts, .r2py_fp_chr(a[[1]]))
    } else if (nm == "C_title") {
      t <- .r2py_fp_chr(a[[1]]); if (length(t)) fp$title <- t[1]
      t <- .r2py_fp_chr(a[[3]]); if (length(t)) fp$xlab <- t[1]
      t <- .r2py_fp_chr(a[[4]]); if (length(t)) fp$ylab <- t[1]
    }
  }
  if (!seen) return(NULL)
  fp
}

# Fingerprint of a ggplot from its built layer data.
.r2py_fp_gg <- function(g) {
  b <- ggplot2::ggplot_build(g)
  fp <- list(src = "ggplot", title = "", xlab = "", ylab = "", texts = character(0),
             px = numeric(0), py = numeric(0), seg = integer(0), bars = numeric(0),
             n_polys = 0L, n_segs = 0L, n_img = 0L)
  for (i in seq_along(b$data)) {
    d <- b$data[[i]]
    geom <- class(g$layers[[i]]$geom)[1]
    if (geom %in% c("GeomBar", "GeomCol", "GeomRect", "GeomTile")) {
      if (all(c("ymin", "ymax") %in% names(d))) {
        fp$bars <- c(fp$bars, .r2py_fp_num(d$ymax - d$ymin))
      } else if ("y" %in% names(d)) fp$bars <- c(fp$bars, .r2py_fp_num(d$y))
    } else if (geom %in% c("GeomPoint", "GeomLine", "GeomPath", "GeomStep", "GeomSmooth", "GeomJitter")) {
      if (all(c("x", "y") %in% names(d))) {
        x <- .r2py_fp_num(d$x); y <- .r2py_fp_num(d$y); n <- min(length(x), length(y))
        fp$px <- c(fp$px, x[seq_len(n)]); fp$py <- c(fp$py, y[seq_len(n)])
        fp$seg <- c(fp$seg, n)
      }
    } else if (geom %in% c("GeomText", "GeomLabel")) {
      fp$texts <- c(fp$texts, .r2py_fp_chr(d$label))
    } else {
      fp$n_polys <- fp$n_polys + nrow(d)
    }
  }
  lab <- b$plot$labels
  t <- .r2py_fp_chr(lab$title); if (length(t)) fp$title <- t[1]
  t <- .r2py_fp_chr(lab$x); if (length(t)) fp$xlab <- t[1]
  t <- .r2py_fp_chr(lab$y); if (length(t)) fp$ylab <- t[1]
  fp
}

# Pages are delimited by hooks: a new page starts on grid.newpage, or on plot.new when the
# previous panel was the last of the layout (par("mfg")) and par(new=TRUE) is not set.
.r2py_fp_open <- FALSE
.r2py_fp_gg_pending <- NULL
.r2py_fp_pages <- list()      # since the last per-entity drain
.r2py_fp_all <- list()        # whole run

.r2py_fp_snap <- function() {
  if (!.r2py_fp_open) return(invisible(NULL))
  .r2py_fp_open <<- FALSE
  fp <- tryCatch({
    if (!is.null(.r2py_fp_gg_pending)) {
      g <- .r2py_fp_gg_pending; .r2py_fp_gg_pending <<- NULL
      .r2py_fp_gg(g)
    } else .r2py_fp_base()
  }, error = function(e) NULL)
  .r2py_fp_pages[[length(.r2py_fp_pages) + 1L]] <<- list(fp = fp)
  .r2py_fp_all[[length(.r2py_fp_all) + 1L]] <<- list(fp = fp)
  invisible(NULL)
}
.r2py_fp_hook_plot_new <- function() {
  mfg <- tryCatch(par("mfg"), error = function(e) c(1L, 1L, 1L, 1L))
  new_page <- !isTRUE(tryCatch(par("new"), error = function(e) FALSE)) &&
    mfg[1] == mfg[3] && mfg[2] == mfg[4]
  if (new_page) { .r2py_fp_snap(); .r2py_fp_open <<- TRUE }
}
.r2py_fp_hook_grid <- function() {
  .r2py_fp_snap()
  .r2py_fp_open <<- TRUE
  if ("ggplot2" %in% loadedNamespaces())
    .r2py_fp_gg_pending <<- tryCatch(ggplot2::last_plot(), error = function(e) NULL)
}
tryCatch({
  # "before.*": the display list still holds the finished page (plot.new's own hook runs
  # after the new page has already cleared it).
  setHook("before.plot.new", .r2py_fp_hook_plot_new, action = "append")
  setHook("before.grid.newpage", .r2py_fp_hook_grid, action = "append")
}, error = function(e) NULL)

# Snapshot the open page and hand back the pages seen since the last drain (as JSON text).
.r2py_fp_drain <- function() {
  .r2py_fp_snap()
  out <- .r2py_fp_pages
  .r2py_fp_pages <<- list()
  jsonlite::toJSON(lapply(out, function(p) p$fp), auto_unbox = TRUE, null = "null", digits = NA)
}
.r2py_fp_write_all <- function() {
  .r2py_fp_snap()
  tryCatch(writeLines(
    as.character(jsonlite::toJSON(lapply(.r2py_fp_all, function(p) p$fp),
                                  auto_unbox = TRUE, null = "null", digits = NA)),
    "_r2py_gfx_meta.json"), error = function(e) NULL)
}
"""

R_EPILOGUE = """\
# r2py graphics capture: fingerprint the last page, then close the PNG device
tryCatch(.r2py_fp_write_all(), error = function(e) NULL)
tryCatch(dev.off(), error = function(e) NULL)
"""


# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------

PY_PREAMBLE = """\
import matplotlib as _r2py_mpl
_r2py_mpl.use('Agg')
_r2py_fig_seq = 0
_r2py_gfx_all = []

def _r2py_fp_num(seq):
    import numpy as _np
    try:
        a = _np.asarray(seq, dtype=float).ravel()
    except Exception:
        return []
    return [float(v) for v in a[_np.isfinite(a)]][:5000]

def _r2py_fp_fig(fig):
    # Content fingerprint of one matplotlib figure (see r2py.stage0.effects.graphics).
    try:
        import numpy as _np
        from matplotlib.patches import Rectangle as _Rect
        from matplotlib.collections import PathCollection as _PC
        fp = {'src': 'mpl', 'title': '', 'xlab': '', 'ylab': '', 'texts': [],
              'px': [], 'py': [], 'seg': [], 'bars': [], 'n_polys': 0, 'n_segs': 0, 'n_img': 0}
        sup = getattr(fig, '_suptitle', None)
        if sup is not None and sup.get_text():
            fp['title'] = sup.get_text()
        for ax in fig.axes:
            if ax.get_title() and not fp['title']:
                fp['title'] = ax.get_title()
            if ax.get_xlabel() and not fp['xlab']:
                fp['xlab'] = ax.get_xlabel()
            if ax.get_ylabel() and not fp['ylab']:
                fp['ylab'] = ax.get_ylabel()
            for ln in ax.lines:
                try:
                    if not ln.get_transform().contains_branch(ax.transData):
                        continue
                except Exception:
                    pass
                x = _r2py_fp_num(ln.get_xdata()); y = _r2py_fp_num(ln.get_ydata())
                n = min(len(x), len(y))
                fp['px'] += x[:n]; fp['py'] += y[:n]; fp['seg'].append(n)
            for c in ax.collections:
                if isinstance(c, _PC):
                    off = _np.asarray(c.get_offsets(), dtype=float).reshape(-1, 2)
                    off = off[_np.isfinite(off).all(axis=1)]
                    fp['px'] += [float(v) for v in off[:, 0]][:5000]
                    fp['py'] += [float(v) for v in off[:, 1]][:5000]
                    fp['seg'].append(len(off))
                else:
                    fp['n_polys'] += len(c.get_paths())
            for p in ax.patches:
                if isinstance(p, _Rect):
                    fp['bars'].append(float(p.get_height()))
                else:
                    fp['n_polys'] += 1
            fp['n_img'] += len(ax.images)
            fp['texts'] += [t.get_text() for t in ax.texts if t.get_text()]
            leg = ax.get_legend()
            if leg is not None:
                fp['texts'] += [t.get_text() for t in leg.get_texts() if t.get_text()]
        fp['px'] = fp['px'][:5000]; fp['py'] = fp['py'][:5000]
        return fp
    except Exception:
        return None

def _r2py_flush_figs(eid_safe=None):
    # Save every open figure (PNG + fingerprint); with eid_safe also as that entity's snapshot.
    global _r2py_fig_seq
    import json as _json
    import matplotlib.pyplot as _plt
    fps = []
    for _k, _fn in enumerate(_plt.get_fignums(), start=1):
        _fig = _plt.figure(_fn)
        _fig.set_size_inches(8, 6)
        _r2py_fig_seq += 1
        fps.append(_r2py_fp_fig(_fig))
        try:
            _fig.savefig(f'_r2py_plot_{_r2py_fig_seq:04d}.png', dpi=100)
            if eid_safe is not None:
                _fig.savefig(f'_r2py_cp_plot_{eid_safe}__{_k:03d}.png', dpi=100)
        except Exception:
            pass
    _r2py_gfx_all.extend(fps)
    if eid_safe is not None:
        with open(f'_r2py_cp_gfx_{eid_safe}.json', 'w', encoding='utf-8') as _f:
            _json.dump(fps, _f)
    return len(fps)
"""

PY_EPILOGUE = """\
try:
    import json as _r2py_json_gfx
    import matplotlib.pyplot as _r2py_plt
    _r2py_flush_figs()
    _r2py_plt.close('all')
    with open('_r2py_gfx_meta.json', 'w', encoding='utf-8') as _f:
        _r2py_json_gfx.dump(_r2py_gfx_all, _f)
except Exception:
    pass
"""


# ---------------------------------------------------------------------------
# Collect
# ---------------------------------------------------------------------------

_MIN_REAL_PLOT_BYTES = 2000  # blank PNGs from device open/close with no content


def _read_pages(files: list[Path]) -> list[bytes]:
    pages: list[bytes] = []
    for p in files:
        try:
            data = p.read_bytes()
        except OSError:
            continue
        if len(data) >= _MIN_REAL_PLOT_BYTES:
            pages.append(data)
    return pages


def read_meta(path: Path) -> list:
    """Fingerprints from a JSON list file; [] if absent or unreadable."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return data if isinstance(data, list) else []


def collect(workdir: Path) -> dict:
    """Every ``_r2py_plot_*.png`` in name order (R segments, then pages) plus fingerprints."""
    return {
        "graphics": _read_pages(sorted(workdir.glob("_r2py_plot_*.png"))),
        "graphics_meta": read_meta(workdir / "_r2py_gfx_meta.json"),
    }
