# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
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
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name'])

def gtable(widths=None, heights=None, respect=False, 
           name="layout", rownames=None, colnames=None, vp=None):
    return GTable(widths=widths, heights=heights, respect=respect, 
                  name=name, rownames=rownames, colnames=colnames, vp=vp)

# r2py:entity:gtable_show_layout
def gtable_show_layout(x):
    if not isinstance(x, GTable):
        raise TypeError("x must be a gtable object")
    
    # To simulate R's gtable_show_layout, we visualize the layout grid using matplotlib
    # Since the specific visual output of gtable_show_layout is a diagnostic grid plot:
    fig, ax = plt.subplots()
    
    # Calculate relative sizes based on 'null' (flexible) and absolute units
    def resolve_units(units_obj):
        vals = units_obj.values
        unts = units_obj.units
        # Simplified: convert cm/inch to arbitrary plot units, null is 1.0
        resolved = []
        for v, u in zip(vals, unts):
            if u == "null":
                resolved.append(1.0)
            elif u == "cm":
                resolved.append(v * 0.39) # rough scale
            elif u == "inch":
                resolved.append(v * 1.0)
            else:
                resolved.append(v)
        return np.array(resolved)

    w_resolved = resolve_units(x.widths)
    h_resolved = resolve_units(x.heights)
    
    w_total = np.sum(w_resolved)
    h_total = np.sum(h_resolved)
    
    curr_x = 0
    for w in w_resolved:
        width = w / w_total
        curr_x += width
        
    curr_y = h_total
    for h in h_resolved:
        height = h / h_total
        # Draw boxes for layout
        start_x = 0
        for w in w_resolved:
            box_w = w / w_total
            rect = patches.Rectangle((start_x, curr_y - height), box_w, height, 
                                     linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            start_x += box_w
        curr_y -= height

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()

# Main execution
# r2py:entity:gt
gt = gtable(widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
            heights=Unit([0.2, 1, 3], ["inch", "null", "cm"]))
# r2py:entity:gtable_show_layout
gtable_show_layout(gt)