# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:gt
class Unit:
    def __init__(self, values, units):
        self.values = np.array(values)
        self.units = np.array(units)
    def __repr__(self):
        return f"unit({self.values}, {self.units})"

def gtable(widths=None, heights=None, respect=False, name="layout", rownames=None, colnames=None, vp=None):
    # Returns a structure mimicking the gTree object with gtable class
    return {
        "widths": widths,
        "heights": heights,
        "respect": respect,
        "name": name,
        "rownames": rownames,
        "colnames": colnames,
        "vp": vp,
        "grobs": [],
        "layout": pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name']),
        "class": "gtable"
    }

# r2py:entity:gtable_show_layout
def gtable_show_layout(gt, **kwargs):
    if not isinstance(gt, dict) or gt.get("class") != "gtable":
        raise TypeError("gt must be a gtable object")

    widths = gt["widths"]
    heights = gt["heights"]
    
    w_vals = widths.values
    w_units = widths.units
    h_vals = heights.values
    h_units = heights.units
    
    def resolve_units(vals, units, total_available=10.0):
        # R's 'null' unit fills the remaining space.
        resolved = np.zeros(len(vals))
        fixed_sum = 0
        null_indices = []
        
        for i in range(len(vals)):
            u = units[i]
            v = vals[i]
            if u == "cm":
                val = v * 0.3937  # Approximate cm to inch
                resolved[i] = val
                fixed_sum += val
            elif u == "inch":
                val = v
                resolved[i] = val
                fixed_sum += val
            elif u == "null":
                null_indices.append(i)
            else:
                resolved[i] = v
                fixed_sum += v
        
        if null_indices:
            remaining = max(0, total_available - fixed_sum)
            null_sum_weights = sum(vals[i] for i in null_indices)
            if null_sum_weights > 0:
                for i in null_indices:
                    resolved[i] = (vals[i] / null_sum_weights) * remaining
            else:
                per_null = remaining / len(null_indices)
                for i in null_indices:
                    resolved[i] = per_null
        
        return resolved

    # Resolve units for layout visualization
    w_res = resolve_units(w_vals, w_units, total_available=10.0)
    h_res = resolve_units(h_vals, h_units, total_available=10.0)
    
    w_total = np.sum(w_res)
    h_total = np.sum(h_res)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    curr_x = 0
    for i in range(len(w_res)):
        width = w_res[i]
        curr_y = 0
        for j in range(len(h_res)):
            height = h_res[j]
            rect = patches.Rectangle((curr_x, curr_y), width, height, 
                                     linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            # R's show_layout typically marks cells
            ax.text(curr_x + width/2, curr_y + height/2, f"({i+1},{j+1})", 
                    ha='center', va='center', fontsize=8)
            curr_y += height
        curr_x += width

    ax.set_xlim(0, w_total)
    ax.set_ylim(0, h_total)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(f"Layout: {gt['name']}")
    plt.show()

# Main Execution
# r2py:entity:gt
gt = gtable(
    widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
    heights=Unit([0.2, 1, 3], ["inch", "null", "cm"])
)
# r2py:entity:gtable_show_layout
gtable_show_layout(gt)