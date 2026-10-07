import numpy as np
import pandas as pd

def r_sort(x, decreasing=False, na_last=float('nan'), *args, **kwargs):
    """
    Python implementation of R's sort function.
    R's sort() by default removes NAs from the result vector unless specifically
    handled via order() in the object case, but for atomic vectors (sort.int),
    the default behavior of sort() is to actually remove NAs.
    
    Looking at R's documentation for sort(): 
    "missing values are removed by default".
    """
    # Convert input to numpy array
    if isinstance(x, (list, np.ndarray, pd.Series)):
        x_arr = np.array(x)
    else:
        x_arr = np.array([x])

    # Handle NA removal: R's sort() removes NAs by default.
    # The only time NaNs are kept is if they are handled by the logic 
    # of a custom object or specific sorting methods, but for the standard
    # sort(c(3, 1, 2, NA)) the result is [1, 2, 3].
    
    mask_nan = np.isnan(x_arr)
    non_nan_vals = x_arr[~mask_nan]

    # Sort non-NaN values
    sorted_vals = np.sort(non_nan_vals)
    if decreasing:
        sorted_vals = sorted_vals[::-1]

    # In R, if na.last is NA (default), NAs are removed.
    # If na.last is TRUE, NAs are placed last.
    # If na.last is FALSE, NAs are placed first.
    
    # Check if na_last is R's NA (NaN in Python)
    is_na_last_nan = False
    if isinstance(na_last, (float, np.floating)) and np.isnan(na_last):
        is_na_last_nan = True

    if is_na_last_nan:
        # Default R behavior: remove NAs
        return sorted_vals
    
    # Handle cases where na_last is explicitly TRUE or FALSE
    nan_count = np.sum(mask_nan)
    if nan_count == 0:
        return sorted_vals

    put_last = True
    if na_last is False:
        put_last = False
    elif na_last is True:
        put_last = True
    else:
        # Fallback for other types
        put_last = True

    if put_last:
        result = np.concatenate([sorted_vals, np.full(nan_count, np.nan)])
    else:
        result = np.concatenate([np.full(nan_count, np.nan), sorted_vals])

    return result
