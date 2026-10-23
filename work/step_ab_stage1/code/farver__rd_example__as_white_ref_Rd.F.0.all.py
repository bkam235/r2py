# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# fow=2 usually refers to the CIE 1931 2-degree observer
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
        tmp = 100 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1 - np.sum(x))])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # R's as_white_ref returns a named vector. 
    # To match the output printing of R, we use a pandas Series but we must format the print carefully.
    return pd.Series(x, index=["X", "Y", "Z"])

def print_r_vector(series):
    # Helper to simulate R's print.default for named numeric vectors
    print("      X         Y         Z ")
    print(f"{series['X']:10.5f} {series['Y']:10.5f} {series['Z']:10.5f}".replace(".00000", ".0"))

# Using names
res1 = as_white_ref('D65')
print("      X         Y         Z ")
print(f"{res1['X']:10.5f} {res1['Y']:10.5f} {res1['Z']:10.5f}")

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
print("      X   Y   Z ")
print(f"{res2['X']:10.0f} {res2['Y']:4.0f} {res2['Z']:4.0f}".replace("    ", " "))