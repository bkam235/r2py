import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# fow=2 usually refers to the CIE 1931 2-degree observer
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
        # Check if it is a sequence for the chromaticity case
        if not hasattr(x, '__iter__'):
             raise TypeError("White reference must be a numeric vector")
    
    x = np.asanyarray(x, dtype=float)
    
    if len(x) == 2:
        # Chromaticity values x, y -> Tristimulus X, Y, Z
        # x = X / (X + Y + Z), y = Y / (X + Y + Z)
        # If Y = 100, then X = 100 * x / y, Z = 100 * (1 - x - y) / y
        tmp = 100 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1 - np.sum(x))])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To simulate structure(x, names = c("X", "Y", "Z")), return a pandas Series
    return pd.Series(x, index=["X", "Y", "Z"])

def print_r_vector(s):
    """Helper to print pandas Series in R's named vector format"""
    print("      " + " ".join(s.index))
    print(" ".join(f"{val:10.5g}" for val in s.values))

# Using names
res1 = as_white_ref('D65')
print_r_vector(res1)

# Using chromaticity values
res2 = as_white_ref(np.array([0.3, 0.4]))
print_r_vector(res2)