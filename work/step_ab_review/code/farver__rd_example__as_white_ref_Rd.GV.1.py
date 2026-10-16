import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# D65 in R farver: X=95.04285, Y=100.00000, Z=108.89004
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
        # Chromaticity to tristimulus: X = 100*x, Y = 100, Z = 100*(1-x-y)
        # Wait, R farver as_white_ref logic for length 2:
        # x = c(0.3, 0.4) -> X=75, Y=100, Z=75? 
        # No: if x = [0.3, 0.4], X = 0.3/(0.3+0.4+0.3)*100? No.
        # Looking at output: as_white_ref(c(0.3, 0.4)) -> 75 100 75
        # Calculation: 0.3 / (0.3 + 0.4 + (1-0.3-0.4)) is 0.3. 
        # Actually: if length is 2, it's treated as chromaticity x, y.
        # X = x * 100 / y, Y = 100, Z = (1 - x - y) * 100 / y
        # For x=0.3, y=0.4: X = 0.3/0.4*100 = 75, Y = 100, Z = (1-0.7)/0.4*100 = 75.
        tmp = 100.0 / x[1]
        x = np.array([x[0] * tmp, 100.0, (1.0 - np.sum(x)) * tmp])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100.0 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To match R's print output for a named vector, we use a Series 
    # but we will format the print call outside or return the series.
    return pd.Series(x, index=["X", "Y", "Z"])

def r_print(s):
    # Mimics R's print for a named numeric vector
    print("      " + " ".join(s.index))
    print(" ".join(map(lambda v: f"{v:g}", s.values)))

# Using names
res1 = as_white_ref('D65')
r_print(res1)

# Using chromaticity values
# r2py:entity:as_white_ref_1
res2 = as_white_ref(np.array([0.3, 0.4]))
r_print(res2)