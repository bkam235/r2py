# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from numpy import interp

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # Handle inputcol as rgb matrix
    if isinstance(inputcol, np.ndarray):
        rgb_col = inputcol
    else:
        rgb_col = np.array(inputcol)
    
    if rgb_col.size <= 1:
        return [inputcol] * numcol

    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")

    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.round(interp(x_to, x_from, rgb_col[:, i]))
    
    # The R source says: outcol[outcol < 0] <- 0; outcol[outcol > 255] <- 0
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    colors = []
    for row in outcol:
        # Convert to uppercase hex to match R output: #RRGGBB
        colors.append('#%02X%02X%02X' % tuple(map(int, row)))
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
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Ensure volcano is treated as a numpy array (coming from shim)
volcano = np.array(volcano)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
# R's filled.contour uses the function 'femmecol' as the 'color' argument
# We simulate this by calculating the number of levels
z_min, z_max = volcano.min(), volcano.max()
levels = np.linspace(z_min, z_max, 101)
colors = femmecol(len(levels) - 1)
plt.contourf(volcano, levels=levels, colors=colors)
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
plt.imshow(data_matrix, aspect='auto', cmap=plt.matplotlib.colors.ListedColormap(femmecol(100)))
plt.title("femmecol")
plt.axis('off') # R image() by default doesn't show typical axes like imshow
plt.show()