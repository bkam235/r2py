# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/lava__vignette__influencefunction_s34.py'
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
    # replicate(rep, split(sample(seq(n)), rep(seq(K), length = n)))
    res = []
    for _ in range(rep_val):
        indices = np.random.permutation(np.arange(n))
        groups = np.repeat(np.arange(1, K + 1), np.ceil(n/K).astype(int))[:n]
        split_data = {i: indices[groups == i].tolist() for i in range(1, K + 1)}
        res.append(split_data)
    
    if not list_val:
        # This logic in R extracts the first replication and reformats based on order
        first_rep = res[0]
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        lengths = [len(first_rep[k]) for k in range(1, K + 1)]
        ids = np.repeat(np.arange(1, K + 1), lengths)
        
        final_res = []
        for k in range(1, K + 1):
            # ids[order(unlist(x))]
            sorted_indices = np.sort(first_rep[k])
            # In the R source, it seems to return indices relative to the 'ids' vector
            # But based on common foldr usage in lava, it's mapping observations to group IDs
            final_res.append(sorted_indices)
            
        if len(res) == 1:
            # The R script calls foldr(nrow(y), N, list=FALSE)
            # which results in a vector of IDs for each observation
            return ids
        return final_res
    return res

# r2py:entity:Print
def Print(x, n=5, digits=None):
    if isinstance(x, pd.DataFrame) or isinstance(x, np.ndarray):
        df = pd.DataFrame(x)
        if len(df) <= 2 * n:
            print(df)
        else:
            print(df.head(n))
            print("---" * (df.shape[1] // 3 + 1))
            print(df.tail(n))
    else:
        print(x)
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    # This is a simplified mock of lava::estimate logic for this specific vignette.
    # In the context of influence functions, it typically returns the estimate 
    # and the aggregated influence function values.
    # Since the full R source for the S3 method estimate.default is truncated,
    # we implement the core behavior observed in the vignette:
    # creating an object that represents the estimation result.
    
    # For the vignette's purpose, e is an object that holds the result.
    # We use a dictionary to simulate the R object.
    return {
        "estimate": np.mean(x),
        "id": id,
        "data": x,
        "type": "aggregated_if"
    }

# r2py:entity:object.size
def object_size(x):
    return sys.getsizeof(x)

# Main script execution
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
# table(id) in R counts occurrences of each unique value
# r2py:entity:Print
counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(counts)

# e <- estimate(cbind(y), id = id)

# object.size(e)
# r2py:entity:object.size
print(object_size(e))

# e
# r2py:entity:e_1
print(e)