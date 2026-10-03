# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import pandas as pd

class SparseVector:
    def __init__(self, values, positions, length, default):
        self.values = np.array(values)
        self.positions = np.array(positions)
        self.length = length
        self.default = default

    def to_dense(self):
        # Create a dense array filled with the default value
        if isinstance(self.default, str):
            dense = np.full(self.length, self.default, dtype=object)
        elif np.issubdtype(type(self.default), np.integer):
            dense = np.full(self.length, self.default, dtype=int)
        else:
            dense = np.full(self.length, self.default, dtype=float)
        
        # R positions are 1-indexed
        if len(self.values) > 0:
            indices = self.positions.astype(int) - 1
            dense[indices] = self.values
        return dense

    def __repr__(self):
        dense = self.to_dense()
        # Formatting to match R's [1] 10 0 0 ... output
        if np.issubdtype(dense.dtype, np.integer):
            res = " ".join(map(str, dense.astype(int)))
        elif np.issubdtype(dense.dtype, np.floating):
            # R's print often omits .0 for whole numbers in simple vectors
            res = " ".join([f"{x:g}" for x in dense])
        else:
            # For characters, R quotes them if they have spaces or are empty, 
            # but the example output shows "" for defaults and "A" etc.
            res = " ".join([f'"{x}"' if x == "" or x is None else f'"{x}"' for x in dense])
        
        return f"[1] {res}"

def sparse_double(values, positions, length, default=0.0):
    return SparseVector(values, positions, length, float(default))

def sparse_integer(values, positions, length, default=0):
    return SparseVector(values, positions, length, int(default))

def sparse_character(values, positions, length, default=""):
    return SparseVector(values, positions, length, str(default))

def sparse_default(x):
    return x.default

def sparse_values(x):
    return x.values

def sparse_positions(x):
    return x.positions

# r2py:entity:sparse_replace_na
def sparse_replace_na(x, replace):
    default = sparse_default(x)
    values = sparse_values(x)
    positions = sparse_positions(x)
    
    if len(values) == 0:
        return x
    
    # Use pandas.isna to handle various NA types (np.nan, None, etc.)
    mask_na = pd.isna(values)
    
    if replace == default:
        # Remove elements that are NA
        new_values = values[~mask_na]
        new_positions = positions[~mask_na]
    else:
        # Replace NA values with the replace value
        new_values = values.copy()
        new_values[mask_na] = replace
        new_positions = positions
        
    # Determine the constructor based on the type of values
    if np.issubdtype(new_values.dtype, np.integer) or (len(new_values) > 0 and isinstance(new_values[0], (int, np.integer))):
        return sparse_integer(new_values, new_positions, x.length, default)
    elif np.issubdtype(new_values.dtype, np.floating) or (len(new_values) > 0 and isinstance(new_values[0], (float, np.floating))):
        return sparse_double(new_values, new_positions, x.length, default)
    else:
        return sparse_character(new_values, new_positions, x.length, default)

# Example 1
# r2py:entity:sparse_replace_na
res1 = sparse_replace_na(
    sparse_double([10, np.nan, 11], [1, 5, 10], 10),
    5
)
print(res1)

# Example 2
# r2py:entity:sparse_replace_na_1
res2 = sparse_replace_na(
    sparse_integer([10, np.nan, 11], [1, 5, 10], 10),
    5
)
print(res2)

# Example 3
# r2py:entity:sparse_replace_na_2
res3 = sparse_replace_na(
    sparse_character(["A", None, "E"], [2, 5, 10], 10),
    "missing"
)
print(res3)