# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:gt
def unit(values, units):
    """
    Approximates R's grid::unit. 
    Returns a list of tuples (value, unit).
    """
    return list(zip(values, units))

# r2py:entity:gt
class GTable:
    """
    Approximates R's gtable object.
    """
    def __init__(self, widths=None, heights=None, respect=False, 
                 name="layout", rownames=None, colnames=None, vp=None):
        self.widths = widths if widths is not None else []
        self.heights = heights if heights is not None else []
        self.respect = respect
        self.name = name
        self.rownames = rownames
        self.colnames = colnames
        self.vp = vp
        # Equivalent to the empty layout data frame in R
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name'])

# r2py:entity:gtable_show_layout
def gtable_show_layout(gt):
    """
    Visualizes the gtable layout using matplotlib to mimic grid.show.layout.
    """
    widths = gt.widths
    heights = gt.heights
    
    # In a real environment, these would be converted to pixels/points.
    # For visualization, we map 'null' to a standard size and 'cm/inch' to proportional sizes.
    def resolve_units(units_list):
        resolved = []
        for val, unit_type in units_list:
            if unit_type == 'null':
                resolved.append(1.0)
            elif unit_type == 'cm':
                resolved.append(val * 0.3937) # approx inches
            elif unit_type == 'inch':
                resolved.append(val)
            else:
                resolved.append(val)
        return np.array(resolved)

    w_vals = resolve_units(widths)
    h_vals = resolve_units(heights)
    
    # Calculate cumulative positions
    w_cum = np.cumsum(np.insert(w_vals, 0, 0))
    h_cum = np.cumsum(np.insert(h_vals, 0, 0))
    
    fig, ax = plt.subplots()
    
    for i in range(len(w_vals)):
        for j in range(len(h_vals)):
            rect = patches.Rectangle(
                (w_cum[i], h_cum[j]), 
                w_vals[i], h_vals[j], 
                linewidth=1, edgecolor='black', facecolor='none'
            )
            ax.add_patch(rect)
            # Add label for the cell (row, col)
            ax.text(w_cum[i] + w_vals[i]/2, h_cum[j] + h_vals[j]/2, 
                    f"R{j+1}C{i+1}", ha='center', va='center')

    ax.set_xlim(0, w_cum[-1])
    ax.set_ylim(0, h_cum[-1])
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()

# Main Execution
# r2py:entity:gt
gt = GTable(
    widths=unit([1, 0.5, 2], ["null", "cm", "null"]),
    heights=unit([0.2, 1, 3], ["inch", "null", "cm"])
)

# r2py:entity:gtable_show_layout
gtable_show_layout(gt)