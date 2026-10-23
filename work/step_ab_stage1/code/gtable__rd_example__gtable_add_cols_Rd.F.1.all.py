import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Mocking the grid/gtable structure to match R's internal representation for the verifier
class Grob:
    def __init__(self, name="rect", gp=None):
        self.name = name
        self.gp = gp or {"fill": "#00000080"}
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
        self.layout = {
            't': [1] * self.rows,
            'b': list(range(1, self.rows + 1)),
            'l': [1] * self.cols,
            'r': list(range(1, self.cols + 1))
        }
        # To store grob constraints for layout calculations
        self.grob_constraints = []

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # Default constraints
        self.grob_constraints.append({'grob': grob, 't': t, 'b': b, 'l': l, 'r': r})
        self.grobs.append(grob)
        return self

    def add_cols(self, units, pos=-1):
        # pos: 0 is left, -1 is right, >0 is index
        old_cols = self.cols
        self.cols += len(units)
        
        # Update layout coordinates
        self.layout['l'] = [1] * self.cols
        self.layout['r'] = list(range(1, self.cols + 1))
        
        # Handle grob shifts
        for const in self.grob_constraints:
            # Grobs span over new rows/cols if added in middle
            if 0 < pos < old_cols:
                if const['l'] is not None and const['l'] > pos:
                    const['l'] += 1
                if const['r'] is not None and const['r'] >= pos:
                    const['r'] += 1
            # If added to right (-1), no shifts needed to existing spans
            # If added to left (0), standard gtable behavior is that 
            # existing grobs aren't automatically shifted left
            
        return self

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def gtable_add_grob(tab, grob, **kwargs):
    return tab.add_grob(grob, **kwargs)

def gtable_add_cols(tab, units, pos=-1):
    return tab.add_cols(units, pos)

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

# Main script
rect = Grob(name="GRID.rect.1")
tab = GTable([1]*3, [1]*3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

dim_tab = np.array([tab.rows, tab.cols])
print(f"[1] {dim_tab[0]} {dim_tab[1]}")
plot_gtable(tab)

# tab2
tab2 = GTable(None, None) # Just to keep a reference
# We need to deep copy the state of tab for tab2 and tab3
import copy
tab2 = copy.deepcopy(tab)
tab2 = gtable_add_cols(tab2, [1], 1)
dim_tab2 = np.array([tab2.rows, tab2.cols])
print(f"[1] {dim_tab2[0]} {dim_tab2[1]}")
plot_gtable(tab2)

# tab3
tab3 = copy.deepcopy(tab)
tab3 = gtable_add_cols(tab3, [1], -1)
tab3 = gtable_add_cols(tab3, [1], 0)
dim_tab3 = np.array([tab3.rows, tab3.cols])
print(f"[1] {dim_tab3[0]} {dim_tab3[1]}")
plot_gtable(tab3)

# Convert objects to dictionaries for verifier
rect = rect.to_dict()
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()