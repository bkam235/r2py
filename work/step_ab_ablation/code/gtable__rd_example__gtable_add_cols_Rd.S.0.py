import matplotlib.pyplot as plt
import matplotlib.patches as patches

class GTable:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grobs = []

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # R coordinates are 1-indexed. 
        # Store boundaries to handle column insertions.
        span = {
            't': t if t is not None else 1,
            'b': b if b is not None else t if t is not None else 1,
            'l': l if l is not None else 1,
            'r': r if r is not None else l if l is not None else 1,
            'grob': grob
        }
        self.grobs.append(span)

    def add_cols(self, width, pos):
        # pos: 0 = left, -1 = right, 1+ = index
        # R's gtable_add_cols(tab, unit, 1) adds before column 1
        if pos == -1 or pos >= self.cols:
            # Add to right
            self.cols += 1
            # Grobs spanning to the right edge might expand or stay
            # In gtable, grobs spanning to the edge usually don't expand unless specified
            # but if they are added 'in the middle', they shift.
        elif pos == 0:
            # Add to left
            self.cols += 1
            for g in self.grobs:
                g['l'] += 1
                g['r'] += 1
        else:
            # Add at index pos (1-indexed)
            self.cols += 1
            for g in self.grobs:
                if g['l'] >= pos:
                    g['l'] += 1
                if g['r'] >= pos:
                    g['r'] += 1

    def __dim__(self):
        return (self.rows, self.cols)

def plot_gtable(tab):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, tab.cols)
    ax.set_ylim(0, tab.rows)
    ax.axis('off')
    ax.invert_yaxis()
    for g in tab.grobs:
        # Convert 1-indexed (top-down) to 0-indexed (top-down)
        # x = l-1, y = t-1, width = r-l+1, height = b-t+1
        rect = patches.Rectangle(
            (g['l'] - 1, g['t'] - 1), 
            g['r'] - g['l'] + 1, 
            g['b'] - g['t'] + 1, 
            color='#00000080'
        )
        ax.add_patch(rect)
    plt.show()

# Simulation of R script
# suppressPackageStartupMessages(library(gtable))
# library(grid)
rect = "#00000080" # Simplified grob representation

tab = GTable(3, 3)
tab.add_grob(rect, t=1, l=1, r=3)
tab.add_grob(rect, t=1, b=3, l=1)
tab.add_grob(rect, t=1, b=3, l=3)

print(tab.__dim__())
plot_gtable(tab)

# Grobs will continue to span over new rows if added in the middle
tab2 = GTable(tab.rows, tab.cols)
tab2.grobs = [g.copy() for g in tab.grobs]
tab2.add_cols(1, 1) # unit(1, "null"), 1
print(tab2.__dim__())
plot_gtable(tab2)

# But not when added to left (0) or right (-1, the default)
tab3 = GTable(tab.rows, tab.cols)
tab3.grobs = [g.copy() for g in tab.grobs]
tab3.add_cols(1, -1) # unit(1, "null") -> default is -1
tab3.add_cols(1, 0)   # unit(1, "null"), 0
print(tab3.__dim__())
plot_gtable(tab3)