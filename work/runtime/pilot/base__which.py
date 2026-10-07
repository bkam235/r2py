import numpy as np
import pandas as pd

def r_which(x, arr_ind=False, useNames=True):
    """
    Python implementation of R's which() function.
    """
    # Determine if x is a scalar for return type purposes
    is_scalar = False
    if isinstance(x, (bool, int, float)):
        is_scalar = True
        x_arr = np.array([x])
    elif isinstance(x, np.ndarray) and x.ndim == 0:
        is_scalar = True
        x_arr = np.array([x.item()])
    else:
        x_arr = np.asarray(x)

    # In R's which(x), NA values are treated as FALSE.
    # If x is logical, NA becomes FALSE. If x is numeric, NA becomes FALSE.
    # We use np.where to handle NaNs and then check for non-zero/True values.
    if np.issubdtype(x_arr.dtype, np.floating):
        mask = np.where(np.isnan(x_arr), False, x_arr != 0)
    elif np.issubdtype(x_arr.dtype, np.bool_):
        # For boolean arrays, NumPy doesn't have NA. 
        # If the input is an object array with None/NaN, we handle it.
        mask = x_arr
    elif x_arr.dtype == object:
        mask = np.array([ (val is not None and not pd.isna(val) and bool(val)) for val in x_arr.ravel() ]).reshape(x_arr.shape)
    else:
        mask = x_arr != 0

    # Flatten for calculation but keep original shape for arr_ind
    flat_mask = mask.ravel()
    wh = np.where(flat_mask)[0] + 1
    
    if arr_ind and x_arr.ndim > 1:
        dims = x_arr.shape
        # R is column-major (Fortran order)
        res = np.unravel_index(np.where(flat_mask)[0], dims, order='F')
        # Stack indices into a matrix where each row is one element's coordinates
        arr_res = np.column_stack([np.array(r) + 1 for r in res])
        return arr_res
    
    # Handle scalar input return
    if is_scalar:
        return wh[0] if len(wh) > 0 else np.array([], dtype=int)
    
    # R returns an integer vector. NumPy arrays are equivalent to R vectors.
    return wh
