import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mock classes for grid/gtable equivalents
class Grob:
    def __init__(self, type_):
        self.type = type_

class GTable:
    def __init__(self, name, data, heights, widths):
        self.name = name
        self.data = data
        self.heights = heights
        self.widths = widths

def rectGrob(gp=None):
    return Grob("rect")

def circleGrob():
    return Grob("circle")

def linesGrob():
    return Grob("lines")

def nullGrob():
    return Grob("null")

def unit(val, type_):
    return (val, type_)

def gtable_matrix(name, matrix_data, heights, widths):
    return GTable(name, matrix_data, heights, widths)

def cbind(gt1, gt2, size="first"):
    if gt1.data.shape[0] != gt2.data.shape[0]:
        raise ValueError("Dimensions must match along bind direction")
    
    combined_data = np.hstack([gt1.data, gt2.data])
    combined_widths = list(gt1.widths) + list(gt2.widths)
    combined_heights = gt1.heights if size == "first" else gt2.heights
    return GTable(gt1.name, combined_data, combined_heights, combined_widths)

def rbind(gt1, gt2, size="last"):
    if gt1.data.shape[1] != gt2.data.shape[1]:
        raise ValueError("Dimensions must match along bind direction")
    
    combined_data = np.vstack([gt1.data, gt2.data])
    combined_heights = list(gt1.heights) + list(gt2.heights)
    combined_widths = gt1.widths if size == "first" else gt2.widths
    return GTable(gt1.name, combined_data, combined_heights, combined_widths)

def plot(gt):
    # Simplified plot representation
    print(f"Plotting GTable with shape {gt.data.shape}")

# R Script Execution
a = rectGrob(gp={"fill": "red"})
b = circleGrob()
c = linesGrob()

row = np.array([[a, b]], dtype=object)
col = np.array([[a], [b]], dtype=object)
mat = np.array([[a, b], [c, nullGrob()]], dtype=object)

row_gt = gtable_matrix("demo", row, unit([1, 1], "null"), unit(1, "null"))
col_gt = gtable_matrix("demo", col, unit(1, "null"), unit([1, 1], "null"))
mat_gt = gtable_matrix("demo", mat, unit([1, 1], "null"), unit([1, 1], "null"))

# cbind
c_binded = cbind(mat_gt, col_gt, size="first")
plot(c_binded)

# rbind
r_binded = rbind(mat_gt, row_gt, size="last")
plot(r_binded)

# Dimensions must match along bind direction
try:
    cbind(mat_gt, row_gt)
except Exception:
    pass # R's try() by default suppresses output