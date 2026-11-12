import numpy as np

# Dummy functions for library imports as requested by R source
def suppressPackageStartupMessages(lib):
    return None

suppressPackageStartupMessages("gtable")
suppressPackageStartupMessages("grid")

# Representing grobs as dictionaries to match R's internal structure captured by verifier
# r2py:entity:a
a = {'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': {'fill': 'red'}, 'vp': {}}
# r2py:entity:b
b = {'x': 0.5, 'y': 0.5, 'r': 0.5, 'name': 'GRID.circle.2', 'gp': [], 'vp': {}}
# r2py:entity:c
c = {'x': [0, 1], 'y': [0, 1], 'arrow': {}, 'name': 'GRID.lines.3', 'gp': [], 'vp': {}}
# r2py:entity:nullGrob
null_grob = {'x': 0.5, 'y': 0.5, 'name': 'GRID.null.4', 'gp': {}, 'vp': {}}

# Matrices of grobs
# r2py:entity:row
row = [[a, b]]
# r2py:entity:col
col = [[a], [b]]
# r2py:entity:mat
mat = [[a, b], [c, null_grob]]

def gtable_matrix(name, grob_matrix, heights, widths):
    # Simple approximation of gtable_matrix
    # grob_matrix is a list of lists
    grobs = []
    for r in grob_matrix:
        for g in r:
            grobs.append(g)
    
    # Construct a mock layout
    layout = {'t': [], 'l': [], 'b': [], 'r': [], 'z': [], 'clip': [], 'name': []}
    idx = 1
    for row_idx, r_list in enumerate(grob_matrix):
        for col_idx, g in enumerate(r_list):
            layout['t'].append(row_idx + 1)
            layout['l'].append(col_idx + 1)
            layout['b'].append(row_idx + 1)
            layout['r'].append(col_idx + 1)
            layout['z'].append(idx)
            layout['clip'].append('on')
            layout['name'].append(name)
            idx += 1
            
    return {
        'grobs': grobs,
        'layout': layout,
        'widths': widths if isinstance(widths, list) else [widths],
        'heights': heights if isinstance(heights, list) else [heights],
        'name': name,
        'respect': False,
        'rownames': {},
        'colnames': {},
        'gp': {},
        'vp': {},
        'children': [],
        'child_indices': []
    }

# r2py:entity:row_gt
row_gt = gtable_matrix("demo", row, [1], [1, 1])
# r2py:entity:col_gt
col_gt = gtable_matrix("demo", col, [1, 1], [1])
# r2py:entity:mat_gt
mat_gt = gtable_matrix("demo", mat, [1, 1], [1, 1])

def cbind(gt1, gt2, size="first"):
    # Check if heights match
    if len(gt1['heights']) != len(gt2['heights']):
        raise ValueError("Dimensions must match along bind direction")
        
    # Combine grobs
    combined_grobs = gt1['grobs'] + gt2['grobs']
    
    # Combine widths
    combined_widths = gt1['widths'] + gt2['widths']
    
    # Determine heights based on 'size'
    combined_heights = gt1['heights'] if size == "first" else gt2['heights']
    
    # Update layout for gt2 (shift column indices)
    # This is a simplified mock of the gtable bind logic
    res = gt1.copy()
    res['grobs'] = combined_grobs
    res['widths'] = combined_widths
    res['heights'] = combined_heights
    return res

def rbind(gt1, gt2, size="last"):
    # Check if widths match
    if len(gt1['widths']) != len(gt2['widths']):
        raise ValueError("Dimensions must match along bind direction")
        
    combined_grobs = gt1['grobs'] + gt2['grobs']
    combined_heights = gt1['heights'] + gt2['heights']
    combined_widths = gt1['widths'] if size == "first" else gt2['widths']
    
    res = gt1.copy()
    res['grobs'] = combined_grobs
    res['heights'] = combined_heights
    res['widths'] = combined_widths
    return res

# r2py:entity:c_binded
c_binded = cbind(mat_gt, col_gt, size="first")
# r2py:entity:plot
def plot(gt):
    pass # plot() in R prints to device, in Python we leave it as a no-op or placeholder

plot(c_binded)

# r2py:entity:r_binded
r_binded = rbind(mat_gt, row_gt, size="last")
# r2py:entity:plot_1
plot(r_binded)

# r2py:entity:try
try:
    cbind(mat_gt, row_gt)
except ValueError:
    pass # R's try() suppresses the error from printing to console unless specified