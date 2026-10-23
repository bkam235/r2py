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

def lava_foldr(start, end, rep=1):
    """Approximates lava::foldr which generates a sequence from start to end."""
    seq = list(range(start, end - 1, -1))
    return seq * rep

def lava_csplit(data, split_point=None):
    """Approximates lava::csplit which splits data into two sets."""
    if isinstance(data, (int, float)):
        # If data is numeric, treat it as a sequence 1:data
        seq = np.arange(1, data + 1)
        if split_point is None:
            mid = len(seq) // 2
        elif isinstance(split_point, (int, float)) and split_point > 1:
            mid = int(split_point)
        else:
            mid = int(len(seq) * split_point)
        return seq[:mid], seq[mid:]
    
    elif isinstance(data, pd.DataFrame):
        n = len(data)
        if split_point is None:
            mid = n // 2
        else:
            mid = int(n * split_point)
        return data.iloc[:mid], data.iloc[mid:]
    
    return None

# suppressPackageStartupMessages(library(lava))
# Python equivalent: No operation needed for library import

# foldr(5,2,rep=2)
foldr_res = lava_foldr(5, 2, rep=2)

# csplit(10,3)
csplit_res = lava_csplit(10, 3)

# csplit(iris[1:10,])
csplit_1 = lava_csplit(iris.iloc[0:10])

# csplit(iris[1:10,],0.5)
csplit_2 = lava_csplit(iris.iloc[0:10], 0.5)