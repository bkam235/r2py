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
    # R's rainbow starts at red and goes through the spectrum
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

# r2py:entity:filledmultigonal
def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red"):
    # Convert angle to radians
    theta_rot = np.radians(angle)
    
    # Normalize colors to a list
    if isinstance(col, str):
        colors = [col]
    elif isinstance(col, (list, np.ndarray)):
        colors = col
    else:
        colors = [col]

    # The R function filledmultigonal draws concentric shapes.
    # The outermost shape is the largest, the innermost is the smallest.
    # We iterate backwards through the colors to draw from largest to smallest
    # or forwards and let them overlap. R usually draws them such that 
    # the last color is the innermost.
    
    n_colors = len(colors)
    
    # We need to determine the vertex positions based on nr
    # If nr is not an integer, R's multigonal handles it by calculating 
    # points on a circle.
    t = np.linspace(0, 2 * np.pi, int(np.ceil(nr)) + 1)
    if int(np.ceil(nr)) == 0: # Handle edge case
        t = np.array([0, 2*np.pi])
        
    # We draw multiple layers
    for i in range(n_colors):
        # Scale factor for the nested effect
        # Outermost (i=0) is scale 1.0, innermost is small.
        scale = 1.0 - (i / max(1, n_colors - 1)) * 0.9 if n_colors > 1 else 1.0
        
        # Basic vertices
        vx = (rx * scale) * np.cos(t)
        vy = (ry * scale) * np.sin(t)
        
        # Apply rotation
        x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
        y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
        
        # Translate to mid
        x_final = x_rot + mid[0]
        y_final = y_rot + mid[1]
        
        plt.fill(x_final, y_final, color=colors[i], edgecolor='none')

# Setup plot
# r2py:entity:emptyplot
plt.figure(figsize=(8, 8))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.axis('equal')

# Sequence of calls
# r2py:entity:filledmultigonal
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette("red", "blue", n=50))
# r2py:entity:filledmultigonal_1
filledmultigonal(rx=0.125, ry=0.25, nr=3, mid=(-0.25, 0.75), 
                 col=shadepalette("red", "yellow", n=50))
# r2py:entity:filledmultigonal_2
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.25, 0.75),  
                 col=["red", "orange"])
# r2py:entity:filledmultigonal_3
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.75, 0.75), 
                 angle=90, col="red")

# r2py:entity:filledmultigonal_4
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.75, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50))
# r2py:entity:filledmultigonal_5
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.25, 0.25),  
                 angle=45, col=shadepalette("red", "blue", n=50))
# r2py:entity:filledmultigonal_6
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.25, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50))
# r2py:entity:filledmultigonal_7
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.75, 0.25), 
                 angle=45, col=shadepalette("red", "blue", n=50))

# r2py:entity:filledmultigonal_8
filledmultigonal(rx=0.25, ry=0.25, nr=5, mid=(-0.75, -0.25),  
                 angle=0, col=shadepalette("darkgreen", "lightgreen", n=50))
# r2py:entity:filledmultigonal_9
filledmultigonal(rx=0.25, angle=0, nr=5, mid=(-0.25, -0.25), 
                 col=rainbow(50))
# r2py:entity:filledmultigonal_10
filledmultigonal(rx=0.25, angle=30, nr=6, mid=(0.25, -0.25), 
                 col=femmecol(50))
# r2py:entity:filledmultigonal_11
filledmultigonal(rx=0.25, ry=0.125, angle=30, nr=6, mid=(0.75, -0.25), 
                 col="black")

# r2py:entity:filledmultigonal_12
filledmultigonal(rx=0.25, col="darkblue", nr=7, mid=(-0.75, -0.75))
# r2py:entity:filledmultigonal_13
filledmultigonal(rx=0.25, col="darkblue", nr=9, mid=(-0.25, -0.75))
# r2py:entity:filledmultigonal_14
filledmultigonal(rx=0.25, col="darkblue", nr=3.7, mid=(0.25, -0.75))
# r2py:entity:filledmultigonal_15
filledmultigonal(rx=0.25, col="darkblue", nr=4.5, mid=(0.75, -0.75))

plt.gca().set_aspect('equal', adjustable='box')
plt.show()