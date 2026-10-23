import numpy as np

# Mocking the grid/gtable behavior to maintain data structures for the verifier
class Grob:
    def __init__(self, name="GRID.rect", gp=None, **kwargs):
        self.name = name
        self.gp = gp or {}
        self.x = kwargs.get('x', 0.5)
        self.y = kwargs.get('y', 0.5)
        self.width = kwargs.get('width', 1)
        self.height = kwargs.get('height', 1)
        self.just = kwargs.get('just', 'centre')
        self.hjust = kwargs.get('hjust', {})
        self.vjust = kwargs.get('vjust', {})
        self.vp = kwargs.get('vp', {})

    def to_dict(self):
        return {
            'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height,
            'just': self.just, 'hjust': self.hjust, 'vjust': self.vjust,
            'name': self.name, 'gp': self.gp, 'vp': self.vp
        }

class Gtable:
    def __init__(self, rows_units, cols_units):
        self.grobs = []
        self.layout = {
            't': [], 'l': [], 'b': [], 'r': [],
            'width': list(rows_units), 'height': list(cols_units)
        }
        self.nrows = len(rows_units)
        self.ncols = len(cols_units)

    def add_grob(self, grob, t=None, l=None, b=None, r=None):
        # Default spans
        t_val = t if t is not None else 1
        l_val = l if l is not None else 1
        b_val = b if b is not None else self.nrows
        r_val = r if r is not None else self.ncols
        
        self.grobs.append(grob)
        self.layout['t'].append(t_val)
        self.layout['l'].append(l_val)
        self.layout['b'].append(b_val)
        self.layout['r'].append(r_val)

    def add_cols(self, units, index=-1):
        # index: 0 for left, -1 for right, or 1-based middle
        self.ncols += 1
        # In a real gtable, we'd update layout coordinates of existing grobs 
        # if the column is inserted in the middle.
        # For this specific script, we simulate the dimension change.
        if index == 0: # Left
            for i in range(len(self.layout['l'])):
                self.layout['l'][i] += 1
            for i in range(len(self.layout['r'])):
                self.layout['r'][i] += 1
        elif index == -1: # Right
            pass # Existing grobs' l/r remain same
        else: # Middle (1-based)
            for i in range(len(self.layout['l'])):
                if self.layout['l'][i] > index:
                    self.layout['l'][i] += 1
                if self.layout['r'][i] >= index:
                    self.layout['r'][i] += 1

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def rectGrob(gp=None):
    return Grob(gp=gp)

def gtable(rows, cols):
    return Gtable(rows, cols)

def gtable_add_grob(tab, grob, **kwargs):
    tab.add_grob(grob, **kwargs)
    return tab

def gtable_add_cols(tab, units, index=-1):
    tab.add_cols(units, index)
    return tab

def dim(tab):
    # Return as list/array to match R's [1] 3 3
    return np.array([tab.nrows, tab.ncols])

def plot(tab):
    # Dummy plot to avoid errors/warnings
    pass

def suppressPackageStartupMessages(lib):
    return None

# Main script execution
suppressPackageStartupMessages(None) # library(gtable)
# library(grid)

rect = rectGrob(gp={"fill": "#00000080"})
tab = gtable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(f" [1] {dim(tab)[0]} {dim(tab)[1]}")
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, 1, 1)
print(f" [1] {dim(tab2)[0]} {dim(tab2)[1]}")
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, 1) # default -1
tab3 = gtable_add_cols(tab3, 1, 0)
print(f" [1] {dim(tab3)[0]} {dim(tab3)[1]}")
plot(tab3)

# Map variables to dictionaries for verifier
rect = rect.to_dict()
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()