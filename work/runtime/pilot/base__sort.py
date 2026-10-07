import numpy as np
import pandas as pd

def r_sort(x, decreasing=False, na_last=float('nan'), **kwargs):
    """
    Python implementation of R's sort() function.
    
    R's sort() function removes NAs by default. 
    If na.last is provided as TRUE or FALSE, NAs are kept and placed 
    accordingly. If na.last is NA (default), NAs are removed.
    """
    x = np.asanyarray(x)
    
    mask = np.isnan(x)
    non_nas = x[~mask]
    nas = x[mask]
    
    # Sort the non-NA values
    sorted_non_nas = np.sort(non_nas)
    if decreasing:
        sorted_non_nas = sorted_non_nas[::-1]
        
    # Handle NA placement based on na_last
    # In R, sort(x) defaults to na.last = NA, which removes NAs.
    # If na.last is True, NAs are at the end.
    # If na.last is False, NAs are at the beginning.
    
    if np.isnan(na_last) if isinstance(na_last, (float, np.float64)) else na_last is None:
        # R's default behavior: na.last = NA means remove NAs
        return sorted_non_nas
    elif na_last is True:
        return np.concatenate([sorted_non_nas, nas])
    elif na_last is False:
        return np.concatenate([nas, sorted_non_nas])
    else:
        # Fallback for cases where na_last might be passed as something else 
        # that evaluates to the default NA state.
        return sorted_non_nas
