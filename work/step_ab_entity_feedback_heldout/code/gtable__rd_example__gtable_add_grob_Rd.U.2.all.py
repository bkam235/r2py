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
        # In R, gtable layout is typically a data frame with columns: 
        # t, l, b, r, w, h, z, clip, name
        self.layout = pd.DataFrame(columns=['t', 'l', 'b', 'r', 'w', 'h', 'z', 'clip', 'name'])

    def add_grob(self, grob, t, l, b=None, r=None, z=float('inf'), clip="on", name=None):
        if b is None: b = t
        if r is None: r = l
        
        self.grobs.append(grob)
        new_row = pd.DataFrame([{
            't': t, 
            'l': l, 
            'b': b, 
            'r': r, 
            'w': 1, # Simple mock for width/height
            'h': 1, 
            'z': z, 
            'clip': clip, 
            'name': name
        }])
        self.layout = pd.concat([self.layout, new_row], ignore_index=True)
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

for i, row in gt.layout.iterrows():
    grob = gt.grobs[i]
    # R indices are 1-based; convert to 0-based for Python GridSpec
    # layout['t'] to layout['b']
    t_idx = int(row['t']) - 1
    b_idx = int(row['b'])
    l_idx = int(row['l']) - 1
    r_idx = int(row['r'])
    
    ax = fig.add_subplot(gs[t_idx:b_idx, l_idx:r_idx])
    ax.scatter(grob['x'], grob['y'])
    ax.axis('off')

plt.tight_layout()
plt.show()