# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# a <- array(c(1:23, NA), c(2,3,4))
# R's array() fills dimensions in order: dim1, then dim2, then dim3.
# This corresponds to Fortran order in numpy.
# r2py:entity:a
data_vals = np.append(np.arange(1, 24), np.nan)
a = np.array(data_vals).reshape((2, 3, 4), order='F')

# We need a way to store dimnames because numpy arrays don't have them.
# We'll use a wrapper or a global variable to simulate the state of 'a'.
class RArray:
    def __init__(self, data, dimnames=None):
        self.data = data
        self.dimnames = dimnames
    def __repr__(self):
        return repr(self.data)
    def shape(self):
        return self.data.shape

# Initialize a as an RArray
a_obj = RArray(a)

# r2py:entity:melt
def melt(data_obj, varnames=None, na_rm=False, value_name="value"):
    # In this context, data_obj is our RArray wrapper
    data = data_obj.data
    dn = data_obj.dimnames
    shape = data.shape
    
    # Generate dimension levels
    dims = []
    for i in range(len(shape)):
        if dn is not None and i < len(dn) and dn[i] is not None:
            dims.append(dn[i])
        else:
            dims.append(list(range(1, shape[i] + 1)))
    
    # R's expand.grid varies the first argument fastest.
    # itertools.product varies the last argument fastest.
    # To emulate expand.grid, we reverse the dimensions for product, then reverse the result.
    grid_iter = itertools.product(*dims)
    labels_list = list(grid_iter)
    
    # Now we need the values in the same order as labels.
    # R's as.vector(array) also follows the column-major order.
    values = data.flatten(order='F')
    
    df = pd.DataFrame(labels_list)
    # Default varnames: Var1, Var2...
    default_varnames = [f"Var{i+1}" for i in range(len(shape))]
    if varnames is not None:
        df.columns = varnames
    else:
        df.columns = default_varnames
        
    df[value_name] = values
    
    if na_rm:
        df = df.dropna(subset=[value_name])
        
    return df

# melt(a)
melt_res = melt(a_obj)
print(melt_res)

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
melt_res_na = melt(a_obj, na_rm=True)
print(melt_res_na)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
melt_res_vars = melt(a_obj, varnames=["X", "Y", "Z"])
print(melt_res_vars)

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
a_obj.dimnames = [LETTERS[:s] for s in a.shape]

# melt(a)
# r2py:entity:melt_3
melt_res_named = melt(a_obj)
print(melt_res_named)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
melt_res_named_vars = melt(a_obj, varnames=["X", "Y", "Z"])
print(melt_res_named_vars)

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
a_obj.dimnames[0] = None

# melt(a)
# r2py:entity:melt_5
melt_res_mixed = melt(a_obj)
print(melt_res_mixed)