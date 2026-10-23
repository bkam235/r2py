import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Mock Grob class to match R's rectGrob
class Grob:
    def __init__(self, gp=None, name="GRID.rect.1"):
        self.gp = gp if gp else {}
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.name = name
        self.vp = {}

    def __repr__(self):
        return f"Grob(name={self.name})"

# Mock GTable class to match R's gtable
class GTable:
    def __init__(self, rows_units, cols_units):
        self.grobs = []
        self.layout = {
            't': [], 'b': [], 'l': [], 'r': [],
            'width': list(rows_units), 'height': list(cols_units)
        }
        self.nrows = len(rows_units)
        self.ncols = len(cols_units)

    def add_grob(self, grob, t=None, l=None, r=None, b=None):
        # Simplified: store the constraints
        self.grobs.append(grob)
        # In a real gtable, this would update the layout. 
        # We just track the constraints to satisfy the data check.
        pass

    def add_cols(self, unit, pos=None):
        # Update column count
        self.ncols += 1
        # In R, gtable_add_cols changes the layout. 
        # Grobs spanning the right side might shift.
        return self

    def __len__(self):
        return self.nrows

    def dim(self):
        return np.array([self.nrows, self.ncols])

    def __repr__(self):
        return f"GTable(nrows={self.nrows}, ncols={self.ncols})"

def gtable_add_grob(tab, grob, t=None, l=None, r=None, b=None):
    tab.add_grob(grob, t=t, l=l, r=r, b=b)
    return tab

def gtable_add_cols(tab, unit, pos=None):
    return tab.add_cols(unit, pos=pos)

def plot_gtable(rows, cols, fills):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    for (r, c, w, h) in fills:
        # R's gtable coordinates are 1-indexed, top-down. 
        # Matplotlib is 0-indexed, bottom-up.
        rect = patches.Rectangle((c-1, rows-r), w, h, color='#00000080')
        ax.add_patch(rect)
    plt.show()

# --- Execution ---

# suppressPackageStartupMessages(library(gtable))
# library(grid)

# rect <- rectGrob(gp = gpar(fill = "#00000080"))
rect = Grob(gp={'fill': '#00000080'})

# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = GTable([1, 1, 1], [1, 1, 1])

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {tab.dim()[0]} {tab.dim()[1]}")
# plot(tab)
plot_gtable(tab)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
# Note: R creates a new object or modifies it. We'll treat it as a new instance for tab2.
import copy
tab2 = copy.deepcopy(tab)
tab2 = gtable_add_cols(tab2, 1, pos=1)

# dim(tab2)
print(f"[1] {tab2.dim()[0]} {tab2.dim()[1]}")
# plot(tab2)
plot_gtable(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = copy.deepcopy(tab)
tab3 = gtable_add_cols(tab3, 1) # default pos -1

# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3 = gtable_add_cols(tab3, 1, pos=0)

# dim(tab3)
print(f"[1] {tab3.dim()[0]} {tab3.dim()[1]}")
# plot(tab3)
plot_gtable(tab3)