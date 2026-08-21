# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 15

import pandas as pd
import numpy as np

# r2py:entity:slice_sample
def slice_sample(data, n=None, prop=None, weight_by=None, replace=False):
    """
    Equivalent to dplyr::slice_sample.
    """
    # Determine the number of rows to sample
    if prop is not None:
        sample_size = int(len(data) * prop)
    elif n is not None:
        sample_size = n
    else:
        raise ValueError("Either 'n' or 'prop' must be specified.")

    # Weights handling
    weights = None
    if weight_by is not None:
        if isinstance(weight_by, str):
            weights = data[weight_by]
        else:
            # Handle cases where weight_by might be a series/array passed explicitly
            weights = weight_by

    # Handle case where n > length(df) and replace=False
    # dplyr::slice_sample just returns all rows if n > size and replace=False
    if not replace and sample_size > len(data):
        sample_size = len(data)

    return data.sample(n=sample_size, replace=replace, weights=weights)

# r2py:entity:sample_n
def sample_n(tbl, size, replace=False, weight=None):
    """Superseded by slice_sample."""
    # sample_n errors if size > length and replace=False
    if not replace and size > len(tbl):
        raise ValueError("sample_n() would error if n was bigger than the group size")
    
    return slice_sample(tbl, n=size, replace=replace, weight_by=weight)

# r2py:entity:sample_frac
def sample_frac(tbl, size=1, replace=False, weight=None):
    """Superseded by slice_sample."""
    return slice_sample(tbl, prop=size, replace=replace, weight_by=weight)

# Main script execution
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 6), 'w': [0.1, 0.1, 0.1, 2, 2]})

# sample_n() -> slice_sample() ----------------------------------------------
# Was:
# r2py:entity:sample_n
print(sample_n(df, 3))
# r2py:entity:sample_n_1
print(sample_n(df, 10, replace=True))
# r2py:entity:sample_n_2
print(sample_n(df, 3, weight='w'))

# Now:
# r2py:entity:slice_sample
print(slice_sample(df, n=3))
# r2py:entity:slice_sample_1
print(slice_sample(df, n=10, replace=True))
# r2py:entity:slice_sample_2
print(slice_sample(df, n=3, weight_by='w'))

# Note that sample_n() would error if n was bigger than the group size
# slice_sample() will just use the available rows
# r2py:entity:try
try:
    sample_n(df, 10)
except ValueError as e:
    print(f"Caught expected error: {e}")

# r2py:entity:slice_sample_3
print(slice_sample(df, n=10))

# sample_frac() -> slice_sample() -------------------------------------------
# Was:
# r2py:entity:sample_frac
print(sample_frac(df, 0.25))
# r2py:entity:sample_frac_1
print(sample_frac(df, 2, replace=True))

# Now:
# r2py:entity:slice_sample_4
print(slice_sample(df, prop=0.25))
# r2py:entity:slice_sample_5
print(slice_sample(df, prop=2, replace=True))