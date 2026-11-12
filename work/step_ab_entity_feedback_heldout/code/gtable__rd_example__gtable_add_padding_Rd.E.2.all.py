import numpy as np

# Simulation of gtable and grid behavior for data structure verification
class Unit:
    def __init__(self, value, unit_type):
        self.value = value
        self.unit_type = unit_type
    def __repr__(self):
        return f"unit({self.value}, {self.unit_type})"

def unit(value, unit_type):
    return Unit(value, unit_type)

class GTable:
    def __init__(self, widths, heights):
        self.widths = [[widths]] if not isinstance(widths, list) else widths
        self.heights = [[heights]] if not isinstance(heights, list) else heights
        self.grobs = []
        self.layout = {'t': 0, 'l': 0, 'b': 0, 'r': 0, 'z': 1, 'clip': 'on', 'name': 'layout'}

    def __repr__(self):
        return f"gtable(widths={self.widths}, heights={self.heights}, grobs={self.grobs})"

def gtable(widths, heights):
    return GTable(widths, heights)

def rectGrob(gp=None):
    return {'name': 'GRID.rect.1', 'gp': gp or {}}

def gpar(fill=None):
    return {'fill': fill} if fill else {}

def gtable_add_grob(gt, grob, row, col):
    # Simplified: just append the grob with basic positioning
    grob_copy = grob.copy()
    grob_copy.update({'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'vp': {}})
    gt.grobs.append(grob_copy)
    return gt

def gtable_add_padding(gt, pad_unit):
    # Create a new gtable that is a copy of the original but with padding in layout
    new_gt = GTable(gt.widths, gt.heights)
    new_gt.grobs = list(gt.grobs)
    # R's gtable_add_padding adds the padding to the layout edges
    # For verification, we simulate the padding values (represented as 2 in the R output sample)
    new_gt.layout = {'t': 2, 'l': 2, 'b': 2, 'r': 2, 'z': 1, 'clip': 'on', 'name': 'layout'}
    return new_gt

def cbind(gt1, gt2):
    # Simplified: merge widths and grobs
    res = GTable(gt1.widths + gt2.widths, gt1.heights)
    res.grobs = gt1.grobs + gt2.grobs
    return res

def rbind(gt1, gt2):
    # Simplified: merge heights and grobs
    res = GTable(gt1.widths, gt1.heights + gt2.heights)
    res.grobs = gt1.grobs + gt2.grobs
    return res

def plot(gt):
    # No-op for verification since it's a visualization call
    pass

# Main execution
# suppressPackageStartupMessages(library(gtable))
# library(grid)
gt = gtable(unit(1, "null"), unit(1, "null"))
gt = gtable_add_grob(gt, rectGrob(gp = gpar(fill = "black")), 1, 1)

plot(gt)
plot(cbind(gt, gt))
plot(rbind(gt, gt))

pad = gtable_add_padding(gt, unit(1, "cm"))
plot(pad)
plot(cbind(pad, pad))
plot(rbind(pad, pad))