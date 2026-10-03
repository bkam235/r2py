# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

# Since isoband/isolines are specialized R packages, we approximate the 
# plotting logic using matplotlib's contouring capabilities.
# r2py:entity:plot_iso
def plot_iso(m, level_min, level_max):
    m = np.array(m)
    rows, cols = m.shape
    x = np.linspace(1/(cols+1), cols/(cols+1), cols)
    y = np.linspace(rows/(rows+1), 1/(rows+1), rows)
    
    # Create grid for plotting
    X, Y = np.meshgrid(x, y)
    
    plt.figure(figsize=(5, 5))
    
    # Handle NaNs for contouring by interpolating or filling
    # RegularGridInterpolator requires no NaNs for simple linear interpolation
    # Here we use matplotlib.contour which handles NaNs by leaving gaps
    
    # Band fill (isobands equivalent)
    plt.contourf(X, Y, m, levels=[level_min, level_max], colors=['cornsilk'], edgecolors='none')
    
    # Line plot (isolines equivalent)
    plt.contour(X, Y, m, levels=[level_min], colors='black')
    
    # Grid points (grid.points equivalent)
    plt.scatter(X, Y, color='black', s=1)
    
    plt.gca().set_aspect('equal')
    plt.show()

# First Case
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Mimicking the grid.points and grid.path logic for the first instance
# We can use the plot_iso helper for consistency
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second Case (with NaNs)
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# Third Case
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# Fourth Case
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)