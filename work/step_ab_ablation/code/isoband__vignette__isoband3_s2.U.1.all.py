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

# Ensure volcano is a numpy array for calculations
if hasattr(volcano, 'values'):
    volcano_arr = volcano.values
else:
    volcano_arr = np.array(volcano)

# R: x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
# r2py:entity:ncol
ncol_val = volcano_arr.shape[1]
x = np.arange(ncol_val) / (ncol_val - 1)

# R: y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
# r2py:entity:nrow
nrow_val = volcano_arr.shape[0]
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# R: lines <- isolines(x, y, volcano, 5*(19:38))
# isolines returns a list of coordinates for the contours
levels_lines = 5 * np.arange(19, 39)
X, Y = np.meshgrid(x, y)
cs = plt.contour(X, Y, volcano_arr, levels=levels_lines)

# Construct the 'lines' object as a dictionary mapping level to coordinates
# to match R's isoband output structure
lines = {}
for i, level in enumerate(levels_lines):
    # Matplotlib's contour paths: each collection is a line segment
    path_col = cs.collections[i].get_paths()
    # Combine vertices for each path in the collection
    xs = []
    ys = []
    for path in path_col:
        v = path.vertices
        xs.extend(v[:, 0])
        ys.extend(v[:, 1])
    lines[str(level)] = {'x': xs, 'y': ys}

# R: g <- isolines_grob(lines, breaks = 20*(5:10), ...)
# In this context, 'g' represents the graphical object. We store the parameters.
breaks = 20 * np.arange(5, 11)
g = {
    'lines': lines,
    'breaks': breaks,
    'gp': {
        'fontsize': 10,
        'lwd': [1, 2, 1, 1],
        'col': ["grey50", "grey20", "grey50", "grey50"]
    }
}

# R: grid.newpage()
plt.figure()

# R: grid.draw(g)
# The 'g' object in R draws specific breaks from the 'lines' data
# We use matplotlib to render the specific breaks defined in g
plt.clf()
# Map the colors and linewidths to the breaks
colors = ["grey50", "grey20", "grey50", "grey50"] # R uses cycling if breaks > colors
lwd = [1, 2, 1, 1]

# Re-plot only the levels specified in g['breaks']
cs_final = plt.contour(X, Y, volcano_arr, levels=breaks)
for i, collection in enumerate(cs_final.collections):
    color_idx = i % len(colors)
    lwd_idx = i % len(lwd)
    collection.set_edgecolor(colors[color_idx])
    collection.set_linewidth(lwd[lwd_idx])

plt.axis('off')
plt.show()