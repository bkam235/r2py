# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# r2py:entity:a
a_data = np.array([float(i) for i in range(1, 24)] + [np.nan])
a = a_data.reshape((2, 3, 4), order='F')

# To track R's dimnames(a)
a_dimnames = [None] * 3

# r2py:entity:melt
def melt(data, na_rm=False, varnames=None, value_name="value"):
    if isinstance(data, np.ndarray):
        shape = data.shape
        
        # Resolve dimension names (equivalent to amv_dimnames)
        dn = []
        for i in range(len(shape)):
            if a_dimnames[i] is not None:
                dn.append(a_dimnames[i])
            else:
                dn.append(list(range(1, shape[i] + 1)))
        
        # R's expand.grid: first dimension varies fastest.
        # itertools.product varies the last dimension fastest.
        # To get R's order, we product in reverse and then reverse each resulting tuple.
        grid_iter = itertools.product(*reversed(dn))
        grid = [list(reversed(row)) for row in grid_iter]
        
        labels_df = pd.DataFrame(grid)
        
        if varnames is not None:
            cols = list(varnames)
            while len(cols) < len(shape):
                cols.append(f"Var{len(cols)+1}")
            labels_df.columns = cols[:len(shape)]
        else:
            labels_df.columns = [f"Var{i+1}" for i in range(len(shape))]
        
        # R's as.vector(a) for arrays is column-major (order='F')
        values = data.flatten(order='F')
        labels_df[value_name] = values
        
        if na_rm:
            labels_df = labels_df.dropna(subset=[value_name])
        
        # R output formatting: if there are no NAs, values are often printed as ints.
        # Pandas floats always print .0. We convert to nullable Int64 to match R's NA/Integer behavior.
        if not labels_df[value_name].isna().any():
            labels_df[value_name] = labels_df[value_name].astype(int)
        else:
            # Use pandas nullable integer type to keep NA but show integers
            labels_df[value_name] = pd.to_numeric(labels_df[value_name], errors='coerce').astype('Int64')

        labels_df.index = range(1, len(labels_df) + 1)
        return labels_df

    return pd.DataFrame()

# melt(a)
print(melt(a))

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
print(melt(a, na_rm=True))

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
print(melt(a, varnames=["X", "Y", "Z"]))

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
a_dimnames[0] = [LETTERS[i] for i in range(a.shape[0])]
a_dimnames[1] = [LETTERS[i] for i in range(a.shape[1])]
a_dimnames[2] = [LETTERS[i] for i in range(a.shape[2])]

# melt(a)
# r2py:entity:melt_3
print(melt(a))

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
print(melt(a, varnames=["X", "Y", "Z"]))

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
a_dimnames[0] = None

# melt(a)
# r2py:entity:melt_5
print(melt(a))