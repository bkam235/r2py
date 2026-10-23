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

# Ensure volcano is a numpy array
# Depending on shim, volcano might be a DataFrame or list of lists
if hasattr(volcano, 'values'):
    volcano_arr = volcano.values
else:
    volcano_arr = np.array(volcano)

# R: x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
ncol_val = volcano_arr.shape[1]
x = np.arange(ncol_val) / (ncol_val - 1)

# R: y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
nrow_val = volcano_arr.shape[0]
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# R: lines <- isolines(x, y, volcano, 5*(19:38))
# isoband::isolines identifies the contour lines. 
# 5*(19:38) = 95, 100, ..., 190
lines_levels = np.arange(19, 39) * 5
lines = lines_levels # In R, 'lines' here is the result of isolines, which Python handles in the plotting call

# R: g <- isolines_grob(...)
# breaks = 20*(5:10) -> [100, 120, 140, 160, 180, 200]
breaks = np.arange(5, 11) * 20
# gp = gpar(fontsize = 10, lwd = c(1, 2, 1, 1), col = c("grey50", "grey20", "grey50", "grey50"))
# Since isolines_grob creates a graphical object, we represent 'g' as the configuration for the plot.
g = {
    'levels': breaks,
    'lwd': [1, 2, 1, 1],
    'col': ["#808080", "#333333", "#808080", "#808080"], # grey50, grey20
    'fontsize': 10
}

# R: grid.newpage()
plt.figure()

# R: grid.draw(g)
X, Y = np.meshgrid(x, y)
# Matplotlib's contour returns a ContourSet
cs = plt.contour(X, Y, volcano_arr, levels=g['levels'])

# Apply the specific line widths and colors from 'g'
# Matplotlib cycles colors if the list is shorter than levels
for i, collection in enumerate(cs.collections):
    # Cycle through the provided colors and linewidths
    col_idx = i % len(g['col'])
    lwd_idx = i % len(g['lwd'])
    collection.set_edgecolor(g['col'][col_idx])
    collection.set_linewidth(g['lwd'][lwd_idx])

plt.axis('off')
plt.show()