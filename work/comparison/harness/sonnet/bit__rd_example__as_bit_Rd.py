# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 5

import numpy as np
import pandas as pd
import math

# r2py:entity:as.bit
def as_bit(x):
    """Convert values to bit (boolean) representation like R's bit package."""
    result = []
    for val in x:
        if val is None or (isinstance(val, float) and np.isnan(val)):
            result.append(False)
        elif isinstance(val, bool):
            result.append(val)
        else:
            result.append(val != 0)
    return result

# r2py:entity:as.bit
def print_bit(values):
    """Print bit vector in R's bit package format."""
    n = len(values)
    # Calculate storage: ceil(n / 32) int32s
    n_int32 = math.ceil(n / 32) if n > 0 else 1
    if n_int32 < 1:
        n_int32 = 1
    print(f"bit length={n} occupying only {n_int32} int32")
    
    # Format indices and values
    indices = [str(i+1) for i in range(n)]
    str_vals = ["TRUE" if v else "FALSE" for v in values]
    
    # Calculate column widths
    col_widths = [max(len(indices[i]), len(str_vals[i])) for i in range(n)]
    
    # Print indices right-aligned
    idx_line = " ".join(idx.rjust(w) for idx, w in zip(indices, col_widths))
    val_line = " ".join(val.rjust(w) for val, w in zip(str_vals, col_widths))
    
    print(idx_line)
    print(val_line)

# as.bit(c(0L, 1L, 2L, -2L, NA))
result1 = as_bit([0, 1, 2, -2, None])
print_bit(result1)

# r2py:entity:as.bit_1
# as.bit(c(0, 1, 2, -2, NA))
result2 = as_bit([0.0, 1.0, 2.0, -2.0, float('nan')])
print_bit(result2)

# r2py:entity:as.bit_2
# as.bit(c(FALSE, NA, TRUE))
result3 = as_bit([False, None, True])
print_bit(result3)