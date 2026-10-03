# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 17

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Since gtable/grid are low-level layout engines for R graphics 
# and Python's plotnine/matplotlib handle layouts differently, 
# we approximate the visual primitives using matplotlib.

# Define approximations for the grobs
# r2py:entity:a
def rectGrob():
    return patches.Rectangle((0, 0), 1, 1, color="red")

# r2py:entity:b
def circleGrob():
    return patches.Circle((0.5, 0.5), 0.5, color="blue")

# r2py:entity:c
def linesGrob():
    return plt.Line2D([0, 1], [0, 1], color="black")

# r2py:entity:mat
def nullGrob():
    return None

a = rectGrob()
b = circleGrob()
c = linesGrob()

# Define matrices
# r2py:entity:row
row = np.array([[a, b]], dtype=object)
# r2py:entity:col
col = np.array([[a], [b]], dtype=object)
mat = np.array([[a, b], [c, nullGrob()]], dtype=object)

# gtable_matrix approximations (Storing layout metadata)
# In Python, we treat these as structures containing the matrix and dimensions
# r2py:entity:row_gt
row_gt = {"name": "demo", "data": row, "heights": [1], "widths": [1, 1]}
# r2py:entity:col_gt
col_gt = {"name": "demo", "data": col, "heights": [1, 1], "widths": [1]}
# r2py:entity:mat_gt
mat_gt = {"name": "demo", "data": mat, "heights": [1, 1], "widths": [1, 1]}

# r2py:entity:c_binded
def cbind(gt1, gt2, size="first"):
    # Approximate horizontal concatenation of layouts
    combined_data = np.hstack([gt1["data"], gt2["data"]])
    combined_widths = gt1["widths"] + gt2["widths"]
    combined_heights = gt1["heights"] if size == "first" else gt2["heights"]
    return {"data": combined_data, "heights": combined_heights, "widths": combined_widths}

# r2py:entity:r_binded
def rbind(gt1, gt2, size="last"):
    # Approximate vertical concatenation of layouts
    combined_data = np.vstack([gt1["data"], gt2["data"]])
    combined_heights = gt1["heights"] + gt2["heights"]
    combined_widths = gt1["widths"] if size == "first" else gt2["widths"]
    return {"data": combined_data, "heights": combined_heights, "widths": combined_widths}

# Execution
c_binded = cbind(mat_gt, col_gt, size="first")

# Visualizing c_binded
# r2py:entity:plot
fig, ax = plt.subplots()
ax.set_xlim(0, 3)
ax.set_ylim(0, 2)
ax.add_patch(patches.Rectangle((0, 1), 1, 1, color="red")) # mat_gt[0,0]
ax.add_patch(patches.Circle((1.5, 1.5), 0.5, color="blue")) # mat_gt[0,1]
ax.add_line(plt.Line2D([0, 1], [0, 1], color="black")) # mat_gt[1,0]
ax.add_patch(patches.Rectangle((2, 1), 1, 1, color="red")) # col_gt[0,0]
ax.add_patch(patches.Circle((2.5, 0.5), 0.5, color="blue")) # col_gt[1,0]
plt.show()

r_binded = rbind(mat_gt, row_gt, size="last")

# Visualizing r_binded
# r2py:entity:plot_1
fig, ax = plt.subplots()
ax.set_xlim(0, 2)
ax.set_ylim(0, 3)
ax.add_patch(patches.Rectangle((0, 2), 1, 1, color="red")) # mat_gt[0,0]
ax.add_patch(patches.Circle((1.5, 2.5), 0.5, color="blue")) # mat_gt[0,1]
ax.add_line(plt.Line2D([0, 1], [1, 2], color="black")) # mat_gt[1,0]
ax.add_patch(patches.Rectangle((0, 0), 1, 1, color="red")) # row_gt[0,0]
ax.add_patch(patches.Circle((1.5, 0.5), 0.5, color="blue")) # row_gt[0,1]
plt.show()

# try(cbind(mat_gt, row_gt))
# r2py:entity:try
try:
    # This should fail if shapes are incompatible for hstack
    cbind(mat_gt, row_gt)
except ValueError as e:
    print(f"Error: {e}")