# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

# r2py:entity:plot_iso
def plot_iso(m, low, high):
    rows, cols = m.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    plt.figure(figsize=(5, 5))
    # Masking NAs for contouring
    masked_m = np.ma.masked_invalid(m)
    
    # Equivalent to isobands (filled contours)
    plt.contourf(X, Y, masked_m, levels=[low, high], colors=['cornsilk'], edges='none')
# r2py:entity:isolines
    # Equivalent to isolines
    plt.contour(X, Y, masked_m, levels=[low], colors='black')
    
# r2py:entity:grid.points
    # Equivalent to grid.points
    g_x, g_y = np.meshgrid(x, y)
    plt.scatter(g_x, g_y, color='black', s=1)
    
    plt.gca().set_aspect('equal')
    plt.show()

# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Translation of the grid/isoband logic into plot_iso utility
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