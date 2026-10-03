# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.py'
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

# mat <- matrix(sample(0:1, 100, TRUE, c(0.9, 0.1)), nrow = 10)
# r2py:entity:mat
mat = np.random.choice([0, 1], size=(10, 10), p=[0.9, 0.1])

# colnames(mat) <- letters[1:10]
# r2py:entity:colnames(mat)
colnames = list("abcdefghij")

# sparse_mat <- Matrix::Matrix(mat, sparse = TRUE)
# r2py:entity:sparse_mat
sparse_mat = sparse.csr_matrix(mat)
print(sparse_mat)

# res <- coerce_to_sparse_tibble(sparse_mat)
# Since sparse_tibble is a specific R structure for columns of sparse vectors,
# the Python equivalent is a Pandas DataFrame where columns are sparse arrays.
# r2py:entity:res
res = pd.DataFrame(mat, columns=colnames).astype(pd.SparseDtype("int", 0))
print(res)

# vapply(res, is_sparse_vector, logical(1))
# r2py:entity:vapply
is_sparse_vector = lambda x: isinstance(x.dtype, pd.SparseDtype)
results = {col: is_sparse_vector(res[col]) for col in res.columns}
print(pd.Series(results))