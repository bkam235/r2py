import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Grob:
    def __init__(self, fill="#00000080"):
        self.fill = fill
        self.t = None
        self.b = None
        self.l = None
        self.r = None

class GTable:
    def __init__(self, rows_units, cols_units):
        self.rows = rows_units
        self.cols = cols_units
        self.grobs = []

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, item):
        # This is for dim() simulation
        return None

    def get_dim(self):
        return (len(self.rows), len(self.cols))

def gtable(rows, cols):
    return GTable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    # Set boundaries. If not provided, use default 1-cell size.
    grob.t = t if t is not None else 1
    grob.b = b if b is not None else (t if t is not None else 1)
    grob.l = l if l is not None else 1
    grob.r = r if r is not None else (l if l is not None else 1)
    tab.grobs.append(grob)
    return tab

def gtable_add_cols(tab, units, pos=-1):
    # pos: 0 for left, -1 for right, 1..N for middle
    # R's gtable_add_cols handles spanning: 
    # Grobs spanning the insertion point expand to cover the new column.
    
    # Expand column definitions
    if pos == -1:
        tab.cols = list(tab.cols) + [units]
    elif pos == 0:
        tab.cols = [units] + list(tab.cols)
    else:
        # Insertion in middle (1-indexed in R, but logic usually implies index)
        # The provided R code uses 1, meaning between col 1 and 2
        idx = pos 
        tab.cols = list(tab.cols[:idx]) + [units] + list(tab.cols[idx:])
        
        # Expand grobs that span across the insertion point
        for g in tab.grobs:
            if g.l <= idx and g.r > idx:
                g.r += 1
            elif g.l > idx:
                g.l += 1
                g.r += 1

    return tab

def plot_gtable(tab):
    rows, cols = tab.get_dim()
    fig, ax = plt.subplots()
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    
    for g in tab.grobs:
        # R: t=1, b=3, l=1, r=3 (1-indexed)
        # Python: x=l-1, y=rows-b, width=r-l+1, height=b-t+1
        rect = patches.Rectangle(
            (g.l - 1, rows - g.b), 
            g.r - g.l + 1, 
            g.b - g.t + 1, 
            color=g.fill
        )
        ax.add_patch(rect)
    plt.show()

# Execution
rect = Grob(fill="#00000080")
tab = gtable([1]*3, [1]*3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

dim_tab = tab.get_dim()
print(dim_tab)
plot_gtable(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, 1, 1)
dim_tab2 = tab2.get_dim()
print(dim_tab2)
plot_gtable(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, 1) # default -1
tab3 = gtable_add_cols(tab3, 1, 0)
dim_tab3 = tab3.get_dim()
print(dim_tab3)
plot_gtable(tab3)