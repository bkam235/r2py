# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/shape__rd_example__femmecol_Rd.py'
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
    if len(inputcol) <= 1:
        return [inputcol[0]] * numcol if isinstance(inputcol, (list, np.ndarray)) else [inputcol] * numcol
    
    if isinstance(inputcol, np.ndarray):
        rgb_col = inputcol
    else:
        # Logic for col2rgb approximation
        rgb_col = np.array(inputcol)

    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if numcol is None:
        # In R: numcol = length(x.to). If x.to is None, it's handled below.
        # We'll set a default or derive it.
        numcol = len(rgb_col)
        
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)

    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")

    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 255
    
    # R's rgb() returns uppercase hex strings
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
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
volcano_np = np.array(volcano)
femme_colors_100 = femmecol(100)
cmap_femme = LinearSegmentedColormap.from_list("femmecol", femme_colors_100)

plt.figure()
plt.contourf(volcano_np, cmap=cmap_femme)
plt.gca().set_aspect(1)
plt.title("femmecol")
# plt.show() # Handled by verifier

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_data = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(img_data, aspect='auto', cmap=cmap_femme)
plt.title("femmecol")
# plt.show() # Handled by verifier