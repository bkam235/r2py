# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy import sparse

# r2py:entity:set.seed
np.random.seed(1234)

# R: mat <- matrix(sample(0:1, 100, TRUE, c(0.9, 0.1)), nrow = 10)
# sample(0:1, 100, TRUE, c(0.9, 0.1)) generates a vector of length 100.
# matrix(..., nrow = 10) fills by column (Fortran order).
# r2py:entity:mat
sampled_vals = np.random.choice([0, 1], size=100, p=[0.9, 0.1])
mat = sampled_vals.reshape((10, 10), order='F')

# letters[1:10] from shim
# r2py:entity:colnames(mat)
colnames_mat = letters[0:10]

# Matrix::Matrix(mat, sparse = TRUE) -> scipy.sparse.csr_matrix
# r2py:entity:sparse_mat
sparse_mat = sparse.csr_matrix(mat)
print(sparse_mat)

# coerce_to_sparse_tibble(sparse_mat)
# In Python, we use a pandas DataFrame with SparseDtype.
# r2py:entity:res
res = pd.DataFrame(mat, columns=colnames_mat).astype(pd.SparseDtype("int", 0))
print(res)

# vapply(res, is_sparse_vector, logical(1))
# Check if each column is a sparse vector (Pandas SparseDtype)
# r2py:entity:vapply
vapply_res = res.apply(lambda x: isinstance(x.dtype, pd.SparseDtype))
print(vapply_res)