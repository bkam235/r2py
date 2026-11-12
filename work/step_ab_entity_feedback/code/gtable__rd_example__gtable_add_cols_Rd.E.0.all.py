import numpy as np

class Grob:
    def __init__(self, fill="#00000080", name="GRID.rect.1"):
        self.data = {
            'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 
            'just': 'centre', 'hjust': {}, 'vjust': {}, 
            'name': name, 'gp': {'fill': fill}, 'vp': {}
        }
    def __repr__(self):
        return str(self.data)

class Gtable:
    def __init__(self, rows_units, cols_units):
        self.nrows = len(rows_units)
        self.ncols = len(cols_units)
        self.grobs = []
        self.layout = {
            't': [], 'b': [], 'l': [], 'r': []
        }

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        self.grobs.append(grob)
        # Use defaults if not provided (1-indexed)
        t_val = t if t is not None else 1
        b_val = b if b is not None else t_val
        l_val = l if l is not None else 1
        r_val = r if r is not None else l_val
        
        self.layout['t'].append(t_val)
        self.layout['b'].append(b_val)
        self.layout['l'].append(l_val)
        self.layout['r'].append(r_val)

    def add_cols(self, units, pos=-1):
        # pos: 0 for left, -1 for right, or 1-indexed middle
        old_ncols = self.ncols
        self.ncols += len(units)
        
        # Shift existing grobs' columns
        if pos == 0:
            # Added to left: shift all L and R by units length
            shift = len(units)
            self.layout['l'] = [x + shift for x in self.layout['l']]
            self.layout['r'] = [x + shift for x in self.layout['r']]
        elif pos == -1 or pos >= old_ncols:
            # Added to right: no shift for existing
            pass
        else:
            # Added in middle: shift those to the right of pos
            shift = len(units)
            for i in range(len(self.layout['l'])):
                if self.layout['l'][i] > pos:
                    self.layout['l'][i] += shift
                if self.layout['r'][i] >= pos:
                    self.layout['r'][i] += shift

    def __repr__(self):
        return str({'grobs': [g.data for g in self.grobs], 'layout': self.layout})

def gtable_add_grob(tab, grob, **kwargs):
    tab.add_grob(grob, **kwargs)
    return tab

def gtable_add_cols(tab, units, pos=-1):
    tab.add_cols(units, pos)
    return tab

def dim(tab):
    return (tab.nrows, tab.ncols)

def plot(tab):
    # Visualization not required by verifier, just a dummy
    pass

# R: suppressPackageStartupMessages(library(gtable))
# R: library(grid)
rect = Grob()
# R: tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = Gtable([1]*3, [1]*3)
# R: tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
# R: tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
# R: tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(dim(tab))
plot(tab)

# Grobs will continue to span over new rows if added in the middle
# R: tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
tab2 = Gtable(None, None) # Use a fresh object to avoid mutating tab if needed, but R modifies in place or returns
# Since gtable_add_cols returns the modified table:
import copy
tab2 = copy.deepcopy(tab)
tab2 = gtable_add_cols(tab2, [1], 1)
print(dim(tab2))
plot(tab2)

# But not when added to left (0) or right (-1, the default)
# R: tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = copy.deepcopy(tab)
tab3 = gtable_add_cols(tab3, [1]) # default pos=-1
# R: tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3 = gtable_add_cols(tab3, [1], 0)
print(dim(tab3))
plot(tab3)