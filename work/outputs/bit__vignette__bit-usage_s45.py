# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

import numpy as np

# r2py:entity:bit_rangediff
def bit_rangediff(rx, y, revx=False, revy=False):
    """
    Equivalent to R's bit_rangediff. 
    Calculates the difference between a range [rx[0], rx[1]] and a set of indices y.
    """
    rx = np.asarray(rx, dtype=int)
    y = np.asarray(y, dtype=int)
    
    # Determine the range boundaries
    start, end = rx[0], rx[1]
    # In R, if rx[1] > rx[2], it handles it as a reversed range
    is_reversed_range = start > end
    actual_start = min(start, end)
    actual_end = max(start, end)
    
    # Create a boolean mask for the range [actual_start, actual_end]
    # R indices are 1-based; we treat them as absolute identifiers here
    full_range = np.arange(actual_start, actual_end + 1)
    
    # Create a set for O(1) lookup of elements in y
    y_set = set(y)
    
    # Find elements in the range that are NOT in y (diff)
    # If revy is True, we look for elements that ARE in y (intersection)
    if not revy:
        res = [val for val in full_range if val not in y_set]
    else:
        res = [val for val in full_range if val in y_set]
        
    res = np.array(res, dtype=int)
    
    # Handle revx (reverse the output logic)
    if revx:
        res = res[::-1]
        
    # If the original range was specified in reverse order, R reverses the result
    if is_reversed_range:
        res = res[::-1]
        
    return res

# Equivalent to bit_rangediff(c(1L, 7L), (1:7))
# r2py:entity:bit_rangediff
print(bit_rangediff([1, 7], np.arange(1, 8)))

# Equivalent to bit_rangediff(c(1L, 7L), -(1:7))
# In R, -c(1, 7) in this context usually refers to the set subtraction or specific bit logic.
# However, in bit_rangediff, y is expected to be an integer vector.
# R's -(1:7) creates a vector of negative integers [-1, -2, ..., -7].
# r2py:entity:bit_rangediff_1
print(bit_rangediff([1, 7], -np.arange(1, 8)))

# Equivalent to bit_rangediff(c(1L, 7L), (1:7), revy=TRUE)
# r2py:entity:bit_rangediff_2
print(bit_rangediff([1, 7], np.arange(1, 8), revy=True))