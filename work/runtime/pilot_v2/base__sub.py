import numpy as np
import pandas as pd
import re

def r_sub(pattern, replacement, x, ignore_case=False, perl=False, fixed=False, useBytes=False):
    # Handle factor-like input (pandas Category)
    if isinstance(x, pd.Series) and isinstance(x.dtype, pd.CategoricalDtype):
        levels = x.cat.categories.tolist()
        # R's sub on factors: replace in levels, then remap
        # Note: The logic 'length(levels(x)) < length(x)' is a shortcut in R.
        # We apply the substitution to the levels.
        new_levels = r_sub(pattern, replacement, np.array(levels), ignore_case, perl, fixed, useBytes)
        # Create a mapping from old levels to new levels
        mapping = dict(zip(levels, new_levels))
        return np.array([mapping[val] if val in mapping else np.nan for val in x])

    # Ensure x is handled as a vector of strings
    if isinstance(x, (pd.Series, pd.Index)):
        x_vals = x.values
    elif isinstance(x, np.ndarray):
        x_vals = x
    elif hasattr(x, "__iter__") and not isinstance(x, (str, bytes)):
        x_vals = np.array(x)
    else:
        x_vals = np.array([x])

    # Cast to string/character (handling NA/NaN)
    # In R, sub(..., NA) returns NA.
    # We use object array to preserve NaNs.
    
    # Convert pattern and replacement to strings (R's as.character)
    pat = str(pattern) if not pd.isna(pattern) else ""
    rep = str(replacement) if not pd.isna(replacement) else ""

    results = []
    for item in x_vals:
        if pd.isna(item):
            results.append(np.nan)
            continue
        
        s = str(item)
        
        if fixed:
            # Fixed string replacement (only first occurrence)
            # R's sub replaces only the first match.
            # Python's replace(old, new, 1) does exactly this.
            results.append(s.replace(pat, rep, 1))
        else:
            # Regular expression replacement
            flags = 0
            if ignore_case:
                flags |= re.IGNORECASE
            
            # R's sub replaces only the first match.
            # re.sub(pattern, repl, string, count=1)
            # Note: R uses a different regex engine than Python (PCRE vs Python),
            # but for standard 'sub' calls, re.sub is the closest equivalent.
            # We use re.sub with count=1.
            try:
                res = re.sub(pat, rep, s, count=1, flags=flags)
                results.append(res)
            except re.error:
                # If regex is invalid, R usually returns the original string 
                # or throws error. Based on typical behavior:
                results.append(s)

    # Return as a numpy array (which is the Python equivalent of R's character vector)
    # However, if input x was a single string (scalar), R returns a single string.
    res_array = np.array(results, dtype=object)
    
    # Handle return shape to match R's behavior
    # If original x was a scalar, return a scalar.
    if not isinstance(x, (np.ndarray, pd.Series, pd.Index, list)):
        return res_array[0]
    
    # For character vectors, R returns a character vector.
    # We return a numpy array of strings/NaNs.
    return res_array
