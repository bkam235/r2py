import numpy as np
import pandas as pd
from typing import Optional, Union, Any

# Mocking bit package behavior for structural equivalence
# r2py:entity:b
class BitArray:
    def __init__(self, data):
        # R's as.bit handles NA by treating them as FALSE or skipping 
        # depending on the specific internal C implementation, 
        # but the resulting 'bit' object is a compact bitset.
        # For the sake of this example, we store as a boolean numpy array.
        self.data = np.array(data, dtype=bool) if data is not None else np.array([], dtype=bool)
        self.length = len(self.data)

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.data[key]
        return self.data[key]

def as_bit(x):
    # In R, as.bit(c(NA, FALSE, TRUE)) converts NAs to FALSE
    if isinstance(x, pd.Series):
        return BitArray(x.fillna(False).astype(bool).values)
    if isinstance(x, np.ndarray):
        # Handle NaNs in object arrays
        mask = np.isnan(x) if x.dtype == float else np.zeros(x.shape, dtype=bool)
        cleaned = np.where(mask, False, x).astype(bool)
        return BitArray(cleaned)
    return BitArray(np.array(x, dtype=bool))

# r2py:entity:all
def r_all(x, range_val: Optional[list] = None):
    # range_val is 1-indexed [start, end]
    data = x.data if isinstance(x, BitArray) else np.array(x, dtype=bool)
    if range_val is not None:
        start = range_val[0] - 1
        end = range_val[1]
        return np.all(data[start:end])
    return np.all(data)

# r2py:entity:min
def r_min(x):
    # For 'bit' objects, min() returns the index (1-based) of the first TRUE
    if isinstance(x, BitArray):
        indices = np.where(x.data)[0]
        return indices[0] + 1 if len(indices) > 0 else 0 # simplified
    
    # For logical vectors with NA, min(l) is NA if any NA is present
    if isinstance(x, pd.Series) and x.isna().any():
        return np.nan
    return np.min(x)

# r2py:entity:sum
def r_sum(x, range_val: Optional[list] = None):
    if isinstance(x, BitArray):
        data = x.data
        if range_val is not None:
            start = range_val[0] - 1
            end = range_val[1]
            return np.sum(data[start:end])
        return np.sum(data)
    
    if isinstance(x, pd.Series) and x.isna().any():
        return np.nan
    return np.sum(x)

# r2py:entity:summary_1
def summary_booltype(x, range_val: Optional[list] = None):
    # Mimics summary.bit or summary.booltype
    # Result: c(FALSE = ..., TRUE = ..., Min. = ..., Max. = ...)
    if not isinstance(x, BitArray):
        x = as_bit(x)
    
    data = x.data
    if range_val is not None:
        start = range_val[0] - 1
        end = range_val[1]
        data = data[start:end]
    
    s = np.sum(data)
    total = len(data)
    
    # Find range of TRUE indices
    indices = np.where(data)[0]
    if len(indices) > 0:
        min_idx = indices[0] + 1
        max_idx = indices[-1] + 1
    else:
        min_idx = np.nan
        max_idx = np.nan
        
    return {
        "FALSE": total - s,
        "TRUE": s,
        "Min.": min_idx,
        "Max.": max_idx
    }

# r2py:entity:summary
def summary_logical(x):
    # Mimics summary.default for logical vectors
    # Returns table with Mode, FALSE, TRUE, NAs
    s = pd.Series(x)
    counts = s.value_counts(dropna=False)
    
    # R output: Mode logical, FALSE count, TRUE count, NAs count
    res = {"Mode": "logical"}
    res["FALSE"] = counts.get(False, 0)
    res["TRUE"] = counts.get(True, 0)
    res["NAs"] = counts.get(np.nan, 0)
    return res

# --- Execution ---

# l <- c(NA, FALSE, TRUE)
# r2py:entity:l
l = pd.Series([np.nan, False, True])

# b <- as.bit(l)
# r2py:entity:b
b = as_bit(l)

# all(l)
# r2py:entity:all
print(f"[1] {r_all(l)}")

# all(b)
# r2py:entity:all_1
print(f"[1] {r_all(b)}")

# all(b, range=c(3, 3))
# r2py:entity:all_2
print(f"[1] {r_all(b, range_val=[3, 3])}")

# all.booltype(l, range=c(3, 3))
# r2py:entity:all.booltype
print(f"[1] {r_all(l, range_val=[3, 3])}")

# min(l)
# r2py:entity:min
res_min_l = r_min(l)
print(f"[1] {res_min_l if not np.isnan(res_min_l) else 'NA'}")

# min(b)
# r2py:entity:min_1
res_min_b = r_min(b)
print(f"[1] {res_min_b}")

# sum(l)
# r2py:entity:sum
res_sum_l = r_sum(l)
print(f"[1] {res_sum_l if not np.isnan(res_sum_l) else 'NA'}")

# sum(b)
# r2py:entity:sum_1
print(f"[1] {r_sum(b)}")

# summary(l)
# r2py:entity:summary
sum_l = summary_logical(l)
print(f"Mode   {sum_l['FALSE']}    {sum_l['TRUE']}     {sum_l['NAs']}")
print(f"logical       {sum_l['FALSE']}       {sum_l['TRUE']}       {sum_l['NAs']}")

# summary(b)
# r2py:entity:summary_1
sum_b = summary_booltype(b)
print(f"      FALSE  TRUE  Min.  Max.\n    {sum_b['FALSE']}     {sum_b['TRUE']}     {sum_b['Min.']}     {sum_b['Max.']}")

# summary.booltype(l)
# r2py:entity:summary.booltype
sum_bl = summary_booltype(l)
print(f"      FALSE  TRUE  Min.  Max.\n    {sum_bl['FALSE']}     {sum_bl['TRUE']}     {sum_bl['Min.']}     {sum_bl['Max.']}")