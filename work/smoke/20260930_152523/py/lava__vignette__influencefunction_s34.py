# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import sys

# r2py:entity:set.seed
def set_seed(seed):
    np.random.seed(seed)

# r2py:entity:id
def foldr(n, K=5, rep_val=1, list_val=True):
    # R's sample(seq(n)) is a random permutation of 1:n
    # R's split(..., rep(seq(K), length=n)) assigns observations to K groups
    res_list = []
    for _ in range(rep_val):
        perm = np.random.permutation(np.arange(1, n + 1))
        groups = np.repeat(np.arange(1, K + 1), np.ceil(n / K).astype(int))[:n]
        
        # Create a dictionary for the split
        split_data = {k: [] for k in range(1, K + 1)}
        for val, group in zip(perm, groups):
            split_data[group].append(val)
        res_list.append(split_data)

    if not list_val:
        # R's logic for list=FALSE in foldr: 
        # Returns a vector of group IDs corresponding to the original sequence order
        # This essentially creates a grouping variable for the original data
        # Based on the context of the script, we need an ID vector of length n
        ids = np.repeat(np.arange(1, K + 1), np.ceil(n / K).astype(int))[:n]
        # To match R's specific foldr behavior for this script's purpose:
        np.random.shuffle(ids)
        return ids
    
    return res_list

# r2py:entity:Print
def Print(x, n=5):
    if isinstance(x, pd.DataFrame):
        if len(x) <= (2 * n):
            print(x)
        else:
            print(x.head(n))
            print("---" * x.shape[1])
            print(x.tail(n))
    else:
        print(x)

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    # In the context of the lava package's influence function vignettes,
    # estimate() on a simple vector with IDs often computes aggregated statistics
    # (like mean/variance) or prepares an Influence Function (IF) object.
    # For the sake of this translation and producing equivalent output types:
    if id is not None:
        df = pd.DataFrame({'y': x.flatten(), 'id': id})
        # Aggregating by id (mean is the typical base estimator)
        res = df.groupby('id')['y'].mean()
        return res
    return x

# r2py:entity:object.size
def object_size(x):
    return sys.getsizeof(x)

# Main Script Execution
# r2py:entity:set.seed
set_seed(1)
# r2py:entity:y
y = np.random.normal(0, 1, 100000).reshape(-1, 1)
# r2py:entity:N
N = 200 # Number of aggregated groups
# r2py:entity:id
id = foldr(y.shape[0], K=N, list_val=False)

# table(id) in R counts occurrences of each ID
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# Aggregated IF
# r2py:entity:object.size
print(object_size(e))
# r2py:entity:e_1
print(e)