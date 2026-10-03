# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import sys

# r2py:entity:id
def foldr(n, K=5, rep_val=1, list_val=True):
    # R's sample(seq(n)) is a random permutation of 1..n
    # We simulate this by shuffling indices
    indices = np.arange(1, n + 1)
    np.random.shuffle(indices)
    
    # split(indices, rep(seq(K), length = n))
    # In R, this splits the shuffled indices into K groups
    groups = [[] for _ in range(K)]
    for i, val in enumerate(indices):
        group_idx = i % K
        groups[group_idx].append(val)
    
    if not list_val:
        # This part of the R function reconstructs a vector that maps 
        # the original observation index to its group membership
        # such that the mapping preserves the order of groups
        ids = np.zeros(n, dtype=int)
        for group_id, members in enumerate(groups, 1):
            for member in members:
                ids[member - 1] = group_id
        return ids
    
    return groups

# r2py:entity:Print
def Print(x, n=5, digits=None):
    # x is expected to be a DataFrame or numpy array
    if isinstance(x, pd.DataFrame):
        df = x
    elif isinstance(x, np.ndarray):
        df = pd.DataFrame(x)
    else:
        print(x)
        return x

    nrows = len(df)
    if nrows <= (2 * n):
        print(df)
    else:
        head = df.head(n)
        tail = df.tail(n)
        print(head)
        print("-" * df.shape[1])
        print(tail)
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    # Based on the context of the lava package and the provided logic:
    # 'estimate' here calculates aggregated statistics/influence functions.
    # Since the full internal implementation is truncated and refers to 
    # complex model-based SEs and ICs, we implement the core requested logic:
    # grouping by 'id' and calculating the mean/estimate.
    
    if isinstance(x, np.ndarray):
        x_df = pd.DataFrame(x)
    else:
        x_df = x
        
    if id is not None:
        x_df['id_col'] = id
        # The estimate function in this context typically returns 
        # an object containing the coefficients and the influence functions.
        # We return a summary object (dict) to mimic the R object structure.
        res = x_df.groupby('id_col').mean()
        return {'coefficients': res, 'data': x_df}
    
    return x_df.mean()

# r2py:entity:object.size
def object_size(x):
    return sys.getsizeof(x)

# Main script
# r2py:entity:set.seed
np.random.seed(1)

# y <- cbind(rnorm(1e5))
# r2py:entity:y
y = np.random.normal(size=(100000, 1))

# N <- 2e2
# r2py:entity:N
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# r2py:entity:id
id = foldr(y.shape[0], K=N, list_val=False)

# Print(cbind(table(id)))
# table(id) in R creates a frequency table of the groups
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# e <- estimate(cbind(y), id = id)
# r2py:entity:e

# object.size(e)
# r2py:entity:object.size
print(object_size(e))

# e
# r2py:entity:e_1
print(e)