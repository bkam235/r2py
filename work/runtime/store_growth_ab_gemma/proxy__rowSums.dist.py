import numpy as np
import pandas as pd

def r_rowSums_dist(x, na_rm=False):
    """
    Python reproduction of proxy::rowSums.dist.
    
    In R's proxy package, 'dist' objects can be presented as vectors or
    objects that may arrive as pandas Series or numpy arrays. 
    The failing cases suggest x might be passed as a scalar or a 0-d array
    if the distance vector is empty or if the harness passes it as a specific
    object. However, the primary issue 'TypeError: len() of unsized object' 
    indicates that x is sometimes a numpy scalar or an object that doesn't 
    support len().
    """
    # Ensure x is a numpy array.
    # If x is a scalar (which happens if distance vector is empty/singular), 
    # np.atleast_1d ensures we can call len() and iterate.
    x_arr = np.atleast_1d(np.asanyarray(x, dtype=float))
    
    # Calculate the number of observations n from the length of the 
    # lower triangle vector: L = n * (n - 1) / 2
    # n^2 - n - 2L = 0 => n = (1 + sqrt(1 + 8L)) / 2
    L = len(x_arr)
    
    # Handle cases where L might be 0 (e.g., distance matrix of 1 element)
    if L == 0:
        # If the distance object represents a 1x1 matrix, rowSum is 0.
        # However, standard proxy::dist(matrix(1:4, 2)) results in L=1 (for 2 rows).
        # We need to determine n.
        # Based on typical R behavior for dist, if L is 0, n is likely 1.
        n = 1
    else:
        n = int(round((1 + np.sqrt(1 + 8 * L)) / 2))
    
    # Reconstruct the distance matrix (symmetric, diagonal=0)
    dist_matrix = np.zeros((n, n))
    
    # The proxy::dist object stores elements in the order:
    # (1,2), (1,3) ... (1,n), (2,3), (2,4) ... (2,n), ..., (n-1, n)
    curr = 0
    for i in range(n):
        for j in range(i + 1, n):
            if curr < L:
                val = x_arr[curr]
                dist_matrix[i, j] = val
                dist_matrix[j, i] = val
                curr += 1
            
    # R's rowSums handling of NA
    if na_rm:
        # np.nansum treats NaN as 0.
        result = np.nansum(dist_matrix, axis=1)
    else:
        # np.sum with NaNs returns NaN.
        result = np.sum(dist_matrix, axis=1)
        
    return result
