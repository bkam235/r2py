# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 5

import numpy as np
import math

# r2py:entity:as.bit
def as_bit(x):
    """
    Convert values to bit (logical) representation, mimicking R's as.bit behavior.
    R rules:
    - For integer/double: 0 -> FALSE, NA -> FALSE, any other value -> TRUE
    - For logical/bool: FALSE -> FALSE, TRUE -> TRUE, NA -> FALSE
    """
    result = []
    for val in x:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            result.append(False)
        elif isinstance(val, bool):
            result.append(val)
        elif isinstance(val, (int, float, np.integer, np.floating)):
            result.append(val != 0)
        else:
            result.append(val != 0)
    return result

# r2py:entity:as.bit
def format_bit(result):
    """Format bit vector output like R's print.bit"""
    n = len(result)
    # Calculate number of int32s needed
    n_ints = max(1, (n + 31) // 32)
    header = f"bit length={n} occupying only {n_ints} int32"
    
    # Format values as TRUE/FALSE strings
    val_strs = []
    for val in result:
        val_strs.append("TRUE" if val else "FALSE")
    
    # R uses fixed-width columns, right-aligned
    # Column width is max of index string width and value string width, at least 5
    idx_strs = [str(i+1) for i in range(n)]
    
    col_widths = []
    for i in range(n):
        w = max(len(idx_strs[i]), len(val_strs[i]))
        col_widths.append(w)
    
    # Format index line and value line
    idx_parts = []
    val_parts = []
    for i in range(n):
        w = col_widths[i]
        idx_parts.append(idx_strs[i].rjust(w))
        val_parts.append(val_strs[i].rjust(w))
    
    idx_line = " ".join(idx_parts)
    val_line = " ".join(val_parts)
    
    return f"{header}\n{idx_line} \n{val_line} "

# r2py:entity:as.bit
result1 = as_bit([0, 1, 2, -2, None])
print(format_bit(result1))

# r2py:entity:as.bit_1
result2 = as_bit([0.0, 1.0, 2.0, -2.0, float('nan')])
print(format_bit(result2))

# r2py:entity:as.bit_2
result3 = as_bit([False, None, True])
print(format_bit(result3))