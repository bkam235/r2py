import numpy as np
import pandas as pd

def r_median(x, na_rm=False, *args, **kwargs):
    # R stops if x is a factor (represented as list of str) or data frame
    if isinstance(x, pd.DataFrame) or (isinstance(x, list) and all(isinstance(i, str) for i in x)):
        raise TypeError("need numeric data")
    
    # Ensure x is a numpy array.
    # Using np.atleast_1d ensures that scalars are converted to arrays with len > 0,
    # which avoids "TypeError: len() of unsized object" for single values.
    x_arr = np.atleast_1d(np.asanyarray(x, dtype=float))
    
    # Handle NA (NaN in numpy)
    if na_rm:
        # x <- x[!is.na(x)]
        x_arr = x_arr[~np.isnan(x_arr)]
    else:
        # else if (any(is.na(x))) return(x[NA_integer_])
        if np.any(np.isnan(x_arr)):
            return np.nan

    n = len(x_arr)
    
    # if (n == 0L) return(x[NA_integer_])
    if n == 0:
        return np.nan

    # R's logic for median:
    # half <- (n + 1L)%/%2L
    half = (n + 1) // 2
    
    # Sort the array to mimic R's sort(x, partial = ...)
    sorted_x = np.sort(x_arr)
    
    if n % 2 == 1:
        # n%%2L == 1L: sort(x, partial = half)[half]
        # R uses 1-based indexing. index [half] in R is index [half-1] in Python.
        return float(sorted_x[half - 1])
    else:
        # else mean(sort(x, partial = half + 0L:1L)[half + 0L:1L])
        # For n=4: half=2. R takes indices 2 and 3. Python takes indices 1 and 2.
        val1 = sorted_x[half - 1]
        val2 = sorted_x[half]
        return float((val1 + val2) / 2.0)
