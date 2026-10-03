# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.colors import ListedColormap

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # inputcol is expected to be a numpy array of shape (N, 3)
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    
    if numcol is None:
        numcol = len(x_from)
        
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
        
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        f = interp1d(x_from, rgb_col[:, i], bounds_error=False, fill_value="extrapolate")
        outcol[:, i] = np.round(f(x_to))
        
    outcol = np.clip(outcol, 0, 255).astype(int)
    
    # R's rgb() produces uppercase hex codes: #RRGGBB
    colors = ['#%02X%02X%02X' % tuple(row) for row in outcol]
    return colors

def femmecol(n=100):
    # R: matrix(nrow = 6, ncol = 3, byrow = TRUE, data = c(0, 0, 143, 0, 0, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 128, 0, 0))
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    # R: x.from <- c(0, seq(0.125, 1, by = 0.25), 1) -> c(0, 0.125, 0.375, 0.625, 0.875, 1)
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Convert volcano from shim (list of lists) to numpy array
volcano_arr = np.array(volcano)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
# filled.contour in R defaults to 20 levels, palette is applied to levels-1
levels = 20
cols = femmecol(levels - 1)
plt.contourf(volcano_arr, levels=levels, colors=cols)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
data_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
cmap = ListedColormap(femmecol(100))
# R's image() is similar to imshow, but usually needs 'extent' for correct axes. 
# Since it's a 1x100 matrix, we use aspect='auto'
plt.imshow(data_matrix, aspect='auto', cmap=cmap)
plt.title("femmecol")
plt.axis('off') # R's image() often lacks axes by default or handles them differently
plt.show()