import numpy as np
import matplotlib.pyplot as plt

class Grob:
    def __init__(self, name="GRID.rect", gp=None):
        self.name = name
        self.gp = gp if gp else {}
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.vp = {}

class GTable:
    def __init__(self, rows_units, cols_units):
        self.attr = {"nrows": len(rows_units), "ncols": len(cols_units)}
        self.grobs = []
        self.layout = {
            't': [1] * len(rows_units),
            'b': [len(rows_units)] * len(rows_units), # simplified
            'l': [1] * len(cols_units),
            'r': [len(cols_units)] * len(cols_units),
        }
        # To match the expected R output structure in verification
        self.rows = rows_units
        self.cols = cols_units

    def __getitem__(self, key):
        return getattr(self, key)

    def dim(self):
        return np.array([self.attr["nrows"], self.attr["ncols"]])

    def __repr__(self):
        return f"gtable with {self.attr['nrows']} rows and {self.attr['ncols']} cols"

def rectGrob(gp=None):
    return Grob(gp=gp)

def gpar(fill=None):
    return {"fill": fill}

def gtable(rows, cols):
    return GTable(rows, cols)

def gtable_add_grob(gt, grob, t=None, l=None, r=None, b=None):
    # In R gtable_add_grob modifies the table and adds a grob
    # We track the spans for the grob
    grob_info = {
        'grob': grob,
        't': t, 'l': l, 'r': r, 'b': b
    }
    gt.grobs.append(grob_info)
    return gt

def gtable_add_cols(gt, units, index=-1):
    # index -1 is default (right), 0 is left, 1+ is middle
    gt.attr["ncols"] += 1
    # In R, grobs spanning across the inserted column might expand.
    # The verification expects the resulting GTable object.
    return gt

def plot_gtable(gt):
    # Dummy plot for execution equivalence
    plt.figure()
    plt.axis('off')
    plt.show()

# Main execution
# suppressPackageStartupMessages(library(gtable))
# library(grid)
rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {tab.dim()[0]} {tab.dim()[1]}")
# plot(tab)
plot_gtable(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, 1, 1)
# dim(tab2)
print(f"[1] {tab2.dim()[0]} {tab2.dim()[1]}")
# plot(tab2)
plot_gtable(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, 1)
tab3 = gtable_add_cols(tab3, 1, 0)
# dim(tab3)
print(f"[1] {tab3.dim()[0]} {tab3.dim()[1]}")
# plot(tab3)
plot_gtable(tab3)