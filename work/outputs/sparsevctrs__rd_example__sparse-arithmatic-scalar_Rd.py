# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/sparsevctrs__rd_example__sparse-arithmatic-scalar_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sparsevctrs__rd_example__sparse-arithmatic-scalar_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
from typing import Union, Optional

# r2py:entity:x_sparse
class SparseVector:
    def __init__(self, values: np.ndarray, positions: np.ndarray, length: int, default: float = 0.0):
        # R positions are 1-indexed, Python are 0-indexed
        self.values = np.asarray(values, dtype=float)
        self.positions = np.asarray(positions, dtype=int) - 1 
        self.length = length
        self.default = default

    def to_dense(self):
        res = np.full(self.length, self.default)
        if self.values.size > 0:
            res[self.positions] = self.values
        return res

    def __repr__(self):
        return f"SparseVector(values={self.values}, positions={self.positions + 1}, length={self.length}, default={self.default})"

def sparse_double(values, positions, length, default=0.0):
    return SparseVector(values, positions, length, default)

def format_r_vector(vec):
    """Helper to mimic R's print output for vectors."""
    res = "      [1] "
    for i, val in enumerate(vec):
        res += f"{val:0.6f} "
        if (i + 1) % 8 == 0 and (i + 1) < len(vec):
            res += f"\n [{i + 9}] "
    return res.strip()

# r2py:entity:sparse_division_scalar
def sparse_division_scalar(x: SparseVector, val: float):
    if np.isnan(val):
        return np.full(x.length, np.nan)
    if val == 0:
        return np.full(x.length, np.inf)
    if val == 1:
        return x.to_dense()
    
    new_values = x.values / val
    return sparse_double(new_values, x.positions + 1, x.length, x.default).to_dense()

# r2py:entity:sparse_multiplication_scalar
def sparse_multiplication_scalar(x: SparseVector, val: float):
    if np.isnan(val):
        return np.full(x.length, np.nan)
    if val == 1:
        return x.to_dense()
    if val == 0:
        return sparse_double([], [], x.length, x.default).to_dense()
    
    new_values = x.values * val
    return sparse_double(new_values, x.positions + 1, x.length, x.default).to_dense()

# r2py:entity:sparse_addition_scalar
def sparse_addition_scalar(x: SparseVector, val: float):
    if np.isnan(val):
        return np.full(x.length, np.nan)
    if val == 0:
        return x.to_dense()
    
    new_values = x.values + val
    new_default = x.default + val
    return sparse_double(new_values, x.positions + 1, x.length, new_default).to_dense()

# r2py:entity:sparse_subtraction_scalar
def sparse_subtraction_scalar(x: SparseVector, val: float):
    if np.isnan(val):
        return np.full(x.length, np.nan)
    if val == 0:
        return x.to_dense()
    
    new_values = x.values - val
    new_default = x.default - val
    return sparse_double(new_values, x.positions + 1, x.length, new_default).to_dense()

# Main Execution
# r2py:entity:x_sparse
x_sparse = sparse_double([np.pi, 5, 0.1], [2, 5, 10], 10)

# r2py:entity:sparse_division_scalar
print(format_r_vector(sparse_division_scalar(x_sparse, 2)))
# r2py:entity:sparse_multiplication_scalar
print(format_r_vector(sparse_multiplication_scalar(x_sparse, 2)))
# r2py:entity:sparse_addition_scalar
print(format_r_vector(sparse_addition_scalar(x_sparse, 2)))
# r2py:entity:sparse_subtraction_scalar
print(format_r_vector(sparse_subtraction_scalar(x_sparse, 2)))