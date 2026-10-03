# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
from scipy.interpolate import RegularGridInterpolator
from matplotlib import pyplot as plt

# r2py:entity:df_lines
def plot_iso(m, low=0.5, high=1.5):
    rows, cols = m.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    # Handle NAs by interpolating or masking
    # Matplotlib's contour handles NaNs by leaving gaps
# r2py:entity:grid.newpage
    plt.figure(figsize=(5, 5))
# r2py:entity:grid.path
    plt.contourf(X, Y, m, levels=[low, high], colors=['cornsilk'])
# r2py:entity:grid.polyline
    plt.contour(X, Y, m, levels=[low], colors='black')
    
    # Grid points
# r2py:entity:grid.points
    plt.scatter(X, Y, color='black', s=1)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.show()

# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# r2py:entity:g
rows, cols = m.shape
x_vals = np.arange(1, cols + 1) / (cols + 1)
y_vals = np.arange(rows, 0, -1) / (rows + 1)
g = pd.DataFrame([(x, y) for x in x_vals for y in y_vals], columns=['x', 'y'])

# Replicating the grid.path/polyline behavior via plot_iso logic
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)