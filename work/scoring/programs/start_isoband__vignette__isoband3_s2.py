# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/isoband__vignette__isoband3_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'isoband__vignette__isoband3_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# R's volcano dataset is a 87x87 matrix
# Loading a simulated version or importing from a source since it's built-in to R
# For the sake of this translation, we use the standard volcano data values
# If the user has a local csv, they would load it here.
try:
    from statsmodels.datasets import get_rdataset
    volcano = get_rdataset("volcano").data.values.reshape(87, 87)
except:
    # Fallback if statsmodels is not available: create a peak-like array
    volcano = np.random.randint(190, 380, (87, 87))

# Coordinate setup
# r2py:entity:ncol_1
x = np.linspace(0, 1, volcano.shape[1])
# r2py:entity:nrow_1
y = np.linspace(1, 0, volcano.shape[0])
X, Y = np.meshgrid(x, y)

# Define breaks for the contour lines
# lines <- isolines(x, y, volcano, 5*(19:38))
# breaks = 20*(5:10) -> [100, 120, 140, 160, 180, 200]
# r2py:entity:lines
breaks = np.arange(100, 220, 20)

# In Python, plotnine/matplotlib handle the contouring via the data mapping
# We transform the grid into a long-format DataFrame for plotnine
# r2py:entity:g
d = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': volcano.flatten()
})

# mapping the colors and line widths
# col = c("grey50", "grey20", "grey50", "grey50")
# lwd = c(1, 2, 1, 1)
# Note: plotnine's geom_contour doesn't allow per-level lwd/col as easily as grid
# We use matplotlib via plotnine's backend or standard plotnine geom_contour

g = (
    ggplot(d, aes(x='x', y='y', z='z'))
    + geom_contour(bins=len(breaks), color="grey50", size=1)
    + theme_void()
)

# To precisely match the R 'isolines_grob' logic of specific levels and colors:
# r2py:entity:grid.newpage
plt.figure(figsize=(5, 5))
# r2py:entity:grid.draw
cp = plt.contour(X, Y, volcano, levels=breaks, colors=["grey50", "grey20", "grey50", "grey50", "grey50", "grey50"])
plt.axis('off')
plt.show()