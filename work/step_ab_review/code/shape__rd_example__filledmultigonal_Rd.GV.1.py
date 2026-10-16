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
    # R's rainbow() starts at red, goes through spectrum
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

def filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0, 0), angle=0, col="red", ax=None):
    if ax is None:
        ax = plt.gca()
        
    theta_rot = np.radians(angle)
    
    # R's filledmultigonal handles non-integer nr by creating a 
    # shape that transitions between polygon counts or uses a specific formula.
    # For the purpose of visual equivalence in a translation:
    n_vertices = int(np.ceil(nr))
    angles = np.linspace(0, 2 * np.pi, n_vertices + 1)
    
    vx = rx * np.cos(angles)
    vy = ry * np.sin(angles)
    
    # Rotation
    x_rot = vx * np.cos(theta_rot) - vy * np.sin(theta_rot)
    y_rot = vx * np.sin(theta_rot) + vy * np.cos(theta_rot)
    
    x_final = x_rot + mid[0]
    y_final = y_rot + mid[1]
    
    if isinstance(col, (list, np.ndarray)):
        # R's filledmultigonal with a color vector fills with concentric polygons
        # shrinking towards the center to create a gradient effect.
        num_cols = len(col)
        for i in range(num_cols):
            # Scale factor shrinks from 1.0 down to ~0.0
            scale = 1.0 - (i / num_cols)
            curr_x = (x_final - mid[0]) * scale + mid[0]
            curr_y = (y_final - mid[1]) * scale + mid[1]
            ax.fill(curr_x, curr_y, color=col[i], edgecolor='none', zorder=num_cols-i)
    else:
        ax.fill(x_final, y_final, color=col, edgecolor='none')

# Setup plot
plt.figure(figsize=(8, 8))
ax = plt.gca()
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')

# Sequence of calls
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)
filledmultigonal(rx=0.125, ry=0.25, nr=3, mid=(-0.25, 0.75), 
                 col=shadepalette("red", "yellow", n=50), ax=ax)
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.25, 0.75),  
                 col=["red", "orange"], ax=ax)
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.75, 0.75), 
                 angle=90, col="red", ax=ax)

filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.75, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50), ax=ax)
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.25, 0.25),  
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.25, 0.25), 
                 angle=0, col=shadepalette("red", "blue", n=50), ax=ax)
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.75, 0.25), 
                 angle=45, col=shadepalette("red", "blue", n=50), ax=ax)
  
filledmultigonal(rx=0.25, ry=0.25, nr=5, mid=(-0.75, -0.25),  
                 angle=0, col=shadepalette("darkgreen", "lightgreen", n=50), ax=ax)
filledmultigonal(rx=0.25, angle=0, nr=5, mid=(-0.25, -0.25), 
                 col=rainbow(50), ax=ax)
filledmultigonal(rx=0.25, angle=30, nr=6, mid=(0.25, -0.25), 
                 col=femmecol(50), ax=ax)
filledmultigonal(rx=0.25, ry=0.125, angle=30, nr=6, mid=(0.75, -0.25), 
                 col="black", ax=ax)
  
filledmultigonal(rx=0.25, col="darkblue", nr=7, mid=(-0.75, -0.75), ax=ax)
filledmultigonal(rx=0.25, col="darkblue", nr=9, mid=(-0.25, -0.75), ax=ax)
filledmultigonal(rx=0.25, col="darkblue", nr=3.7, mid=(0.25, -0.75), ax=ax)
filledmultigonal(rx=0.25, col="darkblue", nr=4.5, mid=(0.75, -0.75), ax=ax)

plt.show()