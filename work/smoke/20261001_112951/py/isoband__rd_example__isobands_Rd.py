# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet

# r2py:entity:plot_iso
def plot_iso(m, low, high):
    m_arr = np.array(m)
    rows, cols = m_arr.shape
    x = np.linspace(1/(cols+1), cols/(cols+1), cols)
    y = np.linspace(rows/(rows+1), 1/(rows+1), rows)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    
    # Handle NaNs for contouring
    # Matplotlib's contour handles NaNs by masking them
    
    # Fill between low and high (isobands)
    cf = ax.contourf(X, Y, m_arr, levels=[low, high], colors=['cornsilk'])
    
    # Line at low (isolines)
    cl = ax.contour(X, Y, m_arr, levels=[low], colors='black')
    
    # Grid points
    ax.scatter(X, Y, s=1, color='black')
    
    ax.set_aspect('equal')
    plt.show()

# First section
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# Equivalent of grid logic and plot_iso
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# Second section
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# Third section
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# Fourth section
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)