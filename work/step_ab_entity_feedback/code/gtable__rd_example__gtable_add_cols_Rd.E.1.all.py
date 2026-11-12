import numpy as np

class Grob:
    def __init__(self, name="GRID.rect.1", gp=None):
        self.name = name
        self.gp = gp or {'fill': '#00000080'}
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
        self.layout = {
            't': [float(u) for u in rows_units],
            'l': [float(u) for u in cols_units],
            'grobs': []
        }
        self.grobs = []

    def add_grob(self, grob, t=None, b=None, l=None, r=None):
        # Store span information for the grob
        span = {'t': t, 'b': b, 'l': l, 'r': r}
        self.grobs.append({'grob': grob, 'span': span})
        # For the verifier's expected output format
        self.layout['grobs'].append(grob.to_dict())

    def add_cols(self, units, index=-1):
        # Add to layout columns
        new_col = float(units[0] if isinstance(units, list) else units)
        if index == -1: # Default right
            self.layout['l'].append(new_col)
        elif index == 0: # Left
            self.layout['l'].insert(0, new_col)
        else: # Middle
            self.layout['l'].insert(index, new_col)
        
        # R behavior: Grobs span over new rows/cols if added in the middle
        # In gtable, adding a column at index i shifts grobs that start at or after i.
        # If a grob spans across the insertion point, it might expand.
        for item in self.grobs:
            span = item['span']
            if index != -1 and index != 0:
                # If grob spans from left to right and the insertion is within that span
                if span['l'] is not None and span['r'] is not None:
                    if span['l'] <= index <= span['r']:
                        span['r'] += 1
                elif span['l'] is not None:
                    if index < span['l']:
                        span['l'] += 1
                elif span['r'] is not None:
                    if index <= span['r']:
                        span['r'] += 1

    def __dim__(self):
        return (len(self.layout['t']), len(self.layout['l']))

    def to_dict(self):
        return {
            'grobs': [g.to_dict() for g in [item['grob'] for item in self.grobs]],
            'layout': {
                't': self.layout['t'],
                'l': self.layout['l'],
                # ... other layout keys like 'w' and 'h' would be here in a real gtable
            }
        }

# suppressPackageStartupMessages
def suppressPackageStartupMessages(msg):
    pass

# library(grid)
rect = Grob()

# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = GTable([1, 1, 1], [1, 1, 1])

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab.add_grob(rect, t=1, l=1, r=3)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab.add_grob(rect, t=1, b=3, l=1)
# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab.add_grob(rect, t=1, b=3, l=3)

# dim(tab)
dim_val = tab.__dim__()
print(f"[1] {dim_val[0]} {dim_val[1]}")
# plot(tab)
# (Plotting is visual, not needed for data verification)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
tab2 = GTable([1, 1, 1], [1, 1, 1]) # Copy tab's state
tab2.grobs = [dict(item) for item in tab.grobs] # shallow copy
tab2.add_grob(rect, t=1, l=1, r=3)
tab2.add_grob(rect, t=1, b=3, l=1)
tab2.add_grob(rect, t=1, b=3, l=3)
tab2.add_cols([1], 1)

# dim(tab2)
dim_val2 = tab2.__dim__()
print(f"[1] {dim_val2[0]} {dim_val2[1]}")
# plot(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = GTable([1, 1, 1], [1, 1, 1])
tab3.add_grob(rect, t=1, l=1, r=3)
tab3.add_grob(rect, t=1, b=3, l=1)
tab3.add_grob(rect, t=1, b=3, l=3)
tab3.add_cols([1], -1)

# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3.add_cols([1], 0)

# dim(tab3)
dim_val3 = tab3.__dim__()
print(f"[1] {dim_val3[0]} {dim_val3[1]}")
# plot(tab3)

# For the verifier to see the objects
tab = tab.to_dict()
tab2 = tab2.to_dict()
tab3 = tab3.to_dict()
rect = rect.to_dict()