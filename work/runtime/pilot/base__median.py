import numpy as np
import pandas as pd

def r_median(x, na_rm=False, **kwargs):
    """
    Python reproduction of R's median function.
    """
    # In R, factors are passed as lists of strings, and data frames as pandas DataFrames.
    if isinstance(x, pd.DataFrame):
        raise TypeError("need numeric data")
    
    # Handle single numeric values (scalars) by converting them to 1D arrays
    if np.isscalar(x):
        x = np.array([x])
    elif isinstance(x, list):
        # Check if it's a "factor" (list of strings)
        if len(x) > 0 and isinstance(x[0], str):
            raise TypeError("need numeric data")
        x = np.array(x)
    else:
        x = np.asanyarray(x)
        # Ensure x is treated as a 1D array if it's 0-d
        if x.ndim == 0:
            x = x.reshape(1)

    # Handle NA cases
    if na_rm:
        # Remove NaNs
        x = x[~np.isnan(x)]
    else:
        # If any NaN is present and na.rm is FALSE, R returns NA (NaN)
        if np.any(np.isnan(x)):
            return np.nan

    n = len(x)
    if n == 0:
        return np.nan

    # Sort the array to find the median
    sorted_x = np.sort(x)
    
    # R's logic:
    # half <- (n + 1L)%/%2L
    # if (n%%2L == 1L) sort(x, partial = half)[half]
    # else mean(sort(x, partial = half + 0L:1L)[half + 0L:1L])
    
    if n % 2 == 1:
        # Odd: middle element
        # R index (n+1)//2 is Python index (n-1)//2
        return sorted_x[(n - 1) // 2]
    else:
        # Even: average of two middle elements
        # R indices (n//2) and (n//2 + 1)
        # Python indices (n//2 - 1) and (n//2)
        mid_left = (n // 2) - 1
        mid_right = n // 2
        return (sorted_x[mid_left] + sorted_x[mid_right]) / 2.0
