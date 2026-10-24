# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

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
import pandas as pd

# Ensure volcano is a numpy array
volcano_np = np.array(volcano)

# R: x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
ncol_val = volcano_np.shape[1]
ncol = ncol_val
ncol_1 = ncol_val
x = np.arange(ncol_val) / (ncol_val - 1)

# R: y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
nrow_val = volcano_np.shape[0]
nrow = nrow_val
nrow_1 = nrow_val
y = np.arange(nrow_val - 1, -1, -1) / (nrow_val - 1)

# R: lines <- isolines(x, y, volcano, 5*(19:38))
levels_lines = np.arange(19, 39) * 5
X, Y = np.meshgrid(x, y)

plt.figure()
cs = plt.contour(X, Y, volcano_np, levels=levels_lines)

# r2py:entity:lines
lines = {}
for i, level in enumerate(levels_lines):
    segs = cs.allsegs[i]
    all_x = []
    all_y = []
    all_id = []
    current_id = 1
    for seg in segs:
        if len(seg) > 0:
            # R's isoband output is essentially a sequence of points
            # where each segment is identified by an ID.
            for pt in seg:
                all_x.append(pt[0])
                all_y.append(pt[1])
                all_id.append(current_id)
            current_id += 1
    lines[str(int(level))] = {'x': all_x, 'y': all_y, 'id': all_id}
plt.close()

# R: g <- isolines_grob(lines, breaks = 20*(5:10), gp = gpar(...))
breaks_g_vals = np.arange(5, 11) * 20
breaks_g_str = [str(int(b)) for b in breaks_g_vals]
gp_params = {
    'fontsize': 10,
    'lwd': [1, 2, 1, 1],
    'col': ["grey50", "grey20", "grey50", "grey50"]
}

# r2py:entity:g
# simulate gTree structure accurately
g = {
    'lines': lines,
    'breaks': breaks_g_str,
    'labels': breaks_g_str,
    'labels_data': pd.DataFrame({
        'index': [i + 1 for i in range(len(breaks_g_str))],
        'break_index': [i + 1 for i in range(len(breaks_g_str))],
        'break_id': breaks_g_str,
        'label': breaks_g_str
    }),
    'gp': gp_params,
    'gp_combined': gp_params,
    'margin': [1, 1, 1, 1],
    'label_col': None,
    'label_alpha': None,
    'label_placer': 'label_placer_minmax',
    'units': 'npc',
    'cl': 'isolines_grob',
    'name': 'isolines_grob',
    'children': [],
    'childrenOrder': [],
    'vp': {}
}

# R: grid.newpage()
# r2py:entity:grid.newpage
plt.figure()

# R: grid.draw(g)
# r2py:entity:grid.draw
cs_final = plt.contour(X, Y, volcano_np, levels=breaks_g_vals)

if hasattr(cs_final, 'collections'):
    for i, collection in enumerate(cs_final.collections):
        col = gp_params['col'][i % len(gp_params['col'])]
        lw = gp_params['lwd'][i % len(gp_params['lwd'])]
        collection.set_edgecolor(col)
        collection.set_linewidth(lw)

plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()