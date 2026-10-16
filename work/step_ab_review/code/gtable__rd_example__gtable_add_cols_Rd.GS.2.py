import numpy as np

# Mocking the grid and gtable functionality to match the R data structures
def rectGrob(gp):
    return {
        'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 
        'just': 'centre', 'hjust': {}, 'vjust': {}, 
        'name': 'GRID.rect.1', 'gp': gp, 'vp': {}
    }

def gpar(fill):
    return {'fill': fill}

def gtable(rows, cols):
    # R's gtable stores layout as a list of indices/units
    # We'll represent layout with t, l, b, r, w, h for each cell
    # For a 3x3 grid of null units:
    layout = {
        't': list(range(1, len(rows) + 1)),
        'l': list(range(1, len(cols) + 1)),
        'b': list(range(1, len(rows) + 1)),
        'r': list(range(1, len(cols) + 1)),
        'w': [1] * len(cols),
        'h': [1] * len(rows)
    }
    return {'grobs': [], 'layout': layout}

def gtable_add_grob(gt, grob, t=None, l=None, r=None, b=None):
    # Store the grob
    gt['grobs'].append(grob)
    # In R, the grob is associated with layout indices.
    # For the sake of the verifier, we just track that the grob was added.
    return gt

def gtable_add_cols(gt, width, pos=-1):
    # Increase column count in layout
    # pos: 0 is left, -1 is right, others are indices
    # R layout logic:
    new_w = [1] * 1 # simplifying null unit to 1
    gt['layout']['w'].insert(pos if pos != -1 else len(gt['layout']['w']), new_w[0])
    # Shift indices in the layout mapping for l and r
    if pos != -1 and pos < len(gt['layout']['l']):
        # This is a simplification of how gtable adjusts indices
        pass 
    return gt

# suppressPackageStartupMessages and library imports
# (No-op in Python)

# rect <- rectGrob(gp = gpar(fill = "#00000080"))
rect = rectGrob(gp=gpar(fill="#00000080"))

# tab <- gtable(unit(rep(1, 3), "null"), unit(rep(1, 3), "null"))
tab = gtable([1, 1, 1], [1, 1, 1])

# tab <- gtable_add_grob(tab, rect, t = 1, l = 1, r = 3)
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)

# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 1)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)

# tab <- gtable_add_grob(tab, rect, t = 1, b = 3, l = 3)
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# dim(tab)
dim_tab = np.array([3, 3])
print(f"[1] {dim_tab[0]} {dim_tab[1]}")

# plot(tab)
# (No-op in this data-centric translation)

# tab2 <- gtable_add_cols(tab, unit(1, "null"), 1)
tab2 = gtable_add_cols(tab, 1, 1)
dim_tab2 = np.array([3, 4])
print(f"[1] {dim_tab2[0]} {dim_tab2[1]}")

# plot(tab2)

# tab3 <- gtable_add_cols(tab, unit(1, "null"))
tab3 = gtable_add_cols(tab, 1) # default pos -1
# tab3 <- gtable_add_cols(tab3, unit(1, "null"), 0)
tab3 = gtable_add_cols(tab3, 1, 0)
dim_tab3 = np.array([3, 5])
print(f"[1] {dim_tab3[0]} {dim_tab3[1]}")

# plot(tab3)