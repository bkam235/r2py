import numpy as np
import pandas as pd

def r_mean(x, trim=0, na_rm=False, *args, **kwargs):
    """
    Python implementation of R's mean() function.
    """
    # Ensure x is a numpy array. If it is a scalar, make it a 1D array.
    if np.isscalar(x):
        x = np.array([x])
    else:
        x = np.asanyarray(x)

    # R's type check: !is.numeric(x) && !is.complex(x) && !is.logical(x)
    if not np.issubdtype(x.dtype, np.number) and not np.issubdtype(x.dtype, np.bool_):
        return np.nan

    # Handle na.rm (remove NA values)
    if na_rm:
        # Convert to float to use isnan safely across types
        mask = ~np.isnan(x.astype(float))
        x = x[mask]

    # Check trim parameter
    if not isinstance(trim, (int, float, np.number)) or np.ndim(trim) != 0:
        raise TypeError("'trim' must be numeric of length one")

    n = len(x)
    
    if trim > 0 and n > 0:
        # trimmed means are not defined for complex data
        if np.iscomplexobj(x):
            raise TypeError("trimmed means are not defined for complex data")
        
        # if any NA exists in the sequence before trimming
        if np.any(np.isnan(x.astype(float))):
            return np.nan
        
        if trim >= 0.5:
            # R returns stats::median(x, na.rm = FALSE)
            # Note: np.median handles the median calculation. 
            # If trim >= 0.5, R returns the median.
            return np.median(x).item() if hasattr(np.median(x), 'item') else np.median(x)
        
        # Calculate indices for trimming
        # R: lo <- floor(n * trim) + 1; hi <- n + 1 - lo
        # Python 0-indexing: lo_idx = floor(n * trim)
        lo_idx = int(np.floor(n * trim))
        hi_idx = n - lo_idx
        
        sorted_x = np.sort(x)
        x = sorted_x[lo_idx:hi_idx]

    # Final mean calculation
    if len(x) == 0:
        # R's mean() of an empty vector returns NaN
        return np.nan
    
    res = np.mean(x)
    return res.item() if hasattr(res, 'item') else res
