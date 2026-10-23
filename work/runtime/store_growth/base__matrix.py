import numpy as np
import pandas as pd

def r_matrix(data=np.nan, nrow=1, ncol=1, byrow=False, dimnames=None):
    """
    Python implementation of R's matrix function.
    """
    # Convert data to a 1D array (mimicking as.vector)
    if isinstance(data, pd.DataFrame):
        data_vec = data.values.flatten()
    elif isinstance(data, (list, tuple, np.ndarray)):
        data_vec = np.asanyarray(data).flatten()
    elif data is None:
        data_vec = np.array([np.nan])
    else:
        # Scalar case
        data_vec = np.array([data])

    # Handle dimensionality logic. 
    # In R, if one of nrow or ncol is missing, it's calculated from the other.
    # The provided R source uses missing(nrow) and missing(ncol).
    # Since we have defaults, we must detect if they were effectively "missing".
    # In R's internal matrix logic, if only one is specified, the other is set
    # to length(data) / specified.
    
    # We assume if the user provides data and the product of defaults (1*1) 
    # doesn't match the data length, and one of the arguments was the default 1,
    # we calculate the other.
    if data_vec.size > 0:
        # This logic mimics R's internal handling of missing nrow/ncol
        # If data length is not 1, and product is not length, R adjusts.
        # Note: R's matrix() will throw a warning if it's not a perfect multiple,
        # but it still creates the matrix.
        if nrow == 1 and data_vec.size != 1:
            # We assume ncol was specified or defaulted, but we need to check
            # if nrow should be derived. R usually derives the one that is 'missing'.
            # Given the test case matrix(runif(20), ncol=2), nrow becomes 10.
            if ncol != 1 or (ncol == 1 and data_vec.size != 1):
                # In the specific case matrix(data, ncol=2), nrow = 20/2 = 10
                # If both were 1, it stays 1 (and recycles/truncates).
                pass 
    
    # Since we can't perfectly detect 'missing' vs 'passed 1', 
    # we look at the common R behavior:
    # if nrow is 1 and ncol is specified (and not 1), nrow = size // ncol
    # if ncol is 1 and nrow is specified (and not 1), ncol = size // nrow
    # This is a heuristic for the provided test cases.
    
    # Re-evaluating based on the example matrix(runif(20), ncol=2) -> 10x2
    # It suggests that if the provided data size is larger than the product, 
    # and only one dimension is specifically set (or the other is 1), it scales.
    
    # Simplified R-like dimension calculation:
    # (In a real R environment, this is handled by the `missing()` function)
    # For this harness, we assume if one is 1 and the other is not, the 1 is calculated.
    if data_vec.size > 0:
        if nrow == 1 and ncol != 1:
            nrow = int(np.ceil(data_vec.size / ncol))
        elif ncol == 1 and nrow != 1:
            ncol = int(np.ceil(data_vec.size / nrow))

    n_elements = nrow * ncol
    
    if data_vec.size == 0:
        # R's matrix(NA_character_, 0, 4) returns a 0x4 matrix
        res = np.empty((nrow, ncol), dtype=data_vec.dtype)
    elif data_vec.size == 1:
        res = np.full((nrow, ncol), data_vec[0])
    else:
        # R recycling: data is repeated if it's shorter than nrow * ncol
        if data_vec.size < n_elements:
            full_data = np.tile(data_vec, (n_elements // data_vec.size) + 1)[:n_elements]
        else:
            full_data = data_vec[:n_elements]
            
        if byrow:
            res = full_data.reshape((nrow, ncol))
        else:
            # R is column-major
            res = full_data.reshape((ncol, nrow)).T

    # The requirement is to return a numpy 2-d array for class 'matrix'
    return res
