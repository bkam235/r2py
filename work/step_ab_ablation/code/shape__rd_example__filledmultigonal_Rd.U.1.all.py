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
    # R's rainbow creates a spectrum; hsv_to_rgb is a good approximation
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red"):
    # Convert angle to radians
    theta_rot = np.radians(angle)
    
    # R's filledmultigonal draws a set of shapes if col is a vector.
    # The number of shapes is the length of col.
    # Each shape is slightly smaller than the previous one to create a "filled" look.
    
    if isinstance(col, (list, np.ndarray)):
        colors = col
        n_layers = len(colors)
    else:
        colors = [col]
        n_layers = 1

    # The "filled" effect in shape::filledmultigonal is achieved by drawing 
    # concentric polygons from the outside in.
    for i in range(n_layers):
        # Scale factor for the inner layers
        scale = 1.0 - (i / n_layers) if n_layers > 1 else 1.0
        
        # Generate vertices based on nr
        # For non-integer nr, the last side is partial or it behaves like a regular polygon
        # approximation. We use ceil(nr) for vertices.
        n_vertices = int(np.ceil(nr))
        angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False)
        
        vx = (rx * scale) * np.cos(angles)
        vy = (ry * scale) * np.sin(angles)
        
        # Apply rotation
        x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
        y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
        
        # Translate to mid
        x_final = x_rot + mid[0]
        y_final = y_rot + mid[1]
        
        # Close the polygon
        x_final = np.append(x_final, x_final[0])
        y_final = np.append(y_final, y_final[0])
        
        plt.fill(x_final, y_final, color=colors[i], edgecolor='none')

# Setup plot - simulating emptyplot
plt.figure(figsize=(8, 8))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.gca().set_aspect('equal', adjustable='box')

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