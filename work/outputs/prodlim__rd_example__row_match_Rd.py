# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/prodlim__rd_example__row_match_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'prodlim__rd_example__row_match_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import string

def r_print_vec(vec):
    """Helper to mimic R's numeric vector printing: [1] 3 8"""
    if vec is None:
        print("NULL")
        return
    # Convert to list and join as strings
    vals = " ".join(map(str, vec))
    print(f"[1] {vals}")

# r2py:entity:row.match
def row_match(x, table, nomatch=np.nan):
    if isinstance(table, np.ndarray):
        table = pd.DataFrame(table)
    
    # If x is not a DataFrame (e.g., list, tuple, numpy array), convert to DataFrame
    # R's as.data.frame(matrix(x, nrow=1)) creates a 1-row DF where elements of x are columns
    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame([x])
    
    # Convert rows to strings joined by \r to create unique identifiers for matching
    # R's paste(..., sep="\r") across columns
    cx = x.astype(str).apply(lambda row: "\r".join(row), axis=1)
    ct = table.astype(str).apply(lambda row: "\r".join(row), axis=1)
    
    # Find the index of the first occurrence of cx in ct
    # R match() returns 1-based indices
    results = []
    for val in cx:
        try:
            # Find first occurrence
            pos = np.where(ct == val)[0][0] + 1
            results.append(pos)
        except IndexError:
            results.append(nomatch)
            
    return np.array(results)

# Main script
# r2py:entity:tab
tab = pd.DataFrame({'num': range(1, 27), 'abc': list(string.ascii_lowercase)})

# r2py:entity:x
x = [3, "c"]
# r2py:entity:row.match
res1 = row_match(x, tab)
r_print_vec(res1)

# r2py:entity:x_1
x = pd.DataFrame({'n': [3, 8], 'z': ["c", "h"]})
# r2py:entity:row.match_1
res2 = row_match(x, tab)
r_print_vec(res2)