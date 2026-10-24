# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb, to_rgb

def col2rgb(col):
    if isinstance(col, str):
        return np.array(to_rgb(col)) * 255
    elif isinstance(col, (list, tuple, np.ndarray)) and len(col) == 3:
        return np.array(col) * 255 if np.max(col) <= 1.0 else np.array(col)
    return np.array(col)

def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    # Convert inputcol to RGB matrix (rows=colors, cols=3)
    if isinstance(inputcol, np.ndarray) and inputcol.ndim == 1:
        # handle numeric inputcol as passed in some R calls
        rgb_col = inputcol.reshape(-1, 1).repeat(3, axis=1) # simplified
    elif isinstance(inputcol, list) or isinstance(inputcol, np.ndarray):
        cols = []
        for c in inputcol:
            cols.append(col2rgb(c))
        rgb_col = np.array(cols)
    else:
        rgb_col = col2rgb(inputcol).reshape(1, 3)

    if rgb_col.shape[0] <= 1:
        return [to_rgb(rgb_col[0]/255) if np.max(rgb_col) > 1 else to_rgb(rgb_col[0])] * (numcol if numcol else 1)

    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    if x_to is None:
        x_to = np.linspace(0, 1, numcol)
    
    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.clip(outcol, 0, 255)
    return [tuple(row / 255.0) for row in outcol]

def shadepalette(inicol="white", endcol="red", n=100, interval=(0, 1)):
    x_to = np.linspace(interval[0], interval[1], n)
    return intpalette([inicol, endcol], numcol=n, x_to=x_to)

def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143], [0, 0, 255], [0, 255, 255], 
        [255, 255, 0], [255, 0, 0], [128, 0, 0]
    ])
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

def rainbow(n=50):
    return [hsv_to_rgb([i/n, 1, 1]) for i in range(n)]

def rotatexy(xy, angle, mid=None):
    xy = np.array(xy)
    if mid is None:
        mid = np.mean(xy, axis=0)
    angpi = np.radians(angle)
    cosa, sina = np.cos(angpi), np.sin(angpi)
    dx = xy[:, 0] - mid[0]
    dy = xy[:, 1] - mid[1]
    ex = mid[0] + cosa * dx - sina * dy
    ey = mid[1] + sina * dx + cosa * dy
    return np.column_stack((ex, ey))

def getellipse(rx=1, ry=1, mid=(0, 0), dr=0.01, angle=0, from_val=-np.pi, to_val=np.pi):
    dr = abs(dr)
    if to_val < from_val:
        to_val = 2 * np.pi + to_val
    x = np.arange(from_val, to_val + dr, dr)
    if len(x) > 0 and x[-1] > to_val:
        x = x[:-1]
    # Ensure the end point is included
    if len(x) == 0 or x[-1] != to_val:
        x = np.append(x, to_val)
    
    xy = np.column_stack((mid[0] + rx * np.cos(x), mid[1] + ry * np.sin(x)))
    if angle != 0:
        xy = rotatexy(xy, angle, mid=mid)
    return xy

def val2col(values, zlim, col):
    if values is not None:
        values = np.array(values)
        idx = np.argsort(values[:, 0])
        values = values[idx]
        if zlim is None:
            zlim = np.array([np.min(values[:, 1]), np.max(values[:, 1])])
        else:
            values[:, 1] = np.clip(values[:, 1], zlim[0], zlim[1])
        
        x_to = (values[:, 1] - zlim[0]) / (zlim[1] - zlim[0])
        Col = intpalette(col, numcol=len(x_to), x_to=x_to)
        nrad = len(values)
        intrad = np.concatenate(([0], values[:, 0] / values[-1, 0]))
        return {"Col": Col, "intrad": intrad, "nrad": nrad}
    else:
        Col = col if isinstance(col, list) else [col]
        nrad = len(Col)
        intrad = np.linspace(0, 1, nrad + 1)
        if len(col) < nrad:
            Col = intpalette(col, numcol=nrad)
        return {"Col": Col, "intrad": intrad, "nrad": nrad}

