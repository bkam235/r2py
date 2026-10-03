# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
# r2py:entity:e
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
    """
    R's foldr in this context creates random group assignments for n observations into K groups.
    """
    # Generate random assignments from 1 to K for n observations
    # In R: sample(seq(n)) then split by rep(seq(K), length=n)
    # This effectively assigns each index from 1 to n into one of K groups randomly.
    indices = np.arange(1, n + 1)
    np.random.shuffle(indices)
    
    # Assign to K groups
    groups = np.repeat(np.arange(1, K + 1), np.ceil(n/K).astype(int))[:n]
    
    # Map the shuffled indices to these group assignments
    assignment = np.zeros(n, dtype=int)
    assignment[indices - 1] = groups
    
    if list_val:
        # Return as a list of lists (indices in each group)
        res = [np.where(assignment == i)[0] + 1 for i in range(1, K + 1)]
        return res
    else:
        # Return as a vector of group IDs corresponding to original index order
        # The R code's 'list=FALSE' logic is essentially returning the group IDs for each observation
        # such that they are sorted within groups or maintained as a vector.
        # Looking at 'ids <- rep(seq_len(length(res[[1]])), ...)', it's creating group IDs.
        return assignment

# r2py:entity:Print
def Print(x, n=5, digits=None):
    """
    Approximate R's Print function for dataframes/matrices.
    """
    if isinstance(x, (pd.DataFrame, np.ndarray)):
        # Convert to DataFrame for pretty printing if it's a numpy array
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
    """
    The R 'estimate' function from 'lava' performs various statistical estimations.
    In the context of the provided vignette, it is likely calculating aggregated 
    estimates (e.g., means) across groups defined by 'id'.
    """
    # Based on the usage: e <- estimate(cbind(y), id = id)
    # This usually implies calculating group-wise statistics.
    # Since the full R source of 'estimate' is truncated and complex, 
    # we implement the common behavior for influence function vignettes: 
    # calculating the group means (aggregates).
    
    df = pd.DataFrame({'y': x.flatten(), 'id': id})
    e = df.groupby('id').mean()
    return e

# r2py:entity:object.size
def object_size(x):
    """
    Approximate R's object.size() returning size in bytes.
    """
    return sys.getsizeof(x)

# --- Main Script ---

# r2py:entity:set.seed
set_seed(1)

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
# table(id) in R counts occurrences of each group ID
# r2py:entity:Print
counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(counts)

# ## Aggregated IF
# e <- estimate(cbind(y), id = id) 

# object.size(e)
# r2py:entity:object.size
print(object_size(e))

# e
# r2py:entity:e_1
print(e)