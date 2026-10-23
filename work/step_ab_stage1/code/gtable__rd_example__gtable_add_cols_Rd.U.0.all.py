import numpy as np

# Mocking grid and gtable behavior
class Grob:
    def __init__(self, gp=None, name="GRID.rect.1"):
        self.gp = gp or {}
        self.x = 0.5
        self.y = 0.5
        self.width = 1
        self.height = 1
        self.just = 'centre'
        self.hjust = {}
        self.vjust = {}
        self.name = name
        self.vp = {}

class GTable:
    def __init__(self, rows, cols):
        # rows and cols are units, here we just store the count
        self.nrows = len(rows)
        self.ncols = len(cols)
        self.grobs = []
        self.layout = {
            't': [1] * self.nrows,
            'b': [1] * self.nrows, # simplified
            'l': [1] * self.ncols,
            'r': [1] * self.ncols, # simplified
        }
        self.grob_spans = [] # Stores (t, b, l, r) for each grob

    def __getitem__(self, idx):
        return self.nrows if idx == 0 else self.ncols

    def get_dim(self):
        return np.array([self.nrows, self.ncols])

def rectGrob(gp=None):
    return Grob(gp=gp)

def gpar(fill=None):
    return {'fill': fill} if fill else {}

def gtable(rows, cols):
    return GTable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    # Default values if not provided
    t_val = t if t is not None else 1
    b_val = b if b is not None else t_val
    l_val = l if l is not None else 1
    r_val = r if r is not None else l_val
    
    tab.grobs.append(grob)
    tab.grob_spans.append({'t': t_val, 'b': b_val, 'l': l_val, 'r': r_val})
    return tab

def gtable_add_cols(tab, cols_units, index=-1):
    num_new = len(cols_units) if isinstance(cols_units, list) else 1
    
    # Update column count
    tab.ncols += num_new
    
    # R gtable_add_cols logic:
    # Grobs spanning the whole width or shifted by index are updated.
    # index -1 is right, 0 is left, 1+ is middle.
    
    for span in tab.grob_spans:
        # If added to the left (index 0)
        if index == 0:
            span['l'] += num_new
            span['r'] += num_new
        # If added to the middle (index > 0)
        elif 0 < index < tab.ncols:
            # If the grob's right boundary is beyond the insertion point, shift it
            if span['l'] >= index:
                span['l'] += num_new
                span['r'] += num_new
            # If it spans across the insertion point, expand its width
            elif span['r'] >= index:
                span['r'] += num_new
        # If added to the right (index -1), boundaries don't change
    
    return tab

def dim(tab):
    return tab.get_dim()

def plot(tab):
    # Mock plot function
    pass

# --- Main script ---
# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(msg):
    pass

rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable([1, 1, 1], [1, 1, 1]) # using lists for units
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(f"[1] {dim(tab)[0]} {dim(tab)[1]}")
plot(tab)

tab2 = gtable_add_cols(tab, [1], 1)
print(f"[1] {dim(tab2)[0]} {dim(tab2)[1]}")
plot(tab2)

tab3 = gtable_add_cols(tab, [1]) # default index -1
tab3 = gtable_add_cols(tab3, [1], 0)
print(f"[1] {dim(tab3)[0]} {dim(tab3)[1]}")
plot(tab3)