"""PNG plot capture for R and Python (§2.2)."""
from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# R
# ---------------------------------------------------------------------------

R_PREAMBLE = """\
# r2py graphics capture: open a PNG device for base/grid plots
.r2py_plot_idx <- 1L
png(
  filename = file.path(getwd(), sprintf("_r2py_plot_%03d.png", .r2py_plot_idx)),
  width = 800, height = 600
)
"""

R_EPILOGUE = """\
# r2py graphics capture: close the PNG device
tryCatch(dev.off(), error = function(e) NULL)
"""


# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------

PY_PREAMBLE = """\
import matplotlib as _r2py_mpl
_r2py_mpl.use('Agg')
"""

PY_EPILOGUE = """\
try:
    import matplotlib.pyplot as _r2py_plt
    for _r2py_fn in _r2py_plt.get_fignums():
        _r2py_fig = _r2py_plt.figure(_r2py_fn)
        _r2py_fig.set_size_inches(8, 6)
        _r2py_fig.savefig(f"_r2py_plot_{_r2py_fn:03d}.png", dpi=100)
    _r2py_plt.close('all')
except Exception:
    pass
"""


# ---------------------------------------------------------------------------
# Collect
# ---------------------------------------------------------------------------

def collect(workdir: Path) -> dict:
    """Read all _r2py_plot_*.png files and return EffectBundle.graphics list."""
    plots = sorted(workdir.glob("_r2py_plot_*.png"))
    graphics: list[bytes] = []
    for p in plots:
        try:
            data = p.read_bytes()
            if len(data) >= 2000:  # skip blank PNGs from device open/close with no content
                graphics.append(data)
        except OSError:
            pass
    return {"graphics": graphics}
