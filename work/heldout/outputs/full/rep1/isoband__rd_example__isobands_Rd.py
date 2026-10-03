# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:entity:plot_iso
def plot_iso(m, vlo, vhi, fill_lo="gray95", fill_mid="gray50", 
             fill_hi="black", fill_band="cornsilk", col_lo="black", 
             col_hi="black", newpage=True):
    # Map R colors to Matplotlib compatible colors
    color_map = {
        "gray95": "#F2F2F2",
        "gray50": "#808080",
        "black": "#000000",
        "cornsilk": "#FFF8DC"
    }
    
    f_lo = color_map.get(fill_lo, fill_lo)
    f_mid = color_map.get(fill_mid, fill_mid)
    f_hi = color_map.get(fill_hi, fill_hi)
    f_band = color_map.get(fill_band, fill_band)
    c_lo = color_map.get(col_lo, col_lo)
    c_hi = color_map.get(col_hi, col_hi)

    rows, cols = m.shape
    x = np.linspace(0, 1, cols)
    y = np.linspace(1, 0, rows) # Y is reversed in the R source's grid logic
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()

    # Draw the band between vlo and vhi
    ax.contourf(X, Y, m, levels=[vlo, vhi], colors=[f_band], alpha=1)
    
    # Draw the isolines at vlo and vhi
    ax.contour(X, Y, m, levels=[vlo], colors=[c_lo])
    ax.contour(X, Y, m, levels=[vhi], colors=[c_hi])

    # Draw the points (grid nodes)
    # Flatten m and determine colors based on thresholds
    z_flat = m.flatten()
    p_fill = []
    p_col = []
    for val in z_flat:
        if np.isnan(val):
            p_fill.append("none")
            p_col.append("none")
        elif val < vlo:
            p_fill.append(f_lo)
            p_col.append("black")
        elif val < vhi:
            p_fill.append(f_mid)
            p_col.append(f_mid)
        else:
            p_fill.append(f_hi)
            p_col.append("black")

    ax.scatter(X.flatten(), Y.flatten(), c=p_fill, edgecolors=p_col, s=10, zorder=3)
    
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()

# one simple connected shape
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

# The R script uses isobands and isolines to create grid objects.
# To maintain equivalence with the visual output, we use the provided plot_iso logic.
# The first part of the R script explicitly builds a plot using grid.points, grid.path, and grid.polyline.
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# NAs are ignored
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

# two separate shapes
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]])
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# shape with hole
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]])
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)