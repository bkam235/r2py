# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.py'
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

# Generate matrix: sample 0s and 1s with 90% 0 and 10% 1
# r2py:entity:mat
mat_data = np.random.choice([0, 1], size=100, p=[0.9, 0.1])
mat = mat_data.reshape(10, 10)
# r2py:entity:colnames(mat)
colnames = list("abcdefghij")

# sparse_mat <- Matrix::Matrix(mat, sparse = TRUE)
# r2py:entity:sparse_mat
sparse_mat = sparse.csr_matrix(mat)
print(sparse_mat)

# res <- coerce_to_sparse_tibble(sparse_mat)
# In Python, we represent this as a DataFrame where columns are stored 
# as sparse arrays (pandas SparseArray)
# r2py:entity:res
res = pd.DataFrame(mat, columns=colnames).astype(pd.SparseDtype("int", 0))
print(res)

# vapply(res, is_sparse_vector, logical(1))
# Check if each column is a pandas SparseArray/Dtype
# r2py:entity:vapply
res_is_sparse = res.apply(lambda col: isinstance(col.dtype, pd.SparseDtype))
print(res_is_sparse)