# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/prodlim__rd_example__row_match_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'prodlim__rd_example__row_match_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import string

# r2py:entity:row.match
def row_match(x, table, nomatch=np.nan):
    """
    Translate the row.match logic from prodlim.
    It concatenates row values and finds the index of the first match.
    """
    if isinstance(table, np.ndarray):
        table = pd.DataFrame(table)
    
    # If x is a vector/list (is.null(dim(x))), treat as a single row DataFrame
    if not hasattr(x, 'shape') or len(x.shape) < 2:
        # R's as.data.frame(matrix(x, nrow=1))
        x = pd.DataFrame([x])
    
    # Concatenate columns using carriage return as separator
    # R: do.call("paste", c(x[, , drop = FALSE], sep = "\r"))
    cx = x.astype(str).apply(lambda row: "\r".join(row), axis=1)
    ct = table.astype(str).apply(lambda row: "\r".join(row), axis=1)
    
    # match(cx, ct) finds the index of the first occurrence of each element of cx in ct
    # R indices are 1-based; Python are 0-based. To be equivalent to R output, we add 1.
    results = []
    for val in cx:
        try:
            # Find first index where ct == val
            idx = ct[ct == val].index[0]
            # Convert pandas index to 1-based position relative to the start of the df
            pos = ct.index.get_loc(idx) + 1
            results.append(pos)
        except (IndexError, KeyError):
            results.append(nomatch)
            
    return np.array(results)

# Setup data
# r2py:entity:tab
tab = pd.DataFrame({'num': range(1, 27), 'abc': list(string.ascii_lowercase)})

# First test case
# r2py:entity:x
x = [3, "c"]
# r2py:entity:row.match
print(row_match(x, tab))

# Second test case
# r2py:entity:x_1
x = pd.DataFrame({'n': [3, 8], 'z': ["c", "h"]})
# r2py:entity:row.match_1
print(row_match(x, tab))