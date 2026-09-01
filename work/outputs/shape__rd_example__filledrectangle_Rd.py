# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

# r2py:entity:emptyplot
def create_gradient_rect(ax, wx, wy, mid, angle, colors, title=""):
    # Calculate coordinates for the rectangle
    # Note: shape::filledrectangle handles gradients and rotations
    # Matplotlib patches don't support internal gradients easily, 
    # so we simulate the layout.
    
    cx, cy = mid
    # Rotate coordinates for the rectangle center
    theta = np.radians(angle)
    
    # Create a rectangle patch
    rect = patches.Rectangle(
        (cx - wx/2, cy - wy/2), wx, wy, 
        angle=angle, 
        facecolor=colors[0] if isinstance(colors, list) else colors,
        edgecolor='none'
    )
    ax.add_patch(rect)
    ax.set_title(title)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

# r2py:entity:color
# Helper for shadepalette approximation
def get_gradient_color(start_col, end_col):
    return LinearSegmentedColormap.from_list("custom", [start_col, end_col])

# Plot 1
fig1, ax1 = plt.subplots()
# r2py:entity:filledrectangle
create_gradient_rect(ax1, 0.5, 0.5, (0.5, 0.5), 0, "lightblue", "filledrectangle")
# r2py:entity:filledrectangle_1
create_gradient_rect(ax1, 0.25, 0.25, (0.5, 0.5), 45, "darkblue", "filledrectangle")
# r2py:entity:filledrectangle_2
create_gradient_rect(ax1, 0.125, 0.125, (0.5, 0.5), 90, "blue", "filledrectangle")

# Plot 2
# r2py:entity:emptyplot_1
fig2, ax2 = plt.subplots()
# r2py:entity:color_1
color_blue = "blue"
# r2py:entity:filledrectangle_3
create_gradient_rect(ax2, 0.5, 0.5, (0, 0), 0, color_blue, "filledrectangle")
# r2py:entity:filledrectangle_4
create_gradient_rect(ax2, 0.5, 0.5, (0.5, 0.5), 90, color_blue, "filledrectangle")
# r2py:entity:filledrectangle_5
create_gradient_rect(ax2, 0.5, 0.5, (-0.5, -0.5), -90, color_blue, "filledrectangle")
# r2py:entity:filledrectangle_6
create_gradient_rect(ax2, 0.5, 0.5, (0.5, -0.5), 180, color_blue, "filledrectangle")
# r2py:entity:filledrectangle_7
create_gradient_rect(ax2, 0.5, 0.5, (-0.5, 0.5), 270, color_blue, "filledrectangle")

plt.show()