# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# r2py:entity:melt
def r_melt_array(data, dimnames=None, varnames=None, na_rm=False, value_name="value"):
    shape = data.shape
    # R's as.vector(array) is column-major
    flat_values = np.ravel(data, order='F')
    
    # Generate coordinates matching R's expand.grid(dn) 
    # where the first dimension varies fastest.
    ranges = [range(s) for s in shape]
    coords = list(itertools.product(*reversed(ranges)))
    coords = [c[::-1] for c in coords]
    
    rows = []
    for i, val in zip(coords, flat_values):
        row = []
        for dim_idx in range(len(shape)):
            if dimnames is not None and dimnames[dim_idx] is not None:
                row.append(dimnames[dim_idx][i[dim_idx]])
            else:
                row.append(i[dim_idx] + 1)
        row.append(val)
        rows.append(row)
    
    if varnames is None:
        varnames = [f"Var{i+1}" for i in range(len(shape))]
    
    df = pd.DataFrame(rows, columns=varnames + [value_name])
    
    if na_rm:
        df = df.dropna(subset=[value_name])
    
    # Convert value column to Int64 to support NaNs while avoiding .0 (float)
    # and ensure coordinate columns are integer if they are numeric
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce').astype('Int64')
    for col in varnames:
        if all(isinstance(x, int) for x in df[col]):
            df[col] = df[col].astype(int)
        
    df.index = range(1, len(df) + 1)
    return df

# a <- array(c(1:23, NA), c(2,3,4))
# r2py:entity:a
a = np.array([list(range(1, 24)) + [np.nan]], dtype=float).flatten()
a = np.reshape(a, (2, 3, 4), order='F')

# melt(a)
melt_res = r_melt_array(a)
print(melt_res.to_string())

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
melt_na_res = r_melt_array(a, na_rm=True)
print(melt_na_res.to_string())

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
melt_varnames_res = r_melt_array(a, varnames=["X", "Y", "Z"])
print(melt_varnames_res.to_string())

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
a_dimnames = [LETTERS[:s] for s in a.shape]

# melt(a)
# r2py:entity:melt_3
melt_dn_res = r_melt_array(a, dimnames=a_dimnames)
print(melt_dn_res.to_string())

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
melt_dn_varnames_res = r_melt_array(a, dimnames=a_dimnames, varnames=["X", "Y", "Z"])
print(melt_dn_varnames_res.to_string())

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
a_dimnames_null = [None] + a_dimnames[1:]

# melt(a)
# r2py:entity:melt_5
melt_null_res = r_melt_array(a, dimnames=a_dimnames_null)
print(melt_null_res.to_string())