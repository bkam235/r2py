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

# r2py:entity:import_isoband
# r2py:entity:import_grid

# Ensure volcano is a numpy array for calculation
volcano_mat = volcano.values if hasattr(volcano, 'values') else np.array(volcano)

# r2py:entity:ncol
# r2py:entity:ncol_1
ncol_val = volcano_mat.shape[1]
# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
# r2py:entity:x
x = np.arange(ncol_val) / (ncol_val - 1)

# r2py:entity:nrow
# r2py:entity:nrow_1
nrow_val = volcano_mat.shape[0]
# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
# r2py:entity:y
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
levels_val = 5 * np.arange(19, 39)
X, Y = np.meshgrid(x, y)

# Use matplotlib to compute the isolines without creating a visible figure
plt.ioff() 
fig_temp = plt.figure()
cs = plt.contour(X, Y, volcano_mat, levels=levels_val)
plt.close(fig_temp)
plt.ion()

# r2py:entity:lines
lines = {}
segs = cs.allsegs
for i, level in enumerate(levels_val):
    level_paths = segs[i]
    lx, ly = [], []
    for path in level_paths:
        if path.size > 0:
            lx.extend(path[:, 0].tolist())
            ly.extend(path[:, 1].tolist())
    lines[str(int(level))] = {'x': lx, 'y': ly}

# g <- isolines_grob(...)
# r2py:entity:g
breaks_val = 20 * np.arange(5, 11)
g = {
    'lines': lines,
    'breaks': [str(int(b)) for b in breaks_val],
    'gp': {'fontsize': 10, 'lwd': [1, 2, 1, 1], 'col': ["#808080", "#333333", "#808080", "#808080"]},
    'gp_combined': {'fontsize': 10, 'lwd': [1, 2, 1, 1], 'col': ["#808080", "#333333", "#808080", "#808080"]},
    'units': 'npc',
    'children': [],
    'childrenOrder': [],
    'label_alpha': None,
    'label_col': None,
    'label_placer': None,
    'labels': [],
    'labels_data': None,
    'margin': None,
    'name': None,
    'vp': None
}

# r2py:entity:grid.newpage
plt.figure(figsize=(5, 5))

# r2py:entity:grid.draw
cols = ["#808080", "#333333", "#808080", "#808080"]
lwds = [1, 2, 1, 1]

final_colors = (cols * (len(breaks_val) // len(cols) + 1))[:len(breaks_val)]
final_lwds = (lwds * (len(breaks_val) // len(lwds) + 1))[:len(breaks_val)]

plt.contour(X, Y, volcano_mat, levels=breaks_val, 
            colors=final_colors, 
            linewidths=final_lwds)
plt.axis('off')
plt.show()