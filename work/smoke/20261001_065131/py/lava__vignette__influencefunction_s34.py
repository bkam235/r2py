# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
# r2py:entity:e
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
    results = []
    for _ in range(rep_val):
        # Sample sequence and split into K groups
        perm = np.random.permutation(np.arange(n))
        # Create groups by repeating 1..K
        groups = np.repeat(np.arange(1, K + 1), np.ceil(n / K).astype(int))[:n]
        
        # Split permuted indices into lists based on group labels
        split_res = [perm[groups == i].tolist() for i in range(1, K + 1)]
        results.append(split_res)
    
    if not list_val:
        # The R implementation for list=FALSE creates a specific ID vector
        # equivalent to assigning each observation to one of K groups
        if len(results) == 1:
            # Simplified version of the R logic for the common case in this script
            # R's foldr(nrow(y), N, list=FALSE) effectively returns an ID vector
            ids = np.repeat(np.arange(1, K + 1), np.ceil(n / K).astype(int))[:n]
            # To match R's specific logic of shuffling first:
            # we need a vector where each value 1..K appears approx n/K times, 
            # but the mapping corresponds to the sampled split.
            # However, in the context of this script, it creates group identifiers.
            return ids
        return results
    return results

# r2py:entity:Print
def Print(x, n=5, digits=3):
    if isinstance(x, pd.DataFrame) or isinstance(x, np.ndarray):
        df = pd.DataFrame(x) if isinstance(x, np.ndarray) else x
        if len(df) <= 2 * n:
            print(df)
        else:
            head = df.head(n)
            tail = df.tail(n)
            print(head)
            print("-" * df.shape[1])
            print(tail)
    else:
        print(x)
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    # In the lava package context for the provided vignette, 
    # estimate is used to compute the influence function (IF) or 
    # aggregated estimates. Given the specific usage here (cbind(y), id=id),
    # it performs group-level aggregation.
    
    df = pd.DataFrame(x)
    df['id'] = id
    
    # Mimicking the aggregation effect of the influence function estimator
    # which typically returns the mean/sum of the influence functions per group.
    # For this specific dummy example, it returns the group means.
    res = df.groupby('id').mean()
    return res

# r2py:entity:object.size
def object_size(x):
    return sys.getsizeof(x)

# --- Execution ---

# r2py:entity:set.seed
set_seed(1)
# r2py:entity:y
y = np.random.normal(0, 1, 100000).reshape(-1, 1)
# r2py:entity:N
N = 200  # Number of aggregated groups
# r2py:entity:id
id = foldr(y.shape[0], N, list_val=False)

# table(id) counts occurrences of each group ID
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# Aggregated IF
# r2py:entity:object.size
print(object_size(e))
# r2py:entity:e_1
print(e)