# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# a <- array(c(1:23, NA), c(2,3,4))
# r2py:entity:a
a = np.array([list(range(1, 24)) + [np.nan]]).reshape(2, 3, 4)

# melt(a)
# In Python, melting a 3D array involves flattening the indices
# We create a DataFrame from the array by iterating through axes
# r2py:entity:melt
d1 = pd.DataFrame(a.reshape(-1, 1), columns=['value'])
d1.insert(0, 'Var3', np.tile(np.arange(4), 6))
d1.insert(1, 'Var2', np.repeat(np.arange(3), 2 * 4))
d1.insert(2, 'Var1', np.tile(np.repeat(np.arange(2), 3 * 4), 1)) # This logic is complex for arrays
# A cleaner approach to mimic reshape2::melt for numpy arrays:
def melt_array(arr):
    indices = np.indices(arr.shape).reshape(arr.ndim, -1).T
    df = pd.DataFrame(indices, columns=[f'Var{i+1}' for i in range(arr.ndim)])
    df['value'] = arr.flatten()
    return df

print(melt_array(a))

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
print(melt_array(a).dropna())

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
res_varnames = melt_array(a)
res_varnames.columns = ["X", "Y", "Z", "value"]
print(res_varnames)

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# Numpy arrays don't have dimnames like R; we must handle this via the melt logic
# r2py:entity:dimnames(a)
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
dim_names = [letters[:d] for d in a.shape]

# r2py:entity:melt_3
def melt_array_named(arr, names):
    indices = np.indices(arr.shape).reshape(arr.ndim, -1).T
    df = pd.DataFrame(indices, columns=[f'Var{i+1}' for i in range(arr.ndim)])
    for i in range(arr.ndim):
        df[f'Var{i+1}'] = df[f'Var{i+1}'].apply(lambda x: names[i][int(x)])
    df['value'] = arr.flatten()
    return df

# melt(a)
print(melt_array_named(a, dim_names))

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
res_named_vars = melt_array_named(a, dim_names)
res_named_vars.columns = ["X", "Y", "Z", "value"]
print(res_named_vars)

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
dim_names_null = [None] + dim_names[1:]
# Because we can't have "None" as a value in the same way R handles NULL dimnames for a dimension,
# we use the original index (0, 1...) for the first dimension.
# r2py:entity:melt_5
def melt_array_mixed(arr, names):
    indices = np.indices(arr.shape).reshape(arr.ndim, -1).T
    df = pd.DataFrame(indices, columns=[f'Var{i+1}' for i in range(arr.ndim)])
    for i in range(arr.ndim):
        if names[i] is not None:
            df[f'Var{i+1}'] = df[f'Var{i+1}'].apply(lambda x: names[i][int(x)])
        else:
            df[f'Var{i+1}'] = df[f'Var{i+1}'].apply(lambda x: int(x) + 1) # R indices start at 1
    df['value'] = arr.flatten()
    return df

# melt(a)
print(melt_array_mixed(a, dim_names_null))