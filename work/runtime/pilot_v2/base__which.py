import numpy as np
import pandas as pd

def r_which(x, arr_ind=False, useNames=True):
    # In R, which() treats any non-zero numeric value as TRUE 
    # and NaN as FALSE (though usually x is logical).
    # We convert to a numpy array to handle various input types.
    x_arr = np.asanyarray(x)
    
    # R's which(x) returns indices where x is TRUE.
    # NaNs are treated as FALSE in R's which().
    mask = np.nan_to_num(x_arr, nan=0).astype(bool)
    
    # Find indices where mask is True
    wh = np.where(mask.ravel())[0]
    
    # R uses 1-based indexing
    wh_1based = wh + 1
    
    if arr_ind and x_arr.ndim > 1:
        # arrayInd implementation
        dims = x_arr.shape
        # R's arrayInd unravels indices in column-major order
        # np.unravel_index does exactly this if we pass the flat index
        # and the shape of the array.
        indices = np.unravel_index(wh, dims)
        
        # R returns a matrix where each column is a dimension
        # The result is indices[0] (row), indices[1] (col), etc.
        # We stack them as columns and add 1 for 1-based indexing.
        res = np.column_stack([idx + 1 for idx in indices])
        
        # If result is empty, R returns a matrix with 0 rows and ncol dimensions
        if res.shape[0] == 0:
            return np.empty((0, len(dims)), dtype=int)
        
        return res
    else:
        # Return as a 1D numpy array of integers
        # If nothing is found, R returns integer(0)
        if len(wh_1based) == 0:
            return np.array([], dtype=int)
        return wh_1based
