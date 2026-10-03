# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# r2py:entity:melt
def melt(data, varnames=None, na_rm=False, value_name="value"):
    if isinstance(data, np.ndarray):
        # R arrays are column-major. NumPy arrays are row-major by default.
        # To mimic R's as.vector(a) and expand.grid, we iterate in the correct order.
        shape = data.shape
        
        # Handle dimnames
        # In this script, dimnames are managed externally via a global/shared list since 
        # numpy arrays don't store them. We'll check if 'dimnames_a' exists.
        dn = []
        if 'dimnames_a' in globals():
            dn = globals()['dimnames_a']
        
        # Default dimnames: 1:dim(a)
        actual_dn = []
        for i in range(len(shape)):
            if i < len(dn) and dn[i] is not None:
                actual_dn.append(dn[i])
            else:
                actual_dn.append(list(range(1, shape[i] + 1)))

        # expand.grid in R: first dimension varies fastest
        # itertools.product varies the last dimension fastest.
        # To match R, we reverse the order for product, then reverse the result back.
        coords = list(itertools.product(*[range(s) for s in shape]))
        # coords is now [(0,0,0), (0,0,1), (0,0,2)...] which is NOT R order.
        # R's expand.grid(dn) produces:
        # Var1: 1 1 1 1 2 2 2 2 ...
        # Var2: 1 1 2 2 1 1 2 2 ...
        # Var3: 1 2 1 2 1 2 1 2 ...
        # This corresponds to:
        # for k in dim3: for j in dim2: for i in dim1:
        
        # Correct R order flattening:
        r_coords = []
        # R order: index 0 changes fastest, then 1, then 2...
        # This is exactly what np.ndindex(shape) does NOT do.
        # We need to iterate such that the first dimension is the inner-most loop.
        # Actually, a simple way to get R's sequence:
        indices = np.indices(shape).reshape(len(shape), -1).T
        # indices[0] is Var1, indices[1] is Var2, etc.
        
        # Map indices to names
        labels = []
        for idx in indices:
            row = []
            for i in range(len(shape)):
                # If the dimension name is None, R's melt for arrays often just uses the index
                # But the prompt says dimnames(a)[1] <- list(NULL)
                # If dn[i] is None, it doesn't provide a name, but the coordinate is still there.
                # However, reshape2::melt.array behaves differently if dimnames are missing.
                # If dimnames(a)[1] is NULL, Var1 is simply not named/omitted from labels?
                # No, it usually keeps the index but labels the column "Var1".
                val = actual_dn[i][idx[i]] if i < len(actual_dn) else idx[i] + 1
                row.append(val)
            labels.append(row)
            
        # Flatten data in R order (column-major / Fortran order)
        values = data.flatten(order='F')
        
        df = pd.DataFrame(labels, columns=[f"Var{i+1}" for i in range(len(shape))])
        df[value_name] = values
        
        if varnames:
            # R's varnames only replaces the names of the coordinate columns
            rename_map = {f"Var{i+1}": name for i, name in enumerate(varnames)}
            df = df.rename(columns=rename_map)
            
        if na_rm:
            df = df.dropna(subset=[value_name])
            
        # If dimnames(a)[1] was NULL, R's melt results in the first column being removed 
        # or treated as if it doesn't have names.
        # In reshape2, if dimnames(a)[1] is NULL, the resulting df has 
        # one fewer coordinate column.
        if 'dimnames_a' in globals() and len(globals()['dimnames_a']) > 0:
            for i, dn_val in enumerate(globals()['dimnames_a']):
                if dn_val is None:
                    col_to_drop = f"Var{i+1}"
                    # If varnames was provided, the column might have been renamed
                    if varnames and i < len(varnames):
                        col_to_drop = varnames[i]
                    if col_to_drop in df.columns:
                        df = df.drop(columns=[col_to_drop])
                        
        return df

# a <- array(c(1:23, NA), c(2,3,4))
# r2py:entity:a
a = np.array(np.append(np.arange(1, 24), np.nan)).reshape(2, 3, 4, order='F')

# Setup for dimnames tracking
dimnames_a = [None] * 3

# melt(a)
# r2py:entity:melt
melt_res1 = melt(a)

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
melt_res2 = melt(a, na_rm=True)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
melt_res3 = melt(a, varnames=["X", "Y", "Z"])

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
dimnames_a[0] = LETTERS[0:2]
dimnames_a[1] = LETTERS[0:3]
dimnames_a[2] = LETTERS[0:4]

# melt(a)
# r2py:entity:melt_3
melt_res4 = melt(a)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
melt_res5 = melt(a, varnames=["X", "Y", "Z"])

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
dimnames_a[0] = None

# melt(a)
# r2py:entity:melt_5
melt_res6 = melt(a)