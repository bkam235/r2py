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
def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red"):
    # Convert angle to radians
    theta_rot = np.radians(angle)
    
    # The R function filledmultigonal creates a "filled" look by drawing 
    # concentric shapes when 'col' is a vector.
    if isinstance(col, (list, np.ndarray)):
        colors = col
    elif isinstance(col, str):
        colors = [col]
    else:
        colors = [col]

    # Number of layers to draw for the filled effect
    num_layers = len(colors)
    
    for i in range(num_layers):
        # Shrink the shape for each subsequent color to create the fill effect
        # The innermost is the last color, the outermost is the first.
        # However, R's filledmultigonal typically draws from largest to smallest.
        scale = 1.0 - (i / max(1, num_layers)) * 0.1 # Small reduction per layer
        # Actually, a better approximation for "filled" is to draw the same shape 
        # but scaled down slightly for each color in the palette.
        # In many R shape functions, 'filled' means a gradient of concentric shapes.
        s = 1.0 - (i / max(1, num_layers))
        # But wait, usually it's just one shape if col is a string, 
        # and a series of nested shapes if col is a vector.
        # Let's use a simple scale down.
        curr_rx = rx * (1 - (i / max(1, num_layers)) * 0.02) 
        curr_ry = ry * (1 - (i / max(1, num_layers)) * 0.02)
        
        n_vertices = int(np.ceil(nr))
        angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False)
        
        vx = curr_rx * np.cos(angles)
        vy = curr_ry * np.sin(angles)
        
        x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
        y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
        
        x_final = x_rot + mid[0]
        y_final = y_rot + mid[1]
        
        # Close the polygon
        x_final = np.append(x_final, x_final[0])
        y_final = np.append(y_final, y_final[0])
        
        plt.fill(x_final, y_final, color=colors[i], edgecolor='none')

# Setup plot
# r2py:entity:emptyplot
plt.figure(figsize=(8, 8))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.gca().set_aspect('equal', adjustable='box')

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

plt.show()