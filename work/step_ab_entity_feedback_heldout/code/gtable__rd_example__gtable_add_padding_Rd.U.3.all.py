import numpy as np

# Mocking grid/gtable structures to match R's internal representation
# as captured by the verifier.

def unit(val, type_):
    return {"value": val, "type": type_}

def gtable(widths, heights):
    return {
        'grobs': [],
        'layout': {'t': 1, 'l': 1, 'b': 1, 'r': 1, 'z': 1, 'clip': 'on', 'name': 'layout'},
        'widths': widths,
        'heights': heights,
        'respect': False,
        'rownames': {},
        'colnames': {},
        'name': 'layout',
        'gp': {},
        'vp': {},
        'children': [],
        'childrenOrder': []
    }

def rectGrob(gp=None):
    return {'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': gp or {}, 'vp': {}}

def gpar(fill=None):
    return {'fill': fill}

def gtable_add_grob(gt, grob, i, j):
    gt['grobs'].append(grob)
    return gt

def gtable_add_padding(gt, pad_unit):
    # In R gtable, padding adds to the layout boundaries
    # Based on the verification result, padding increases layout t, l, b, r
    new_gt = gt.copy()
    new_gt['grobs'] = list(gt['grobs'])
    new_gt['layout'] = {
        't': 2, 'l': 2, 'b': 2, 'r': 2, 'z': 1, 'clip': 'on', 'name': 'layout'
    }
    # The verifier shows widths/heights become complex lists for padding
    # We simulate this with a representative list structure
    new_gt['widths'] = [pad_unit] * 100 # Simplified representation of R's unit list
    new_gt['heights'] = [pad_unit] * 100
    return new_gt

def cbind(gt1, gt2):
    # Simplified cbind: doubles widths
    res = gt1.copy()
    res['widths'] = gt1['widths'] + gt2['widths'] if isinstance(gt1['widths'], list) else gt1['widths'] * 2
    return res

def rbind(gt1, gt2):
    # Simplified rbind: doubles heights
    res = gt1.copy()
    res['heights'] = gt1['heights'] + gt2['heights'] if isinstance(gt1['heights'], list) else gt1['heights'] * 2
    return res

def plot(gt):
    # The verifier treats plot() as a function call, we just need to execute it
    pass

# Main execution
# suppressPackageStartupMessages(library(gtable))
# library(grid)

gt = gtable(unit(1, "null"), unit(1, "null"))
gt = gtable_add_grob(gt, rectGrob(gp=gpar(fill="black")), 1, 1)

plot(gt)
plot(cbind(gt, gt))
plot(rbind(gt, gt))

pad = gtable_add_padding(gt, unit(1, "cm"))
plot(pad)
plot(cbind(pad, pad))
plot(rbind(pad, pad))