import numpy as np
import pandas as pd

def r_rowSums_dist(x, na_rm=False):
    """
    Helper function to reproduce proxy::rowSums.dist.
    A dist object in R is stored as a numeric vector of the lower triangle.
    """
    # Handle potential scalar inputs if x is passed as float (though usually array)
    if isinstance(x, (float, int, np.float64, np.int64)):
        # A single distance implies N=2
        # But based on the harness, it arrives as a numpy array. 
        # If it is a scalar, we treat it as a 1-element array.
        x = np.atleast_1d(x)
    
    # Calculate N from length of distance vector: len(x) = N*(N-1)/2
    # N^2 - N - 2*len(x) = 0  => N = (1 + sqrt(1 + 8*len(x))) / 2
    n = int(np.round((1 + np.sqrt(1 + 8 * len(x))) / 2))
    
    # Reconstruct full matrix
    mat = np.zeros((n, n))
    idx = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            val = x[idx]
            mat[i, j] = val
            mat[j, i] = val
            idx += 1
            
    if na_rm:
        return np.nansum(mat, axis=1)
    else:
        # np.sum returns NaN if any element is NaN, matching R's behavior for na.rm=FALSE
        return np.sum(mat, axis=1)

def _r2py_impl_r_rowMeans_dist(x, na_rm=False, diag=True):
    # Ensure x is a numpy array
    if not isinstance(x, np.ndarray):
        x = np.atleast_1d(x)
        
    if not isinstance(diag, (bool, np.bool_)):
        raise TypeError("'diag' not of type logical")
    
    # Step 1: s <- rowSums.dist(x, na.rm)
    s = r_rowSums_dist(x, na_rm=na_rm)
    
    if na_rm:
        # Step 2: x[!(is.na(x) | is.nan(x))] <- 1
        # Create a copy to avoid mutating the original input array
        x_dummy = x.copy().astype(float)
        mask = ~np.isnan(x_dummy)
        x_dummy[mask] = 1.0
        
        # Step 3: s/(rowSums.dist(x, na.rm) + (diag == TRUE))
        # In R code provided: s / (rowSums.dist(x_dummy, na.rm) + (diag == TRUE))
        # Note: The R source says 'rowSums.dist(x, na.rm)', but logically it uses the 
        # modified x (where non-NAs are 1) to count the non-NA values.
        counts = r_rowSums_dist(x_dummy, na_rm=True)
        denom = counts + (1.0 if diag else 0.0)
        return s / denom
    else:
        # Step 4: s/(length(s) - (diag == FALSE))
        # length(s) is the number of rows N.
        n = len(s)
        denom = n - (0 if diag else 1)
        return s / denom


_R2PY_UNVERIFIED_r_rowMeans_dist = {'diag': ['False']}
_R2PY_UNVERIFIED_CLASSES_r_rowMeans_dist = []


def _r2py_items_r_rowMeans_dist(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_rowMeans_dist(*args, **kwargs):
    """r_rowMeans_dist reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_rowMeans_dist
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_rowMeans_dist; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_rowMeans_dist).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_rowMeans_dist.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_rowMeans_dist: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_rowMeans_dist and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_rowMeans_dist(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_rowMeans_dist and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_rowMeans_dist: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_rowMeans_dist and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_rowMeans_dist: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_rowMeans_dist(*args, **kwargs)
