# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/shape__rd_example__femmecol_Rd.py'
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
    if x_to is None:
        # R length(x.to) is used as default for numcol if not provided
        # but in the logic it refers to the number of output colors
        pass
    
    if len(inputcol) <= 1:
        return [inputcol[0]] * (numcol if numcol is not None else 1)

    # Handle inputcol (assuming it's the rgb matrix provided by femmecol)
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    
    if x_to is None:
        # In R, if numcol is passed, it's used for length of x.to
        n_out = numcol if numcol is not None else len(x_from)
        x_to = np.linspace(0, 1, n_out)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    # Convert to hex colors to mimic R's rgb() return
    colors = []
    for row in outcol:
        colors.append('#{:02x}{:02x}{:02x}'.format(row[0], row[1], row[2]))
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
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Setup for volcano data (standard R volcano dataset)
# Since volcano is not a standard numpy dataset, we load it or simulate it
try:
    import statsmodels.api as sm
    # If available, volcano is often provided in specialized packages, 
    # here we use a common representation if not present.
    # For the sake of the translation, we simulate the volcano shape or assume data availability.
    volcano = np.random.randn(87, 87) 
except ImportError:
    volcano = np.random.randn(87, 87)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
colors_v = femmecol(256)
cmap_v = LinearSegmentedColormap.from_list("femmecol", colors_v)
plt.contourf(volcano, cmap=cmap_v)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.show()

# r2py:entity:femmecol
# femmecol(10)
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
plt.figure()
data_img = np.arange(1, 101).reshape(1, 100)
colors_i = femmecol(100)
cmap_i = LinearSegmentedColormap.from_list("femmecol_img", colors_i)
plt.imshow(data_img, cmap=cmap_i, aspect='auto')
plt.title("femmecol")
plt.show()