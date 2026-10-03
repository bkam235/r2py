import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:entity:isobands
def isobands(x, y, z, levels_low, levels_high):
    """
    Approximate R isobands: returns a list of dataframes containing 
    x, y, and id for the regions between levels_low and levels_high.
    """
    l_low = [levels_low] if np.isscalar(levels_low) else levels_low
    l_high = [levels_high] if np.isscalar(levels_high) else levels_high
    
    X, Y = np.meshgrid(x, y)
    # R's isobands uses a specific contouring algorithm. 
    # Matplotlib's contourf is the closest approximation.
    cs = plt.contourf(X, Y, z, levels=[l_low[0], l_high[0]], alpha=0)
    
    results = []
    paths = cs.get_paths()
    for i, path in enumerate(paths):
        verts = path.vertices
        if len(verts) > 0:
            # R's isoband output typically omits the duplicated closing vertex
            # found in Matplotlib's closed paths.
            if verts[0, 0] == verts[-1, 0] and verts[0, 1] == verts[-1, 1]:
                v_slice = verts[:-1]
            else:
                v_slice = verts
            
            results.append(pd.DataFrame({
                'x': v_slice[:, 0],
                'y': v_slice[:, 1],
                'id': [i + 1] * len(v_slice)
            }))
    
    plt.close()
    return results if results else [pd.DataFrame({'x': [], 'y': [], 'id': []})]

# r2py:entity:isolines
def isolines(x, y, z, levels):
    """
    Approximate R isolines: returns a list of dataframes containing 
    x, y, and id for the contours at the specified levels.
    """
    l = [levels] if np.isscalar(levels) else levels
    X, Y = np.meshgrid(x, y)
    cs = plt.contour(X, Y, z, levels=l, alpha=0)
    
    results = []
    paths = cs.get_paths()
    for i, path in enumerate(paths):
        verts = path.vertices
        if len(verts) > 0:
            # Remove duplicated closing vertex for consistency with isoband
            if verts[0, 0] == verts[-1, 0] and verts[0, 1] == verts[-1, 1]:
                v_slice = verts[:-1]
            else:
                v_slice = verts
            
            results.append(pd.DataFrame({
                'x': v_slice[:, 0],
                'y': v_slice[:, 1],
                'id': [i + 1] * len(v_slice)
            }))
    
    plt.close()
    return results if results else [pd.DataFrame({'x': [], 'y': [], 'id': []})]

# r2py:entity:plot_iso
def plot_iso(m, vlo, vhi, fill_lo="gray95", fill_mid="gray50", 
             fill_hi="black", fill_band="cornsilk", col_lo="black", 
             col_hi="black", newpage=True):
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
    x = 0.05 + 0.9 * np.linspace(0, 1, cols)
    y = 0.05 + 0.9 * np.linspace(1, 0, rows)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    
    ax.contourf(X, Y, m, levels=[vlo, vhi], colors=[f_band], alpha=1)
    ax.contour(X, Y, m, levels=[vlo], colors=[c_lo])
    ax.contour(X, Y, m, levels=[vhi], colors=[c_hi])

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

# --- Main Execution ---

# one simple connected shape
# r2py:entity:m
m = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]], dtype=float)

# r2py:entity:g
x_coords = np.arange(1, m.shape[1] + 1) / (m.shape[1] + 1)
y_coords = np.arange(m.shape[0], 0, -1) / (m.shape[0] + 1)
df_bands = isobands(x_coords, y_coords, m, 0.5, 1.5)[0]

df_lines = isolines(x_coords, y_coords, m, 0.5)[0]

# expand.grid(x = ..., y = ...)
# R: x repeats first, then y. x: 1 2 3 1 2 3, y: 1 1 1 2 2 2
# This means x is the inner loop.
g_data = []
for yi in y_coords:
    for xi in x_coords:
        g_data.append({'x': xi, 'y': yi})
g = pd.DataFrame(g_data)

# Grid plotting
# r2py:entity:grid.newpage
fig, ax = plt.subplots()
# r2py:entity:grid.points
ax.scatter(g['x'], g['y'], color='black', s=10)
# r2py:entity:grid.path
if not df_bands.empty:
    ax.fill(df_bands['x'], df_bands['y'], color="cornsilk", edgecolor='none')
# r2py:entity:grid.polyline
if not df_lines.empty:
    ax.plot(df_lines['x'], df_lines['y'], color='black', linewidth=1)

ax.set_aspect('equal')
ax.axis('off')
plt.show()

# a similar plot can be generated with the plot_iso() function
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
# r2py:entity:plot_iso_1
plot_iso(m, 0.5, 1.5)

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