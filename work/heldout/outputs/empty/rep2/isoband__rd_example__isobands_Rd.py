# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

# r2py:entity:plot_iso
def plot_iso(m, lower, upper):
    # Helper function to mimic plot_iso logic using matplotlib/plotnine
    # since isobands/isolines are specific to R's grid/isoband system
    rows, cols = m.shape
    x = np.linspace(1/(cols+1), cols/(cols+1), cols)
    y = np.linspace(rows/(rows+1), 1/(rows+1), rows)
    X, Y = np.meshgrid(x, y)
    
    # Create plot
    fig, ax = plt.subplots()
    
    # Fill between levels (equivalent to isobands)
    ax.contourf(X, Y, m, levels=[lower, upper], colors=['cornsilk'], edgecolors='none')
    
    # Draw line at specific level (equivalent to isolines)
    ax.contour(X, Y, m, levels=[lower], colors='black')
    
    # Grid points
    ax.scatter(X, Y, color='black', s=1)
    
    ax.set_aspect('equal')
    plt.show()

# First matrix
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Replicating the grid/isoband logic for the first section
# r2py:entity:g
cols_m = m.shape[1]
rows_m = m.shape[0]
x_coords = np.arange(1, cols_m + 1) / (cols_m + 1)
y_coords = np.arange(rows_m, 0, -1) / (rows_m + 1)
X_grid, Y_grid = np.meshgrid(x_coords, y_coords)

# Using matplotlib to emulate the grid.path/grid.polyline output
# r2py:entity:grid.newpage
fig, ax = plt.subplots()
# r2py:entity:grid.points
ax.scatter(X_grid, Y_grid, color='black', s=2)
# r2py:entity:df_bands
ax.contourf(X_grid, Y_grid, m, levels=[0.5, 1.5], colors=['cornsilk'], edgecolors='none')
# r2py:entity:df_lines
ax.contour(X_grid, Y_grid, m, levels=[0.5], colors='black')
ax.set_aspect('equal')
plt.show()

# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second matrix (with NaNs)
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# Third matrix
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# Fourth matrix
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)