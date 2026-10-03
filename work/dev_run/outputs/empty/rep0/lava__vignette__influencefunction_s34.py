# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd

# r2py:entity:id
def foldr(n, K=5, rep_val=1, list_val=True):
    """
    Equivalent to R's foldr helper function.
    Creates clusters of observations.
    """
    # Sample indices from 0 to n-1
    indices = np.arange(n)
    # Shuffle indices
    shuffled = np.random.permutation(indices)
    
    # Split into K groups
    # In R, split(sample(seq(n)), rep(seq(K), length = n))
    # This essentially assigns each index to a group 1..K
    groups = np.tile(np.arange(K), int(np.ceil(n / K)))[:n]
    
    if list_val:
        # Return a list of arrays, each containing indices for that group
        return [shuffled[groups == i] for i in range(K)]
    else:
        # If list=FALSE, R returns a vector of IDs corresponding to original order
        # The logic in the R snippet for list=FALSE is complex, but it effectively
        # returns a vector of group assignments (IDs).
        return groups + 1 # 1-indexed to match R

# r2py:entity:Print
def Print(x, n=5):
    """
    Equivalent to the custom Print function in the R snippet.
    """
    if isinstance(x, pd.DataFrame) or isinstance(x, np.ndarray):
        if len(x) <= 2 * n:
            print(x)
        else:
            head = x[:n]
            tail = x[-n:]
            print(head)
            print("---" * (x.shape[1] if hasattr(x, 'shape') else 1))
            print(tail)
    else:
        print(x)

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    """
    Simplified version of lava::estimate for the specific context of 
    Aggregated Influence Functions. 
    In this context, it typically calculates the mean or 
    aggregated statistics per group.
    """
    # Convert to DataFrame for grouping
    df = pd.DataFrame(x)
    if id is not None:
        df['id'] = id
        # Aggregated IF typically involves calculating group-level means/estimates
        res = df.groupby('id').mean()
        return res
    return df.mean()

# Main Execution
# r2py:entity:set.seed
np.random.seed(1)

# y <- cbind(rnorm(1e5))
# r2py:entity:y
y = np.random.normal(0, 1, 100000).reshape(-1, 1)

# N <- 2e2
# r2py:entity:N
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# r2py:entity:id
id = foldr(y.shape[0], N, list_val=False)

# Print(cbind(table(id)))
# table(id) counts occurrences of each group ID
# r2py:entity:Print
counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(counts)

# e <- estimate(cbind(y), id = id)
# r2py:entity:e

# object.size(e)
# In Python, sys.getsizeof() is used, but for pandas objects 
# .memory_usage() is more accurate.
# r2py:entity:object.size
import sys
print(f"Object size: {sys.getsizeof(e)} bytes")

# e
# r2py:entity:e_1
print(e)