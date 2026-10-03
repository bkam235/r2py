# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# Global storage to simulate R's attribute system for numpy arrays
attributes = {}

def get_dimnames(data_id):
    return attributes.get(data_id, None)

def set_dimnames(data_id, value):
    attributes[data_id] = value

# r2py:entity:melt
def melt(data, varnames=None, na_rm=False, value_name="value"):
    data_id = id(data)
    shape = data.shape
    
    # R arrays are column-major.
    values = data.flatten(order='F')
    
    dn_attr = get_dimnames(data_id)
    dn = []
    for i in range(len(shape)):
        if dn_attr is not None and i < len(dn_attr) and dn_attr[i] is not None:
            dn.append(dn_attr[i])
        else:
            # R's default dimnames are 1:dim
            dn.append(list(range(1, shape[i] + 1)))
            
    # R's expand.grid varies the first dimension fastest.
    labels_iter = itertools.product(*reversed(dn))
    labels = [list(reversed(t)) for t in labels_iter]
    
    if varnames is None:
        varnames = [f"Var{i+1}" for i in range(len(shape))]
        
    df = pd.DataFrame(labels, columns=varnames)
    
    # Use nullable integer type to avoid .0 in output and support NaNs
    df[value_name] = pd.Series(values).astype('Int64')
    
    if na_rm:
        df = df.dropna(subset=[value_name])
        
    # R data frames are 1-indexed.
    df.index = range(1, len(df) + 1)
    return df

# a <- array(c(1:23, NA), c(2,3,4))
# r2py:entity:a
raw_data = np.append(np.arange(1, 24), np.nan)
a = raw_data.reshape((2, 3, 4), order='F')
set_dimnames(id(a), None)

# melt(a)
# r2py:entity:melt
melt_res = melt(a)
print(melt_res)

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
melt_na_rm = melt(a, na_rm=True)
print(melt_na_rm)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
melt_varnames = melt(a, varnames=["X", "Y", "Z"])
print(melt_varnames)

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
a_shape = a.shape
new_dn = [LETTERS[:s] for s in a_shape]
set_dimnames(id(a), new_dn)

# melt(a)
# r2py:entity:melt_3
melt_dn = melt(a)
print(melt_dn)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
melt_dn_varnames = melt(a, varnames=["X", "Y", "Z"])
print(melt_dn_varnames)

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
current_dn = get_dimnames(id(a))
if current_dn is not None:
    updated_dn = list(current_dn)
    updated_dn[0] = None
    set_dimnames(id(a), updated_dn)

# melt(a)
# r2py:entity:melt_5
melt_dn_partial = melt(a)
print(melt_dn_partial)