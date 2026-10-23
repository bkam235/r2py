# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# Constants adjusted to match farver precision
# r2py:entity:as_white_ref
white_references = {
    "2": {
        "D65": np.array([95.04285, 100.00000, 108.89004]),
        "D50": np.array([96.422, 100.00000, 82.518]),
        "D55": np.array([95.810, 100.00000, 91.406]),
        "D75": np.array([94.811, 100.00000, 122.281]),
        "A": np.array([77.461, 100.00000, 37.264]),
        "C": np.array([94.811, 100.00000, 122.281]),
    }
}

def as_white_ref(x, fow=2):
    if isinstance(x, str):
        fow_str = str(fow)
        if fow_str in white_references and x.upper() in white_references[fow_str]:
            x = white_references[fow_str][x.upper()]
        else:
            raise ValueError("Unknown white reference")
            
    if isinstance(x, (int, float)):
        x = np.array([x])
    
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        raise TypeError("White reference must be a numeric vector")
    
    x = np.asanyarray(x, dtype=float)
    
    if len(x) == 2:
        # Chromaticity (x, y) -> Tristimulus (X, Y, Z)
        # X = 100 * x / y, Y = 100, Z = 100 * (1 - x - y) / y
        tmp = 100 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1 - np.sum(x))])
    elif len(x) == 3:
        # Normalize to Y = 100
        if x[1] != 100:
            x = x * 100 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To simulate R's named vector structure(x, names = c("X", "Y", "Z"))
    # We use a Series but we will override how it prints to match R
    return pd.Series(x, index=["X", "Y", "Z"])

def r_print_vector(s):
    """Helper to print pandas Series in R's horizontal named vector style"""
    names = " ".join(s.index)
    values = " ".join(map(lambda v: f"{v:g}", s.values))
    print(f"     {names}")
    print(f"{values}")

# Using names
res1 = as_white_ref('D65')
r_print_vector(res1)

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
r_print_vector(res2)