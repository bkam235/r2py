import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mocking gtable and grid logic to match R's internal structures
class Grob:
    def __init__(self, name="GRID.rect.1", gp=None):
        self.name = name
        self.gp = gp or {'fill': '#00000080'}
        # Default grid properties from R's rectGrob
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
        self.grobs = []
        self.nrows = len(rows_units)
        self.ncols = len(cols_units)
        # layout is represented as lists of coordinates
        self.layout = {
            't': list(range(1, self.nrows + 1)),
            'b': list(range(1, self.nrows + 1)),
            'l': list(range(1, self.ncols + 1)),
            'r': list(range(1, self.ncols + 1))
        }
        # To match R's gtable, the layout usually stores indices for each grob
        # However, the layout in the verification result is a dict of lists.
        # For the initial empty gtable, we'll initialize these as lists 
        # that will be expanded as grobs are added.
        self.layout = {'t': [], 'l': [], 'b': [], 'r': []}

    def add_grob(self, grob, t=None, l=None, r=None, b=None):
        self.grobs.append(grob)
        # In gtable, if a value is not provided, it defaults to the table boundaries
        self.layout['t'].append(t if t is not None else 1)
        self.layout['l'].append(l if l is not None else 1)
        self.layout['r'].append(r if r is not None else self.ncols)
        self.layout['b'].append(b if b is not None else self.nrows)

    def add_cols(self, units, pos=-1):
        # pos = -1 (default) add to right, 0 add to left, 1+ add in middle
        num_new_cols = len(units) if isinstance(units, list) else 1
        
        # Update existing grobs' right bounds if they span across the insertion point
        for i in range(len(self.grobs)):
            # If adding to the left (0)
            if pos == 0:
                self.layout['l'][i] += num_new_cols
                self.layout['r'][i] += num_new_cols
            # If adding in middle
            elif 0 < pos < self.ncols:
                if self.layout['l'][i] >= pos:
                    self.layout['l'][i] += num_new_cols
                    self.layout['r'][i] += num_new_cols
                elif self.layout['r'][i] >= pos:
                    self.layout['r'][i] += num_new_cols
            # If adding to right (-1)
            elif pos == -1:
                pass # No shift needed for left/right bounds of existing grobs
        
        self.ncols += num_new_cols

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def gtable_add_grob(tab, grob, **kwargs):
    tab.add_grob(grob, **kwargs)
    return tab

def gtable_add_cols(tab, units, pos=-1):
    tab.add_cols(units, pos)
    return tab

def plot_gtable(rows, cols, fills):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis('off')
    for (r, c, w, h) in fills:
        # R's gtable coordinates are 1-indexed, top-down. 
        # Matplotlib is 0-indexed, bottom-up.
        rect = patches.Rectangle((c-1, rows-r), w, h, color='#00000080')
        ax.add_patch(rect)
    plt.show()

# --- Main Script ---

# suppressPackageStartupMessages(library(gtable))
# library(grid)

# rect <- rectGrob(gp = gpar(fill = "#00000080"))
rect = Grob()

# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = GTable([1]*3, [1]*3)

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)

# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)

# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
print(f"[1] {tab.nrows} {tab.ncols}")

# plot(tab)
plot_gtable(tab)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
# We must copy tab to create tab2 so we don't modify tab in place
import copy
tab2 = copy.deepcopy(tab)
tab2 = gtable_add_cols(tab2, [1], 1)

# dim(tab2)
print(f"[1] {tab2.nrows} {tab2.ncols}")

# plot(tab2)
plot_gtable(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = copy.deepcopy(tab)
tab3 = gtable_add_cols(tab3, [1]) # default pos = -1

# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3 = gtable_add_cols(tab3, [1], 0)

# dim(tab3)
print(f"[1] {tab3.nrows} {tab3.ncols}")

# plot(tab3)
plot_gtable(tab3)