import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class GTable:
    def __init__(self, rows_units, cols_units):
        self.rows = len(rows_units)
        self.cols = len(cols_units)
        self.grobs = []

    def __len__(self):
        return self.rows

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # R's gtable coordinates are 1-indexed.
        # We store the spans: top, bottom, left, right.
        # If only t is provided, it occupies one row.
        # If only l is provided, it occupies one column.
        top = t if t is not None else 1
        bottom = b if b is not None else top
        left = l if l is not None else 1
        right = r if r is not None else left
        
        self.grobs.append({'grob': grob, 't': top, 'b': bottom, 'l': left, 'r': right})
        return self

    def add_cols(self, units, index=None):
        # index: 0 for left, -1 (or None) for right, 1+ for specific position
        # Note: R's gtable_add_cols index logic:
        # index=1 means add before column 1? No, in R gtable, 
        # index 1 means it's inserted at position 1, shifting others.
        # -1 is the default (append to right).
        
        new_cols_count = len(units) if isinstance(units, list) else 1
        
        if index is None or index == -1:
            # Append to right
            self.cols += new_cols_count
            # Grobs spanning to the rightmost edge expand
            for g in self.grobs:
                if g['r'] == self.cols - new_cols_count:
                    g['r'] += new_cols_count
        elif index == 0:
            # Add to left
            self.cols += new_cols_count
            for g in self.grobs:
                g['l'] += new_cols_count
                g['r'] += new_cols_count
        else:
            # Add in the middle (at index)
            # Grobs to the right of the insertion point shift
            # Grobs spanning across the insertion point expand
            self.cols += new_cols_count
            for g in self.grobs:
                if g['l'] >= index:
                    g['l'] += new_cols_count
                    g['r'] += new_cols_count
                elif g['r'] >= index:
                    g['r'] += new_cols_count
        
        return GTable(None, None) # To be replaced by self logic

    def __repr__(self):
        return f"gtable with {self.rows} rows and {self.cols} cols"

def gtable_add_grob(tab, grob, **kwargs):
    return tab.add_grob(grob, **kwargs)

def gtable_add_cols(tab, units, index=-1):
    # The R function returns the modified table
    # To match Python's object modification but R's return style:
    if isinstance(units, float) or isinstance(units, int):
        units = [units]
    
    # Actual logic embedded in the method for simplicity
    tab.add_cols(units, index)
    return tab

def dim(tab):
    return (tab.rows, tab.cols)

def plot(tab):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, tab.cols)
    ax.set_ylim(0, tab.rows)
    ax.invert_yaxis() # R's top=1 is the top of the plot
    ax.axis('off')
    
    for g in tab.grobs:
        # Map 1-indexed spans to 0-indexed coordinates
        # left is the start x, right is the end x
        # top is start y, bottom is end y
        x = g['l'] - 1
        y = g['t'] - 1
        width = g['r'] - g['l'] + 1
        height = g['b'] - g['t'] + 1
        rect = patches.Rectangle((x, y), width, height, color='#00000080', fill=True)
        ax.add_patch(rect)
    
    plt.show()

# Setup
rect = "rectGrob" # Placeholder for the grob object
tab = GTable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(dim(tab))
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, 1, 1)
print(dim(tab2))
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, 1)
tab3 = gtable_add_cols(tab3, 1, 0)
print(dim(tab3))
plot(tab3)