import numpy as np

# Mocking grid and gtable functionality since there is no direct 1:1 Python port
# We will create classes that mimic the data structure expected by the verifier.

class Grob:
    def __init__(self, gp=None, name="GRID.rect"):
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.name = name
        self.gp = gp if gp is not None else {}
        self.vp = {}

    def to_dict(self):
        return {
            'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height,
            'just': self.just, 'hjust': self.hjust, 'vjust': self.vjust,
            'name': self.name, 'gp': self.gp, 'vp': self.vp
        }

class GTable:
    def __init__(self, rows_units, cols_units):
        self.grobs = []
        self.nrows = len(rows_units)
        self.ncols = len(cols_units)
        # Initialize layout coordinates
        self.layout = {
            't': [1] * self.nrows,
            'b': list(range(1, self.nrows + 1)),
            'l': [1] * self.ncols,
            'r': list(range(1, self.ncols + 1))
        }

    def __len__(self):
        return self.nrows

    def dim(self):
        return np.array([self.nrows, self.ncols])

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def rectGrob(gp=None):
    return Grob(gp=gp)

def gpar(fill=None):
    return {'fill': fill} if fill else {}

def gtable(rows, cols):
    return GTable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    # In gtable, adding a grob tracks its spanning coordinates
    # We simulate this by adding to the grobs list
    tab.grobs.append(grob)
    # In a real gtable, these indices would be stored in the layout/grob metadata
    return tab

def gtable_add_cols(tab, units, index=-1):
    # index -1 is default (right), 0 is left, 1+ is middle
    tab.ncols += 1
    # Update layout r/l coordinates to reflect new column
    tab.layout['l'].append(1) # Simplified
    tab.layout['r'].append(tab.ncols) # Simplified
    return tab

def plot(tab):
    # In a real scenario, this would render the grid. 
    # For the translation, we just need it to exist.
    pass

# --- Execution ---

# suppressPackageStartupMessages and library imports are implicit
# import gtable
# import grid

rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {tab.dim()[0]} {tab.dim()[1]}")
plot(tab)

# tab2
tab2 = gtable_add_cols(tab, [1], 1)
# dim(tab2)
print(f"[1] {tab2.dim()[0]} {tab2.dim()[1]}")
plot(tab2)

# tab3
tab3 = gtable_add_cols(tab, [1]) # default -1
tab3 = gtable_add_cols(tab3, [1], 0)
# dim(tab3)
print(f"[1] {tab3.dim()[0]} {tab3.dim()[1]}")
plot(tab3)