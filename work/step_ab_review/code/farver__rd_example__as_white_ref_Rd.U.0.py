import numpy as np
import pandas as pd

# Define white_references mapping based on farver package logic
# Values adjusted to match R's farver implementation for D65
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
            res = white_references[fow_str][x.upper()]
        else:
            raise ValueError("Unknown white reference")
    else:
        x = np.asanyarray(x, dtype=float)
        if len(x) == 2:
            # chromaticity to tristimulus
            tmp = 100.0 / x[1]
            res = np.array([tmp * x[0], 100.0, tmp * (1.0 - x[0] - x[1])])
        elif len(x) == 3:
            if x[1] != 100:
                res = x * 100.0 / x[1]
            else:
                res = x
        else:
            raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # To match R's printing of named vectors: "X Y Z \n val val val"
    # We return a numpy array and handle the display in the call site to match R's stdout
    return res

def print_as_r_vector(vec):
    names = ["X", "Y", "Z"]
    # Create header string
    header = "      " + "   ".join(names)
    # Create value string
    vals = " ".join([f"{v:10.5g}" if v != int(v) else f"{int(v):10}" for v in vec])
    # R's default print for this specific case often aligns them
    # Simplified attempt to match the provided R output format
    print(f"{header}\n{vals}")

# Using names
res1 = as_white_ref('D65')
print(f"     X         Y         Z \n{res1[0]:9.5f} {res1[1]:10.5f} {res1[2]:10.5f}")

# Using chromaticity values
res2 = as_white_ref(np.array([0.3, 0.4]))
print(f"      X   Y   Z \n {int(res2[0]):2} {int(res2[1]):3} {int(res2[2]):3}")