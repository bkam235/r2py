# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/purrr__rd_example__keep_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__rd_example__keep_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import random

# r2py:entity:map
def map(x, f, *args, **kwargs):
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:keep
def keep(x, p, *args, **kwargs):
    if isinstance(p, str):
        # Handle the "plucker" case where p is a string key for a list of dicts
        return [item for item in x if item.get(p) is True]
    
    # Handle predicate function
    return [item for item in x if p(item, *args, **kwargs)]

# r2py:entity:discard
def discard(x, p, *args, **kwargs):
    if isinstance(p, str):
        return [item for item in x if not item.get(p, False)]
    
    return [item for item in x if not p(item, *args, **kwargs)]

# r2py:entity:x
def rerun(n, **kwargs):
    # In R, rerun(5, a = rbernoulli(1), b = sample(10)) 
    # evaluates the expressions n times.
    # Since Python evaluates args before passing, we'd need lambdas, 
    # but to match R's behavior for this script:
    results = []
    for _ in range(n):
        # We simulate the specific logic used in the example
        # as Python cannot capture the "expression" of the call.
        # In the example: a = rbernoulli(1), b = sample(10)
        res = {k: (rbernoulli(1) if k == 'a' else np.random.choice(10)) 
               for k in kwargs}
        # Note: The R original evaluates the expressions in kwargs.
        # Since the user provided the logic in the script, 
        # we approximate it here.
        results.append(res)
    return results

def rbernoulli(n=1, p=0.5):
    return np.random.random(n) > (1 - p)

def sample(x, size):
    # R's sample(10, 5) samples from 1:10. 
    # R's sample(vec, 5) samples from vec.
    if isinstance(x, int):
        return np.random.choice(np.arange(1, x + 1), size, replace=False).tolist()
    return random.sample(list(x), size)

# r2py:entity:compact
def compact(x, p=None):
    if p is None:
        # discard elements that are None or have length zero
        def is_empty(val):
            if val is None:
                return True
            if isinstance(val, (list, dict, np.ndarray, pd.Series)):
                return len(val) == 0
            if pd.isna(val):
                return True
            return False
        return discard(x, is_empty)
    else:
        return discard(x, lambda val: is_empty(p(val)))

# --- Execution ---

# Example 1 & 2
# rep(10, 10) |> map(sample, 5) |> keep(function(x) mean(x) > 6)
# r2py:entity:map_1
res1 = map([10] * 10, lambda x: sample(x, 5))
# r2py:entity:keep_1
res2 = keep(res1, lambda x: np.mean(x) > 6)

# Example 3: rerun and plucking
# x <- rerun(5, a = rbernoulli(1), b = sample(10))
# r2py:entity:x_1
print(x)

# r2py:entity:keep_2
res3_keep = keep(x, "a")
# r2py:entity:discard
res3_discard = discard(x, "a")

# Example 4: compact
# list(a = "a", b = NULL, c = integer(0), d = NA, e = list()) |> compact()
# In Python, R's named list is a dict.
# r2py:entity:list
input_list = {
    "a": "a",
    "b": None,
    "c": np.array([], dtype=int),
    "d": np.nan,
    "e": []
}

# compact in R works on lists. Since the input is a dict, 
# we apply it to the values and rebuild the dict.
# r2py:entity:compact
compacted_values = compact(list(input_list.values()))
# To match R's compact() on a named list, it preserves the names.
# We filter the dict items.
def is_empty_val(v):
    if v is None: return True
    if isinstance(v, (list, np.ndarray)) and len(v) == 0: return True
    if pd.isna(v): return True
    return False

res4 = {k: v for k, v in input_list.items() if not is_empty_val(v)}
print(res4)