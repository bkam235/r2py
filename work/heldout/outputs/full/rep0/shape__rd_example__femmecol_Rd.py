# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# r2py:entity:filled.contour
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    rgb_col = np.array(inputcol)
    if rgb_col.ndim == 1:
        return [rgb_col] * (numcol if numcol is not None else 1)
    
    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if x_to is None:
        # numcol is expected to be provided if x_to is not
        if numcol is None:
            numcol = len(x_from)
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        f = interp1d(x_from, rgb_col[:, i], kind='linear')
        outcol[:, i] = np.round(f(x_to))
    
    outcol = np.clip(outcol, 0, 255).astype(int)
    # R's rgb() returns hex by default in this context
    return ["#%02x%02x%02x" % tuple(row) for row in outcol]

# r2py:entity:femmecol
def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# 1. filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# volcano is provided by shim as a list of lists (matrix)
# r2py:entity:filled.contour
volcano_arr = np.array(volcano)
plt.figure(figsize=(6, 6))
# We create a custom colormap from the femmecol palette
from matplotlib.colors import ListedColormap
cmap_femmecol = ListedColormap(femmecol(256))
plt.contourf(volcano_arr, cmap=cmap_femmecol)
plt.title("femmecol")
plt.gca().set_aspect('equal')
plt.show()

# 2. femmecol(10)
# r2py:entity:femmecol
res_femmecol_10 = femmecol(10)
print(res_femmecol_10)

# 3. image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
d = np.arange(1, 101).reshape(1, 100)
plt.figure(figsize=(10, 2))
cmap_femmecol_100 = ListedColormap(femmecol(100))
plt.imshow(d, aspect='auto', cmap=cmap_femmecol_100)
plt.title("femmecol")
plt.axis('off')
plt.show()