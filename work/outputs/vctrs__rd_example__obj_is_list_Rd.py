# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__rd_example__obj_is_list_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__obj_is_list_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:obj_is_list
def obj_is_list(obj):
    return isinstance(obj, list)

# r2py:entity:list_all_vectors
def list_all_vectors(obj):
    if not isinstance(obj, list):
        raise TypeError("Input must be a list")
    # In Python, we check if elements are basic scalars or numpy arrays/pandas series
    return [isinstance(i, (int, float, str, np.ndarray, pd.Series)) for i in obj]

# r2py:entity:list_all_size
def list_all_size(obj, size):
    if not isinstance(obj, list):
        raise TypeError("Input must be a list")
    return all(len(i) == size if hasattr(i, '__len__') else size == 1 for i in obj)

# r2py:entity:list_all_recyclable
def list_all_recyclable(obj, size):
    if not isinstance(obj, list):
        raise TypeError("Input must be a list")
    # Simple interpretation of R's recycling: length 1 or exactly divides size
    def is_recyclable(i):
        l = len(i) if hasattr(i, '__len__') else 1
        return l == 1 or size % l == 0
    return all(is_recyclable(i) for i in obj)

# r2py:entity:list_check_all_vectors
def list_check_all_vectors(obj, allow_null=False):
    if not isinstance(obj, list):
        raise TypeError("Input must be a list")
    for i in obj:
        if i is None:
            if not allow_null:
                raise ValueError("Null value encountered")
            continue
        if not isinstance(i, (int, float, str, np.ndarray, pd.Series)):
            raise TypeError("Non-vector element encountered")
    return True

# r2py:entity:list_check_all_size
def list_check_all_size(obj, size, allow_null=False):
    if not isinstance(obj, list):
        raise TypeError("Input must be a list")
    for i in obj:
        if i is None:
            if not allow_null:
                raise ValueError("Null value encountered")
            continue
        l = len(i) if hasattr(i, '__len__') else 1
        if l != size:
            raise ValueError(f"Element size {l} does not match {size}")
    return True

# Test cases
# r2py:entity:obj_is_list
print(obj_is_list([]))
# r2py:entity:obj_is_list_1
print(obj_is_list([1]))
# r2py:entity:obj_is_list_2
print(obj_is_list(pd.DataFrame()))

# r2py:entity:list_all_vectors
print(list_all_vectors([1, pd.DataFrame(np.random.randn(5, 2))])) # DataFrame is not a simple vector
# r2py:entity:list_all_vectors_1
print(list_all_vectors([1, locals()])) # locals() is a dict

# r2py:entity:list_all_size
print(list_all_size([[1, 2], [2, 3]], 2))
# r2py:entity:list_all_size_1
print(list_all_size([[1, 2], [2, 3, 4]], 2))

# r2py:entity:list_all_recyclable
print(list_all_recyclable([1, [2, 3]], 2))
# r2py:entity:list_all_recyclable_1
print(list_all_recyclable([1, [2, 3, 4]], 2))

# r2py:entity:try
try:
    list_all_vectors(locals())
except Exception as e:
    print(f"Caught: {e}")

# r2py:entity:try_1
try:
    list_check_all_vectors([1, None, 2])
except Exception as e:
    print(f"Caught: {e}")

# r2py:entity:try_2
try:
    list_check_all_size([1, None, 2], size=1)
except Exception as e:
    print(f"Caught: {e}")

# r2py:entity:list_check_all_vectors
print(list_check_all_vectors([1, None, 2], allow_null=True))
# r2py:entity:list_check_all_size
print(list_check_all_size([1, None, 2], size=1, allow_null=True))

# r2py:entity:xs
xs = [1, None, [2, 3]]
# r2py:entity:try_3
try:
    list_check_all_size(xs, size=1, allow_null=True)
except Exception as e:
    print(f"Caught: {e}")

# Equivalent to vec_slice(xs, !vec_detect_missing(xs))
# r2py:entity:xs_1
xs = [i for i in xs if i is not None]

# r2py:entity:try_4
try:
    list_check_all_size(xs, size=1)
except Exception as e:
    print(f"Caught: {e}")