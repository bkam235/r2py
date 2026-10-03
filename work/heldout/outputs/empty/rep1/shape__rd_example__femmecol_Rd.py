# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# r2py:entity:filled.contour
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol = np.clip(outcol, 0, 255)
    
    # Use uppercase hex for R compatibility
    colors = ['#{:02X}{:02X}{:02X}'.format(row[0], row[1], row[2]) for row in outcol]
    return colors

def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour equivalent
plt.figure()
cmap_filled = ListedColormap(femmecol(100))
plt.contourf(volcano, cmap=cmap_filled)
plt.gca().set_aspect('equal')
plt.title("femmecol")

# r2py:entity:femmecol
# femmecol(10)
print(femmecol(10))

# r2py:entity:image
# image equivalent
data_mat = np.arange(1, 101).reshape(1, 100)
plt.figure()
cmap_image = ListedColormap(femmecol(100))
plt.imshow(data_mat, aspect='auto', cmap=cmap_image)
plt.title("femmecol")