import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# The values are standard CIE XYZ white points for the 2-degree observer (fow=2)
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
    
    return pd.Series(x, index=["X", "Y", "Z"])

def print_r_style(series):
    """Helper to print pandas Series in R's named vector format."""
    names = " ".join(series.index)
    # Formatting floats to match R's default print (roughly)
    values = " ".join([f"{v:g}" if v == int(v) else f"{v:.5g}" for v in series.values])
    # R prints the index on one line and values on the next for short vectors
    # But for this specific farver output, it's often:
    #      X         Y         Z 
    # 95.04285 100.00000 108.89004
    print(f"     {'  '.join(series.index)}")
    print(f"{series.values[0]:.5f} {series.values[1]:.5f} {series.values[2]:.5f}")

# Using names
# r2py:entity:as_white_ref
res1 = as_white_ref('D65')
# We use a manual print to match R's output formatting exactly
print(f"     X         Y         Z ")
print(f"{res1['X']:.5f} {res1['Y']:.5f} {res1['Z']:.5f}")

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
print(f"     X   Y   Z ")
print(f"{res2['X']:g} {res2['Y']:g} {res2['Z']:g}")