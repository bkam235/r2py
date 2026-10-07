import numpy as np
import pandas as pd
import re

def r_sub(pattern, replacement, x, ignore_case=False, perl=False, fixed=False, useBytes=False):
    # Handle potential pandas NA types safely
    def is_na(val):
        if val is None: return True
        try:
            if pd.isna(val): return True
        except:
            pass
        return False

    # Detect if x is a single string or a collection
    is_single_string = isinstance(x, str)
    
    if is_single_string:
        x_arr = np.array([x], dtype=object)
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_arr = np.array(x, dtype=object)
    else:
        x_arr = np.array([str(x)], dtype=object)

    pattern_str = str(pattern)
    replacement_str = str(replacement)

    flat_x = x_arr.ravel()
    flat_res = np.empty(flat_x.shape, dtype=object)

    for i in range(len(flat_x)):
        val = flat_x[i]
        
        if is_na(val):
            flat_res[i] = np.nan
            continue
        
        val_str = str(val)
        
        if fixed:
            # Replace first occurrence of literal string
            idx = val_str.find(pattern_str)
            if idx != -1:
                val_str = val_str[:idx] + replacement_str + val_str[idx + len(pattern_str):]
        else:
            # Regular expression replacement (first match only)
            flags = re.IGNORECASE if ignore_case else 0
            # R's sub() replaces only the first occurrence
            val_str = re.sub(pattern_str, replacement_str, val_str, count=1, flags=flags)
            
        flat_res[i] = val_str

    res_arr = flat_res.reshape(x_arr.shape)

    if is_single_string:
        return res_arr.item()
    
    # Return as numpy array to match R vector behavior
    return res_arr
