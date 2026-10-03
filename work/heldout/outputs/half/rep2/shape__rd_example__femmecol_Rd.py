# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/shape__rd_example__femmecol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__femmecol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# r2py:entity:femmecol
def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    if x_from is None:
        # If inputcol is a matrix (list of RGBs), use its length
        rgb_col = np.array(inputcol)
        x_from = np.linspace(0, 1, len(rgb_col))
    
    if numcol is None:
        numcol = len(x_from)
        
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x_to > ranges x_from")
        
    rgb_col = np.array(inputcol)
    outcol = np.zeros((numcol, 3))
    
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
        
    outcol = np.round(outcol).astype(int)
    outcol = np.clip(outcol, 0, 255)
    
    # Convert to hex strings to mimic R's rgb() return
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
    x_from = [0, 0.125, 0.375, 0.625, 0.875, 1.0]
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# Load volcano dataset (approximate representation of R's volcano)
# Since volcano is a built-in R dataset, we load it if available or create it
try:
    from statsmodels.datasets import get_rdataset
    volcano = get_rdataset("volcano").data.values.reshape(87, 87)
except:
    # Fallback: generic volcano-like surface if dataset not available
    x = np.linspace(-5, 5, 87)
    y = np.linspace(-5, 5, 87)
    X, Y = np.meshgrid(x, y)
    volcano = np.exp(-(X**2 + Y**2)/10) * 200 + np.random.randn(87, 87) * 10

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
cmap_femmecol = ListedColormap(femmecol(256))
plt.contourf(volcano, cmap=cmap_femmecol)
plt.gca().set_aspect('equal')
plt.title("femmecol")
plt.show()

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
img_data = np.arange(1, 101).reshape(1, 100)
plt.figure()
plt.imshow(img_data, aspect='auto', cmap=ListedColormap(femmecol(100)))
plt.title("femmecol")
plt.colorbar()
plt.show()