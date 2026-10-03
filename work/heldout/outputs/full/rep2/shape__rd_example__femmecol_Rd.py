# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
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
        f = interp1d(x_from, rgb_col[:, i], kind='linear')
        outcol[:, i] = np.round(f(x_to))
        
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    hex_cols = []
    for row in outcol:
        hex_cols.append('#{:02x}{:02x}{:02x}'.format(int(row[0]), int(row[1]), int(row[2])))
    
    return np.array(hex_cols)

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

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
colors_list = femmecol(256)
cmap = plt.matplotlib.colors.ListedColormap(colors_list)
plt.contourf(volcano, cmap=cmap)
plt.gca().set_aspect('equal')
plt.title("femmecol")

# femmecol(10)
# r2py:entity:femmecol
res_10 = femmecol(10)
# Formatting print to better match R's printed array layout
print(' ', end='')
for i, val in enumerate(res_10):
    if i == 7:
        print('\n', end='')
    print(f'"{val}"', end=' ')
print()

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(img_matrix, aspect='auto', cmap=plt.matplotlib.colors.ListedColormap(femmecol(100)), interpolation='nearest')
plt.title("femmecol")
plt.axis('off') # R's image() often suppresses axis labels in these simple examples