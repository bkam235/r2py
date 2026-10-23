import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mock for suppressPackageStartupMessages
def suppressPackageStartupMessages(expr):
    return expr

# Mock for grid/gtable entities
class Grob:
    def __init__(self, gp=None):
        self.gp = gp

class GTable:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grobs = []

    def __getitem__(self, key):
        return key

    def __len__(self):
        return self.rows

    def dim(self):
        return (self.rows, self.cols)

def unit(val, type_):
    return {"val": val, "type": type_}

def gtable(rows_units, cols_units):
    return GTable(len(rows_units), len(cols_units))

def rectGrob(gp=None):
    return Grob(gp=gp)

def gpar(fill=None):
    return {"fill": fill}

def gtable_add_grob(gt, grob, t=None, b=None, l=None, r=None):
    # Store the constraints as provided in R (1-indexed)
    # t: top, b: bottom, l: left, r: right
    # Default to single cell if not provided
    top = t if t is not None else 1
    bottom = b if b is not None else t if t is not None else 1
    left = l if l is not None else 1
    right = r if r is not None else l if l is not None else 1
    
    gt.grobs.append({'grob': grob, 't': top, 'b': bottom, 'l': left, 'r': right})
    return gt

def gtable_add_cols(gt, col_units, pos=-1):
    # pos: 0 is left, -1 is right, >0 is index (1-indexed in R)
    num_new = len(col_units) if isinstance(col_units, list) else 1
    
    # Logic from gtable: Grobs span over new rows/cols if added in the middle
    # If pos is 0 (left) or -1 (right), the existing grobs' boundaries are not shifted in a way
    # that expands them, but the grid dimensions increase.
    
    if 0 < pos < gt.cols:
        # Shift grobs that start at or after the insertion point
        for g in gt.grobs:
            if g['l'] >= pos + 1:
                g['l'] += num_new
            if g['r'] >= pos + 1:
                g['r'] += num_new
            # If a grob spans across the insertion point, it expands
            if g['l'] <= pos + 1 <= g['r']:
                g['r'] += num_new
    
    gt.cols += num_new
    return gt

def plot(gt):
    fig, ax = plt.subplots()
    ax.set_xlim(0, gt.cols)
    ax.set_ylim(0, gt.rows)
    ax.invert_yaxis()
    ax.axis('off')
    
    for g in gt.grobs:
        # Convert 1-indexed top/left to 0-indexed Matplotlib
        # t=1, b=3 -> ymin=0, ymax=3
        # l=1, r=3 -> xmin=0, xmax=3
        rect = patches.Rectangle(
            (g['l'] - 1, g['t'] - 1), 
            g['r'] - g['l'] + 1, 
            g['b'] - g['t'] + 1, 
            color='#00000080'
        )
        ax.add_patch(rect)
    plt.show()

# Execution
suppressPackageStartupMessages(None) # Dummy call
rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable(unit([1, 1, 1], "null"), unit([1, 1, 1], "null"))
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(tab.dim())
# plot(tab)
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, unit(1, "null"), 1)
# dim(tab2)
print(tab2.dim())
# plot(tab2)
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, unit(1, "null")) # default pos=-1
tab3 = gtable_add_cols(tab3, unit(1, "null"), 0)
# dim(tab3)
print(tab3.dim())
# plot(tab3)
plot(tab3)