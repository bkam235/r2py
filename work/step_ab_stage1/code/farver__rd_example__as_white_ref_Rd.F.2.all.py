# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# fow=2 usually refers to the CIE 1931 2-degree observer
# r2py:entity:as_white_ref
white_references = {
    "2": {
        "D65": np.array([0.9504285, 1.00000, 1.0889004]),
        "D50": np.array([0.96422, 1.00000, 0.82518]),
        "D55": np.array([0.95810, 1.00000, 0.91406]),
        "D75": np.array([0.94811, 1.00000, 1.22281]),
        "A": np.array([0.77461, 1.00000, 0.37264]),
        "C": np.array([0.94811, 1.00000, 1.22281]),
    }
}

def as_white_ref(x, fow=2):
    if isinstance(x, str):
        fow_str = str(fow)
        if fow_str in white_references and x.upper() in white_references[fow_str]:
            # Convert 0-1 scale to 0-100 scale as R does for these constants
            x = white_references[fow_str][x.upper()] * 100
        else:
            raise ValueError("Unknown white reference")
            
    if isinstance(x, (int, float)):
        x = np.array([x])
    
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        raise TypeError("White reference must be a numeric vector")
    
    x = np.asanyarray(x, dtype=float)
    
    if len(x) == 2:
        tmp = 100 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1 - np.sum(x))])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    return pd.Series(x, index=["X", "Y", "Z"])

def r_print_named_vector(s):
    # Simulates R's printing of a named numeric vector
    names = " ".join(s.index)
    values = " ".join(map(lambda v: f"{v:g}", s.values))
    print(f"      {names}")
    print(f"{values}")

# Using names
res1 = as_white_ref('D65')
r_print_named_vector(res1)

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
r_print_named_vector(res2)