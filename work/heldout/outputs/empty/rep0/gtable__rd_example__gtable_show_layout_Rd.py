# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Any, Optional

# r2py:entity:gt
@dataclass
class Unit:
    value: List[float]
    unit: List[str]

@dataclass
class GTable:
    widths: Unit
    heights: Unit
    respect: bool = False
    name: str = "layout"
    rownames: Optional[List[str]] = None
    colnames: Optional[List[str]] = None
    vp: Any = None
    layout: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=['t', 'l', 'b', 'r', 'z', 'clip', 'name']
    ))

def gtable(widths=None, heights=None, respect=False, name="layout", 
           rownames=None, colnames=None, vp=None):
    return GTable(
        widths=widths, 
        heights=heights, 
        respect=respect, 
        name=name, 
        rownames=rownames, 
        colnames=colnames, 
        vp=vp
    )

# r2py:entity:gtable_show_layout
def gtable_show_layout(x, **kwargs):
    # Mimics grid.show.layout by plotting the proportions of the gtable
    # R's grid.show.layout draws a grid representing the layout
    widths = x.widths.value
    heights = x.heights.value
    
    # Handle "null" units by treating them as flexible space (1.0)
    # and fixed units (cm, inch) by treating them as their value
    def resolve_units(vals, units):
        resolved = []
        for v, u in zip(vals, units):
            if u == "null":
                resolved.append(1.0)
            elif u == "cm":
                resolved.append(v * 0.3937) # approx inch
            elif u == "inch":
                resolved.append(v)
            else:
                resolved.append(v)
        return resolved

    w_vals = resolve_units(widths, x.widths.unit)
    h_vals = resolve_units(heights, x.heights.unit)
    
    sum_w = sum(w_vals)
    sum_h = sum(h_vals)
    w_rel = [v / sum_w for v in w_vals]
    h_rel = [v / sum_h for v in h_vals]

    fig, ax = plt.subplots()
    
    # Draw vertical lines
    curr_x = 0
    for w in w_rel:
        curr_x += w
        ax.axvline(curr_x, color='black', linewidth=1)
        
    # Draw horizontal lines
    curr_y = 0
    for h in h_rel:
        curr_y += h
        ax.axhline(curr_y, color='black', linewidth=1)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(f"Layout: {x.name}")
    plt.show()

# Main execution
# r2py:entity:gt
gt = gtable(
    widths=Unit([1, 0.5, 2], ["null", "cm", "null"]),
    heights=Unit([0.2, 1, 3], ["inch", "null", "cm"])
)

# r2py:entity:gtable_show_layout
gtable_show_layout(gt)