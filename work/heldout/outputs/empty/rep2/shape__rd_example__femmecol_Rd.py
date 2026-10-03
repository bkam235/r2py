# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/shape__rd_example__femmecol_Rd.py'
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
    if isinstance(inputcol, np.ndarray) and inputcol.ndim == 2:
        rgb_col = inputcol
    else:
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
    outcol[outcol > 255] = 255
    
    colors = ['#%02x%02x%02x' % tuple(row) for row in outcol]
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
    # R: c(0, seq(0.125, 1, by = 0.25), 1) -> 0, 0.125, 0.375, 0.625, 0.875, 1.0
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
volcano_data = np.array(volcano)
colors_256 = femmecol(256)
cmap_femme = LinearSegmentedColormap.from_list("femmecol", colors_256)
plt.figure()
plt.contourf(volcano_data, cmap=cmap_femme)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_data = np.arange(1, 101).reshape(1, 100)
colors_100 = femmecol(100)
cmap_femme_100 = LinearSegmentedColormap.from_list("femmecol100", colors_100)
plt.figure()
plt.imshow(img_data, aspect='auto', cmap=cmap_femme_100)
plt.title("femmecol")
plt.axis('off') # image() in R usually doesn't show axes by default like imshow does
plt.show()