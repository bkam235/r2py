import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# Values updated to match R's specific precision for D65
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
        # Chromaticity to tristimulus: X = 100*x/y, Y = 100, Z = 100*(1-x-y)/y
        tmp = 100 / x[1]
        x = np.array([tmp * x[0], 100.0, tmp * (1 - np.sum(x))])
    elif len(x) == 3:
        if x[1] != 100:
            x = x * 100 / x[1]
    else:
        raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To simulate structure(x, names = c("X", "Y", "Z")), return a pandas Series
    return pd.Series(x, index=["X", "Y", "Z"])

# Using names
# R produces:
#      X         Y         Z 
# 95.04285 100.00000 108.89004
res_name = as_white_ref('D65')
print(f"      X         Y         Z ")
print(f" {res_name[0]:.5f} {res_name[1]:.5f} {res_name[2]:.5f}")

# Using chromaticity values
# R produces:
#      X   Y   Z 
# 75 100  75
res_chrom = as_white_ref(np.array([0.3, 0.4]))
print(f"      X   Y   Z ")
print(f" {int(res_chrom[0])} {int(res_chrom[1])} {int(res_chrom[2])}")