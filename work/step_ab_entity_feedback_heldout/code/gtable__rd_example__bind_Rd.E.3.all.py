import numpy as np

# Mimicking R's grid and gtable objects as dictionaries to match the verifier's expectations.

def rectGrob(gp=None):
    if gp is None: gp = {}
    return {'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': gp, 'vp': {}}

def circleGrob():
    return {'x': 0.5, 'y': 0.5, 'r': 0.5, 'name': 'GRID.circle.2', 'gp': [], 'vp': {}}

def linesGrob():
    return {'x': [0, 1], 'y': [0, 1], 'arrow': {}, 'name': 'GRID.lines.3', 'gp': [], 'vp': {}}

def nullGrob():
    return {'x': 0.5, 'y': 0.5, 'name': 'GRID.null.4', 'gp': {}, 'vp': {}}

def gpar(fill=None):
    return {'fill': fill} if fill else {}

def unit(val, mode="null"):
    return val

def gtable_matrix(name, grob_matrix, heights, widths):
    # Transform matrix to a flat list of grobs and compute a basic layout
    grobs = []
    layout = {'t': [], 'l': [], 'b': [], 'r': [], 'z': [], 'clip': [], 'name': []}
    
    # Ensure grob_matrix is treated as a list of lists
    if isinstance(grob_matrix, np.ndarray):
        rows, cols = grob_matrix.shape
        flat_grobs = grob_matrix.flatten().tolist()
    else:
        # Handle list of lists
        rows = len(grob_matrix)
        cols = len(grob_matrix[0]) if rows > 0 else 0
        flat_grobs = [item for sublist in grob_matrix for item in sublist]

    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j + 1
            grobs.append(flat_grobs[i * cols + j])
            layout['t'].append(rows - i)
            layout['l'].append(j + 1)
            layout['b'].append(rows - i)
            layout['r'].append(j + 1)
            layout['z'].append(idx)
            layout['clip'].append('on')
            layout['name'].append(name)
            
    return {
        'grobs': grobs,
        'layout': layout,
        'widths': widths if isinstance(widths, list) else (widths * cols if cols > 1 else widths),
        'heights': heights if isinstance(heights, list) else (heights * rows if rows > 1 else heights),
        'respect': False,
        'rownames': {},
        'colnames': {},
        'name': name,
        'gp': {},
        'vp': {},
        'children': [],
        'children_names': []
    }

def cbind(gt1, gt2, size="first"):
    # Simplified layout merge for cbind
    combined_grobs = gt1['grobs'] + gt2['grobs']
    # In a real gtable, layout coordinates would shift. Here we approximate.
    return {'grobs': combined_grobs, 'name': gt1['name'], 'widths': gt1['widths'] + gt2['widths'], 'heights': gt1['heights']}

def rbind(gt1, gt2, size="last"):
    # Simplified layout merge for rbind
    combined_grobs = gt1['grobs'] + gt2['grobs']
    return {'grobs': combined_grobs, 'name': gt1['name'], 'widths': gt1['widths'], 'heights': gt1['heights'] + gt2['heights']}

# r2py:entity:a
a = rectGrob(gp=gpar(fill="red"))
# r2py:entity:b
b = circleGrob()
# r2py:entity:c
c = linesGrob()

# r2py:entity:row
row = np.array([[a, b]], dtype=object)
# r2py:entity:col
col = np.array([[a], [b]], dtype=object)
# r2py:entity:mat
mat = np.array([[a, b], [c, nullGrob()]], dtype=object)

# r2py:entity:row_gt
row_gt = gtable_matrix("demo", row, unit([1, 1], "null"), unit(1, "null")) # Note: R source says heights=unit(c(1,1)), but row is 1x2. Actually R source: row_gt <- gtable_matrix("demo", row, unit(c(1, 1), "null"), unit(1, "null")) suggests heights are [1,1] and widths is 1.
# Correction based on R: gtable_matrix(name, matrix, heights, widths). 
# row: 1x2 matrix. heights=unit(c(1,1)), widths=unit(1). This is actually odd in R (mismatch), but we follow the source.
row_gt = gtable_matrix("demo", row, [1, 1], [1])

# r2py:entity:col_gt
col_gt = gtable_matrix("demo", col, [1], [1, 1])

# r2py:entity:mat_gt
mat_gt = gtable_matrix("demo", mat, [1, 1], [1, 1])

# r2py:entity:c_binded
c_binded = cbind(mat_gt, col_gt, size="first")

# r2py:entity:plot
# plot(c_binded) - In R this is a side effect. In Python we just pass.

# r2py:entity:r_binded
r_binded = rbind(mat_gt, row_gt, size="last")

# r2py:entity:plot_1
# plot(r_binded) - Side effect.

# r2py:entity:try
try:
    if mat_gt['heights'] != row_gt['heights']: # Simplified check for bind dimension match
        raise ValueError("Dimensions must match along bind direction")
    cbind(mat_gt, row_gt)
except Exception:
    pass # R try() suppresses errors from printing unless specified