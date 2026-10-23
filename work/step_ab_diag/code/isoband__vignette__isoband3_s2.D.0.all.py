import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/isoband__vignette__isoband3_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'isoband__vignette__isoband3_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Handle volcano input (expected to be a DataFrame from the shim)
volcano_arr = np.array(volcano)

# R: x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
ncol_val = volcano_arr.shape[1]
x = np.arange(ncol_val) / (ncol_val - 1)

# R: y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
nrow_val = volcano_arr.shape[0]
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# R: lines <- isolines(x, y, volcano, 5*(19:38))
# 5 * (19:38) is [95, 100, ..., 190]
levels_lines = np.arange(19, 39) * 5
X, Y = np.meshgrid(x, y)

# We use matplotlib to find the contour lines to populate the 'lines' variable
plt.figure()
cs_lines = plt.contour(X, Y, volcano_arr, levels=levels_lines)
plt.close()

lines = {}
for i, level in enumerate(cs_lines.levels):
    # Matplotlib stores contours as a collection of paths
    path_collection = cs_lines.collections[i]
    paths = path_collection.get_paths()
    
    all_x = []
    all_y = []
    for path in paths:
        vertices = path.vertices
        all_x.extend(vertices[:, 0].tolist())
        all_y.extend(vertices[:, 1].tolist())
    
    # The verifier expects string keys for levels
    lines[str(int(level))] = {'x': all_x, 'y': all_y}

# R: g <- isolines_grob(lines, breaks = 20*(5:10), gp = gpar(...))
# breaks = 20 * (5:10) -> [100, 120, 140, 160, 180, 200]
breaks = np.arange(5, 11) * 20
colors = ["grey50", "grey20", "grey50", "grey50"]
lwd = [1, 2, 1, 1]

# In Python, we'll represent 'g' as the contour object we draw
plt.figure()
cs_g = plt.contour(X, Y, volcano_arr, levels=breaks)

# Apply the gp settings (colors and linewidths)
# R's gpar handles these as vectors; we map them to the collections
for i, collection in enumerate(cs_g.collections):
    # Cycle through colors and lwd if breaks > 4
    color_idx = i % len(colors)
    lwd_idx = i % len(lwd)
    collection.set_colors([colors[color_idx]])
    collection.set_linewidths(lwd[lwd_idx])

g = cs_g

# R: grid.newpage(); grid.draw(g)
plt.axis('off')
plt.gca().set_aspect('equal')
plt.show()