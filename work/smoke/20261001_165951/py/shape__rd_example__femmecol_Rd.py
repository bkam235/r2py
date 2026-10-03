# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/shape__rd_example__femmecol_Rd.py'
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
    # R's length(inputcol) for a matrix is total elements. 
    # But here inputcol is usually the rgb.col matrix.
    if np.size(inputcol) <= 1:
        return np.tile(inputcol, numcol)

    # Handle numeric vs color string input
    if isinstance(inputcol, np.ndarray) or isinstance(inputcol, list):
        rgb_col = np.array(inputcol)
    else:
        # This part approximates col2rgb
        rgb_col = np.array([plt.colors.to_rgb(c) for c in inputcol]) * 255

    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    if np.min(x_to) < np.min(x_from) or np.max(x_to) > np.max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
    
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        # approx(x, y, xout) in R is linear interpolation
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    
    # R source: outcol[outcol < 0] <- 0; outcol[outcol > 255] <- 0
    # Note: the R source provided explicitly says outcol[outcol > 255] <- 0
    outcol[outcol < 0] = 0
    outcol[outcol > 255] = 0
    
    # Convert to hex strings like R's rgb()
    colors = []
    for row in outcol:
        colors.append('#{:02x}{:02x}{:02x}'.format(int(row[0]), int(row[1]), int(row[2])))
    return np.array(colors)

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
    # seq(0.125, 1, by = 0.25) is [0.125, 0.375, 0.625, 0.875, 1.125] wait.
    # In R: seq(0.125, 1, by = 0.25) -> 0.125, 0.375, 0.625, 0.875
    # Then c(0, ..., 1) -> 0, 0.125, 0.375, 0.625, 0.875, 1
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
# r2py:entity:filled.contour
plt.figure()
# Convert hex colors to a cmap
colors_list = femmecol(256)
cmap_volcano = ListedColormap(colors_list)
plt.contourf(volcano, cmap=cmap_volcano)
plt.gca().set_aspect('equal')
plt.title("femmecol")

# femmecol(10)
# r2py:entity:femmecol
print(femmecol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = femmecol(100), main = "femmecol")
# r2py:entity:image
plt.figure()
img_data = np.arange(1, 101).reshape(1, 100)
colors_image = femmecol(100)
cmap_image = ListedColormap(colors_image)
# R's image() defaults to different axis orientations and mapping
plt.imshow(img_data, cmap=cmap_image, aspect='auto')
plt.title("femmecol")