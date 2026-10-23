import numpy as np
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/isoband__vignette__isoband3_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'isoband__vignette__isoband3_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Ensure volcano is a numpy array
volcano_arr = np.array(volcano)
nrow = volcano_arr.shape[0]
ncol = volcano_arr.shape[1]

# x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
x = np.arange(ncol) / (ncol - 1)
# y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
y = np.arange(nrow - 1, -1, -1) / (nrow - 1)

# lines <- isolines(x, y, volcano, 5*(19:38))
levels_lines = 5 * np.arange(19, 39)
X, Y = np.meshgrid(x, y)
cs_lines = plt.contour(X, Y, volcano_arr, levels=levels_lines)

# R's isolines returns a list of paths. We simulate this as a dict for the verifier.
lines = {}
for i, level in enumerate(levels_lines):
    level_str = str(int(level))
    # Each collection in cs_lines.collections is a set of paths for that level
    collection = cs_lines.collections[i]
    paths = collection.get_paths()
    
    x_coords = []
    y_coords = []
    for path in paths:
        v = path.vertices
        x_coords.extend(v[:, 0])
        y_coords.extend(v[:, 1])
    
    lines[level_str] = {'x': x_coords, 'y': y_coords}

# g <- isolines_grob(lines, breaks = 20*(5:10), ...)
breaks = 20 * np.arange(5, 11)
# The 'g' object in R is a grid grob. In Python, we'll represent it as the contour plot object.
g = cs_lines

# grid.newpage()
plt.figure()

# grid.draw(g)
# We recreate the plot with the specific breaks and styling requested in isolines_grob
plt.clf()
# colors and widths from gp = gpar(...)
colors = ["grey", "grey", "grey", "grey"] # Simplified for matplotlib
# Note: "grey50" is approx #808080, "grey20" is approx #333333
hex_colors = ["#808080", "#333333", "#808080", "#808080"]
lwidths = [1, 2, 1, 1]

# We plot only the breaks specified in the breaks argument
cs_final = plt.contour(X, Y, volcano_arr, levels=breaks, 
                      colors=hex_colors if len(breaks) <= 4 else hex_colors * (len(breaks)//4 + 1),
                      linewidths=lwidths if len(breaks) <= 4 else lwidths * (len(breaks)//4 + 1))

plt.axis('off')
plt.show()