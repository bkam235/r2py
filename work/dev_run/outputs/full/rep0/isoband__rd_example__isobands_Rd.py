# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:entity:isobands
def get_contour_data(X, Y, Z, levels, is_band=False):
    """Helper to approximate R's isobands/isolines output format."""
    cs = plt.contour(X, Y, Z, levels=levels)
    paths = cs.collections[0].get_paths() if hasattr(cs, 'collections') and len(cs.collections) > 0 else []
    
    all_x, all_y, all_id = [], [], []
    for i, path in enumerate(paths):
        v = path.vertices
        all_x.extend(v[:, 0])
        all_y.extend(v[:, 1])
        all_id.extend([i + 1] * len(v))
    
    return pd.DataFrame({'x': all_x, 'y': all_y, 'id': all_id})

# r2py:entity:plot_iso
def plot_iso(m, low, high):
    rows, cols = m.shape
    x = 0.05 + 0.9 * np.arange(cols) / (cols - 1 if cols > 1 else 1)
    y = 0.05 + 0.9 * np.arange(rows - 1, -1, -1) / (rows - 1 if rows > 1 else 1)
    X, Y = np.meshgrid(x, y)
    
    plt.figure(figsize=(5, 5))
    mask = np.isnan(m)
    z = np.ma.masked_array(m, mask=mask)
    
    # Fill bands
    plt.contourf(X, Y, z, levels=[low, high], colors=['cornsilk'], alpha=1.0)
    # Lines
    plt.contour(X, Y, z, levels=[low], colors='black')
    # Points
    plt.scatter(X, Y, color='black', s=10)
    plt.gca().set_aspect('equal')
    plt.show()

# Section 1
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])

x_coords = (np.arange(1, m.shape[1] + 1)) / (m.shape[1] + 1)
y_coords = (np.arange(m.shape[0], 0, -1)) / (m.shape[0] + 1)
X, Y = np.meshgrid(x_coords, y_coords)
# r2py:entity:df_bands
df_bands = get_contour_data(X, Y, m, [0.5, 1.5])

# r2py:entity:df_lines
df_lines = get_contour_data(X, Y, m, [0.5])

# r2py:entity:g
g = pd.DataFrame({'x': np.tile(x_coords, m.shape[0]), 
                  'y': np.repeat(y_coords, m.shape[1])})

# r2py:entity:grid.newpage
plt.figure(figsize=(5, 5))

# r2py:entity:grid.points
plt.scatter(g['x'], g['y'], color='black', s=10)

# r2py:entity:grid.path
if not df_bands.empty:
    plt.fill(df_bands['x'], df_bands['y'], color='cornsilk', edgecolor='none')

# r2py:entity:grid.polyline
if not df_lines.empty:
    plt.plot(df_lines['x'], df_lines['y'], color='black')

plt.gca().set_aspect('equal')
plt.show()

# Call plot_iso as requested in R source
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