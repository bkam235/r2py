import numpy as np
import pandas as pd

def r_rowSums(x, na_rm=False, dims=1):
    """
    Python implementation of R's rowSums function.
    """
    # Handle data frames by converting to matrix (numpy array)
    if isinstance(x, pd.DataFrame):
        x = x.to_numpy()
    
    # Validate input is an array-like object
    if not isinstance(x, np.ndarray):
        x = np.asanyarray(x)
        
    # R's rowSums requires at least two dimensions
    if x.ndim < 2:
        raise ValueError("'x' must be an array of at least two dimensions")
        
    # Validate 'dims' parameter
    # R: dims must be 1 <= dims < length(dn)
    if not isinstance(dims, (int, np.integer)) or dims < 1 or dims > x.ndim - 1:
        raise ValueError("invalid 'dims'")
    
    # In R, rowSums(x, dims=1) sums over all dimensions except the 1st.
    # rowSums(x, dims=2) sums over all dimensions except the 2nd, etc.
    # The result should have the length of the dimension specified by 'dims'.
    
    # Determine which axis to keep (1-indexed in R -> 0-indexed in Python)
    keep_axis = dims - 1
    
    # Determine axes to sum over (all except keep_axis)
    sum_axes = tuple(i for i in range(x.ndim) if i != keep_axis)
    
    if na_rm:
        # np.nansum treats NaN as zero. 
        # Note: if all values in a slice are NaN, nansum returns 0, 
        # but R's rowSums(na.rm=TRUE) also returns 0 for all-NA slices.
        result = np.nansum(x, axis=sum_axes)
    else:
        # np.sum with NaNs returns NaN, matching R's default behavior
        result = np.sum(x, axis=sum_axes)
    
    # R returns a vector (1D array) if the original x was a matrix.
    # If x was a higher-dimensional array, it returns an array with the 
    # dimension specified by 'dims'.
    
    # Since the prompt asks for the result as R returns it:
    # If x is 2D, R returns a numeric vector.
    # If x is > 2D, R returns an array with the shape of the kept dimension.
    
    # Ensure the result is a numpy array of floats (numeric)
    return result.astype(float)
