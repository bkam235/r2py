# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Mocking gtable and grid logic to maintain structural equivalence
def gtable(widths, heights):
    # r2py:entity:gt
    return {
        'grobs': [],
        'layout': {
            't': [], 'l': [], 'b': [], 'r': [], 
            'z': [], 'clip': [], 'name': []
        },
        'widths': widths,
        'heights': heights,
        'respect': False,
        'rownames': {},
        'colnames': {},
        'name': 'layout',
        'gp': {},
        'vp': {},
        'children': [],
        'childrenOrder': []
    }

# r2py:entity:gt_1
def gtable_add_grob(gt, grob, t, l, b=None, r=None, z=float('inf'), clip="on", name=None):
    # In R, if b or r are not provided, they default to t and l respectively
    if b is None:
        b = t
    if r is None:
        r = l
    
    gt['grobs'].append(grob)
    gt['layout']['t'].append(t)
    gt['layout']['l'].append(l)
    gt['layout']['b'].append(b)
    gt['layout']['r'].append(r)
    gt['layout']['z'].append(z)
    gt['layout']['clip'].append(clip)
    gt['layout']['name'].append(name)
    return gt

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

# Extracting layout lists for easier iteration
t_vals = gt['layout']['t']
l_vals = gt['layout']['l']
b_vals = gt['layout']['b']
r_vals = gt['layout']['r']

for i in range(len(gt['grobs'])):
    grob = gt['grobs'][i]
    # Convert R 1-based indices to 0-based Python indices
    # t=top, l=left, b=bottom, r=right
    top = t_vals[i] - 1
    left = l_vals[i] - 1
    bottom = b_vals[i]
    right = r_vals[i]
    
    ax = fig.add_subplot(gs[top:bottom, left:right])
    ax.scatter(grob['x'], grob['y'])
    ax.axis('off')

plt.tight_layout()
plt.show()