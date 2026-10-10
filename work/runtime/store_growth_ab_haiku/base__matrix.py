import numpy as np
import pandas as pd

def _r2py_impl_r_matrix(data=None, nrow=1, ncol=1, byrow=False, dimnames=None):
    """
    Reproduce R's matrix function.
    
    Parameters:
    data: array-like or scalar (default NA)
    nrow: number of rows (default 1)
    ncol: number of columns (default 1)
    byrow: fill by rows if True, by columns if False (default False)
    dimnames: row and column names (default None)
    
    Returns:
    numpy ndarray with shape (nrow, ncol)
    """
    
    # Handle the case where data is None (represents R's NA)
    if data is None:
        data = np.nan
    
    # Convert data to a list/array if needed
    if isinstance(data, (list, tuple)):
        data_vec = list(data)
    elif isinstance(data, np.ndarray):
        data_vec = data.flatten().tolist()
    elif np.isscalar(data):
        data_vec = [data]
    else:
        # Try to convert to list
        try:
            data_vec = list(data)
        except TypeError:
            data_vec = [data]
    
    # Calculate total elements needed
    total_elements = nrow * ncol
    
    # Recycle or truncate data to match matrix size
    if len(data_vec) == 0:
        data_vec = [np.nan] * total_elements
    else:
        # Recycle data to fill the matrix
        if len(data_vec) < total_elements:
            # Recycle data
            cycles = (total_elements + len(data_vec) - 1) // len(data_vec)
            data_vec = (data_vec * cycles)[:total_elements]
        else:
            # Truncate if too long
            data_vec = data_vec[:total_elements]
    
    # Create matrix
    if byrow:
        # Fill by rows
        matrix = np.array(data_vec, dtype=object).reshape((nrow, ncol))
    else:
        # Fill by columns (default R behavior)
        matrix = np.array(data_vec, dtype=object).reshape((nrow, ncol), order='F')
    
    return matrix


_R2PY_UNVERIFIED_r_matrix = {}
_R2PY_UNVERIFIED_CLASSES_r_matrix = ['vector input']


def _r2py_items_r_matrix(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_matrix(*args, **kwargs):
    """r_matrix reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_matrix
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_matrix; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_matrix).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_matrix.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_matrix: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_matrix and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_matrix(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_matrix and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_matrix: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_matrix and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_matrix: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_matrix(*args, **kwargs)
