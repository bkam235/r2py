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
import matplotlib.pyplot as plt

# Ensure volcano is a numpy array (it comes from shim as a DataFrame or list of lists)
if hasattr(volcano, 'values'):
    volcano_arr = volcano.values
else:
    volcano_arr = np.array(volcano)

# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
# r2py:entity:ncol_1
ncol_volcano = volcano_arr.shape[1]
x = np.arange(ncol_volcano) / (ncol_volcano - 1)

# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
# r2py:entity:nrow_1
nrow_volcano = volcano_arr.shape[0]
y = np.arange(nrow_volcano - 1, -1, -1) / (nrow_volcano - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
# 5*(19:38) = 95, 100, ..., 190
levels_lines = 5 * np.arange(19, 39)
# isolines usually returns a list of paths. In Python, contour handles this internally.
lines = levels_lines 

# g <- isolines_grob(lines, breaks = 20*(5:10), ...)
# breaks = 20*(5:10) = 100, 120, 140, 160, 180, 200
breaks = 20 * np.arange(5, 11)
# colors: grey50, grey20, grey50, grey50 (repeated/cycled)
colors = ["#808080", "#333333", "#808080", "#808080"]
# widths: 1, 2, 1, 1
linewidths = [1, 2, 1, 1]

# In Python, we represent the 'grob' (graphical object) as the contour set result
# Since matplotlib.contour handles drawing and generation together:
X, Y = np.meshgrid(x, y)

# grid.newpage()
plt.figure()

# grid.draw(g)
# We use the breaks for levels and the colors/widths for the specific lines
# Matplotlib cycles colors if the list is shorter than the number of levels
cs = plt.contour(X, Y, volcano_arr, levels=breaks, colors=colors, linewidths=linewidths)

# Final formatting to match grid-like output (no axes)
plt.axis('off')
plt.gca().set_aspect('equal')