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
from functools import reduce

def foldr(func, init, *args, **kwargs):
    # R's foldr processes from right to left.
    # If func is not callable (like the 5 in the R snippet), 
    # it's a lava-specific behavior. Assuming standard foldr logic for translation.
    # In the snippet: foldr(5, 2, rep=2). If 5 is a function index, we simulate.
    # Since we don't have lava's internals, we use a placeholder that handles the arguments.
    seq = list(args)
    if 'rep' in kwargs:
        seq = [kwargs['rep']] * kwargs['rep'] if isinstance(kwargs['rep'], int) else []
    
    res = init
    for x in reversed(seq):
        if callable(func):
            res = func(x, res)
        else:
            # Simulation for when func is a numeric constant as seen in lava examples
            res = res + x 
    return res

def csplit(x, split_val=None):
    # csplit splits into two sets. 
    # If split_val is None, it defaults to n/2.
    # If split_val is numeric, it's an index (1-based) or a proportion.
    n = len(x)
    if split_val is None:
        idx = n // 2
    elif 0 < split_val < 1:
        idx = int(n * split_val)
    else:
        idx = int(split_val)
    
    # Python slice is 0-based. R index 'k' splits into 1:k and k+1:n.
    # Here we interpret idx as the split point.
    if isinstance(x, pd.DataFrame):
        return [x.iloc[:idx], x.iloc[idx:]]
    else:
        return [x[:idx], x[idx:]]

# suppressPackageStartupMessages(library(lava))
# (Library import handled by function definitions above)

# foldr(5,2,rep=2)
foldr_res = foldr(5, 2, rep=2)

# csplit(10,3)
# R: csplit(10, 3) where 10 is treated as a sequence 1:10
csplit_res1 = csplit(np.arange(1, 11), 3)

# csplit(iris[1:10,])
# R: iris[1:10,] -> Python: iris.iloc[0:10]
csplit_res2 = csplit(iris.iloc[0:10])

# csplit(iris[1:10,], 0.5)
csplit_res3 = csplit(iris.iloc[0:10], 0.5)