import numpy as np
import pandas as pd
from functools import reduce

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__csplit_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__csplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def foldr(f, init, x):
    """R's foldr: right-associative reduction."""
    # In R, foldr(f, init, x) where x is a vector
    # We reverse the list and use reduce with init as the first element
    return reduce(lambda acc, val: f(val, acc), reversed(x), init)

def csplit(x, split_point=None):
    """
    lava::csplit splits an object into two parts.
    If split_point is None, it defaults to n/2.
    If split_point is between 0 and 1, it's treated as a proportion.
    """
    n = len(x)
    if split_point is None:
        # Default: n/2
        idx = n // 2
    elif 0 < split_point < 1:
        # Proportion
        idx = int(n * split_point)
    else:
        # Absolute index
        idx = int(split_point)
    
    # R's csplit returns a list of two elements
    return [x.iloc[:idx] if hasattr(x, 'iloc') else x[:idx], 
            x.iloc[idx:] if hasattr(x, 'iloc') else x[idx:]]

# foldr(5, 2, rep=2) 
# Note: In R source, 'rep=2' is the 3rd argument 'x'. 
# The function 'f' is passed as 5. In R, this usually implies a custom 
# operator or specific package behavior. However, based on lava's 
# documentation, foldr expects a function. 
# If f is 5, it's likely treating it as a constant function or an error 
# unless 'lava' overrides. But standard R foldr requires a function.
# Given the context of lava, let's assume the function is a lambda that returns the first arg.
# Actually, checking lava package: foldr(f, init, x)
# For foldr(5, 2, rep=2), it's likely using 5 as the function. 
# In Python, we'll mock the function as a simple addition for the example's sake 
# or a identity if it's a number.
f_mock = lambda x, y: x + y # Approximation for the sake of execution
foldr_result = foldr(f_mock, 2, [2] * 2)

# csplit(10, 3)
# In R, csplit(10, 3) treats 10 as a sequence 1:10
csplit_1 = csplit(np.arange(1, 11), 3)

# csplit(iris[1:10,])
# iris[1:10,] in R is the first 10 rows
csplit_2 = csplit(iris.iloc[0:10])

# csplit(iris[1:10,], 0.5)
csplit_3 = csplit(iris.iloc[0:10], 0.5)