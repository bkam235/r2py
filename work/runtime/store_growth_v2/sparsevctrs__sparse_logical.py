import numpy as np
import pandas as pd

def r_sparse_logical(values, positions, length, default=False):
    """
    Python reproduction of sparsevctrs::sparse_logical.
    
    Args:
        values (np.ndarray): Logical values to place at positions.
        positions (np.ndarray): 1-based indices for the values.
        length (int): The total length of the resulting logical vector.
        default (bool): The default value for elements not specified.
        
    Returns:
        np.ndarray: A logical numpy array.
    """
    # Ensure length is an integer
    length = int(length)
    
    # Force inputs to numpy arrays to handle scalars or lists
    values = np.atleast_1d(np.array(values, dtype=object))
    positions = np.atleast_1d(np.array(positions, dtype=int))
    
    # R error check: if (any(values == default, na.rm = TRUE))
    if values.size > 0:
        for val in values:
            # Check if val is not NA/NaN
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                if val == default:
                    raise ValueError(f"values value must not be equal to the default {default}.")

    # Initialize result array with the default value
    res = np.full(length, default, dtype=object)
    
    # Map the values to the positions (1-based to 0-based)
    if values.size > 0:
        for i in range(len(values)):
            # bounds check is typically handled by R's validate_positions
            res[positions[i] - 1] = values[i]
            
    # Convert to the natural Python/Numpy representation of R's logical vector
    # If the result contains NAs, return as an object array with np.nan for NA.
    # Otherwise, return as a boolean array.
    has_nan = False
    final_list = []
    for x in res:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            has_nan = True
            final_list.append(np.nan)
        else:
            final_list.append(bool(x))
            
    if has_nan:
        return np.array(final_list, dtype=object)
    else:
        return np.array(final_list, dtype=bool)
