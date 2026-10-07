import numpy as np

def r_rep_len(x, length_out):
    """
    Reproduces R's rep_len function.
    Repeats the values of x until the resulting vector has length length_out.
    """
    # Ensure x is a numpy array
    x = np.asanyarray(x)
    
    if length_out <= 0:
        # Return an empty array with the same dtype as x
        return np.array([], dtype=x.dtype)
    
    if length_out == 0:
        return np.array([], dtype=x.dtype)

    # If x is empty, R's rep_len typically returns a vector of NAs or empty 
    # depending on the context, but for a standard vector input:
    if x.size == 0:
        # R's rep_len with empty x returns a vector of length length_out filled with NA
        # However, the dtype depends on what x would have been.
        # In R, rep_len(numeric(0), 5) -> [NA, NA, NA, NA, NA]
        return np.full(length_out, np.nan)

    # Calculate how many times x needs to be tiled and how many elements of the last tile
    num_repeats = length_out // x.size
    remainder = length_out % x.size
    
    # Create the repeated array
    # np.tile repeats the whole array, then we slice to get exactly length_out
    res = np.tile(x, num_repeats + (1 if remainder > 0 else 0))
    
    return res[:length_out]
