# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'sparsevctrs__rd_example__coerce_to_sparse_tibble_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy import sparse

# set.seed(1234)
# r2py:entity:set.seed
np.random.seed(1234)

# mat <- matrix(sample(0:1, 100, TRUE, c(0.9, 0.1)), nrow = 10)
# colnames(mat) <- letters[1:10]
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
# In Python, we approximate the sparse tibble by using a pandas DataFrame 
# where columns are stored as sparse arrays
# r2py:entity:res
res = pd.DataFrame(
    mat, 
    columns=colnames
).astype(pd.SparseDtype("int", 0))
print(res)

# vapply(res, is_sparse_vector, logical(1))
# Checking if columns are sparse in pandas
# r2py:entity:vapply
is_sparse_vector = res.apply(lambda x: isinstance(x.dtype, pd.SparseDtype))
print(is_sparse_vector)