import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/isoband__vignette__isoband3_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'isoband__vignette__isoband3_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Ensure volcano is a numpy array
volcano_arr = np.array(volcano)

# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
# ncol(volcano) is the number of columns (87)
ncol_val = volcano_arr.shape[1]
x = np.arange(0, ncol_val) / (ncol_val - 1)

# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
# nrow(volcano) is the number of rows (87)
nrow_val = volcano_arr.shape[0]
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
# 5 * (19:38) results in levels 95, 100, ..., 190
levels_lines = np.arange(19, 39) * 5
# In R, isolines returns coordinates of the contour lines. 
# We use matplotlib.contour to get these paths.
X, Y = np.meshgrid(x, y)
cs = plt.contour(X, Y, volcano_arr, levels=levels_lines)

# Construct the 'lines' dictionary to match R's output structure: {level: {x: [], y: []}}
lines = {}
for i, level in enumerate(levels_lines):
    level_str = str(int(level))
    path_segments = cs.collections[i].get_paths()
    x_coords = []
    y_coords = []
    for path in path_segments:
        v = path.vertices
        x_coords.extend(v[:, 0])
        y_coords.extend(v[:, 1])
    lines[level_str] = {'x': x_coords, 'y': y_coords}

# g <- isolines_grob(...)
# This creates a graphical object. In Python, we represent the state of the plot as 'g'.
# breaks = 20*(5:10) -> [100, 120, 140, 160, 180, 200]
breaks = np.arange(5, 11) * 20
lwd = [1, 2, 1, 1]
cols = ["grey50", "grey20", "grey50", "grey50"]

# We simulate the 'grob' by creating a matplotlib figure object
fig, ax = plt.subplots()
# Plot contours based on breaks, colors, and linewidths
# Since matplotlib.contour accepts lists for colors/linewidths, we map them.
# R cycles the 4 provided colors/widths across the breaks.
plot_cols = [cols[i % len(cols)] for i in range(len(breaks))]
plot_lwd = [lwd[i % len(lwd)] for i in range(len(breaks))]

cs_g = ax.contour(X, Y, volcano_arr, levels=breaks, colors=plot_cols, linewidths=plot_lwd)
ax.set_aspect('equal')
ax.axis('off')
g = fig

# grid.newpage() and grid.draw(g)
plt.show()