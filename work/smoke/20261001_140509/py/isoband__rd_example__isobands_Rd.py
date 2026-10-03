# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# r2py:entity:plot_iso
def plot_iso(m, lower, upper):
    # Convert matrix to DataFrame for plotnine
    rows, cols = m.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    # Handle NaNs for interpolation by filling with a value outside range or masking
    m_filled = np.nan_to_num(m, nan=np.nanmean(m) if not np.isnan(m).all() else 0)
    
    # Create coordinates for contouring
    # plotnine's geom_contour requires a long-format dataframe
    df_iso = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': m_filled.flatten()})
    
    # Using matplotlib for the specific isoband/isolines logic as plotnine 
    # wraps ggplot2 which handles contours via geom_contour
    # To match the R visual exactly (filled bands + lines)
    plt.figure()
    plt.contourf(X, Y, m_filled, levels=[lower, upper], colors=['cornsilk'])
    plt.contour(X, Y, m_filled, levels=[lower], colors='black')
    
    # Grid points (equivalent to grid.points)
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

# Mimicking the explicit grid.path/polyline logic
# In Python, we typically use the plotting wrapper directly
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second Case (with NAs)
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