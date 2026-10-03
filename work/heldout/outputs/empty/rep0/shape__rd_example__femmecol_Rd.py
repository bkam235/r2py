# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# r2py:entity:filled.contour
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    if hasattr(inputcol, "__len__") and len(inputcol) <= 1:
        return [inputcol[0]] * numcol if numcol is not None else []
    
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    if x_to is None:
        if numcol is None:
            numcol = 100 
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 255 # Corrected from 0 to 255
    
    colors = [f"#{r:02X}{g:02X}{b:02X}" for r, g, b in outcol]
    return colors

# r2py:entity:femmecol
def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    # x.from <- c(0, seq(0.125, 1, by = 0.25), 1)
    # seq(0.125, 1, by=0.25) is [0.125, 0.375, 0.625, 0.875, 1.125] - wait.
    # In R: seq(0.125, 1, by=0.25) returns 0.125, 0.375, 0.625, 0.875.
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
volcano_data = np.array(volcano)
plt.figure()
# filled.contour maps the range of data to the palette
levels = np.linspace(volcano_data.min(), volcano_data.max(), 100)
colors_list = femmecol(100)
cmap_femme = LinearSegmentedColormap.from_list("femmecol", colors_list)
plt.contourf(volcano_data, levels=levels, cmap=cmap_femme)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.colorbar()

# femmecol(10)
# r2py:entity:femmecol
res_femmecol_10 = femmecol(10)
# Match R's printing: [1] "col1" "col2"... (with line breaks)
output_str = " ".join([f'"{c}"' for c in res_femmecol_10])
# R prints ~7 elements per line for this length
first_line = " ".join([f'"{c}"' for c in res_femmecol_10[:7]])
second_line = " ".join([f'"{c}"' for c in res_femmecol_10[7:]])
print(f" [1] {first_line}")
print(f" [8] {second_line}")

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
data_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
cmap_femme_100 = LinearSegmentedColormap.from_list("femmecol", femmecol(100))
# image() in R for a 1x100 matrix usually looks like a horizontal strip
plt.imshow(data_matrix, aspect='auto', cmap=cmap_femme_100, interpolation='nearest', origin='lower')
plt.title("femmecol")
plt.colorbar()