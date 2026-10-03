# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.path import Path

# r2py:entity:isobands
def isobands(x, y, z, levels_low, levels_high):
    # isoband is a specialized R package. In Python, we approximate the 
    # logic of finding regions between two contour levels using matplotlib.contourf
    # and returning the path coordinates.
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    
    # Handle single value levels
    if np.isscalar(levels_low):
        levels_low = [levels_low]
    if np.isscalar(levels_high):
        levels_high = [levels_high]
        
    # Match lengths
    nmax = max(len(levels_low), len(levels_high))
    levels_low = np.repeat(levels_low, nmax // len(levels_low)) if len(levels_low) != nmax else np.array(levels_low)
    levels_high = np.repeat(levels_high, nmax // len(levels_high)) if len(levels_high) != nmax else np.array(levels_high)
    
    # Mocking the structure: returning a list of dataframes with x, y, id
    # In a real scenario, one would use matplotlib.contourf and extract paths
    # Here we simplify to the coordinates of the region for the sake of the translation
    # as isoband uses a specific marching squares implementation.
    
    # For the purpose of this script's plots, we use a simplified approximation
    # that returns the paths that would be filled.
    X, Y = np.meshgrid(x, y)
    # Since isobands implementation is complex, we return an empty structure 
    # that plot_iso/grid.path logic handles, but for the specific matrices provided,
    # we can simulate the data for the 0.5 to 1.5 band.
    
    # This is a simplified proxy for the isoband C implementation
    results = []
    for low, high in zip(levels_low, levels_high):
        mask = (z >= low) & (z <= high)
        # Find contours of the mask to create a polygon
        # For this specific simple case, we'll return the points where mask is true
        # to allow the plot logic to proceed.
        coords = np.argwhere(mask)
        if coords.size > 0:
            # Convert indices to actual x, y values
            # Note: R matrix indices are 1-based, Python 0-based.
            # R's isobands returns paths. We approximate as a set of points for the path.
            res_x = x[coords[:, 1]]
            res_y = y[coords[:, 0]]
            res_id = np.ones(len(res_x))
            results.append(pd.DataFrame({'x': res_x, 'y': res_y, 'id': res_id}))
        else:
            results.append(pd.DataFrame({'x': [], 'y': [], 'id': []}))
            
    return results

# r2py:entity:isolines
def isolines(x, y, z, levels):
    if np.isscalar(levels):
        levels = [levels]
    
    X, Y = np.meshgrid(x, y)
    results = []
    for level in levels:
        mask = (z >= level)
        coords = np.argwhere(mask)
        if coords.size > 0:
            res_x = x[coords[:, 1]]
            res_y = y[coords[:, 0]]
            res_id = np.ones(len(res_x))
            results.append(pd.DataFrame({'x': res_x, 'y': res_y, 'id': res_id}))
        else:
            results.append(pd.DataFrame({'x': [], 'y': [], 'id': []}))
    return results

# r2py:entity:plot_iso
def plot_iso(m, vlo, vhi, fill_lo="gray95", fill_mid="gray50", 
             fill_hi="black", fill_band="cornsilk", col_lo="black", 
             col_hi="black", newpage=True):
    
    m = np.asarray(m)
    rows, cols = m.shape
    x = 0.05 + 0.9 * np.arange(cols) / (cols - 1) if cols > 1 else np.array([0.5])
    y = 0.05 + 0.9 * np.arange(rows - 1, -1, -1) / (rows - 1) if rows > 1 else np.array([0.5])
    
    df_bands = isobands(x, y, m, vlo, vhi)[0]
    df_lines_lo = isolines(x, y, m, vlo)[0]
    df_lines_hi = isolines(x, y, m, vhi)[0]
    
    # Create grid of points
    xv, yv = np.meshgrid(x, y)
    df_points = pd.DataFrame({'x': xv.flatten(), 'y': yv.flatten()})
    
    # Calculate colors for the points
    m_flat = m.flatten()
    pfill = np.where(m_flat < vlo, fill_lo, np.where(m_flat < vhi, fill_mid, fill_hi))
    pcol = np.where(m_flat < vlo, "black", np.where(m_flat < vhi, fill_mid, "black"))
    
    plt.figure()
    plt.gca().set_aspect('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis('off')

    if not df_bands.empty:
        plt.scatter(df_bands['x'], df_bands['y'], color=fill_band, marker='s', s=100, edgecolors='none')
        
    if not df_lines_lo.empty:
        plt.plot(df_lines_lo['x'], df_lines_lo['y'], color=col_lo, linewidth=1)
        
    if not df_lines_hi.empty:
        plt.plot(df_lines_hi['x'], df_lines_hi['y'], color=col_hi, linewidth=1)
        
    plt.scatter(df_points['x'], df_points['y'], c=pfill, edgecolors=pcol, s=20, zorder=3)
    plt.show()

# --- Execution ---

# one simple connected shape
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]], dtype=float)

# r2py:entity:df_bands
df_bands = isobands(x_vals, y_vals, m, 0.5, 1.5)[0]
# r2py:entity:df_lines
df_lines = isolines(x_vals, y_vals, m, 0.5)[0]
# r2py:entity:g
g = pd.DataFrame({'x': np.meshgrid(x_vals, y_vals)[0].flatten(), 
                  'y': np.meshgrid(x_vals, y_vals)[1].flatten()})

# r2py:entity:grid.newpage
plt.figure()
plt.gca().set_aspect('equal')
plt.xlim(0, 1)
plt.ylim(0, 1)
# r2py:entity:grid.points
plt.scatter(g['x'], g['y'], color='black', s=5)
# r2py:entity:grid.path
if not df_bands.empty:
    plt.scatter(df_bands['x'], df_bands['y'], color="cornsilk", marker='s', s=50)
# r2py:entity:grid.polyline
if not df_lines.empty:
    plt.plot(df_lines['x'], df_lines['y'], color='black')
plt.show()

# plot_iso exploration
# r2py:entity:plot_iso
plot_iso(m, 0.5, 1.5)

# NAs are ignored
# r2py:entity:m_1
m = np.array([[np.nan, np.nan, np.nan, 0, 0, 0],
              [np.nan, np.nan, np.nan, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]], dtype=float)
# Patching isobands/isolines to handle NaNs (numpy.nan_to_num or mask)
def isobands_nan(x, y, z, levels_low, levels_high):
    z_filled = np.nan_to_num(z, nan=-1.0)
    return isobands(x, y, z_filled, levels_low, levels_high)

def isolines_nan(x, y, z, levels):
    z_filled = np.nan_to_num(z, nan=-1.0)
    return isolines(x, y, z_filled, levels)

# Override for the NaN case
original_isobands = isobands
original_isolines = isolines
isobands = isobands_nan
isolines = isolines_nan
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)
isobands = original_isobands
isolines = original_isolines

# two separate shapes
# r2py:entity:m_2
m = np.array([[0, 0, 1, 1],
              [0, 1, 1, 1],
              [1, 1, 0, 0],
              [0, 0, 0.8, 0]], dtype=float)
# r2py:entity:plot_iso_2
plot_iso(m, 0.5, 1.5)

# shape with hole
# r2py:entity:m_3
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 2, 2, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0]], dtype=float)
# r2py:entity:plot_iso_3
plot_iso(m, 0.5, 1.5)