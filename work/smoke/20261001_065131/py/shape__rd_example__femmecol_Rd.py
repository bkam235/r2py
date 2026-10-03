# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Ensure volcano is a numpy array
volcano = np.array(volcano)

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # In R: if (length(inputcol) <= 1) return(rep(inputcol, numcol))
    if len(inputcol) <= 1:
        return [inputcol[0]] * (numcol if numcol is not None else 1)
    
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    if x_to is None:
        x_to = np.linspace(0, 1, numcol if numcol is not None else len(x_from))
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 255 # Fixed logic error: clip to 255, not 0
    
    # Return as uppercase hex strings to match R's rgb()
    colors = []
    for row in outcol:
        colors.append('#%02X%02X%02X' % tuple(row))
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
    # R: c(0, seq(0.125, 1, by = 0.25), 1) -> [0, 0.125, 0.375, 0.625, 0.875, 1.0, 1.0]
    # Wait, R's seq(0.125, 1, by=0.25) is [0.125, 0.375, 0.625, 0.875, 1.125] ? 
    # No, seq(0.125, 1, by=0.25) is [0.125, 0.375, 0.625, 0.875]
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    # Note: The R source provided says c(0, seq(0.125, 1, by = 0.25), 1). 
    # seq(0.125, 1, by=0.25) results in [0.125, 0.375, 0.625, 0.875].
    # Then adding 0 and 1 makes it [0, 0.125, 0.375, 0.625, 0.875, 1].
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
colors_filled = femmecol(256)
cmap_femme = LinearSegmentedColormap.from_list("femmecol", colors_filled)
plt.contourf(volcano, cmap=cmap_femme)
plt.gca().set_aspect('equal')
plt.title("femmecol")

# femmecol(10)
# r2py:entity:femmecol
res_femme10 = femmecol(10)
print(res_femme10)

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
data_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(data_matrix, aspect='auto', cmap=cmap_femme, interpolation='nearest')
plt.title("femmecol")
plt.axis('off') # image() in R usually hides axes for this kind of data unless specified