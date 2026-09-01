# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import numpy as np
import pandas as pd

# r2py:entity:bit_unique
def bit_unique(x, na_rm=None, range_na=None):
    # R's bit_unique is a fast implementation of unique() for integers
    # na.rm = NA (None) -> NA is treated as a value (kept)
    # na.rm = TRUE -> NAs are removed
    # na.rm = FALSE -> NA is treated as a value, but specific to bit_unique logic
    
    # Convert to numpy array for handling
    arr = np.array(x)
    
    if na_rm is True:
        # Remove NAs first, then get unique values
        mask = ~pd.isna(arr)
        return np.unique(arr[mask])
    
    # R's unique(..., incomparables=FALSE) treats NA as a value
    # np.unique handles np.nan correctly (keeps one)
    return np.unique(arr)

# r2py:entity:bit_duplicated
def bit_duplicated(x, na_rm=None, range_na=None):
    # Returns a boolean array indicating duplicates
    arr = np.array(x)
    
    # Handle NA logic equivalent to R's duplicated()
    # In R, duplicated(x, incomparables=FALSE) treats NA as a value.
    # duplicated(x, incomparables=NA) treats NA as distinct (all NAs are unique)
    
    if na_rm is True:
        # All NAs are considered duplicates of previous NAs (or just marked True)
        # Logic: duplicated(x, FALSE) | is.na(x)
        is_na = pd.isna(arr)
        # We find duplicates treating NA as a value, then force all NAs to True
        duplicated_mask = np.zeros(len(arr), dtype=bool)
        seen = set()
        for i, val in enumerate(arr):
            # Normalize nan for set lookup
            v = val if not pd.isna(val) else 'NA_TOKEN'
            if v in seen:
                duplicated_mask[i] = True
            else:
                seen.add(v)
        return duplicated_mask | is_na
    
    elif na_rm is False:
        # NA is incomparable (each NA is unique)
        duplicated_mask = np.zeros(len(arr), dtype=bool)
        seen = set()
        for i, val in enumerate(arr):
            if pd.isna(val):
                continue
            if val in seen:
                duplicated_mask[i] = True
            else:
                seen.add(val)
        return duplicated_mask
    
    else: # na_rm is None (NA)
        # Treat NA as a normal value
        duplicated_mask = np.zeros(len(arr), dtype=bool)
        seen = set()
        for i, val in enumerate(arr):
            v = val if not pd.isna(val) else 'NA_TOKEN'
            if v in seen:
                duplicated_mask[i] = True
            else:
                seen.add(v)
        return duplicated_mask

# r2py:entity:bit_anyDuplicated
def bit_anyDuplicated(x, na_rm=None, range_na=None):
    # Returns the index of the first duplicate (1-based in R) or 0
    dups = bit_duplicated(x, na_rm=na_rm, range_na=range_na)
    indices = np.where(dups)[0]
    return int(indices[0] + 1) if len(indices) > 0 else 0

# r2py:entity:bit_sumDuplicated
def bit_sumDuplicated(x, na_rm=None, range_na=None):
    # Returns the total count of duplicates
    dups = bit_duplicated(x, na_rm=na_rm, range_na=range_na)
    return int(np.sum(dups))

# Input data
data = [2, 1, np.nan, np.nan, 1, 2]

# Tests for bit_unique
# r2py:entity:bit_unique
print(bit_unique(data))
# r2py:entity:bit_unique_1
print(bit_unique(data, na_rm=False))
# r2py:entity:bit_unique_2
print(bit_unique(data, na_rm=True))

# Tests for bit_duplicated
# r2py:entity:bit_duplicated
print(bit_duplicated(data))
# r2py:entity:bit_duplicated_1
print(bit_duplicated(data, na_rm=False))
# r2py:entity:bit_duplicated_2
print(bit_duplicated(data, na_rm=True))

# Tests for bit_anyDuplicated
# r2py:entity:bit_anyDuplicated
print(bit_anyDuplicated(data))
# r2py:entity:bit_anyDuplicated_1
print(bit_anyDuplicated(data, na_rm=False))
# r2py:entity:bit_anyDuplicated_2
print(bit_anyDuplicated(data, na_rm=True))

# Tests for bit_sumDuplicated
# r2py:entity:bit_sumDuplicated
print(bit_sumDuplicated(data))
# r2py:entity:bit_sumDuplicated_1
print(bit_sumDuplicated(data, na_rm=False))
# r2py:entity:bit_sumDuplicated_2
print(bit_sumDuplicated(data, na_rm=True))