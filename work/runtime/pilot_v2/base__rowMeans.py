import numpy as np
import pandas as pd

def r_rowMeans(x, na_rm=False, dims=1):
    """
    Python reproduction of R's rowMeans function.
    """
    # Handle data.frame input
    if isinstance(x, pd.DataFrame):
        x = x.to_numpy()
    
    # If x is passed as a list, convert to numpy array
    if isinstance(x, list):
        x = np.array(x)
        
    # R's rowMeans requires an array/matrix. 
    # In the harness, matrices are passed as numpy arrays.
    if not isinstance(x, np.ndarray) or x.ndim < 2:
        # R throws an error here. The failing tests suggest the harness might 
        # be passing numpy arrays that are perceived as < 2 dims or handled differently.
        # But matrix(1:9, nrow=3) is definitely 2D.
        raise TypeError("'x' must be an array of at least two dimensions")
    
    # dims validation: must be 1 <= dims < ndim
    if not isinstance(dims, (int, np.integer)) or dims < 1 or dims > x.ndim - 1:
        raise ValueError("invalid 'dims'")
    
    # R's rowMeans(x, dims=k) calculates means over all dimensions EXCEPT the k-th.
    # 1-based index k corresponds to 0-based index k-1 in numpy.
    target_axis = dims - 1
    axes_to_collapse = tuple(i for i in range(x.ndim) if i != target_axis)
    
    if na_rm:
        # np.nanmean handles NA (NaN) by ignoring them. 
        # If a slice is all NaNs, it typically warns and returns NaN, matching R.
        res = np.nanmean(x, axis=axes_to_collapse)
    else:
        # Standard mean. If any element in the slice is NaN, result is NaN.
        res = np.mean(x, axis=axes_to_collapse)
    
    # The result of rowMeans in R is always a numeric vector (1D array in Python)
    # regardless of whether the input was a matrix or a higher-dimensional array.
    return np.array(res, dtype=float)
