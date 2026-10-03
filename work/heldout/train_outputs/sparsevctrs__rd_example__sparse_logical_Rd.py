import numpy as np
import pandas as pd

# r2py:entity:sparse_logical
class SparseLogical:
    """
    Equivalent to sparsevctrs::sparse_logical.
    Stores a logical vector sparsely by keeping only values 
    different from the default.
    """
    def __init__(self, values, positions, length, default=False):
        self.values = np.array(values, dtype=object)
        self.positions = np.array(positions, dtype=int)
        self.length = int(length)
        self.default = default

    def to_dense(self):
        """Expand the sparse representation to a dense numpy array."""
        res = np.full(self.length, self.default, dtype=object)
        if len(self.positions) > 0:
            # R positions are 1-indexed
            res[self.positions - 1] = self.values
        return res

    def __repr__(self):
        # For top-level printing, R prints the expanded vector
        # But we need to handle the huge length case for str()
        if self.length > 100:
            return f"logi [{1}:{self.length}] {self.to_dense()[:6]} ..."
        
        dense = self.to_dense()
        # Convert to R-style logical string representation
        str_vals = []
        for v in dense:
            if pd.isna(v):
                str_vals.append("NA")
            else:
                str_vals.append(str(v).upper())
        return f"[1] {' '.join(str_vals)}"

def sparse_logical(values, positions, length, default=False):
    if not isinstance(default, (bool, np.bool_)):
        raise TypeError(f"default must be logical, not {type(default)}")
    
    if not isinstance(length, (int, np.integer)):
        try:
            length = int(length)
        except (ValueError, TypeError):
            raise TypeError("length must be an integer")

    values_arr = np.array(values, dtype=object)
    positions_arr = np.array(positions, dtype=int)

    if len(values_arr) != len(positions_arr):
        raise ValueError("values and positions must have the same length")
    if len(positions_arr) > 0:
        if np.any(positions_arr < 1) or np.any(positions_arr > length):
            raise ValueError("positions must be between 1 and length")

    # Check that no value equals the default (excluding NA)
    mask = (values_arr == default)
    if np.any(mask & pd.notna(values_arr)):
        offenders = np.where(mask & pd.notna(values_arr))[0] + 1
        raise ValueError(f"values value must not be equal to the default {default}. "
                         f"Values at index: {offenders}")

    return SparseLogical(values_arr, positions_arr, length, default)

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for the SparseLogical object."""
    if isinstance(obj, SparseLogical):
        dense = obj.to_dense() if obj.length < 100 else None
        if dense is not None:
            # For small vectors, str() shows a few values
            vals = []
            for v in dense[:6]:
                vals.append("NA" if pd.isna(v) else str(v).upper())
            print(f"logi [{1}:{obj.length}] {' '.join(vals)} ...")
        else:
            # For huge vectors, it shows the range and the first few values
            # R output: logi [1:1000000000] FALSE TRUE FALSE FALSE NA FALSE ...
            # We compute the first 6 elements of the sparse vector
            res = np.full(6, obj.default, dtype=object)
            for v, p in zip(obj.values, obj.positions):
                if 1 <= p <= 6:
                    res[p-1] = v
            vals = []
            for v in res:
                vals.append("NA" if pd.isna(v) else str(v).upper())
            print(f"logi [{1}:{obj.length}] {' '.join(vals)} ...")
    else:
        print(repr(obj))

# Example 1: sparse_logical(logical(), integer(), 10)
# r2py:entity:sparse_logical
res1 = sparse_logical([], [], 10)
print(res1)

# Example 2: sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 10)
# r2py:entity:sparse_logical_1
res2 = sparse_logical([True, np.nan, True], [2, 5, 10], 10)
print(res2)

# Example 3: str(sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 1000000000))
# r2py:entity:str
res3 = sparse_logical([True, np.nan, True], [2, 5, 10], 1000000000)
str_obj(res3)