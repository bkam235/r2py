import numpy as np

class Grob:
    def __init__(self, gp=None, name="GRID.rect.1"):
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.name = name
        self.gp = gp if gp else {}
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
        self.layout = {
            't': [], 'b': [], 'l': [], 'r': [],
            'width': list(rows_units), 'height': list(cols_units)
        }
        # Note: R gtable layout lists t, b, l, r correspond to the grobs
        self.rows = len(rows_units)
        self.cols = len(cols_units)

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # In gtable, if b is not provided, it's t. If r is not provided, it's l.
        # R indices are 1-based.
        g_t = t if t is not None else 1
        g_b = b if b is not None else g_t
        g_l = l if l is not None else 1
        g_r = r if r is not None else g_l
        
        self.grobs.append(grob)
        self.layout['t'].append(g_t)
        self.layout['b'].append(g_b)
        self.layout['l'].append(g_l)
        self.layout['r'].append(g_r)
        return self

    def add_cols(self, units, pos=-1):
        # pos: 0 is left, -1 is right, positive is index
        if pos == 0:
            # Added to left
            self.cols += len(units)
            for i in range(len(self.layout['l'])):
                self.layout['l'][i] += len(units)
            for i in range(len(self.layout['r'])):
                self.layout['r'][i] += len(units)
        elif pos == -1:
            # Added to right
            self.cols += len(units)
            # Grobs don't shift when added to right
        else:
            # Added in middle (pos is 1-indexed)
            self.cols += len(units)
            for i in range(len(self.layout['l'])):
                if self.layout['l'][i] > pos:
                    self.layout['l'][i] += len(units)
                if self.layout['r'][i] > pos:
                    self.layout['r'][i] += len(units)
        
        # Update width/height lists to match new dim
        # This is a simplification of R's unit handling
        self.layout['width'] = [1] * self.rows # simplified
        self.layout['height'] = [1] * self.cols # simplified
        return self

    def __len__(self):
        return (self.rows, self.cols)

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def dim(obj):
    return np.array(obj.layout['width'], dtype=int) if hasattr(obj, 'layout') else np.array([0]) # Mock

# For the specific dim() call in the script, it returns (rows, cols)
def get_dim(obj):
    return np.array([obj.rows, obj.cols])

# Simulation of the R script
# suppressPackageStartupMessages(library(gtable))
# library(grid)

rect = Grob(gp={'fill': '#00000080'})

# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = GTable([1, 1, 1], [1, 1, 1])

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab = tab.add_grob(rect, t=1, l=1, r=3)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab = tab.add_grob(rect, t=1, b=3, l=1)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab = tab.add_grob(rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {get_dim(tab)[0]} {get_dim(tab)[1]}")
# plot(tab) - No-op for data capture

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
# Note: gtable_add_cols modifies the object or returns a copy. R is often copy-on-modify.
import copy
tab_copy = copy.deepcopy(tab)
tab2 = tab_copy.add_cols([1], pos=1)

# dim(tab2)
print(f"[1] {get_dim(tab2)[0]} {get_dim(tab2)[1]}")
# plot(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab_copy3 = copy.deepcopy(tab)
tab3 = tab_copy3.add_cols([1]) # default -1

# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3 = tab3.add_cols([1], pos=0)

# dim(tab3)
print(f"[1] {get_dim(tab3)[0]} {get_dim(tab3)[1]}")
# plot(tab3)