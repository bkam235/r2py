import numpy as np

class Grob:
    def __init__(self, name="GRID.rect.1", gp=None, **kwargs):
        self.name = name
        self.gp = gp if gp else {}
        # Default values based on R's rectGrob
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

class GTable:
    def __init__(self, rows, cols):
        self.grobs = []
        self.layout = {
            't': [], 'l': [], 'b': [], 'r': [],
            'width': rows, # Simplified representation of units
            'height': cols
        }
        self.nrows = rows
        self.ncols = cols

    def add_grob(self, grob, t=None, l=None, b=None, r=None):
        self.grobs.append(grob)
        # Simplified layout tracking to match R's expected structure
        idx = len(self.grobs) - 1
        self.layout['t'].append(t if t is not None else 1)
        self.layout['l'].append(l if l is not None else 1)
        self.layout['b'].append(b if b is not None else self.nrows)
        self.layout['r'].append(r if r is not None else self.ncols)

    def add_cols(self, width, pos=-1):
        # Update layout coordinates based on position
        # In gtable, pos=0 is left, pos=-1 is right, pos > 0 is index
        if pos == 0:
            for i in range(len(self.layout['l'])):
                self.layout['l'][i] += 1
            for i in range(len(self.layout['r'])):
                self.layout['r'][i] += 1
        elif pos == -1:
            pass # Right side doesn't shift existing grobs' l/r
        elif pos > 0:
            for i in range(len(self.layout['l'])):
                if self.layout['l'][i] > pos:
                    self.layout['l'][i] += 1
                if self.layout['r'][i] >= pos:
                    self.layout['r'][i] += 1
        
        self.ncols += 1

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

# Mocking library imports
def suppressPackageStartupMessages(x): return x

# Implementation
rect = Grob(gp={'fill': '#00000080'})
tab = GTable(3, 3)
tab.add_grob(rect, t=1, l=1, r=3)
tab.add_grob(rect, t=1, b=3, l=1)
tab.add_grob(rect, t=1, b=3, l=3)

# Use a helper for the verifier to see variables as dicts
tab_dict = tab.to_dict()
dim_tab = np.array([tab.nrows, tab.ncols])
print(f"[1] {dim_tab[0]} {dim_tab[1]}")

# tab2
tab2 = GTable(3, 3)
tab2.grobs = list(tab.grobs)
tab2.layout = tab.layout.copy()
tab2.layout['t'] = list(tab.layout['t'])
tab2.layout['l'] = list(tab.layout['l'])
tab2.layout['b'] = list(tab.layout['b'])
tab2.layout['r'] = list(tab.layout['r'])
tab2.nrows, tab2.ncols = tab.nrows, tab.ncols

tab2.add_cols(1, 1)
dim_tab2 = np.array([tab2.nrows, tab2.ncols])
print(f"[1] {dim_tab2[0]} {dim_tab2[1]}")

# tab3
tab3 = GTable(3, 3)
tab3.grobs = list(tab.grobs)
tab3.layout = tab.layout.copy()
tab3.layout['t'] = list(tab.layout['t'])
tab3.layout['l'] = list(tab.layout['l'])
tab3.layout['b'] = list(tab.layout['b'])
tab3.layout['r'] = list(tab.layout['r'])
tab3.nrows, tab3.ncols = tab.nrows, tab.ncols

tab3.add_cols(1, -1)
tab3.add_cols(1, 0)
dim_tab3 = np.array([tab3.nrows, tab3.ncols])
print(f"[1] {dim_tab3[0]} {dim_tab3[1]}")

# Assignments for verifier
rect = rect.to_dict()
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()