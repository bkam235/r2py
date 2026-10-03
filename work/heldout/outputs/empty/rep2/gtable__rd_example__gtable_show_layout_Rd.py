# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:gt
class Unit:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"unit({self.value}, {self.unit})"

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
    return GTable(widths=widths, heights=heights, respect=respect, name=name, rownames=rownames, colnames=colnames, vp=vp)

# r2py:entity:gtable_show_layout
def gtable_show_layout(x):
    """
    Simulates the visualization of a gtable layout.
    In R, this draws the grid layout. In Python, we'll visualize it using Matplotlib.
    """
    if not isinstance(x, GTable):
        raise TypeError("x must be a GTable object")
    
    widths = x.widths
    heights = x.heights
    
    # Simple mapping to determine plot dimensions based on units
    # 'null' is treated as relative (flexible), cm/inch as absolute
    # For visualization, we convert everything to a consistent scale
    def get_scale(units):
        vals = []
        for u in units:
            if u.unit == "null":
                vals.append(1.0) # Default relative weight
            elif u.unit == "cm":
                vals.append(u.value / 2.54) # convert to inches
            elif u.unit == "inch":
                vals.append(u.value)
            else:
                vals.append(u.value)
        return vals

    w_scales = get_scale(widths)
    h_scales = get_scale(heights)
    
    total_w = sum(w_scales)
    total_h = sum(h_scales)
    
    fig, ax = plt.subplots()
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, total_h)
    
    curr_x = 0
    for i, w in enumerate(w_scales):
        curr_y = 0
        for j, h in enumerate(h_scales):
            # Draw the cell
            rect = patches.Rectangle((curr_x, curr_y), w, h, linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            # Label the cell
            ax.text(curr_x + w/2, curr_y + h/2, f"R{j+1}C{i+1}", ha='center', va='center')
            curr_y += h
        curr_x += w
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

# --- Execute Example ---
# r2py:entity:gt
gt = gtable(
    widths=[Unit(1, "null"), Unit(0.5, "cm"), Unit(2, "null")],
    heights=[Unit(0.2, "inch"), Unit(1, "null"), Unit(3, "cm")]
)

# r2py:entity:gtable_show_layout
gtable_show_layout(gt)