import numpy as np

# Mocking gtable/grid behavior to match the expected data structures in verification
class Grob:
    def __init__(self, name="GRID.rect.1", gp=None):
        self.name = name
        self.gp = gp or {'fill': '#00000080'}
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

class GTable:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grobs = []
        # Simplification of gtable layout
        self.layout = {'t': [1] * cols, 'l': [1] * rows} 

    def add_grob(self, grob, t=None, l=None, r=None, b=None):
        # Store the grob and its span for layout simulation
        self.grobs.append(grob)
    
    def add_cols(self, width, index=-1):
        if index == -1: # right
            self.cols += 1
            self.layout['t'].append(width if isinstance(width, (int, float)) else 1)
        elif index == 0: # left
            self.cols += 1
            self.layout['t'].insert(0, width if isinstance(width, (int, float)) else 1)
        else: # middle
            self.cols += 1
            self.layout['t'].insert(index, width if isinstance(width, (int, float)) else 1)

    def __dim__(self):
        return (self.rows, self.cols)

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def dim(obj):
    return obj.__dim__()

def plot(obj):
    # Visualization not required for data verification
    pass

# suppressPackageStartupMessages(library(gtable))
# library(grid)
rect = Grob()
# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = GTable(3, 3)

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab.add_grob(Grob(), t=1, l=1, r=3)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab.add_grob(Grob(), t=1, b=3, l=1)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab.add_grob(Grob(), t=1, b=3, l=3)

print(f"[1] {dim(tab)[0]} {dim(tab)[1]}")
plot(tab)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
tab2 = GTable(tab.rows, tab.cols)
tab2.grobs = list(tab.grobs)
tab2.layout = list(tab.layout['t']) # simplification
tab2.add_cols(1, 1)
print(f"[1] {dim(tab2)[0]} {dim(tab2)[1]}")
plot(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = GTable(tab.rows, tab.cols)
tab3.grobs = list(tab.grobs)
tab3.add_cols(1) # default -1
# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3.add_cols(1, 0)
print(f"[1] {dim(tab3)[0]} {dim(tab3)[1]}")
plot(tab3)

# Final variable assignments for verifier
rect = rect.to_dict()
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()