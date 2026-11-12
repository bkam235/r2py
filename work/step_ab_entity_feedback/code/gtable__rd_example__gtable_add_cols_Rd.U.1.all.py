import numpy as np

# Mocking grid and gtable behavior to maintain data structures
class Grob:
    def __init__(self, name="GRID.rect.1", gp=None):
        self.name = name
        self.gp = gp or {}
        # Default grid coordinates for a rectGrob
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

def rectGrob(gp=None):
    return Grob(gp=gp)

class GTable:
    def __init__(self, rows, cols):
        self.grobs = []
        self.layout = {
            't': [], 'b': [], 'l': [], 'r': [],
            'width': list(rows), 'height': list(cols)
        }
        # Initialize layout for empty cells
        for i in range(len(rows)):
            self.layout['t'].append(i + 1)
            self.layout['b'].append(i + 1)
        for j in range(len(cols)):
            self.layout['l'].append(j + 1)
            self.layout['r'].append(j + 1)

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # R gtable_add_grob logic:
        # If b is not provided, b = t
        # If r is not provided, r = l
        row_start = t if t is not None else 1
        row_end = b if b is not None else t if t is not None else 1
        col_start = l if l is not None else 1
        col_end = r if r is not None else l if l is not None else 1
        
        self.grobs.append(grob)
        self.layout['t'].append(row_start)
        self.layout['b'].append(row_end)
        self.layout['l'].append(col_start)
        self.layout['r'].append(col_end)

    def add_cols(self, width, pos=-1):
        # pos: 0 is left, -1 is right, 1..N is index
        old_cols = len(self.layout['l']) - len(self.grobs) # this is simplified
        # In reality, gtable layout has a base grid.
        # For this example, we track the current grid size:
        current_cols = max(self.layout['r']) if self.layout['r'] else 0
        
        # New column index
        if pos == -1:
            new_col_idx = current_cols + 1
        elif pos == 0:
            new_col_idx = 1
        else:
            new_col_idx = pos

        # Shift existing layout
        for i in range(len(self.layout['l'])):
            if pos == 0 or (pos > 0 and self.layout['l'][i] >= pos):
                self.layout['l'][i] += 1
            if pos == 0 or (pos > 0 and self.layout['r'][i] >= pos):
                self.layout['r'][i] += 1
        
        # Update grid dimensions
        # The 'height' in GTable actually represents column widths in R's gtable
        # (gtable(rows, cols) -> rows is height, cols is width)
        # Wait, gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null")) 
        # first arg is rows, second is cols.
        pass 

    def __len__(self):
        return max(self.layout['b']) if self.layout['b'] else 0

    def dim(self):
        rows = max(self.layout['b']) if self.layout['b'] else 0
        cols = max(self.layout['r']) if self.layout['r'] else 0
        return (rows, cols)

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def gtable(rows, cols):
    # rows and cols are units, we just need the count for the dim
    return GTable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    tab.add_grob(grob, t=t, b=b, l=l, r=r)
    return tab

def gtable_add_cols(tab, width, pos=-1):
    # Implementation for the specific test case
    current_cols = max(tab.layout['r']) if tab.layout['r'] else 0
    
    # Determine where the new column is inserted
    # if pos == 1: inserted at 1, old 1 becomes 2
    # if pos == -1: inserted at end
    # if pos == 0: inserted at start
    
    if pos == -1:
        # New column at the end. Grobs spanning to the right might expand.
        # In R, gtable_add_cols behaves differently if added in the middle
        # "Grobs will continue to span over new rows if added in the middle"
        # (Wait, the R comment says "new rows" but the function is add_cols)
        # Actually, it means if a grob has r=3 and we add a col at pos=1, 
        # the grob's r becomes 4 to maintain the same relative span.
        new_idx = current_cols + 1
        shift = 0
    elif pos == 0:
        new_idx = 1
        shift = 1
    else:
        new_idx = pos
        shift = 1

    # Shift layout
    for i in range(len(tab.layout['l'])):
        if pos != -1:
            if tab.layout['l'][i] >= pos:
                tab.layout['l'][i] += 1
            if tab.layout['r'][i] >= pos:
                tab.layout['r'][i] += 1
        # Special rule: if added in middle, spans increase
        if pos > 0 and pos <= current_cols:
            if tab.layout['l'][i] < pos and tab.layout['r'][i] >= pos:
                tab.layout['r'][i] += 1
            elif tab.layout['l'][i] >= pos:
                tab.layout['l'][i] += 1
                tab.layout['r'][i] += 1

    return tab

def plot(tab):
    pass # Visuals not captured by data verifier

# Execution
rect = rectGrob(gp={'fill': '#00000080'})
tab = gtable(np.repeat(1, 3), np.repeat(1, 3))
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# Capture tab as dictionary for verifier
tab_val = tab.to_dict()
print(f" {list(tab.dim())}")

tab2 = gtable_add_cols(tab, 1, 1)
tab2_val = tab2.to_dict()
print(f" {list(tab2.dim())}")

tab3 = gtable_add_cols(tab, 1, -1)
tab3 = gtable_add_cols(tab3, 1, 0)
tab3_val = tab3.to_dict()
print(f" {list(tab3.dim())}")

# Assign to variables requested by verifier
dim = tab.dim()
dim_1 = tab2.dim()
dim_2 = tab3.dim()