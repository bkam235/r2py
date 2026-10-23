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

# Prepare volcano data as a numpy array
if hasattr(volcano, 'values'):
    volcano_arr = volcano.values
else:
    volcano_arr = np.array(volcano)

# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
ncol_1 = volcano_arr.shape[1]
x = np.arange(ncol_1) / (ncol_1 - 1)

# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
nrow_1 = volcano_arr.shape[0]
y = np.arange(nrow_1 - 1, -1, -1) / (nrow_1 - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
# The isolines call in R computes the contour paths. 
# In Python, we can represent this by the levels passed to contour.
levels_lines = 5 * np.arange(19, 39)
lines = levels_lines

# g <- isolines_grob(...)
# breaks = 20*(5:10)
breaks = 20 * np.arange(5, 11)
# col = c("grey50", "grey20", "grey50", "grey50")
# lwd = c(1, 2, 1, 1)
colors = ["#808080", "#333333", "#808080", "#808080"]
lwidths = [1, 2, 1, 1]

# grid.newpage()
plt.figure()

# grid.draw(g)
# Use contour to draw the lines. Matplotlib's contour handles the 'isolines' logic.
X, Y = np.meshgrid(x, y)
# We only plot the breaks specified in isolines_grob
cs = plt.contour(X, Y, volcano_arr, levels=breaks, colors=colors, linewidths=lwidths)

# Since isolines_grob might have labels or specific formatting, 
# we set the axes to match grid's clean output.
plt.axis('off')
plt.gca().set_aspect('equal')

g = cs # Assigning the contour set to g to match R variable name