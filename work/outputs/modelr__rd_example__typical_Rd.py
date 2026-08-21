# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/modelr__rd_example__typical_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'modelr__rd_example__typical_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from typing import Union, Any

# r2py:entity:typical
def typical(x: Any) -> Any:
    # Convert to pandas Series for consistent handling
    if not isinstance(x, pd.Series):
        s = pd.Series(x)
    else:
        s = x

    # Handle ordered categorical (median)
    if isinstance(s.dtype, pd.CategoricalDtype) and s.dtype.ordered:
        # R typical for ordered factors returns the median
        # This is the value at the 50th percentile of the sorted data
        sorted_s = s.sort_values()
        n = len(sorted_s)
        if n == 0:
            return None
        
        # R median for factors: if n is odd, middle element. 
        # If even, it can be a tie or an average. 
        # However, modelr::typical for ordered factors usually returns the category.
        mid = (n - 1) / 2
        if mid.is_integer():
            res = sorted_s.iloc[int(mid)]
            return res
        else:
            # For even length, R median typically interpolates. 
            # For factors, it often returns the two middle values if they differ.
            low = int(np.floor(mid))
            high = int(np.ceil(mid))
            v_low = sorted_s.iloc[low]
            v_high = sorted_s.iloc[high]
            if v_low == v_high:
                return v_low
            else:
                # Return as a list/array to simulate R's multiple return
                return np.array([v_low, v_high])

    # Handle standard categorical/factor or strings (mode)
    if isinstance(s.dtype, pd.CategoricalDtype) or s.dtype == object or np.issubdtype(s.dtype, np.bytes_) or (hasattr(np, 'str_') and np.issubdtype(s.dtype, np.str_)):
        counts = s.value_counts()
        if counts.empty:
            return None
        max_count = counts.max()
        modes = counts[counts == max_count].index.tolist()
        # R returns a single value if only one mode, otherwise a vector
        # To match R's output for typical(x) where x is char:
        if len(modes) == 1:
            return modes[0]
        return np.array(modes)

    # Handle numeric (median)
    if np.issubdtype(s.dtype, np.number):
        return np.median(s)

    return None

# median of numeric vector
# r2py:entity:typical
res_typical_num = typical(np.random.poisson(lam=10, size=100))
print(f"[1] {int(res_typical_num) if isinstance(res_typical_num, (float, np.float64)) and res_typical_num.is_integer() else res_typical_num}")

# most frequent value of character or factor
# r2py:entity:x
x_vals = np.random.choice(["a", "b", "c"], 100, p=[0.6, 0.2, 0.2], replace=True)
# Use the shim variable 'x' if it exists, otherwise use generated
x_input = x if 'x' in globals() else x_vals

# r2py:entity:typical_1
res_typical_1 = typical(x_input)
if isinstance(res_typical_1, np.ndarray):
    print(f"[1] {' '.join(map(str, res_typical_1))}")
else:
    print(f'[1] "{res_typical_1}"')

# r2py:entity:typical_2
x_factor = pd.Series(pd.Categorical(x_input))
res_typical_2 = typical(x_factor)
if isinstance(res_typical_2, np.ndarray):
    print(f"[1] {' '.join(map(str, res_typical_2))}")
else:
    print(f'[1] "{res_typical_2}"')

# if tied, returns them all
# r2py:entity:x_1
x_tied = pd.Series(["a", "a", "b", "b", "c"])
# r2py:entity:typical_3
res_typical_3 = typical(x_tied)
if isinstance(res_typical_3, np.ndarray):
    print(f"[1] {' '.join(map(str, res_typical_3))}")
else:
    print(f'[1] "{res_typical_3}"')

# median of an ordered factor
# r2py:entity:typical_4
x_ord_vals = ["a", "a", "b", "c", "d"]
x_ordered = pd.Series(pd.Categorical(x_ord_vals, categories=["a", "b", "c", "d"], ordered=True))
res_typical_4 = typical(x_ordered)
if isinstance(res_typical_4, np.ndarray):
    print(f"[1] {' '.join(map(str, res_typical_4))}")
else:
    print(f'[1] "{res_typical_4}"')