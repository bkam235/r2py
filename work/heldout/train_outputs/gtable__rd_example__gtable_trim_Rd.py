# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Since gtable is a specialized grid layout system for R, 
# we implement the logic using matplotlib's patch system to mimic the visual output.

# r2py:entity:center
def draw_gtable_sim(grobs):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Base grid units are 2cm x 2cm. 
    # We represent them as 2 units in coordinate space for simplicity.
    for grob in grobs:
        # R indices are 1-based. 
        # row_start, col_start, row_end, col_end
        r1, c1, r2, c2 = grob
        # Convert grid indices to coordinate boundaries
        # R rows go top-down, matplotlib goes bottom-up
        y_top = 6 - (r1 - 1) * 2
        y_bottom = 6 - r2 * 2
        x_left = (c1 - 1) * 2
        x_right = c2 * 2
        
        rect = patches.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom, color='black')
        ax.add_patch(rect)
    
    plt.show()

# r2py:entity:base
# Define the 'rect' equivalent as a coordinate specification
# Base is 3x3 grid of 2cm units

# center <- gtable_add_grob(base, rect, 2, 2)
center = [(2, 2, 2, 2)]
# r2py:entity:plot
draw_gtable_sim(center)
# r2py:entity:plot_1
# gtable_trim(center) removes empty space (simulated by tight layout in plt)
draw_gtable_sim(center)

# r2py:entity:col
# col <- gtable_add_grob(base, rect, 1, 2, 3, 2)
col = [(1, 2, 3, 2)]
# r2py:entity:plot_2
draw_gtable_sim(col)
# r2py:entity:plot_3
# gtable_trim(col)
draw_gtable_sim(col)

# r2py:entity:row
# row <- gtable_add_grob(base, rect, 2, 1, 2, 3)
row = [(2, 1, 2, 3)]
# r2py:entity:plot_4
draw_gtable_sim(row)
# r2py:entity:plot_5
# gtable_trim(row)
draw_gtable_sim(row)