import numpy as np
import pandas as pd

def r_sparse_logical(values, positions, length, default=False):
    """
    Reproduces the behavior of sparsevctrs::sparse_logical.
    """
    # Ensure length is an integer
    length = int(length)
    
    # Convert inputs to numpy arrays.
    # If input is a scalar (e.g., TRUE), asarray makes it a 0-d array.
    values = np.asarray(values)
    positions = np.asarray(positions)
    
    # Ensure positions is integer
    if positions.size > 0:
        positions = positions.astype(int)
    
    # Check if values contains the default value (ignoring NAs)
    if values.size > 0:
        # Mask out NaNs to match na.rm = TRUE
        mask_non_na = ~pd.isna(values)
        if np.any(values[mask_non_na] == default):
            raise ValueError(f"values value must not be equal to the default {default}.")

    # Initialize the vector with the default value
    # We use dtype=object to support both booleans and np.nan (R's NA)
    res = np.full(length, default, dtype=object)
    
    # Handle the case where values/positions might be 0-d arrays (scalars)
    # We convert them to 1-d to iterate correctly
    v_flat = np.atleast_1d(values)
    p_flat = np.atleast_1d(positions)
    
    if v_flat.size > 0:
        # R uses 1-based indexing for positions
        idx = p_flat - 1
        
        for i in range(len(v_flat)):
            pos = idx[i]
            val = v_flat[i]
            
            if pd.isna(val):
                res[pos] = np.nan
            else:
                res[pos] = bool(val)

    # Final conversion: if there are no NaNs, cast to boolean for the return type
    if not np.any(pd.isna(res)):
        return res.astype(bool)
    
    return res
