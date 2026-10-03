# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/full/rep0/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# r2py:entity:image
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if numcol is None:
        numcol = len(x_from)
        
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
        
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
        
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    # Convert RGB to hex colors
    colors = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in outcol]
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
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Data: volcano is a built-in R dataset
# Loading a representation of volcano (roughly 87x87)
from statsmodels.datasets import get_rdataset

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
levels = np.linspace(np.min(volcano), np.max(volcano), 101)
palette_levels = femmecol(100)
cmap_femmecol = ListedColormap(palette_levels)
plt.contourf(volcano, levels=levels, cmap=cmap_femmecol)
plt.gca().set_aspect(1)
plt.title("femmecol")
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
d = np.arange(1, 101).reshape(1, 100)
palette_100 = femmecol(100)
cmap_custom = ListedColormap(palette_100)

plt.figure()
plt.imshow(d, aspect='auto', cmap=cmap_custom)
plt.title("femmecol")
plt.axis('off')
plt.show()