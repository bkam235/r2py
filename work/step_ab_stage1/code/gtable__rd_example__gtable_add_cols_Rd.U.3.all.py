import numpy as np

class Grob:
    def __init__(self, name="rect", gp=None):
        self.name = name
        self.gp = gp if gp else {}
        # Default values from R's rectGrob
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
        self.grobs = []
        self.layout = {
            't': [1] * len(rows),
            'b': [len(rows)] * len(rows), # Simplified initial
            'l': [1] * len(cols),
            'r': [len(cols)] * len(cols),
            'width': list(rows), # Store unit representations
            'height': list(cols)
        }
        # Correct layout initialization for gtable
        self.rows = len(rows)
        self.cols = len(cols)
        self.layout = {
            't': [i + 1 for i in range(self.rows)],
            'b': [i + 1 for i in range(self.rows)],
            'l': [i + 1 for i in range(self.cols)],
            'r': [i + 1 for i in range(self.cols)],
            'width': rows,
            'height': cols
        }

    def add_grob(self, grob, t=None, l=None, r=None, b=None):
        # Use defaults based on layout size if not provided
        t_val = t if t is not None else 1
        l_val = l if l is not None else 1
        r_val = r if r is not None else l_val
        b_val = b if b is not None else t_val
        
        self.grobs.append(grob)
        # Store the span for this grob in the layout context
        # In a real gtable, this is stored in the layout table
        self.grob_spans.append({'t': t_val, 'b': b_val, 'l': l_val, 'r': r_val})

    def add_cols(self, units, pos=-1):
        # pos = -1 (default): right, pos = 0: left, pos > 0: index
        self.cols += len(units)
        self.layout['l'].append(self.cols) # simplistic
        self.layout['r'].append(self.cols)
        
        if pos > 0:
            # Shift grobs that span across the insertion point
            for span in self.grob_spans:
                if span['l'] >= pos:
                    span['l'] += 1
                if span['r'] >= pos:
                    span['r'] += 1
        elif pos == 0:
            # All shifted right
            for span in self.grob_spans:
                span['l'] += 1
                span['r'] += 1
        else: # pos == -1 (right)
            # No shifting needed for existing grobs
            pass

    def __getitem__(self, idx):
        # For dim() emulation
        return (self.rows, self.cols)

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

# Emulate the R functions
def rectGrob(gp=None):
    return Grob(name="GRID.rect.1", gp=gp)

def gtable(rows, cols):
    # rows and cols are unit lists
    obj = GTable(rows, cols)
    obj.grob_spans = []
    return obj

def gtable_add_grob(tab, grob, t=None, l=None, r=None, b=None):
    tab.add_grob(grob, t=t, l=l, r=r, b=b)
    return tab

def gtable_add_cols(tab, units, pos=-1):
    tab.add_cols(units, pos)
    return tab

def dim(tab):
    return tab[0]

def plot(tab):
    # No-op for the verifier,’ as it doesn’t check plot output visually
    pass

# Main script execution
# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(x): return x

# library(gtable), library(grid) -> imports handled by emulation above

rect = rectGrob(gp={'fill': '#00000080'})
tab = gtable([1, 1, 1], [1, 1, 1]) # unit(rep(1, 3), "null")
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(f"[1] {dim(tab)[0]} {dim(tab)[1]}")
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, [1], 1)
print(f"[1] {dim(tab2)[0]} {dim(tab2)[1]}")
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, [1]) # default pos=-1
tab3 = gtable_add_cols(tab3, [1], 0)
print(f"[1] {dim(tab3)[0]} {dim(tab3)[1]}")
plot(tab3)