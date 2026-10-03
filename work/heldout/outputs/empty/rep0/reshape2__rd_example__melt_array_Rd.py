# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/reshape2__rd_example__melt_array_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_array_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# Global to track dimnames of array 'a'
current_dimnames = None

def r_print(df):
    """Helper to match R's printing style (NA instead of NaN, no .0 for Int64)"""
    if df is None:
        return
    # Convert to string and replace NaN with NA
    out = df.copy()
    # Ensure indices start at 1
    out.index = range(1, len(out) + 1)
    # Format values to match R (NaN -> NA)
    s = out.to_string()
    s = s.replace('NaN', 'NA')
    print(s)

# r2py:entity:melt
def melt_array(data, varnames=None, na_rm=False, value_name="value"):
    global current_dimnames
    shape = data.shape
    
    # Mimic R's amv_dimnames
    dn = []
    for i in range(len(shape)):
        if current_dimnames is not None and i < len(current_dimnames) and current_dimnames[i] is not None:
            dn.append(current_dimnames[i])
        else:
            dn.append(list(range(1, shape[i] + 1)))

    # Handle varnames
    if varnames is not None:
        actual_varnames = varnames
    else:
        actual_varnames = [f"Var{i+1}" for i in range(len(shape))]

    # R's expand.grid: first dimension varies fastest
    grid_raw = list(itertools.product(*dn[::-1]))
    grid = [tup[::-1] for tup in grid_raw]
    
    # Flatten data in Fortran order (column-major)
    values = data.flatten(order='F')
    
    df = pd.DataFrame(grid, columns=actual_varnames)
    df[value_name] = values
    
    if na_rm:
        df = df.dropna(subset=[value_name])
        
    # Use pandas Int64 to avoid .0 for integers while allowing NaNs
    try:
        # Check if it's essentially integers
        if np.all(np.nan_to_num(df[value_name]) % 1 == 0):
            df[value_name] = df[value_name].astype('Int64')
    except:
        pass

    df.index = range(1, len(df) + 1)
    return df

# a <- array(c(1:23, NA), c(2,3,4))
# r2py:entity:a
a_data = np.array([list(range(1, 24)) + [np.nan]], dtype=float).flatten()
a = a_data.reshape((2, 3, 4), order='F')

# Initialize global dimnames shim
current_dimnames = None

# melt(a)
melt = melt_array(a)
r_print(melt)

# melt(a, na.rm = TRUE)
# r2py:entity:melt_1
melt_1 = melt_array(a, na_rm=True)
r_print(melt_1)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_2
melt_2 = melt_array(a, varnames=["X", "Y", "Z"])
r_print(melt_2)

# dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
# r2py:entity:dimnames(a)
current_dimnames = [LETTERS[:s] for s in a.shape]

# melt(a)
# r2py:entity:melt_3
melt_3 = melt_array(a)
r_print(melt_3)

# melt(a, varnames=c("X","Y","Z"))
# r2py:entity:melt_4
melt_4 = melt_array(a, varnames=["X", "Y", "Z"])
r_print(melt_4)

# dimnames(a)[1] <- list(NULL)
# r2py:entity:dimnames(a)[1]
current_dimnames[0] = None

# melt(a)
# r2py:entity:melt_5
melt_5 = melt_array(a)
r_print(melt_5)