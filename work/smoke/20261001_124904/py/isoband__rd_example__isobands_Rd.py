# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

# r2py:entity:plot_iso
def plot_iso(m, level_min, level_max):
    m_np = np.array(m)
    rows, cols = m_np.shape
    x = np.arange(1, cols + 1) / (cols + 1)
    y = np.arange(rows, 0, -1) / (rows + 1)
    X, Y = np.meshgrid(x, y)
    
    fig, ax = plt.subplots()
    
    # Fill bands
    ax.contourf(X, Y, m_np, levels=[level_min, level_max], colors=['cornsilk'], alpha=1)
    # Draw lines
    ax.contour(X, Y, m_np, levels=[0.5], colors='black')
    
    # Grid points
    ax.scatter(X, Y, color='black', s=1)
    
    ax.set_aspect('equal')
    plt.show()

# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Mimicking the grid/isoband logic via matplotlib contouring
# r2py:entity:g
rows, cols = m.shape
x = np.arange(1, cols + 1) / (cols + 1)
y = np.arange(rows, 0, -1) / (rows + 1)
X, Y = np.meshgrid(x, y)

# Initial Plot
fig, ax = plt.subplots()
# r2py:entity:isobands
ax.contourf(X, Y, m, levels=[0.5, 1.5], colors=['cornsilk'])
# r2py:entity:isolines
ax.contour(X, Y, m, levels=[0.5], colors='black')
# r2py:entity:grid.points
ax.scatter(X, Y, color='black', s=1)
ax.set_aspect('equal')
plt.show()

# Call plot_iso for the first matrix
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