def filledshape(xyouter, xyinner=None, col="red", values=None, zlim=None, lcol=None, lwd=2):
    if xyinner is None:
        xyinner = np.mean(xyouter, axis=0).reshape(1, 2)
    
    res = val2col(values, zlim, col)
    Col = res["Col"]
    intrad = res["intrad"]
    nrad = res["nrad"]
    
    extern = np.array(xyouter)
    middle = np.array(xyinner).reshape(-1, 2)
    
    # To mimic R's polygon filling with concentric rings
    for i in range(nrad):
        relrad = intrad[i+1]
        # The current ring's outer boundary is the previous ring's inner boundary
        #’s logic is handled by the iteration and the slice
        outer_r = intrad[i]
        inner_r = intrad[i+1]
        
        # Interpolate between middle and extern
        p_outer = middle + outer_r * (extern - middle)
        p_inner = middle + inner_r * (extern - middle)
        
        # In R, polygon(c(outer, rev(inner))) creates a ring
        # We simplify: fill the larger and then the smaller? No, that's not how it works.
        # We draw rings from outer to inner.
        # To get a ring: combine outer poly and reverse inner poly
        poly_x = np.concatenate([p_outer[:, 0], p_inner[::-1, 0]])
        poly_y = np.concatenate([p_outer[:, 1], p_inner[::-1, 1]])
        plt.fill(poly_x, poly_y, color=Col[i], edgecolor='none')

    if lcol is not None:
        plt.plot(extern[:, 0], extern[:, 1], color=lcol, linewidth=lwd)

def filledmultigonal(mid=(0, 0), rx=1, ry=1, nr=4, col=None, values=None, zlim=None, lwd=2, lcol=None, angle=0):
    if col is None:
        col = femmecol(100)
    
    # dr is 2*pi/nr
    xy = getellipse(rx=rx, ry=ry, mid=mid, dr=2*np.pi/nr, from_val=0, to_val=2*np.pi)
    if angle != 0:
        xy = rotatexy(xy, angle, mid=mid)
    
    filledshape(xyouter=xy, xyinner=mid, col=col, values=values, zlim=zlim, lwd=lwd, lcol=lcol)
    return {"xyouter": xy, "xyinner": mid}

# Setup plot
plt.figure(figsize=(8, 8))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title("filledmultigonal")
plt.gca().set_aspect('equal')
plt.axis('off')

# Sequence of calls
# r2py:entity:filledmultigonal
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette("white", "red", n=50)) # Note: R's shadepalette default inicol is white
# Actually the R call in the prompt is shadepalette("red", "blue", n=50). 
# Looking at R source: shadepalette <- function (n = 100, endcol = "red", inicol = "white", ...)
# Wait, the R source provided says: shadepalette(rx=..., col=shadepalette("red", "blue", n=50))
# In the R source, the arguments for shadepalette are "red", "blue". 
# Based on the function definition `shadepalette(n=100, endcol="red", inicol="white", ...)`, 
# calling `shadepalette("red", "blue", n=50)` means n="red", endcol="blue", inicol=50. 
# This looks like a bug in the prompt's R source or I'm misreading. 
# Actually, in R, if you call `shadepalette("red", "blue", n=50)`, 
# "red" goes to n, "blue" to endcol. But n should be numeric.
# Checking the actual `shape` package: shadepalette(n=100, endcol="red", inicol="white", ...)
# The call `shadepalette("red", "blue", n=50)` in the R code is likely intended as `shadepalette(n=50, endcol="blue", inicol="red")`.
# Let's adjust the Python wrapper to be flexible or just follow the intended logic.

def shadepalette_fixed(c1, c2, n=50):
    return intpalette([c1, c2], numcol=n)

# Correcting the calls to use the fixed palette helper for clarity
# r2py:entity:filledmultigonal
filledmultigonal(rx=0.25, ry=0.125, nr=3, mid=(-0.75, 0.75), 
                 angle=45, col=shadepalette_fixed("red", "blue", 50))
# r2py:entity:filledmultigonal_1
filledmultigonal(rx=0.125, ry=0.25, nr=3, mid=(-0.25, 0.75), 
                 col=shadepalette_fixed("red", "yellow", 50))
# r2py:entity:filledmultigonal_2
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.25, 0.75),  
                 col=["red", "orange"])
# r2py:entity:filledmultigonal_3
filledmultigonal(rx=0.25, ry=0.25, nr=3, mid=(0.75, 0.75), 
                 angle=90, col="red")

# r2py:entity:filledmultigonal_4
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.75, 0.25), 
                 angle=0, col=shadepalette_fixed("red", "blue", 50))
# r2py:entity:filledmultigonal_5
filledmultigonal(rx=0.25, ry=0.25, nr=4, mid=(-0.25, 0.25),  
                 angle=45, col=shadepalette_fixed("red", "blue", 50))
# r2py:entity:filledmultigonal_6
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.25, 0.25), 
                 angle=0, col=shadepalette_fixed("red", "blue", 50))
# r2py:entity:filledmultigonal_7
filledmultigonal(rx=0.25, ry=0.125, nr=4, mid=(0.75, 0.25), 
                 angle=45, col=shadepalette_fixed("red", "blue", 50))

# r2py:entity:filledmultigonal_8
filledmultigonal(rx=0.25, ry=0.25, nr=5, mid=(-0.75, -0.25),  
                 angle=0, col=shadepalette_fixed("darkgreen", "lightgreen", 50))
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