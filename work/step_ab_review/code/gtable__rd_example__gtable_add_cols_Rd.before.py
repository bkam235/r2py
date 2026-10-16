# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 17

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# In Python, gtable (a grid layout manager for grid graphics) 
# is best approximated using Matplotlib's GridSpec or Axes.
# Since plotnine is requested, we use matplotlib as the backend for grid-like layouts.

# r2py:entity:rect
def plot_gtable(rows, cols, fills):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    for (r, c, w, h) in fills:
        # R's gtable coordinates are 1-indexed, top-down. 
        # Matplotlib is 0-indexed, bottom-up.
        rect = patches.Rectangle((c-1, rows-r), w, h, color='#00000080')
        ax.add_patch(rect)
    plt.show()

# tab: 3x3 grid with specific rectangles
# rect 1: t=1, l=1, r=3 (Top row, spans all cols) -> (r=1, c=1, w=3, h=1)
# rect 2: t=1, b=3, l=1 (Left col, spans all rows) -> (r=1, c=1, w=1, h=3)
# rect 3: t=1, b=3, l=3 (Right col, spans all rows) -> (r=1, c=3, w=1, h=3)
# r2py:entity:tab_3
tab_fills = [(1, 1, 3, 1), (1, 1, 1, 3), (1, 3, 1, 3)]
tab_dim = (3, 3)
# r2py:entity:dim
print(tab_dim)
# r2py:entity:plot
plot_gtable(3, 3, tab_fills)

# tab2: add 1 column at index 1
# Original cols 3 -> 4
# r2py:entity:tab2
tab2_dim = (3, 4)
# Adjusting fills for the new column shift
tab2_fills = [(1, 1, 4, 1), (1, 1, 1, 3), (1, 4, 1, 3)]
# r2py:entity:dim_1
print(tab2_dim)
# r2py:entity:plot_1
plot_gtable(3, 4, tab2_fills)

# tab3: add 1 col at end, 1 col at beginning
# Original cols 3 -> 5
# r2py:entity:tab3_1
tab3_dim = (3, 5)
# Adjusting fills for shifts
tab3_fills = [(1, 1, 5, 1), (1, 1, 1, 3), (1, 5, 1, 3)]
# r2py:entity:dim_2
print(tab3_dim)
# r2py:entity:plot_2
plot_gtable(3, 5, tab3_fills)