# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb

def shadepalette(color1, color2, n=50):
    cmap = LinearSegmentedColormap.from_list("custom", [color1, color2])
    return [cmap(i/max(1, n-1)) for i in range(n)]

def femmecol(n=50):
    # Approximation of femmecol (typically pinks/purples)
    cmap = LinearSegmentedColormap.from_list("femme", ["#ffc0cb", "#ff69b4", "#800080"])
    return [cmap(i/max(1, n-1)) for i in range(n)]

def rainbow(n=50):
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

# r2py:entity:filledmultigonal
def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red", ax=None):
    if ax is None:
        ax = plt.gca()
        
    theta_rot = np.radians(angle)
    
    # Handle coloring: filledmultigonal fills from outside in or inside out
    # In R, if 'col' is a vector, it draws multiple polygons
    if isinstance(col, (list, np.ndarray)):
        colors = col
    elif isinstance(col, str):
        colors = [col]
    else:
        colors = [col]

    n_colors = len(colors)
    
    # The 'filling' is achieved by drawing polygons of decreasing size
    # from 1.0 down to nearly 0.
    for i in range(n_colors):
        # Scale the radii for the 'filling' effect
        # We iterate backwards so the smallest (center) is drawn last
        # or forwards and scale from outer to inner.
        # R's filledmultigonal usually works by layers.
        scale = 1.0 - (i / max(1, n_colors - 1)) * 0.95 if n_colors > 1 else 1.0
        
        # To match the visual filling of R, we draw from the outermost color to the innermost
        # but R's filledmultigonal specifically uses the palette for layers.
        # Let's use the palette in reverse order if we draw from outer to inner, 
        # or just use the current color and shrink.
        
        # For a true filling effect, we draw concentric polygons.
        # The 'i-th' polygon has radius scaled by (n_colors - i) / n_colors
        layer_scale = (n_colors - i) / n_colors
        
        cur_rx = rx * layer_scale
        cur_ry = ry * layer_scale
        
        n_vertices = int(np.ceil(nr))
        angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False)
        
        vx = cur_rx * np.cos(angles)
        vy = cur_ry * np.sin(angles)
        
        # Apply rotation
        x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
        y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
        
        # Translate to mid
        x_final = x_rot + mid[0]
        y_final = y_rot + mid[1]
        
        # Close the polygon
        x_final = np.append(x_final, x_final[0])
        y_final = np.append(y_final, y_final[0])
        
        ax.fill(x_final, y_final, color=colors[i], edgecolor='none')

# Setup plot
plt.figure(figsize=(8, 8))
ax = plt.gca()
# r2py:entity:emptyplot
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_title("filledmultigonal")
ax.set_aspect('equal')
ax.axis('off')

# Sequence of calls
# r2py:entity:filledmultigonal
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)
# r2py:entity:filledmultigonal_1
filledmultigonal(rx=0.125, ry=0.25, nr=3, mid=(-0.25, 0.75), 
                 col=shadepalette("red", "yellow", n=50), ax=ax)
# r2py:entity:filledmultigonal_2
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.25, 0.75),  
                 col=["red", "orange"], ax=ax)
# r2py:entity:filledmultigonal_3
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.75, 0.75), 
                 angle=90, col="red", ax=ax)

# r2py:entity:filledmultigonal_4
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.75, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50), ax=ax)
# r2py:entity:filledmultigonal_5
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.25, 0.25),  
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)
# r2py:entity:filledmultigonal_6
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.25, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50), ax=ax)
# r2py:entity:filledmultigonal_7
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.75, 0.25), 
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)

# r2py:entity:filledmultigonal_8
filledmultigonal(rx=0.25, ry=0.25, nr=5, mid=(-0.75, -0.25),  
                 angle=0, col=shadepalette("darkgreen", "lightgreen", n=50), ax=ax)
# r2py:entity:filledmultigonal_9
filledmultigonal(rx=0.25, angle=0, nr=5, mid=(-0.25, -0.25), 
                 col=rainbow(50), ax=ax)
# r2py:entity:filledmultigonal_10
filledmultigonal(rx=0.25, angle=30, nr=6, mid=(0.25, -0.25), 
                 col=femmecol(50), ax=ax)
# r2py:entity:filledmultigonal_11
filledmultigonal(rx=0.25, ry=0.125, angle=30, nr=6, mid=(0.75, -0.25), 
                 col="black", ax=ax)

# r2py:entity:filledmultigonal_12
filledmultigonal(rx=0.25, col="darkblue", nr=7, mid=(-0.75, -0.75), ax=ax)
# r2py:entity:filledmultigonal_13
filledmultigonal(rx=0.25, col="darkblue", nr=9, mid=(-0.25, -0.75), ax=ax)
# r2py:entity:filledmultigonal_14
filledmultigonal(rx=0.25, col="darkblue", nr=3.7, mid=(0.25, -0.75), ax=ax)
# r2py:entity:filledmultigonal_15
filledmultigonal(rx=0.25, col="darkblue", nr=4.5, mid=(0.75, -0.75), ax=ax)

plt.show()