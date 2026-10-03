import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# No-op in Python

# Library 'shape' functions are implemented below

# r2py:entity:shadepalette
def col2rgb(color):
    """Helper to convert color string to RGB 0-255."""
    return np.array(to_rgb(color)) * 255

def intpalette(inputcol, numcol, x_from=None, x_to=None):
    """Helper logic for R's intpalette."""
    if len(inputcol) <= 1:
        return [inputcol[0]] * numcol
    
    # Convert input colors to RGB matrix
    rgb_col = np.array([col2rgb(c) for c in inputcol])
    
    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if x_to.min() < x_from.min() or x_to.max() > x_from.max():
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
        
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.clip(np.round(outcol), 0, 255).astype(int)
    
    # Convert RGB to hex strings to match R's output
    colors = ["#%02x%02x%02x" % tuple(row) for row in outcol]
    return colors

def shadepalette(n=100, endcol="red", inicol="white", interval=(0, 1)):
    x_to = np.linspace(interval[0], interval[1], n)
    return intpalette([inicol, endcol], n, x_to=x_to)

# Example 1: shadepalette(n = 10, "white", "black")
# Note: In R, the arguments are n=10, endcol="white", inicol="black"
res1 = shadepalette(10, "white", "black")
print(res1)

# Example 2: image(matrix(nrow = 1, ncol = 100, data = 1:100), 
#                  col = shadepalette(100, "red", "blue"), main = "shadepalette")
# r2py:entity:image
d = np.arange(1, 101).reshape(1, 100)
palette_100 = shadepalette(100, "red", "blue")

# To use a list of hex colors in imshow, we create a ListedColormap
from matplotlib.colors import ListedColormap
cmap_custom = ListedColormap(palette_100)

plt.figure()
plt.imshow(d, aspect='auto', cmap=cmap_custom)
plt.title("shadepalette")
plt.axis('off')
plt.show()