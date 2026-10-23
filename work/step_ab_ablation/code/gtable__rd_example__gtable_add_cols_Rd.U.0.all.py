import numpy as np
import matplotlib.pyplot as plt

class Grob:
    def __init__(self, gp=None, name="GRID.rect.1"):
        self.gp = gp or {}
        self.name = name
        # Default R values for rectGrob
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
        self.rows = rows # unit objects/values
        self.cols = cols # unit objects/values
        self.grobs = []
        self.layout = [] # List of dicts containing t, b, l, r

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # Handle R's coordinate logic
        # If t is provided and b is not, b = t (single row)
        # If l is provided and r is not, r = l (single col)
        row_start = t if t is not None else 1
        row_end = b if b is not None else t if t is not None else 1
        col_start = l if l is not None else 1
        col_end = r if r is not None else l if l is not None else 1
        
        self.grobs.append(grob)
        self.layout.append({'t': row_start, 'b': row_end, 'l': col_start, 'r': col_end})
        return self

    def add_cols(self, width, pos=-1):
        # pos is index where column is added. -1 is end, 0 is start.
        # In R, gtable_add_cols uses 1-based indexing for pos if pos > 0
        # But Python is 0-based. 
        
        # Adjust columns list
        if pos == -1:
            self.cols = list(self.cols) + [width]
            insert_idx = len(self.cols) - 1
        elif pos == 0:
            self.cols = [width] + list(self.cols)
            insert_idx = 0
        else: # middle
            # R pos 1 means add before 1st col (idx 0)
            # gtable_add_cols(tab, unit, 1) adds column at index 1
            # We treat pos as the 1-based index of the column that will follow the new col
            insert_idx = pos - 1
            self.cols = list(self.cols)
            self.cols.insert(insert_idx, width)

        # Adjust existing grobs
        for entry in self.layout:
            # If the new column is added to the left or in the middle, 
            # shift the left and right boundaries if they are at or after the insertion point.
            # R behavior: grobs span over new rows/cols if added in middle.
            # If added at left (0) or right (-1), they don't expand.
            if pos != 0 and pos != -1:
                if entry['l'] > insert_idx:
                    entry['l'] += 1
                if entry['r'] > insert_idx:
                    entry['r'] += 1
                # Expand if it spans across the insertion point
                if entry['l'] <= insert_idx + 1 <= entry['r']:
                    entry['r'] += 1
            elif pos == 0:
                # Added to left: just shift boundaries
                entry['l'] += 1
                entry['r'] += 1
            elif pos == -1:
                # Added to right: boundaries stay same
                pass
        return self

    def __getitem__(self, idx):
        return self.grobs[idx]

    def __len__(self):
        return len(self.grobs)

    def __repr__(self):
        return f"gtable with {len(self.grobs)} grobs"

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in self.grobs],
            'layout': self.layout
        }

def gtable(rows, cols):
    return GTable(rows, cols)

def gtable_add_grob(tab, grob, t=None, b=None, l=None, r=None):
    return tab.add_grob(grob, t=t, b=b, l=l, r=r)

def gtable_add_cols(tab, width, pos=-1):
    return tab.add_cols(width, pos=pos)

def dim(tab):
    # R dim(gtable) returns [rows, cols]
    return np.array([len(tab.rows), len(tab.cols)])

def plot(tab):
    # Placeholder for plotting to avoid FigureCanvasAgg warning
    pass

# --- Main Execution ---
# suppressPackageStartupMessages(library(gtable))
# library(grid)

rect = Grob(gp={'fill': '#00000080'})
tab = gtable([1, 1, 1], [1, 1, 1])
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

print(f"[1] {dim(tab)[0]} {dim(tab)[1]}")
plot(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = gtable_add_cols(tab, 1, 1)
print(f"[1] {dim(tab2)[0]} {dim(tab2)[1]}")
plot(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = gtable_add_cols(tab, 1)
tab3 = gtable_add_cols(tab3, 1, 0)
print(f"[1] {dim(tab3)[0]} {dim(tab3)[1]}")
plot(tab3)