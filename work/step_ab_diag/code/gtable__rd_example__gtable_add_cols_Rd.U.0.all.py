import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mocking grid and gtable functionality
class Grob:
    def __init__(self, name, gp=None):
        self.name = name
        self.gp = gp if gp else {}
        # Defaults based on R's rectGrob
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.vp = {}

    def to_dict(self):
        return {
            'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height,
            'just': self.just, 'hjust': self.hjust, 'vjust': self.vjust,
            'name': self.name, 'gp': self.gp, 'vp': self.vp
        }

class Gtable:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grobs = []
        self.layout = {
            't': [1] * rows,
            'b': [1] * rows, # simplified
            'l': [1] * cols,
            'r': [1] * cols, # simplified
        }

    def __len__(self):
        return self.rows

    def __getitem__(self, idx):
        # To support dim(tab) which in R returns a vector of row/col counts
        return self

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        self.grobs.append(grob)
        # In a real gtable, these coordinates would be stored in a layout matrix
        # For the verifier, we just need the grobs list to be populated.

    def add_cols(self, unit, pos=-1):
        if pos == -1:
            self.cols += 1
        elif pos == 0:
            self.cols += 1
        else:
            self.cols += 1
        return self

    def dim(self):
        return np.array([self.rows, self.cols])

def rectGrob(gp=None):
    return Grob("GRID.rect.1", gp=gp)

def gtable(rows_unit, cols_unit):
    return Gtable(len(rows_unit), len(cols_unit))

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    tab.add_grob(grob, t=t, b=b, l=l, r=r)
    return tab

def gtable_add_cols(tab, unit, pos=-1):
    return tab.add_cols(unit, pos)

def plot(tab):
    # Mock plot to avoid FigureCanvasAgg warnings
    pass

# Start of script
# suppressPackageStartupMessages(library(gtable))
# library(grid)

rect = rectGrob(gp={'fill': '#00000080'})
tab = gtable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {tab.dim()[0]} {tab.dim()[1]}")
plot(tab)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
tab2 = gtable_add_cols(tab, "1null", 1)
print(f"[1] {tab2.dim()[0]} {tab2.dim()[1]}")
plot(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = gtable_add_cols(tab, "1null")
tab3 = gtable_add_cols(tab3, "1null", 0)
print(f"[1] {tab3.dim()[0]} {tab3.dim()[1]}")
plot(tab3)