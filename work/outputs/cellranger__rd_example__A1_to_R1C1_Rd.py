# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np
import re

# r2py:entity:A1_to_R1C1
def a1_to_r1c1(coords, strict=True):
    """
    Translates Excel-style A1 notation to R1C1 coordinates.
    """
    def convert(cell):
        if pd.isna(cell) or not isinstance(cell, str):
            return np.nan
        
        # Matches pattern like A1 or A$1 or $A$1
        match = re.match(r'^(\$)?([A-Z]+)(\$)?(\d+)$', cell)
        if not match:
            return np.nan
        
        col_str, row_str = match.group(2), match.group(4)
        
        # Convert column letters to number (A=1, B=2, etc.)
        col_num = 0
        for char in col_str:
            col_num = col_num * 26 + (ord(char) - ord('A') + 1)
        
        # Determine referencing style (Relative vs Absolute)
        # R1C1 format: R[row]C[col]. Adding $ makes it absolute.
        row_ref = f"R{row_str}" if match.group(3) == "$" else f"R[{row_str}]"
        col_ref = f"C{col_num}" if match.group(1) == "$" else f"C[{col_num}]"
        
        return f"{row_ref}{col_ref}"

    # Handle vector/list input
    if isinstance(coords, (list, pd.Series, np.ndarray)):
        results = [convert(c) for c in coords]
        
        # Simulating R's strict behavior: check if any failed to match
        if strict and any(res is np.nan for res in results):
            import warnings
            warnings.warn("Some coordinates could not be parsed strictly.")
            
        return results
    else:
        res = convert(coords)
        if strict and res is np.nan:
            import warnings
            warnings.warn("Coordinate could not be parsed strictly.")
        return res

# Tests
# r2py:entity:A1_to_R1C1
print(a1_to_r1c1("$A$1"))
# r2py:entity:A1_to_R1C1_1
print(a1_to_r1c1("A1"))                    # raises warning, returns nan
# r2py:entity:A1_to_R1C1_2
print(a1_to_r1c1("A1", strict=False))      # no warning
# r2py:entity:A1_to_R1C1_3
print(a1_to_r1c1(["A1", "B$4"]))          # raises warning, contains nan
# r2py:entity:A1_to_R1C1_4
print(a1_to_r1c1(["A1", "B$4"], strict=False))