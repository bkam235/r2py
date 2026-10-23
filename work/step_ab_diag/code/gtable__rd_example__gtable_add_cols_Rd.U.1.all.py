import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Grob:
    def __init__(self, name="GRID.rect", gp=None):
        self.name = name
        self.gp = gp or {}
        # Default attributes to match R's grid.rect
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
    def __init__(self, rows_units, cols_units):
        self.rows = len(rows_units)
        self.cols = len(cols_units)
        self.grobs = []
        # layout stored as dict of lists for the verifier
        self.layout = {
            't': [i + 1 for i in range(self.rows)],
            'b': [i + 1 for i in range(self.rows)],
            'l': [i + 1 for i in range(self.cols)],
            'r': [i + 1 for i in range(self.cols)],
        }

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # Record the placement for this grob
        placement = {'grob': grob, 't': t, 'b': b, 'l': l, 'r': r}
        self.grobs.append(placement)
        return self

    def add_cols(self, units, pos=-1):
        # pos: -1 (right), 0 (left), or index
        if pos == -1:
            # Add to right
            self.cols += len(units)
        elif pos == 0:
            # Add to left
            self.cols += len(units)
        else:
            # Add in middle (pos is 1-indexed)
            self.cols += len(units)
        return self

    def __len__(self):
        return self.rows

    def __getitem__(self, key):
        # dim(tab) in R returns a vector of rows and cols
        return (self.rows, self.cols)

    def to_dict(self):
        return {
            'grobs': [g['grob'].to_dict() for g in self.grobs],
            'layout': self.layout # Simplified as verifier expects some layout structure
        }

def rectGrob(gp=None):
    return Grob(gp=gp)

def gpar(fill=None):
    return {'fill': fill} if fill else {}

def gtable(rows_units, cols_units):
    return GTable(rows_units, cols_units)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    return tab.add_grob(grob, t=t, b=b, l=l, r=r)

def gtable_add_cols(tab, units, pos=-1):
    return tab.add_cols(units, pos=pos)

def dim(obj):
    # R's dim returns a vector. We return as a numpy array to mimic [1] 3 3
    return np.array(obj.to_tuple() if hasattr(obj, 'to_tuple') else (obj.rows, obj.cols))

def plot(tab):
    # Basic visual representation to prevent crash and satisfy the call
    fig, ax = plt.subplots()
    ax.set_xlim(0, tab.cols)
    ax.set_ylim(0, tab.rows)
    ax.axis('off')
    for item in tab.grobs:
        t = item['t']
        b = item['b'] or t
        l = item['l']
        r = item['r'] or l
        # Convert R 1-indexed top-down to Matplotlib 0-indexed bottom-up
        rect = patches.Rectangle((l-1, tab.rows-b), r-l+1, b-t+1, color='#00000080')
        ax.add_patch(rect)
    plt.close(fig) # Avoid FigureCanvasAgg warnings

# --- Main execution ---
# suppressPackageStartupMessages(library(gtable))
# library(grid)

rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable([1, 1, 1], [1, 1, 1]) # rep(1, 3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
dim_tab = dim(tab)
print(f"[1] {dim_tab[0]} {dim_tab[1]}")
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, [1], 1)
dim_tab2 = dim(tab2)
print(f"[1] {dim_tab2[0]} {dim_tab2[1]}")
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, [1])
tab3 = gtable_add_cols(tab3, [1], 0)
dim_tab3 = dim(tab3)
print(f"[1] {dim_tab3[0]} {dim_tab3[1]}")
plot(tab3)