import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

# r2py:entity:import_gtable
# gtable is a layout engine for grid graphics. 
# We simulate its behavior using dictionaries and numpy arrays.

# r2py:entity:import_grid
# grid primitives simulation

def rectGrob(gp=None):
    return {"type": "rect", "gp": gp}

def circleGrob():
    return {"type": "circle"}

def linesGrob():
    return {"type": "lines"}

def nullGrob():
    return {"type": "null"}

def unit(val, type_):
    return {"val": val, "type": type_}

def gtable_matrix(name, data, heights, widths):
    return {
        "name": name,
        "children": np.array(data, dtype=object),
        "heights": heights,
        "widths": widths
    }

# r2py:entity:a
a = rectGrob(gp={"fill": "red"})
# r2py:entity:b
b = circleGrob()
# r2py:entity:c
c = linesGrob()

# r2py:entity:row
row = np.array([[a, b]], dtype=object)
# r2py:entity:col
col = np.array([[a], [b]], dtype=object)
# r2py:entity:mat
mat = np.array([[a, b], [c, nullGrob()]], dtype=object)

# r2py:entity:row_gt
row_gt = gtable_matrix("demo", row, [unit(1, "null"), unit(1, "null")], unit(1, "null"))
# r2py:entity:col_gt
col_gt = gtable_matrix("demo", col, unit(1, "null"), [unit(1, "null"), unit(1, "null")])
# r2py:entity:mat_gt
mat_gt = gtable_matrix("demo", mat, [unit(1, "null"), unit(1, "null")], [unit(1, "null"), unit(1, "null")])

def cbind(gt1, gt2, size="first"):
    # In gtable, cbind concatenates horizontally. 
    # The height of the resulting gtable must be compatible.
    if gt1["children"].shape[0] != gt2["children"].shape[0]:
        raise ValueError("Dimensions must match along bind direction")
    
    combined_children = np.hstack([gt1["children"], gt2["children"]])
    combined_widths = list(gt1["widths"]) + list(gt2["widths"])
    combined_heights = gt1["heights"] if size == "first" else gt2["heights"]
    
    return {"children": combined_children, "heights": combined_heights, "widths": combined_widths}

def rbind(gt1, gt2, size="last"):
    # In gtable, rbind concatenates vertically.
    # The width of the resulting gtable must be compatible.
    if gt1["children"].shape[1] != gt2["children"].shape[1]:
        raise ValueError("Dimensions must match along bind direction")
    
    combined_children = np.vstack([gt1["children"], gt2["children"]])
    combined_heights = list(gt1["heights"]) + list(gt2["heights"])
    combined_widths = gt1["widths"] if size == "first" else gt2["widths"]
    
    return {"children": combined_children, "heights": combined_heights, "widths": combined_widths}

# r2py:entity:c_binded
c_binded = cbind(mat_gt, col_gt, size="first")

# r2py:entity:plot
def plot_gt(gt):
    # Placeholder for plotting the simulated gtable
    pass

plot_gt(c_binded)

# r2py:entity:r_binded
r_binded = rbind(mat_gt, row_gt, size="last")

# r2py:entity:plot_1
plot_gt(r_binded)

# r2py:entity:try
try:
    cbind(mat_gt, row_gt)
except Exception:
    pass # R's try() by default does not print the error to stdout in this context