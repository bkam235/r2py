# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.colors import ListedColormap

# Ensure volcano is a numpy array
if 'volcano' in globals():
    volcano = np.array(volcano)

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # Handle simple case
    if len(inputcol) <= 1:
        return [inputcol[0]] * (numcol if numcol is not None else 1)
    
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
    
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        f = interp1d(x_from, rgb_col[:, i], kind='linear')
        outcol[:, i] = np.round(f(x_to))
    
    # R source: outcol[outcol > 255] <- 0
    mask_too_high = outcol > 255
    outcol[mask_too_high] = 0
    outcol[outcol < 0] = 0
    
    # Convert to uppercase hex to match R's rgb() output
    colors = ['#%02X%02X%02X' % tuple(row.astype(int)) for row in outcol]
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
    # R: c(0, seq(0.125, 1, by = 0.25), 1) is [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
levels = 50
cmap_femme_contour = ListedColormap(femmecol(levels))
# R's filled.contour plots the matrix such that [1,1] is bottom-left. 
# Matplotlib's contourf treats the matrix indices as (y, x). 
# We transpose or flip to match R's view.
plt.contourf(volcano, levels=levels, cmap=cmap_femme_contour, origin='lower')
plt.title("femmecol")
plt.gca().set_aspect('equal')
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_data = np.arange(1, 101).reshape(1, 100)
plt.figure()
cmap_femme_image = ListedColormap(femmecol(100))
# R image() plots [1,1] at bottom-left.
plt.imshow(img_data, aspect='auto', cmap=cmap_femme_image, origin='lower', extent=[0, 100, 0, 1])
plt.title("femmecol")
plt.axis('off')
plt.show()