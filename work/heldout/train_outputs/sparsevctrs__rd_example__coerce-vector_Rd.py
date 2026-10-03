# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/sparsevctrs__rd_example__coerce-vector_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sparsevctrs__rd_example__coerce-vector_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x_sparse']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np

# r2py:entity:x_sparse
class SparseDouble:
    def __init__(self, values, positions, length, default=0.0):
        self.values = np.array(values, dtype=float)
        self.positions = np.array(positions, dtype=int)
        self.length = int(length)
        self.default = float(default)

    def __repr__(self):
        return f"SparseDouble(values={self.values}, positions={self.positions}, length={self.length}, default={self.default})"

# r2py:entity:is_sparse_double
def is_sparse_double(x):
    return isinstance(x, SparseDouble)

def validate_values_double(values):
    values = np.asanyarray(values)
    if not np.issubdtype(values.dtype, np.number):
        raise TypeError("values must be a numeric vector")
    if np.any(np.isinf(values)):
        raise ValueError("values must not contain infinite values")
    if np.any(np.isnan(values)):
        raise ValueError("values must not contain NaN values")

def check_number_decimal(x):
    if not isinstance(x, (int, float, np.number)):
        raise TypeError("Value must be a decimal number")

def validate_length(length):
    if not isinstance(length, (int, np.integer)) or length < 0:
        raise ValueError("length must be a non-negative integer")

def validate_positions(positions, length, len_values):
    positions = np.asanyarray(positions)
    if not np.issubdtype(positions.dtype, np.number):
        raise TypeError("positions must be an integer vector")
    if np.any(np.isinf(positions)) or np.any(np.isnan(positions)):
        raise ValueError("positions must not contain infinite or NaN values")
    if not np.all(np.mod(positions, 1) == 0):
        raise ValueError("positions must contain integer values")
    if len(positions) != len_values:
        raise ValueError("values and positions must have the same length")
    if len(positions) > 0:
        if len(np.unique(positions)) != len(positions):
            raise ValueError("positions must not contain duplicate values")
        if not np.all(np.diff(positions) > 0):
            raise ValueError("positions must be sorted in increasing order")
        if np.max(positions) > length:
            raise ValueError("positions value must not be larger than length")
        if np.min(positions) < 1:
            raise ValueError("positions value must be positive")

def sparse_double(values, positions, length, default=0):
    check_number_decimal(default)
    validate_length(length)
    
    default = float(default)
    values = np.asanyarray(values, dtype=float)
    validate_values_double(values)
    
    validate_positions(positions, length, len(values))
    positions = np.array(positions, dtype=int)
    
    if np.any(values == default):
        raise ValueError(f"values value must not be equal to the default {default}")
        
    return SparseDouble(values, positions, length, default)

def as_sparse_double(x, default=0):
    if is_sparse_double(x):
        return x
    
    x = np.asanyarray(x)
    validate_values_double(x)
    check_number_decimal(default)
    
    # R indices are 1-based. which() returns indices of TRUE elements.
    # x != default | is.na(x)
    mask = (x != default) | np.isnan(x)
    index = np.where(mask)[0] + 1 # Convert to 1-based indexing to match R logic
    
    return sparse_double(
        values=x[mask], 
        positions=index, 
        length=len(x), 
        default=default
    )

# r2py:entity:x_dense
x_dense = np.array([3, 0, 2, 0, 0, 0, 4, 0, 0, 0])
# r2py:entity:x_sparse_1
print(x_sparse)

# r2py:entity:is_sparse_double
print(is_sparse_double(x_sparse))