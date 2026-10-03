# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    if inputcol.shape[0] <= 1:
        res = np.tile(inputcol, (numcol, 1))
        return ["#%02x%02x%02x" % tuple(row.astype(int)) for row in res]
    
    if x_from is None:
        x_from = np.linspace(0, 1, inputcol.shape[0])
    
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, inputcol[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 255
    
    return ["#%02x%02x%02x" % tuple(row) for row in outcol]

def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Ensure volcano is a numpy array
volcano_arr = np.array(volcano)

# r2py:entity:filled.contour
# Equivalent to filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
plt.figure()
# Convert hex colors to float for LinearSegmentedColormap
hex_cols = femmecol(256)
float_cols = [[int(c[1:3], 16)/255, int(c[3:5], 16)/255, int(c[5:7], 16)/255] for c in hex_cols]
cmap_femme = LinearSegmentedColormap.from_list("femmecol", float_cols)
plt.contourf(volcano_arr, cmap=cmap_femme)
plt.gca().set_aspect(1)
plt.title("femmecol")
plt.colorbar()
plt.show()

# r2py:entity:femmecol
# femmecol(10)
print(femmecol(10))

# r2py:entity:image
# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
data_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(data_matrix, aspect='auto', cmap=cmap_femme)
plt.title("femmecol")
plt.axis('off')
plt.show()