# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:gt
class Unit:
    def __init__(self, values, units):
        self.values = np.array(values)
        self.units = np.array(units)

    def __repr__(self):
        return f"Unit(values={self.values}, units={self.units})"

class GTable:
    def __init__(self, widths=None, heights=None, respect=False, name="layout", rownames=None, colnames=None, vp=None):
        self.widths = widths
        self.heights = heights
        self.respect = respect
        self.name = name
        self.rownames = rownames
        self.colnames = colnames
        self.vp = vp
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name'])

def gtable(widths=None, heights=None, respect=False, name="layout", rownames=None, colnames=None, vp=None):
    if widths is not None:
        if colnames is not None and len(colnames) != len(widths.values):
            raise ValueError("colnames must either be None or have the same length as widths")
    if heights is not None:
        if rownames is not None and len(rownames) != len(heights.values):
            raise ValueError("rownames must either be None or have the same length as heights")
    
    return GTable(widths=widths, heights=heights, respect=respect, name=name, rownames=rownames, colnames=colnames, vp=vp)

# r2py:entity:gtable_show_layout
def gtable_show_layout(gt):
    # Approximation of grid.show.layout for Python using matplotlib
    # This visualizes the widths and heights defined in the gtable
    fig, ax = plt.subplots()
    
    # Calculate relative sizes for visualization
    # 'null' in gtable acts as a flexible space. We assign it a base value of 1.
    def get_relative_sizes(units_obj):
        vals = units_obj.values
        unit_types = units_obj.units
        relative = []
        for v, u in zip(vals, unit_types):
            if u == 'null':
                relative.append(v)
            else:
                # Convert cm/inch to a rough relative scale for the plot
                scale = 1.0 if u == 'cm' else 2.54
                relative.append(v * scale)
        return np.array(relative)

    w_rel = get_relative_sizes(gt.widths)
    h_rel = get_relative_sizes(gt.heights)
    
    w_sum = sum(w_rel)
    h_sum = sum(h_rel)
    
    current_x = 0
    for i, w in enumerate(w_rel):
        current_y = 0
        for j, h in enumerate(h_rel):
            rect = plt.Rectangle((current_x, current_y), w, h, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            ax.text(current_x + w/2, current_y + h/2, f"R{j+1}C{i+1}", ha='center', va='center')
            current_y += h
        current_x += w

    ax.set_xlim(0, w_sum)
    ax.set_ylim(0, h_sum)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()

# Translation of the example script
# r2py:entity:gt
gt = gtable(
    widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
    heights=Unit([0.2, 1, 3], ["inch", "null", "cm"])
)
# r2py:entity:gtable_show_layout
gtable_show_layout(gt)