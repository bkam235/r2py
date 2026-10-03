# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# a <- array(c(1:23, NA), c(2,3,4))
# R arrays are 1-indexed and fill by column; Python/Numpy fill by row.
# To mimic R's array(1:24, c(2,3,4)), we create the sequence and reshape/transpose.
# r2py:entity:a
a = np.array(np.append(np.arange(1, 24), np.nan)).reshape(4, 3, 2).transpose(2, 1, 0)

# r2py:entity:melt
def melt_array(arr, na_rm=False, varnames=None):
    # This helper approximates reshape2::melt for multi-dimensional numpy arrays
    # It converts the array to a long-format DataFrame
    shape = arr.shape
    # Create coordinate grids for each dimension
    coords = np.indices(shape).reshape(len(shape), -1).T
    # Flatten the array to get values
    values = arr.flatten()
    
    df = pd.DataFrame(coords, columns=[varnames[i] if varnames else f"Var{i+1}" for i in range(len(shape))])
    df['value'] = values
    
    if na_rm:
        df = df.dropna(subset=['value'])
    return df

# melt(a)
print(melt_array(a))

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
print(melt_array(a, na_rm=True))

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
print(melt_array(a, varnames=["X", "Y", "Z"]))

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# Numpy arrays don't have named dimensions like R. 
# We simulate this by passing the specific names to our melt function.
# r2py:entity:dimnames(a)
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
dim_names = [letters[:s] for s in a.shape]

# melt(a) with dimnames
# To mimic R's melt with dimnames, we map the integer coordinates to the letters
# r2py:entity:melt_3
def melt_named_array(arr, names, varnames=None):
    shape = arr.shape
    coords = np.indices(shape).reshape(len(shape), -1).T
    values = arr.flatten()
    
    data = []
    for row in coords:
        # Map index to the letter provided in dim_names
        mapped_row = [names[i][idx] for i, idx in enumerate(row)]
        data.append(mapped_row)
        
    df = pd.DataFrame(data, columns=[varnames[i] if varnames else f"Var{i+1}" for i in range(len(shape))])
    df['value'] = values
    return df

print(melt_named_array(a, dim_names))

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
print(melt_named_array(a, dim_names, varnames=["X", "Y", "Z"]))

# dimnames(a)[1] <- list(NULL)
# Simulate removing the name of the first dimension
# r2py:entity:dimnames(a)[1]
dim_names_null = [None] + dim_names[1:]
def melt_partial_named_array(arr, names):
    shape = arr.shape
    coords = np.indices(shape).reshape(len(shape), -1).T
    values = arr.flatten()
    
    data = []
    for row in coords:
        mapped_row = []
        for i, idx in enumerate(row):
            if names[i] is None:
                mapped_row.append(idx + 1) # R indices are 1-based
            else:
                mapped_row.append(names[i][idx])
        data.append(mapped_row)
        
    df = pd.DataFrame(data, columns=[f"Var{i+1}" for i in range(len(shape))])
    df['value'] = values
    return df

# r2py:entity:melt_5
print(melt_partial_named_array(a, dim_names_null))