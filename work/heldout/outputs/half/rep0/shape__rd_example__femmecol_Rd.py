# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/shape__rd_example__femmecol_Rd.py'
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
    rgb_col = np.array(inputcol)
    
    if rgb_col.ndim == 1 or (rgb_col.ndim == 2 and rgb_col.shape[0] <= 1):
        return [inputcol] * (numcol if numcol is not None else 1)

    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    
    if x_to is None:
        if numcol is None:
            numcol = 100
        x_to = np.linspace(0, 1, numcol)
    elif numcol is None:
        numcol = len(x_to)

    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
        
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    
    # R source logic: outcol[outcol < 0] <- 0; outcol[outcol > 255] <- 0
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    # R's rgb() returns lowercase hex codes
    colors = []
    for row in outcol:
        colors.append('#{:02x}{:02x}{:02x}'.format(row[0], row[1], row[2]).lower())
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
    # R: x.from <- c(0, seq(0.125, 1, by = 0.25), 1)
    # seq(0.125, 1, by=0.25) -> 0.125, 0.375, 0.625, 0.875
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
colors_list = femmecol(100)
cmap_femme = LinearSegmentedColormap.from_list("femmecol", colors_list)

plt.figure()
# volcano is often provided as a list or array; ensure it's a numpy array
volcano_np = np.array(volcano)
plt.contourf(volcano_np, cmap=cmap_femme)
plt.gca().set_aspect('equal')
plt.title("femmecol")

# femmecol(10)
# r2py:entity:femmecol
res_10 = femmecol(10)
print(res_10)

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_data = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(img_data, aspect='auto', cmap=cmap_femme)
plt.title("femmecol")
plt.axis('off') # image() in R by default doesn't show axes like imshow does