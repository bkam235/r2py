# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:gt
class Unit:
    def __init__(self, values, units):
        self.values = values
        self.units = units

    def __repr__(self):
        return f"Unit({self.values}, {self.units})"

class GTable:
    def __init__(self, widths=None, heights=None, respect=False, 
                 name="layout", rownames=None, colnames=None, vp=None):
        self.widths = widths
        self.heights = heights
        self.respect = respect
        self.name = name
        self.rownames = rownames
        self.colnames = colnames
        self.vp = vp
        # layout is a dataframe simulating the R gtable layout
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name'])

def gtable(widths=None, heights=None, respect=False, 
           name="layout", rownames=None, colnames=None, vp=None):
    return GTable(widths=widths, heights=heights, respect=respect, 
                  name=name, rownames=rownames, colnames=colnames, vp=vp)

# r2py:entity:gtable_show_layout
def gtable_show_layout(x):
    if not isinstance(x, GTable):
        raise TypeError("x must be a gtable object")
    
    # In R, gtable_show_layout visualizes the grid layout.
    # Python implementation using matplotlib to mimic the layout visualization.
    widths = x.widths
    heights = x.heights
    
    # Simple logic to map 'null', 'cm', 'inch' to relative plot coordinates for visualization
    def resolve_units(u):
        vals = []
        for v, unit in zip(u.values, u.units):
            if unit == "null":
                vals.append(1.0) # Relative weight
            elif unit == "cm":
                vals.append(v * 0.39) # Approx conversion to inch for scale
            elif unit == "inch":
                vals.append(v)
            else:
                vals.append(v)
        return vals

    w_vals = resolve_units(widths)
    h_vals = resolve_units(heights)
    
    fig, ax = plt.subplots()
    
    # Calculate cumulative positions
    curr_x = 0
    for w in w_vals:
        curr_y = 0
        for h in h_vals:
            rect = patches.Rectangle((curr_x, curr_y), w, h, linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            curr_y += h
        curr_x += w
        
    ax.set_xlim(0, sum(w_vals))
    ax.set_ylim(0, sum(h_vals))
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()

# Execution
# r2py:entity:gt
gt = gtable(widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
             heights=Unit([0.2, 1, 3], ["inch", "null", "cm"]))
# r2py:entity:gtable_show_layout
gtable_show_layout(gt)