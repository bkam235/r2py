import numpy as np
import pandas as pd

def r_sparse_logical(values, positions, length, default=False):
    """
    Python reproduction of sparsevctrs::sparse_logical.
    
    Args:
        values (np.ndarray): Logical values (with NaNs for NA).
        positions (np.ndarray): 1-based indices where values are placed.
        length (int): The total length of the resulting vector.
        default (bool): The default value for unfilled positions.
        
    Returns:
        np.ndarray: A boolean/object array representing the logical vector.
    """
    # Validate length
    if not isinstance(length, (int, np.integer)):
        length = int(length)
    
    # Ensure values and positions are numpy arrays for indexing
    values = np.asarray(values)
    positions = np.asarray(positions, dtype=int)
    
    # R's check: if any(values == default, na.rm = TRUE) then abort.
    # We must handle NaNs in values carefully.
    if values.size > 0:
        # Mask out NaNs to simulate na.rm = TRUE
        mask = ~np.isnan(values.astype(float)) if values.dtype == object or np.issubdtype(values.dtype, np.floating) else np.ones(values.shape, dtype=bool)
        # If values are strictly boolean (no NaNs), mask is all True. 
        # If values contain NaNs (object array), we check non-NaNs.
        if np.any(values[mask] == default):
            # In a real scenario, this would raise an exception like cli_abort.
            # Since we are reproducing the logic, we assume valid inputs per examples 
            # or raise an error if the condition is met.
            raise ValueError(f"values value must not be equal to the default {default}.")

    # Initialize result array with the default value
    # Using object dtype to allow for both Booleans and np.nan (R's NA_logical)
    res = np.full(length, default, dtype=object)
    
    # R is 1-indexed. Convert positions to 0-indexed.
    # positions are 1-based indices.
    if positions.size > 0:
        idx = positions - 1
        # Basic bounds checking (though R's validate_positions would handle this)
        res[idx] = values
        
    # Convert to a boolean-like array if no NaNs are present, otherwise keep as object
    # R's logical vectors can contain NA. In numpy, the best representation is object or float
    # but the prompt asks for the natural Python object.
    # For R logicals: TRUE -> True, FALSE -> False, NA -> np.nan
    
    # Clean up the result to match R's logical vector behavior:
    # Replace 1/0/True/False with actual bools and keep np.nan.
    final_res = np.array([bool(x) if pd.notnull(x) else np.nan for x in res], dtype=object)
    
    # If the entire result is just True/False (no NaNs), we can return a bool array
    # but usually, an object array is safer to represent the presence of NA.
    # However, for the specific examples:
    if not np.any(pd.isnull(final_res)):
        return final_res.astype(bool)
    
    return final_res
