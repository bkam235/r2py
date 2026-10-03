# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# r2py:entity:plot_iso
def plot_iso(m, lower, upper):
    rows, cols = m.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    # Use matplotlib's contouring to approximate isobands/isolines
    plt.figure(figsize=(5, 5))
    # Handle NAs by masking
    masked_m = np.ma.masked_invalid(m)
    
    # Fill between lower and upper (bands)
    plt.contourf(X, Y, masked_m, levels=[lower, upper], colors=['cornsilk'], alpha=1)
    # Draw the line at the threshold
    plt.contour(X, Y, masked_m, levels=[lower], colors='black')
    
    # Plot grid points
    plt.scatter(X, Y, color='black', s=1)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.show()

# First block
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Translation of the grid/path logic to the plot_iso call as requested by the flow
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second block (with NAs)
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0,       0,       1,     1, 1, 0],
              [0,       1,       1,     0, 0, 0],
              [0,       0,       0,     1, 0, 0],
              [0,       0,       0,     0, 0, 0]])
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