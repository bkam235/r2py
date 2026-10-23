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

# Convert volcano to numpy array for calculation
# volcano is loaded as a DataFrame or list by the shim
volcano_np = np.array(volcano)

# r2py:entity:ncol
ncol_val = volcano_np.shape[1]
# r2py:entity:nrow
nrow_val = volcano_np.shape[0]

# r2py:entity:x
x = np.arange(0, ncol_val) / (ncol_val - 1)
# r2py:entity:y
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# r2py:entity:lines
# isolines(x, y, volcano, 5*(19:38))
levels_lines = 5 * np.arange(19, 39)
# In R, isolines computes the contours. In Python, we store the levels.
lines = levels_lines

# r2py:entity:g
# isolines_grob(lines, breaks = 20*(5:10), gp = gpar(...))
breaks = 20 * np.arange(5, 11)
# gp parameters
fontsize = 10
lwd = [1, 2, 1, 1]
cols = ["grey50", "grey20", "grey50", "grey50"]

# To simulate the grob 'g', we store the plot configuration
g = {
    "levels": breaks,
    "lwd": lwd,
    "colors": cols,
    "fontsize": fontsize
}

# r2py:entity:grid.newpage
plt.figure()

# r2py:entity:grid.draw
# The R code draws a contour plot with specific breaks and styling.
X, Y = np.meshgrid(x, y)
# Note: volcano in R is usually indexed (row, col). 
# To match grid's coordinate system where (0,0) is bottom-left:
cs = plt.contour(X, Y, volcano_np, levels=breaks, colors=cols, linewidths=lwd)

# To handle the 'breaks' labels (simulated by fontsize)
plt.clabel(cs, inline=True, fontsize=fontsize)
plt.axis('off')
plt.show()