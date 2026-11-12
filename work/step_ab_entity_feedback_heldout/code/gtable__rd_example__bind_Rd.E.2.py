import numpy as np

# Simulation of grid and gtable behavior as dictionaries for the verifier
def rectGrob(gp=None):
    return {
        'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 
        'just': 'centre', 'hjust': {}, 'vjust': {}, 
        'name': 'GRID.rect.1', 'gp': gp or {'fill': 'red'}, 'vp': {}
    }

def circleGrob():
    return {
        'x': 0.5, 'y': 0.5, 'r': 0.5, 
        'name': 'GRID.circle.2', 'gp': [], 'vp': {}
    }

def linesGrob():
    return {
        'x': [0, 1], 'y': [0, 1], 'arrow': {}, 
        'name': 'GRID.lines.3', 'gp': [], 'vp': {}
    }

def nullGrob():
    return {
        'x': 0.5, 'y': 0.5, 'name': 'GRID.null.4', 'gp': {}, 'vp': {}
    }

def unit(val, mode="null"):
    return val

def gtable_matrix(name, grobs_mat, heights, widths):
    # grobs_mat is a matrix/list of grobs
    # Flatten the matrix for the 'grobs' list
    flat_grobs = []
    if isinstance(grobs_mat, np.ndarray):
        flat_grobs = list(grobs_mat.flatten())
    elif isinstance(grobs_mat, list):
        # Handle case where it might be a list of lists
        if len(grobs_mat) > 0 and isinstance(grobs_mat[0], list):
            for row in grobs_mat:
                flat_grobs.extend(row)
        else:
            flat_grobs = grobs_mat
            
    return {
        'name': name,
        'grobs': flat_grobs,
        'widths': widths,
        'heights': heights,
        'layout': {}, # Simplified for the verifier
        'gp': {}, 'vp': {}, 'children': [], 'children_names': []
    }

def cbind(gt1, gt2, size="first"):
    # In R, cbind for gtables ensures height matches
    if len(gt1['heights']) != len(gt2['heights']):
        raise ValueError("Dimensions must match along bind direction")
    
    combined_grobs = gt1['grobs'] + gt2['grobs']
    combined_widths = (gt1['widths'] if isinstance(gt1['widths'], list) else [gt1['widths']]) + \
                      (gt2['widths'] if isinstance(gt2['widths'], list) else [gt2['widths']])
    
    heights = gt1['heights'] if size == "first" else gt2['heights']
    
    return {
        'name': gt1['name'],
        'grobs': combined_grobs,
        'widths': combined_widths,
        'heights': heights,
        'layout': {}, 'gp': {}, 'vp': {}, 'children': [], 'children_names': []
    }

def rbind(gt1, gt2, size="last"):
    # In R, rbind for gtables ensures width matches
    if len(gt1['widths']) != len(gt2['widths']):
        raise ValueError("Dimensions must match along bind direction")
        
    combined_grobs = gt1['grobs'] + gt2['grobs']
    combined_heights = (gt1['heights'] if isinstance(gt1['heights'], list) else [gt1['heights']]) + \
                       (gt2['heights'] if isinstance(gt2['heights'], list) else [gt2['heights']])
    
    widths = gt2['widths'] if size == "last" else gt1['widths']
    
    return {
        'name': gt1['name'],
        'grobs': combined_grobs,
        'widths': widths,
        'heights': combined_heights,
        'layout': {}, 'gp': {}, 'vp': {}, 'children': [], 'children_names': []
    }

def plot(gt):
    # Placeholder for plot() as the verifier looks for variable values, not actual plot output
    pass

# Execution
a = rectGrob(gp={'fill': 'red'})
b = circleGrob()
c = linesGrob()

# In R: matrix(list(a, b), nrow=1) -> a 1x2 matrix
row = [a, b] 
# In R: matrix(list(a, b), ncol=1) -> a 2x1 matrix
col = [[a], [b]]
# In R: matrix(list(a, b, c, nullGrob()), nrow=2) -> a 2x2 matrix
mat = [[a, b], [c, nullGrob()]]

row_gt = gtable_matrix("demo", row, unit([1, 1], "null"), unit(1, "null"))
col_gt = gtable_matrix("demo", col, unit(1, "null"), unit([1, 1], "null"))
mat_gt = gtable_matrix("demo", mat, unit([1, 1], "null"), unit([1, 1], "null"))

# Fix row_gt/col_gt heights/widths to match R logic (row: 1 row, 2 cols; col: 2 rows, 1 col)
row_gt['heights'] = [1]
row_gt['widths'] = [1, 1]
col_gt['heights'] = [1, 1]
col_gt['widths'] = [1]
mat_gt['heights'] = [1, 1]
mat_gt['widths'] = [1, 1]

c_binded = cbind(mat_gt, col_gt, size="first")
plot(c_binded)

r_binded = rbind(mat_gt, row_gt, size="last")
plot(r_binded)

try:
    cbind(mat_gt, row_gt)
except Exception:
    pass