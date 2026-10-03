# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Unit:
    def __init__(self, value, units):
        self.value = np.atleast_1d(value)
        self.units = units
    def __repr__(self):
        return f"unit({self.value}, '{self.units}')"

def unit(x, units):
    return Unit(x, units)

# r2py:entity:rect
class Grob:
    def __init__(self, name=None, gp=None, vp=None, cl=None):
        self.name = name
        self.gp = gp
        self.vp = vp
        self.cl = cl

class RectGrob(Grob):
    def __init__(self, x=unit(0.5, "npc"), y=unit(0.5, "npc"), 
                 width=unit(1, "npc"), height=unit(1, "npc"), 
                 just="centre", hjust=None, vjust=None, 
                 default_units="npc", name=None, gp=None, vp=None):
        super().__init__(name=name, gp=gp, vp=vp, cl="rect")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.just = just
        self.hjust = hjust
        self.vjust = vjust

def rectGrob(**kwargs):
    return RectGrob(**kwargs)

# r2py:entity:gt
class GTable:
    def __init__(self, widths=None, heights=None, respect=False, 
                 name="layout", rownames=None, colnames=None, vp=None):
        self.widths = widths if widths is not None else []
        self.heights = heights if heights is not None else []
        self.respect = respect
        self.name = name
        self.rownames = rownames
        self.colnames = colnames
        self.vp = vp
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name'])
        self.grobs = []

def gtable_matrix(name, grobs, widths=None, heights=None, z=None, 
                 respect=False, clip="on", vp=None):
    grobs_arr = np.array(grobs, dtype=object)
    rows, cols = grobs_arr.shape
    
    if widths is None or len(widths) != cols:
        raise ValueError("widths must be the same as the number of columns in grobs")
    if heights is None or len(heights) != rows:
        raise ValueError("heights must be the same as the number of rows in grobs")
    
    gt = GTable(widths=widths, heights=heights, respect=respect, 
                name=name, vp=vp)
    
    z_val = z if z is not None else float('inf')
    
    # Logic for gtable_add_grob
    for r in range(rows):
        for c in range(cols):
            grob_obj = grobs_arr[r, c]
            # t, l, b, r in gtable are 1-indexed and refer to boundaries
            gt.layout = pd.concat([gt.layout, pd.DataFrame([{
                't': r + 1, 'l': c + 1, 'b': r + 2, 'r': c + 2, 
                'z': z_val, 'clip': clip, 'name': getattr(grob_obj, 'name', None)
            }])], ignore_index=True)
            gt.grobs.append(grob_obj)
    return gt

# r2py:entity:gt_1
def gtable_add_row_space(gt, height):
    n = len(gt.heights) - 1
    if n == 0:
        return gt
    
    h_vals = np.atleast_1d(height)
    if len(h_vals) == 1:
        h_vals = np.repeat(h_vals, n)
    elif len(h_vals) != n:
        raise ValueError("height must be of length 1 or nrow - 1")
    
    # Insert rows in reverse order to maintain indices
    for i in range(n, 0, -1):
        # Simulating gtable_add_rows
        gt.heights.insert(i, h_vals[i-1])
        mask = gt.layout['t'] > i
        gt.layout.loc[mask, 't'] += 1
        mask_b = gt.layout['b'] > i
        gt.layout.loc[mask_b, 'b'] += 1
    return gt

# r2py:entity:gt_2
def gtable_add_col_space(gt, width):
    n = len(gt.widths) - 1
    if n == 0:
        return gt
    
    w_vals = np.atleast_1d(width)
    if len(w_vals) == 1:
        w_vals = np.repeat(w_vals, n)
    elif len(w_vals) != n:
        raise ValueError("width must be of length 1 or ncol - 1")
    
    for i in range(n, 0, -1):
        # Simulating gtable_add_cols
        gt.widths.insert(i, w_vals[i-1])
        mask = gt.layout['l'] > i
        gt.layout.loc[mask, 'l'] += 1
        mask_r = gt.layout['r'] > i
        gt.layout.loc[mask_r, 'r'] += 1
    return gt

# r2py:entity:plot
def plot_gt(gt):
    # Mock plot function to visualize the structure
    fig, ax = plt.subplots()
    ax.set_xlim(0, len(gt.widths))
    ax.set_ylim(0, len(gt.heights))
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.title(f"GTable: {gt.name}")
    plt.show()

# Execution
# r2py:entity:rect
rect = rectGrob()
# r2py:entity:rect_mat
rect_mat = np.tile([rect], 9).reshape(3, 3)

# r2py:entity:gt
gt = gtable_matrix("rects", rect_mat, 
                    widths=[unit(1, "null")] * 3, 
                    heights=[unit(1, "null")] * 3)

# r2py:entity:plot
plot_gt(gt)

# Add spacing between the grobs
# r2py:entity:gt_1
gt = gtable_add_row_space(gt, unit(0.5, "cm"))

# Different width between the columns
# r2py:entity:gt_2
gt = gtable_add_col_space(gt, [unit(0.5, "cm"), unit(1, "cm")])

# r2py:entity:plot_1
plot_gt(gt)