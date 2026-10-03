# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

# r2py:entity:plot_iso
def plot_iso(m, level_min, level_max):
    # Prepare coordinates based on R logic: (1:ncol)/(ncol+1)
    rows, cols = m.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    fig, ax = plt.subplots()
    
# r2py:entity:isobands
    # Fill between levels (isobands)
    ax.contourf(X, Y, m, levels=[level_min, level_max], colors=['cornsilk'])
    
# r2py:entity:isolines
    # Draw line at the specific threshold (isolines)
    ax.contour(X, Y, m, levels=[level_min], colors='black')
    
# r2py:entity:grid.points
    # Grid points
    ax.scatter(X, Y, color='black', s=1)
    
    ax.set_aspect('equal')
    plt.show()

# First block
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Replicating the grid/isoband manual drawing logic using plot_iso
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second block (with NAs)
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# Third block
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# Fourth block
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)