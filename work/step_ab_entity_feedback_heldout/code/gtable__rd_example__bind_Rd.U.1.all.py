import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mocking grid-like objects
def rectGrob(gp=None):
    return "rect"

def circleGrob():
    return "circle"

def linesGrob():
    return "lines"

def nullGrob():
    return "null"

def unit(val, type_val):
    return val

# Entities
a = rectGrob()
b = circleGrob()
c = linesGrob()

row = np.array([[a, b]], dtype=object)
col = np.array([[a], [b]], dtype=object)
mat = np.array([[a, b], [c, nullGrob()]], dtype=object)

def gtable_matrix(name, data, heights, widths):
    return {"name": name, "data": data, "heights": heights, "widths": widths}

row_gt = gtable_matrix("demo", row, unit([1, 1], "null"), unit(1, "null"))
col_gt = gtable_matrix("demo", col, unit(1, "null"), unit([1, 1], "null"))
mat_gt = gtable_matrix("demo", mat, unit([1, 1], "null"), unit([1, 1], "null"))

def cbind(gt1, gt2, size="first"):
    # R's cbind for gtable checks if the number of rows match
    if gt1["data"].shape[0] != gt2["data"].shape[0]:
        raise ValueError("Dimensions must match along bind direction")
    
    combined_data = np.hstack([gt1["data"], gt2["data"]])
    combined_widths = list(gt1["widths"]) + list(gt2["widths"])
    combined_heights = gt1["heights"] if size == "first" else gt2["heights"]
    return {"data": combined_data, "heights": combined_heights, "widths": combined_widths}

def rbind(gt1, gt2, size="last"):
    # R's rbind for gtable checks if the number of columns match
    if gt1["data"].shape[1] != gt2["data"].shape[1]:
        raise ValueError("Dimensions must match along bind direction")
        
    combined_data = np.vstack([gt1["data"], gt2["data"]])
    combined_heights = list(gt1["heights"]) + list(gt2["heights"])
    combined_widths = gt1["widths"] if size == "first" else gt2["widths"]
    return {"data": combined_data, "heights": combined_heights, "widths": combined_widths}

# cbind
c_binded = cbind(mat_gt, col_gt, size="first")

# plot(c_binded)
def plot_gt(gt):
    # Dummy plot to avoid errors and match R's silent plot for gtable
    plt.figure()
    plt.title("gtable plot")
    plt.close()

plot_gt(c_binded)

# rbind
r_binded = rbind(mat_gt, row_gt, size="last")

# plot(r_binded)
plot_gt(r_binded)

# Dimensions must match along bind direction
try:
    cbind(mat_gt, row_gt)
except Exception:
    # R's try() by default suppresses output and just returns the error object
    pass