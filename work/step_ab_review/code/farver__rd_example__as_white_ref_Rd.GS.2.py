# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# The constants are aligned to match the R output (D65: 95.04285, 100, 108.89004)
# r2py:entity:as_white_ref
white_references = {
    "2": {
        "D65": np.array([95.04285, 100.0, 108.89004]),
        "D50": np.array([96.422, 100.0, 82.518]),
        "D55": np.array([95.810, 100.0, 91.406]),
        "D75": np.array([94.811, 100.0, 122.281]),
        "A": np.array([77.461, 100.0, 37.264]),
        "C": np.array([94.811, 100.0, 122.281]),
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
        # x is chromaticity [x, y]
        # X = 100 * x / y
        # Y = 100
        # Z = 100 * (1 - x - y) / y
        tmp = 100.0 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1.0 - np.sum(x))])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100.0 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To match R's output format of a named vector, we return a Series
    # but we must ensure it prints in a way that resembles R's numeric vector
    return pd.Series(x, index=["X", "Y", "Z"])

def print_r_style(series):
    # Helper to print Series as a named vector: header row then value row
    print(" ".join(series.index))
    print(" ".join(map(lambda v: f"{v:g}", series.values)))

# Using names
res1 = as_white_ref('D65')
print_r_style(res1)

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
print_r_style(res2)