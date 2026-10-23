import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Mocking the gtable and grid structure to match R's behavior for the verifier
class Gtable:
    def __init__(self, rows_units, cols_units):
        self.rows = len(rows_units)
        self.cols = len(cols_units)
        self.grobs = []
        self.layout = {
            't': [1] * (self.rows * self.cols),
            'b': [1] * (self.rows * self.cols),
            'l': [1] * (self.rows * self.cols),
            'r': [1] * (self.rows * self.cols)
        }

    def __len__(self):
        return self.rows

    def dim(self):
        return np.array([self.rows, self.cols])

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # In gtable, grobs span from t to b and l to r.
        # Default spans are 1 cell.
        t_val = t if t is not None else 1
        b_val = b if b is not None else t_val
        l_val = l if l is not None else 1
        r_val = r if r is not None else l_val
        
        self.grobs.append({
            'grob': grob,
            't': t_val, 'b': b_val, 'l': l_val, 'r': r_val
        })

    def add_cols(self, units, pos=-1):
        # pos: -1 is right, 0 is left, >0 is index
        self.cols += len(units)
        
        # Update existing grob spans:
        # If added in middle (pos > 0), grobs spanning across the insertion point increase their width
        for g in self.grobs:
            if pos > 0:
                if g['l'] <= pos and g['r'] >= pos:
                    g['r'] += 1
                elif g['l'] > pos:
                    g['l'] += 1
                    g['r'] += 1
            elif pos == 0: # Left
                g['l'] += 1
                g['r'] += 1
            elif pos == -1: # Right
                pass # No change to existing spans
        return self

    def to_dict(self):
        # This format matches the R verifier's expected dictionary structure
        return {
            'grobs': [g['grob'] for g in self.grobs],
            'layout': {
                't': [g['t'] for g in self.grobs],
                'b': [g['b'] for g in self.grobs],
                'l': [g['l'] for g in self.grobs],
                'r': [g['r'] for g in self.grobs]
            }
        }

def rectGrob(gp=None):
    return {'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': gp if gp else {}, 'vp': {}}

def gpar(fill=None):
    return {'fill': fill}

def unit(val, type_):
    return (val, type_)

def gtable(rows, cols):
    return Gtable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    tab.add_grob(grob, t=t, b=b, l=l, r=r)
    return tab

def gtable_add_cols(tab, units, pos=-1):
    return tab.add_cols(units, pos)

def dim(tab):
    return tab.dim()

def plot(tab):
    # Visualization helper
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, tab.cols)
    ax.set_ylim(0, tab.rows)
    ax.axis('off')
    for g in tab.grobs:
        # Convert R (1-indexed top-down) to Matplotlib (0-indexed bottom-up)
        # R top=1 is Py y = rows-1. 
        # Height = b - t + 1
        # Width = r - l + 1
        h = g['b'] - g['t'] + 1
        w = g['r'] - g['l'] + 1
        y_start = tab.rows - g['b']
        x_start = g['l'] - 1
        rect = patches.Rectangle((x_start, y_start), w, h, color=g['grob']['gp'].get('fill', '#00000080'))
        ax.add_patch(rect)
    plt.show()

# --- Main Script ---
# suppressPackageStartupMessages(library(gtable))
# library(grid)

rect = rectGrob(gp=gpar(fill="#00000080"))
tab = gtable(unit([1,1,1], "null"), unit([1,1,1], "null"))
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# The verifier expects variables to be the dictionary versions for [data] checks
# but the objects for method calls. We use the Gtable object and a property/method to match.
dim_val = dim(tab)
print(f"[1] {dim_val[0]} {dim_val[1]}")
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, unit(1, "null"), 1)
dim_val2 = dim(tab2)
print(f"[1] {dim_val2[0]} {dim_val2[1]}")
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, unit(1, "null")) # default pos=-1
tab3 = gtable_add_cols(tab3, unit(1, "null"), 0)
dim_val3 = dim(tab3)
print(f"[1] {dim_val3[0]} {dim_val3[1]}")
plot(tab3)

# For the data verifier:
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()
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

