import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb

def shadepalette(color1, color2, n=50):
    cmap = LinearSegmentedColormap.from_list("custom", [color1, color2])
    return [cmap(i/max(1, n-1)) for i in range(n)]

def femmecol(n=50):
    # Approximation of femmecol (typically pinks/purples/reds)
    cmap = LinearSegmentedColormap.from_list("femme", ["#ffc0cb", "#ff69b4", "#800080"])
    return [cmap(i/max(1, n-1)) for i in range(n)]

def rainbow(n=50):
    # R's rainbow() is a standard HSV hue cycle
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red"):
    """
    R's filledmultigonal draws concentric filled polygons to create a shaded effect.
    The number of layers is determined by the length of the 'col' vector.
    """
    theta_rot = np.radians(angle)
    
    # Determine the number of layers based on the length of col
    if isinstance(col, (list, np.ndarray)):
        n_layers = len(col)
    elif isinstance(col, str):
        n_layers = 1
        col = [col]
    else:
        n_layers = 1
        col = [col]

    # Generate points for the outer boundary
    n_vertices = int(np.ceil(nr))
    # Handle nr < 3 if necessary, though typically nr >= 3
    if n_vertices < 3:
        n_vertices = 3
        
    angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False)
    
    # We draw concentric polygons from the outside in (or inside out)
    # To create the filled effect, we iterate from the outer limit down to 0
    for i in range(n_layers):
        # Calculate a scaling factor for the i-th layer
        # Layers go from 1.0 (outermost) down to ~0 (innermost)
        scale = 1.0 - (i / n_layers)
        
        vx = scale * rx * np.cos(angles)
        vy = scale * ry * np.sin(angles)
        
        # Apply rotation
        x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
        y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
        
        # Translate to mid
        x_final = x_rot + mid[0]
        y_final = y_rot + mid[1]
        
        # Fill the polygon. In R, these are layered.
        # We use the i-th color from the palette.
        plt.fill(np.append(x_final, x_final[0]), np.append(y_final, y_final[0]), 
                 color=col[i], edgecolor='none')

# Setup plot
plt.figure(figsize=(8, 8))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')

# Sequence of calls
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette("red", "blue", n=50))
filledmultigonal(rx=0.125, ry=0.25, nr=3, mid=(-0.25, 0.75), 
                 col=shadepalette("red", "yellow", n=50))
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.25, 0.75),  
                 col=["red", "orange"])
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.75, 0.75), 
                 angle=90, col="red")

filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.75, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50))
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.25, 0.25),  
                 angle=45, col=shadepalette("red", "blue", n=50))
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.25, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50))
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.75, 0.25), 
                 angle=45, col=shadepalette("red", "blue", n=50))

filledmultigonal(rx=0.25, ry=0.25, nr=5, mid=(-0.75, -0.25),  
                 angle=0, col=shadepalette("darkgreen", "lightgreen", n=50))
filledmultigonal(rx=0.25, angle=0, nr=5, mid=(-0.25, -0.25), 
                 col=rainbow(50))
filledmultigonal(rx=0.25, angle=30, nr=6, mid=(0.25, -0.25), 
                 col=femmecol(50))
filledmultigonal(rx=0.25, ry=0.125, angle=30, nr=6, mid=(0.75, -0.25), 
                 col="black")

filledmultigonal(rx=0.25, col="darkblue", nr=7, mid=(-0.75, -0.75))
filledmultigonal(rx=0.25, col="darkblue", nr=9, mid=(-0.25, -0.75))
filledmultigonal(rx=0.25, col="darkblue", nr=3.7, mid=(0.25, -0.75))
filledmultigonal(rx=0.25, col="darkblue", nr=4.5, mid=(0.75, -0.75))

plt.show()