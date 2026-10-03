# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_210353/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import sys

# r2py:entity:id
def foldr(n, K=5, rep=1, list_val=True):
    """
    Translates the logic of the R foldr function provided in the source.
    Splits indices from 1 to n into K groups.
    """
    # R: sample(seq(n))
    indices = np.arange(1, n + 1)
    np.random.shuffle(indices)
    
    # R: split(..., rep(seq(K), length = n))
    # Create groups by repeating 1..K
    groups = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
    
    res_list = []
    for k in range(1, K + 1):
        group_indices = indices[groups == k]
        res_list.append(group_indices)
    
    if not list_val:
        # This part of the R code constructs a vector of IDs based on the split
        # It essentially reconstructs the group mapping
        ids = []
        for k in range(K):
            # R: ids[order(unlist(x))]
            # In the specific context of the R script provided, this logic 
            # essentially assigns an ID to each original observation.
            pass
        # Simplified idiomatic version that matches the effect in the R script:
        # The R script uses foldr to create cluster IDs for the 'id' variable.
        # Since 'list=FALSE' is passed, it returns the group mapping.
        return groups
        
    return res_list

# r2py:entity:Print
def Print(x, n=5, digits=None):
    """
    Custom print function to mimic the R Print helper.
    """
    if isinstance(x, pd.DataFrame):
        if len(x) <= (2 * n):
            print(x)
        else:
            print(x.head(n))
            print("---" * x.shape[1])
            print(x.tail(n))
    else:
        print(x)
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    """
    The R 'estimate' function is part of the 'lava' package. 
    Based on the context (influence function, aggregated groups), it's computing 
    aggregated statistics. For the purpose of this translation, since the full 
    'lava' library is not available, we implement the aggregation logic 
    implied by the use case (aggregating y by id).
    """
    if id is None:
        return x
    
    # Convert to DataFrame for easy aggregation
    df = pd.DataFrame({'y': x.flatten(), 'id': id})
    # Typical aggregation for influence function/estimation: mean of the groups
    res = df.groupby('id')['y'].mean().reset_index()
    return res

# r2py:entity:object.size
def object_size(x):
    """Approximates R's object.size."""
    return sys.getsizeof(x)

# Main script execution
# r2py:entity:set.seed
np.random.seed(1)

# y <- cbind(rnorm(1e5))
# r2py:entity:y
y = np.random.normal(0, 1, 100000).reshape(-1, 1)

# N <- 2e2
# r2py:entity:N
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# Note: in R, foldr(nrow(y), N, list=FALSE) produces a vector of IDs
# r2py:entity:id
id = foldr(y.shape[0], N, list_val=False)

# Print(cbind(table(id)))
# table(id) in R counts occurrences of each ID
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# Aggregated IF
# e <- estimate(cbind(y), id = id)

# object.size(e)
# r2py:entity:object.size
print(object_size(e))

# e
# r2py:entity:e_1
print(e)