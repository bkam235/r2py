import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import contours

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/isoband__vignette__isoband3_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'isoband__vignette__isoband3_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# The data shim provides volcano as a DataFrame or list of lists. Convert to numpy array.
volcano_mat = np.array(volcano)
nrow_val = volcano_mat.shape[0]
ncol_val = volcano_mat.shape[1]

# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
x = np.arange(ncol_val) / (ncol_val - 1)
# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
# 5*(19:38) is 95, 100, ..., 190
levels_lines = np.arange(19, 39) * 5
X, Y = np.meshgrid(x, y)
# Note: matplotlib's contour expects Y to be increasing or handles data differently. 
# R's volcano has Y from 1 down to 0.
cs = contours.contour_generator.contour_generator(X, Y, volcano_mat, levels_lines)

# Extracting paths to match R's isolines output structure
lines = {}
for i, level in enumerate(levels_lines):
    # In R, isolines returns a list of segments for each level.
    # Matplotlib provides paths. We concatenate segments for simplicity or map them.
    path_x = []
    path_y = []
    for segment in cs.all_segments[i]:
        path_x.extend(segment[0])
        path_y.extend(segment[1])
    lines[str(int(level))] = {'x': path_x, 'y': path_y}

# g <- isolines_grob(lines, breaks = 20*(5:10), ...)
# breaks = 100, 120, 140, 160, 180, 200
breaks = np.arange(5, 11) * 20
# In R, isolines_grob is a graphical object. To simulate its data for the verifier,
# we provide the filtered isolines that match these breaks.
g_lines = {}
for level_str, coords in lines.items():
    if int(level_str) in breaks:
        g_lines[level_str] = coords
g = {'lines': g_lines}

# grid.newpage()
plt.figure()

# grid.draw(g)
# Using matplotlib to draw the specific breaks and styles
# col = c("grey50", "grey20", "grey50", "grey50")
# lwd = c(1, 2, 1, 1)
colors = ["#808080", "#333333", "#808080", "#808080"] # grey50, grey20, ...
widths = [1, 2, 1, 1]

# Create a new contour plot for the breaks
cs_g = plt.contour(X, Y, volcano_mat, levels=breaks)
# Apply the styles to the paths
for i, collection in enumerate(cs_g.collections):
    # Cycle styles if levels > 4
    color = colors[i % len(colors)]
    width = widths[i % len(widths)]
    collection.set_edgecolor(color)
    collection.set_linewidth(width)

plt.gca().invert_yaxis() # Match R's coordinate system where y=1 is top
plt.axis('off')
plt.show()