# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

# r2py:entity:intpalette
def intpalette(inputcol, numcol=10, x_from=None, x_to=None):
    """
    Python implementation of shape::intpalette.
    Interpolates between a set of colors.
    """
    if len(inputcol) <= 1:
        return [inputcol[0]] * numcol
    
    # Convert colors to RGB (0-255)
    # Using matplotlib.colors to get RGB values
    from matplotlib.colors import to_rgb
    rgb_col = np.array([to_rgb(c) for c in inputcol]) * 255
    
    if x_from is None:
        x_from = np.linspace(0, 1, len(rgb_col))
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
        
    if min(x_to) < min(x_from) or max(x_to) > max(x_from):
        raise ValueError("intpalette: cannot interpolate; ranges x.to > ranges x.from")
    
    outcol = np.zeros((numcol, 3))
    for i in range(3):
        # np.interp is equivalent to approx in R
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol = np.clip(outcol, 0, 255)
    
    # Convert to hex colors to match R's rgb() output
    colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in outcol]
    return colors

# suppressPackageStartupMessages(library(shape))
import shape # This is a placeholder as 'shape' is an R package; the functions are implemented above.

# intpalette(c("white", "black"), n = 10)
# r2py:entity:intpalette
palette1 = intpalette(["white", "black"], numcol=10)
print(palette1)

# grey(seq(1, 0, length.out = 10))
# r2py:entity:grey
def grey(level, alpha=1.0):
    # R's grey() produces colors based on a 0-1 scale
    return [f"#{int(c*255):02x}{int(c*255):02x}{int(c*255):02x}" for c in level]

grey_seq = grey(np.linspace(1, 0, 10))
print(grey_seq)

# image(matrix(nrow = 1,ncol = 100, data = 1:100),
#       col = intpalette(c("red", "blue"), numcol = 100),
#       main = "intpalette")
# r2py:entity:image
d1 = np.arange(1, 101).reshape(1, 100)
palette_d1 = intpalette(["red", "blue"], numcol=100)
cmap1 = ListedColormap(palette_d1)

plt.figure()
plt.imshow(d1, aspect='auto', cmap=cmap1)
plt.title("intpalette")
plt.axis('off')
plt.show()

# image(matrix(nrow = 1, ncol = 100, data = 1:100),
#       col = intpalette(c("red", "blue", "yellow"), numcol = 100),
#       main = "intpalette")
# r2py:entity:image_1
d2 = np.arange(1, 101).reshape(1, 100)
palette_d2 = intpalette(["red", "blue", "yellow"], numcol=100)
cmap2 = ListedColormap(palette_d2)

plt.figure()
plt.imshow(d2, aspect='auto', cmap=cmap2)
plt.title("intpalette")
plt.axis('off')
plt.show()