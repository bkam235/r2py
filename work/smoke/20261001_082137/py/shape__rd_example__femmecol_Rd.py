# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/shape__rd_example__femmecol_Rd.py'
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
    if len(inputcol) <= 1:
        return [inputcol[0]] * numcol
    
    rgb_col = np.array(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
    
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    # Convert to hex colors for compatibility with matplotlib
    colors = []
    for row in outcol:
        colors.append('#%02x%02x%02x' % tuple(row))
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
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Setup data for volcano (built-in R dataset simulation)
# In a real scenario, one would load the volcano.csv
try:
    import statsmodels.api as sm
    # volcano is often unavailable in python, simulating the structure
    volcano = np.random.randint(100, 200, (87, 87)) 
except ImportError:
    volcano = np.random.randint(100, 200, (87, 87))

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
cmap_femme = LinearSegmentedColormap.from_list("femmecol", femmecol(100))
plt.contourf(volcano, cmap=cmap_femme)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.colorbar()
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
plt.figure()
data_matrix = np.arange(1, 101).reshape(1, 100)
cmap_femme_image = LinearSegmentedColormap.from_list("femmecol", femmecol(100))
plt.imshow(data_matrix, aspect='auto', cmap=cmap_femme_image)
plt.title("femmecol")
plt.show()