import numpy as np
import pandas as pd

def r_rowSums(x, na_rm=False, dims=1):
    """
    Python implementation of R's rowSums.
    """
    # Handle data frames
    if isinstance(x, pd.DataFrame):
        # as.matrix(x) in R converts to numeric if possible, 
        # but generally we convert to numpy array.
        x = x.to_numpy()
    
    # Convert to numpy array if not already
    if not isinstance(x, np.ndarray):
        x = np.array(x)

    # R check: !is.array(x) || length(dn <- dim(x)) < 2L
    # In numpy, x.ndim gives the number of dimensions.
    if x.ndim < 2:
        raise ValueError("'x' must be an array of at least two dimensions")

    # R check: length(dims) != 1L || dims < 1L || dims > length(dn) - 1L
    # dims is expected to be an integer.
    if not isinstance(dims, (int, np.integer)):
        raise ValueError("invalid 'dims'")
    
    dn = x.shape
    if dims < 1 or dims > len(dn) - 1:
        raise ValueError("invalid 'dims'")

    # R logic:
    # p <- prod(dn[-(id <- seq_len(dims))])
    # dn <- dn[id]
    # z <- .Internal(rowSums(x, prod(dn), p, na.rm))
    # Essentially, it sums over all dimensions AFTER the 'dims'-th dimension.
    
    # Create a tuple of axes to sum over: from dims (0-indexed) to the end
    axes_to_sum = tuple(range(dims, len(dn)))
    
    if na_rm:
        # np.nansum treats NaN as 0. If all elements are NaN, it returns 0.
        # R's rowSums(na.rm=TRUE) returns 0 if all are NA.
        res = np.nansum(x, axis=axes_to_sum)
    else:
        # np.sum returns NaN if any element is NaN, matching R's default.
        res = np.sum(x, axis=axes_to_sum)

    # Return result as a numpy array.
    # R's rowSums returns a vector (1D array).
    return np.asarray(res)
