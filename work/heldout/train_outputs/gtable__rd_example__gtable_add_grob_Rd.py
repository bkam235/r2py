# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Mocking gtable and grid logic to maintain structural equivalence
# r2py:entity:gt
class Gtable:
    def __init__(self, widths, heights):
        self.widths = widths
        self.heights = heights
        self.grobs = []
        self.layout = [] # List of dicts with t, l, b, r, z, clip, name

    def add_grob(self, grob, t, l, b=None, r=None, z=float('inf'), clip="on", name=None):
        if b is None: b = t
        if r is None: r = l
        
        # R indices are 1-based; convert to 0-based for Python GridSpec
        # t = top, l = left, b = bottom, r = right
        self.grobs.append(grob)
        self.layout.append({
            't': t - 1, 
            'l': l - 1, 
            'b': b - 1, 
            'r': r - 1, 
            'z': z, 
            'clip': clip, 
            'name': name
        })
        return self

def gtable(widths, heights):
    return Gtable(widths, heights)

# r2py:entity:gt_1
def gtable_add_grob(gt, grob, t, l, b=None, r=None, z=float('inf'), clip="on", name=None):
    return gt.add_grob(grob, t, l, b, r, z, clip, name)

# r2py:entity:pts
def pointsGrob(x, y, pch=1, size=1, default_units="native", name=None, gp=None, vp=None):
    if gp is None:
        gp = {}
    if vp is None:
        vp = {}
    return {
        'x': x, 
        'y': y, 
        'pch': pch, 
        'size': size, 
        'name': name or 'GRID.points.1', 
        'gp': gp, 
        'vp': vp
    }

# suppressPackageStartupMessages(library(gtable))
# library(grid)

# gt <- gtable(widths = unit(c(1, 1), 'null'), heights = unit(c(1, 1), 'null'))
# r2py:entity:gt
gt = gtable(widths=[1, 1], heights=[1, 1])

# pts <- pointsGrob(x = runif(5), y = runif(5))
# r2py:entity:pts
pts = pointsGrob(x=np.random.rand(5), y=np.random.rand(5))

# Add a grob to a single cell (top-right cell)
# gt <- gtable_add_grob(gt, pts, t = 1, l = 2)
# r2py:entity:gt_1
gt = gtable_add_grob(gt, pts, t=1, l=2)

# Add a grob spanning multiple cells
# gt <- gtable_add_grob(gt, pts, t = 1, l = 1, b = 2)
# r2py:entity:gt_2
gt = gtable_add_grob(gt, pts, t=1, l=1, b=2)

# plot(gt)
# r2py:entity:plot
fig = plt.figure(figsize=(6, 6))
gs = fig.add_gridspec(2, 2)

for i, layout in enumerate(gt.layout):
    grob = gt.grobs[i]
    # Create axis spanning from layout['t'] to layout['b']+1 and layout['l'] to layout['r']+1
    ax = fig.add_subplot(gs[layout['t']:layout['b']+1, layout['l']:layout['r']+1])
    ax.scatter(grob['x'], grob['y'])
    ax.axis('off')

plt.tight_layout()
plt.show()