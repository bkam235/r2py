# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/lava__vignette__influencefunction_s34.py'
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
    """
    R-equivalent of foldr provided in source.
    Groups n observations into K aggregated groups.
    """
    res_list = []
    for _ in range(rep_val):
        # sample(seq(n)) is a permutation of 1:n
        perm = np.random.permutation(np.arange(1, n + 1))
        # split into K groups
        groups = np.array_split(perm, K)
        res_list.append([g.tolist() for g in groups])
    
    if not list_val:
        # Logic for list=FALSE: creates a vector of group IDs sorted by original index
        # In the provided R code: ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        # Then it sorts. Simplest way to achieve the same result as R's foldr(list=FALSE) 
        # for the case rep=1 is to generate a group ID for every observation.
        first_rep = res_list[0]
        ids = np.zeros(n, dtype=int)
        for group_idx, members in enumerate(first_rep):
            for m in members:
                ids[m-1] = group_idx + 1
        return ids
    
    return res_list

# r2py:entity:Print
def Print(x, n=5, digits=None):
    """
    R-equivalent of the Print function provided in source.
    Prints head and tail of a dataframe or matrix.
    """
    if not isinstance(x, (pd.DataFrame, np.ndarray)):
        print(x)
        return x
    
    df = pd.DataFrame(x)
    nrow = len(df)
    
    if nrow <= (2 * n):
        print(df)
    else:
        print(df.head(n))
        print("-" * df.shape[1])
        print(df.tail(n))
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    """
    Simplified implementation of lava::estimate logic for the context of 
    influence functions and aggregation. 
    In the R script, it's calculating an aggregated estimate based on IDs.
    """
    # Based on the R source and the context of influence functions:
    # When 'id' is provided, it typically performs an aggregated mean/estimate.
    if id is not None:
        df = pd.DataFrame({'y': x.flatten(), 'id': id})
        # The 'estimate' call here essentially computes the mean of the aggregated groups
        res = df.groupby('id')['y'].mean()
        return res
    return np.mean(x)

# Main script translation
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
id = foldr(y.shape[0], N, list_val=False)

# Print(cbind(table(id)))
# table(id) counts occurrences of each ID
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# e <- estimate(cbind(y), id = id)

# object.size(e)
# r2py:entity:object.size
print(sys.getsizeof(e))

# e
# r2py:entity:e_1
print(e)