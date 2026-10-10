import numpy as np
import pandas as pd

def r_sparse_logical(values, positions, length, default=False):
    """
    Create a sparse logical vector.
    
    Parameters:
    - values: numpy array of logical values (with NaN for NA)
    - positions: numpy array of positions (1-based indexing)
    - length: integer length of the result
    - default: logical default value (False or True)
    
    Returns:
    - numpy array of logical values with NaN for NA
    """
    
    # Validate default is bool
    if not isinstance(default, (bool, np.bool_)):
        raise TypeError("default must be logical")
    
    # Validate length is integer
    if not isinstance(length, (int, np.integer)):
        length = int(length)
    
    # Validate length is positive
    if length < 0:
        raise ValueError("length must be non-negative")
    
    # Convert inputs to numpy arrays
    if values is None or (isinstance(values, np.ndarray) and values.size == 0):
        values = np.array([], dtype=float)
    else:
        values = np.asarray(values, dtype=float)
    
    if positions is None or (isinstance(positions, np.ndarray) and positions.size == 0):
        positions = np.array([], dtype=int)
    else:
        positions = np.asarray(positions, dtype=int)
    
    # Validate values are logical (boolean or NaN)
    if values.size > 0:
        valid_mask = np.isnan(values) | (values == 0.0) | (values == 1.0)
        if not np.all(valid_mask):
            raise ValueError("values must be logical (TRUE/FALSE/NA)")
    
    # Validate positions
    if positions.size != values.size:
        raise ValueError("positions and values must have the same length")
    
    if positions.size > 0:
        if np.any(positions < 1) or np.any(positions > length):
            raise ValueError(f"positions must be between 1 and {length}")
    
    # Check that values don't equal default (except for NA)
    if values.size > 0:
        # Check non-NA values
        non_na_mask = ~np.isnan(values)
        non_na_values = values[non_na_mask]
        default_as_float = float(default)
        
        if np.any(non_na_values == default_as_float):
            offenders = np.where((values == default_as_float) & ~np.isnan(values))[0] + 1  # 1-based
            raise ValueError(f"values value must not be equal to the default {default}. {default} values at index: {offenders.tolist()}")
    
    # Create result array filled with default value
    result = np.full(length, float(default), dtype=float)
    
    # Fill in the sparse values at specified positions (convert from 1-based to 0-based)
    if positions.size > 0:
        result[positions - 1] = values
    
    return result
