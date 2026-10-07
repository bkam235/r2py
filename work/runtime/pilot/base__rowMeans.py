import numpy as np
import pandas as pd

def r_rowMeans(x, na_rm=False, dims=1):
    """
    Python implementation of R's rowMeans.
    """
    # If x is a data frame, convert to numpy array (like as.matrix in R)
    if isinstance(x, pd.DataFrame):
        x_arr = x.to_numpy()
    elif isinstance(x, np.ndarray):
        x_arr = x
    else:
        # Fallback for other array-like inputs
        x_arr = np.asanyarray(x)

    # Validate dimensions
    if x_arr.ndim < 2:
        raise ValueError("'x' must be an array of at least two dimensions")

    # R's dims parameter specifies how many leading dimensions to keep.
    # For rowMeans, usually dims=1.
    if not isinstance(dims, (int, np.integer)) or dims < 1 or dims > x_arr.ndim - 1:
        raise ValueError("invalid 'dims'")

    # Calculate means along the axes starting from index 'dims' to the end.
    # R's rowMeans(x, dims=1) computes mean over columns for each row.
    # If dims=2, it computes mean over all dimensions after the 2nd.
    axes_to_reduce = tuple(range(dims, x_arr.ndim))
    
    if na_rm:
        # nanmean ignores NaNs
        res = np.nanmean(x_arr, axis=axes_to_reduce)
    else:
        # In R, if any value is NA and na.rm=FALSE, the result is NA
        # np.mean handles NaNs by returning NaN, which matches R's behavior.
        res = np.mean(x_arr, axis=axes_to_reduce)

    # The output of np.mean on an ndarray is a numpy array.
    # R returns a vector if the result is 1D, or an array if higher dim.
    # Since we are reducing from index 'dims' onwards, the result has shape x_arr.shape[:dims].
    
    # Handle result shape and type to match R's behavior
    # R's rowMeans typically returns a numeric vector.
    if res.ndim == 1:
        return res
    else:
        return res
