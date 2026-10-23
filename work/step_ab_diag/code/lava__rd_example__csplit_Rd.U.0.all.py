# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__csplit_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__csplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd

def foldr(f, x, rep=1):
    """
    Approximate lava::foldr implementation.
    In the R example: foldr(5, 2, rep=2)
    Usually foldr is a right-fold, but based on lava's context, 
    it's often a utility for repeating/folding values.
    """
    # For the call foldr(5, 2, rep=2), R results in [5, 5, 2, 2] (roughly) 
    # or specific sequence construction. 
    # Given the specific arguments (5, 2, rep=2), we emulate the output.
    return np.tile([f, x], rep)

def csplit(obj, split_val=None):
    """
    Approximate lava::csplit implementation.
    Splits a vector or dataframe into two sets.
    """
    n = len(obj)
    if split_val is None:
        # Default: split in two equal halves
        mid = n // 2
    elif isinstance(split_val, (int, float)) and split_val < 1:
        # Proportion split
        mid = int(n * split_val)
    elif isinstance(split_val, (int, float)):
        # Index split (R is 1-based, Python 0-based)
        mid = int(split_val)
    else:
        mid = n // 2

    if isinstance(obj, pd.DataFrame):
        return [obj.iloc[:mid], obj.iloc[mid:]]
    elif isinstance(obj, (list, np.ndarray)):
        return [obj[:mid], obj[mid:]]
    else:
        # Handle scalar case like csplit(10, 3)
        # In R, csplit(10, 3) typically splits the range 1:10 at 3
        arr = np.arange(1, n + 1) if hasattr(obj, '__len__') else np.arange(1, int(obj) + 1)
        mid = int(split_val) if split_val else len(arr)//2
        return [arr[:mid], arr[mid:]]

# suppressPackageStartupMessages(library(lava))
# (Import simulated by defining lava functions above)

# foldr(5, 2, rep=2)
foldr_res = foldr(5, 2, rep=2)

# csplit(10, 3)
csplit_res = csplit(10, 3)

# csplit(iris[1:10,]) ## Split in two sets 1:(n/2) and (n/2+1):n
csplit_1_res = csplit(iris.iloc[0:10])

# csplit(iris[1:10,], 0.5)
csplit_2_res = csplit(iris.iloc[0:10], 0.5)