# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

# Approximation of plot_iso function using plotnine/matplotlib
# r2py:entity:df_lines
def plot_iso(m, low, high):
    m_np = np.array(m)
    rows, cols = m_np.shape
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)[::-1]
    
    # Create grid for contouring
    xi = np.linspace(0, 1, 100)
    yi = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(xi, yi)
    
    # Handle NaNs for interpolation
    m_filled = np.nan_to_num(m_np, nan=np.nanmean(m_np) if not np.all(np.isnan(m_np)) else 0)
    
    # Interpolator
    interp = RegularGridInterpolator((y[::-1], x), m_filled)
    Z = interp(np.stack([Y.flatten(), X.flatten()], axis=1)).reshape(100, 100)
    
    # Plotting
# r2py:entity:grid.newpage
    plt.figure(figsize=(5, 5))
# r2py:entity:grid.path
    plt.contourf(X, Y, Z, levels=[low, high], colors=['cornsilk'])
# r2py:entity:grid.polyline
    plt.contour(X, Y, Z, levels=[low], colors='black')
    
    # Grid points
# r2py:entity:grid.points
    gx, gy = np.meshgrid(x, y)
    plt.scatter(gx, gy, s=10, color='black')
    plt.gca().invert_yaxis()
    plt.show()

# Section 1
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# R logic for coordinates
# r2py:entity:g
cols_m = m.shape[1]
rows_m = m.shape[0]
x_coords = np.arange(1, cols_m + 1) / (cols_m + 1)
y_coords = np.arange(rows_m, 0, -1) / (rows_m + 1)

g = pd.DataFrame({'x': np.tile(x_coords, rows_m), 
                  'y': np.repeat(y_coords, cols_m)})
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Section 2
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# Section 3
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# Section 4
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)