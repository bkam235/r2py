# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# r2py:entity:gt
def unit(values, units):
    """Approximate R's grid::unit."""
    return {"values": values, "units": units}

def gtable(widths=None, heights=None, respect=False, name="layout", rownames=None, colnames=None, vp=None):
    """Approximate R's gtable function."""
    # The R source produces a gTree object with specific fields
    return {
        "grobs": [],
        "layout": pd.DataFrame(columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name']),
        "widths": widths,
        "heights": heights,
        "respect": respect,
        "name": name,
        "rownames": rownames,
        "colnames": colnames,
        "vp": vp,
        "class": "gtable"
    }

# r2py:entity:gtable_show_layout
def gtable_show_layout(gt, **kwargs):
    """Approximate R's gtable_show_layout."""
    widths_info = gt["widths"]
    heights_info = gt["heights"]
    
    # Extract numerical values for ratios
    w_vals = widths_info["values"]
    h_vals = heights_info["values"]
    
    fig = plt.figure(figsize=(8, 6))
    # Use GridSpec to visualize the layout
    gs = fig.add_gridspec(len(h_vals), len(w_vals), 
                          width_ratios=w_vals, 
                          height_ratios=h_vals)
    
    for r in range(len(h_vals)):
        for c in range(len(w_vals)):
            ax = fig.add_subplot(gs[r, c])
            ax.text(0.5, 0.5, f'Cell [{r+1},{c+1}]', ha='center', va='center')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f"R{r+1}C{c+1}", fontsize=8)
    
    plt.tight_layout()
    # We do not call plt.show() here to avoid "non-interactive" warnings in head-less environments,
    # but the figure is created and stored in the global state.

# No-op in Python

# Handled by defining gtable and gtable_show_layout above

# r2py:entity:gt
gt = gtable(
    widths=unit([1, 0.5, 2], ["null", "cm", "null"]),
    heights=unit([0.2, 1, 3], ["inch", "null", "cm"])
)

# r2py:entity:gtable_show_layout
gtable_show_layout(gt)