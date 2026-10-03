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
        return f"Unit(values={self.values}, units={self.units})"

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
    
    # Logic to simulate grid.show.layout by visualizing the unit specifications
    fig, ax = plt.subplots()
    ax.set_title(f"Layout: {x.name}")
    
    # This is a simplified representation of the gtable layout
    # In a real environment, this would map the units to a physical canvas
    w_vals = x.widths.values if isinstance(x.widths, Unit) else []
    w_units = x.widths.units if isinstance(x.widths, Unit) else []
    h_vals = x.heights.values if isinstance(x.heights, Unit) else []
    h_units = x.heights.units if isinstance(x.heights, Unit) else []
    
    # Create a grid of rectangles to represent the layout
    for i in range(len(w_vals)):
        for j in range(len(h_vals)):
            rect = patches.Rectangle((i, j), 0.9, 0.9, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(i + 0.45, j + 0.45, f"W:{w_units[i]}\nH:{h_units[j]}", 
                    ha='center', va='center', fontsize=8)
            
    ax.set_xlim(0, len(w_vals))
    ax.set_ylim(0, len(h_vals))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

# Main script translation
# r2py:entity:gt
gt = gtable(widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
            heights=Unit([0.2, 1, 3], ["inch", "null", "cm"]))
# r2py:entity:gtable_show_layout
gtable_show_layout(gt)