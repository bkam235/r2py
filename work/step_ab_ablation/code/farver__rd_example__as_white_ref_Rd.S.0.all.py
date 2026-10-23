# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np

# Define white_references mapping based on farver package logic
# Values are the standard CIE 1931 2-degree observer reference whites
white_references = {
    "D65": np.array([0.950303, 1.000000, 1.088840]),
    "D50": np.array([0.964223, 1.000000, 0.825181]),
    "D55": np.array([0.958102, 1.000000, 0.914060]),
    "D75": np.array([0.948112, 1.000000, 1.222812]),
    "A":   np.array([0.774611, 1.000000, 0.372638]),
    "C":   np.array([0.948112, 1.000000, 1.222812]),
}

def as_white_ref(x):
    if isinstance(x, str):
        if x.upper() in white_references:
            res = white_references[x.upper()].copy()
        else:
            raise ValueError("Unknown white reference")
    else:
        x = np.asanyarray(x, dtype=float)
        if len(x) == 2:
            # Chromaticity x, y -> Tristimulus X, Y, Z
            # Y is normalized to 1.0
            # X = x / y, Z = (1 - x - y) / y
            y = x[1]
            res = np.array([x[0]/y, 1.0, (1.0 - x[0] - y)/y])
        elif len(x) == 3:
            # Tristimulus X, Y, Z -> Normalize Y to 1.0
            res = x / x[1]
        else:
            raise ValueError("White reference must be of length 2 (chromaticity) or 3 (tristimulus)")
    
    # R's as_white_ref returns a named numeric vector.
    # In Python, we return a numpy array. To simulate names, we could use a dict or custom object,
    # but for numerical equivalence in tests, a numpy array is standard.
    return res

# Using names
as_white_ref('D65')

# Using chromaticity values
# r2py:entity:as_white_ref_1
as_white_ref(np.array([0.3, 0.4]))