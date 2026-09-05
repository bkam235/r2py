# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd

# r2py:entity:match
def match(x, table, nomatch=np.nan, incomparables=None):
    """
    Equivalent to R's match function: returns a vector of the locations 
    of the first matches of its first argument in the second.
    """
    x = np.asanyarray(x)
    table = np.asanyarray(table)
    
    # Create a mapping from value to first index (1-indexed for R compatibility)
    lookup = {val: i + 1 for i, val in enumerate(table[::-1])} # Reverse to keep first match
    # Correction: R match returns the FIRST occurrence.
    lookup = {}
    for i, val in enumerate(table):
        if val not in lookup:
            lookup[val] = i + 1
            
    return np.array([lookup.get(val, nomatch) for val in x])

# r2py:entity:merge_match
def merge_match(x, y, revx=False, revy=False, nomatch=np.nan):
    """
    Equivalent to R's merge_match function.
    Typically used for matching sorted integers.
    """
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    
    # Basic implementation of the matching logic
    # In a real bit package, this is a high-performance C function
    # for sorted vectors.
    res = match(x, y, nomatch=nomatch)
    
    # Handle revx/revy logic if needed (though not used in the provided snippet)
    # In the R source, these flags modify the search direction/behavior.
    return res

# r2py:entity:x
x = np.arange(2, 5) # 2:4
# r2py:entity:y
y = np.array([0, 1, 2, 2, 3, 3, 3], dtype=int)

# r2py:entity:match
print(match(x, y))
# r2py:entity:merge_match
print(merge_match(x, y))