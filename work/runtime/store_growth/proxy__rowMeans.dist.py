import numpy as np
import pandas as pd

def r_rowSums_dist(x, na_rm=False):
    """
    Helper function to reproduce proxy::rowSums.dist.
    In R, dist objects are passed as vectors of length n*(n-1)/2.
    """
    # Ensure x is a numpy array. 
    x = np.asarray(x)
    # If the input is a scalar (which happens in some test runners if the dist 
    # object only has 1 element), ensure it is treated as a 1D array.
    if x.ndim == 0:
        x = x.reshape(1)
        
    # Calculate n from length of the distance vector: L = n*(n-1)/2 => n^2 - n - 2L = 0
    # n = (1 + sqrt(1 + 8L)) / 2
    L = len(x)
    n = int(round((1 + np.sqrt(1 + 8 * L)) / 2))
    
    # Create the symmetric distance matrix
    full_mat = np.zeros((n, n))
    curr = 0
    for i in range(n):
        for j in range(i + 1, n):
            val = x[curr]
            full_mat[i, j] = val
            full_mat[j, i] = val
            curr += 1
            
    if na_rm:
        # np.nansum handles NaNs as 0
        return np.nansum(full_mat, axis=1)
    else:
        # Standard sum (returns NaN if any element is NaN)
        return np.sum(full_mat, axis=1)

def r_rowMeans_dist(x, na_rm=False, diag=True):
    # Ensure x is a numpy array
    x = np.asarray(x)
    if x.ndim == 0:
        x = x.reshape(1)
    
    if not isinstance(diag, (bool, np.bool_)):
        # Use a generic exception or match the "stop" message
        raise TypeError("'diag' not of type logical")
    
    s = r_rowSums_dist(x, na_rm=na_rm)
    # s is a numpy array; length(s) in R is the number of rows n
    n_obs = len(s)
    
    if na_rm:
        # R source logic:
        # x[!(is.na(x) | is.nan(x))] <- 1
        # s/(rowSums.dist(x, na.rm) + (diag == TRUE))
        
        # Create a mask vector where non-NAs are 1 and NAs are 0
        mask = np.where(np.isnan(x), 0, 1)
        
        # Get the sum of non-NAs per row (off-diagonal counts)
        row_counts = r_rowSums_dist(mask, na_rm=True)
        
        # Divisor is off-diagonal count + 1 if diag is True (the 0 on the diagonal is not NA)
        divisor = row_counts + (1 if diag else 0)
        return s / divisor
    else:
        # s/(length(s) - (diag == FALSE))
        # length(s) is n.
        # If diag=True, divisor is n. If diag=False, divisor is n-1.
        divisor = n_obs - (0 if diag else 1)
        return s / divisor
