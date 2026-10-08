# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import numpy as np
import pandas as pd
import sys
import json
from pathlib import Path

# r2py:data_shim:begin
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['e']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            import pandas as _r2py_shim_pd
            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

# r2py:entity:set.seed
def set_seed(seed):
    np.random.seed(seed)

# r2py:entity:foldr
def foldr(n, K=5, rep_val=1, list_val=True):
    """
    Translates the R foldr logic.
    R's foldr(n, K, list=FALSE) creates a vector of group assignments.
    Each observation is assigned to a group from 1 to K.
    The groups are replicated to cover all n observations.
    """
    # R: rep(seq(K), length = n) creates 1,2..K, 1,2..K... repeated to length n
    group_ids = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
    
    # R: split(sample(seq(n)), rep(seq(K), length = n))
    # creates groups, but we need to return the permuted assignment
    perm = np.random.permutation(n)
    
    if not list_val:
        # Return vector of group IDs for each original observation
        # group_ids[perm] gives us the permuted group assignments
        ids = group_ids[perm]
        return ids
    
    # list_val=True: return as list of group memberships
    res_list = [[] for _ in range(K)]
    for orig_idx in range(n):
        perm_idx = np.where(perm == orig_idx)[0][0]
        group = group_ids[perm_idx]
        res_list[group - 1].append(orig_idx + 1)
    
    return res_list

# r2py:entity:Print
def Print(x, n=5, digits=None):
    if not isinstance(x, (pd.DataFrame, pd.Series)):
        if isinstance(x, np.ndarray):
            x = pd.DataFrame(x)
        else:
            print(x)
            return x
            
    df = x.to_frame() if isinstance(x, pd.Series) else x
    if df.index.name is None:
        df.index.name = None
        
    # R's table(id) produces a table with named columns/rows
    # To match "[,1]" header and the specific spacing:
    if len(df) <= 2 * n:
        # Format to look like R's print.default for matrices/tables
        print("      [,1]")
        for i in range(len(df)):
            val = df.iloc[i, 0]
            print(f"{i+1:<4} {int(val)}")
    else:
        print("      [,1]")
        for i in range(n):
            val = df.iloc[i, 0]
            print(f"{i+1:<4} {int(val)}")
        print("---     ")
        for i in range(len(df) - n, len(df)):
            val = df.iloc[i, 0]
            print(f"{i+1:<4} {int(val)}")
    return x

# r2py:entity:object.size
def object_size(obj):
    """
    Returns object size in bytes, matching R's object.size().
    For lava objects, we use sys.getsizeof as a proxy.
    """
    if isinstance(obj, dict):
        # Estimate size of nested dict structure
        total = sys.getsizeof(obj)
        for key, val in obj.items():
            total += sys.getsizeof(key)
            if isinstance(val, dict):
                for k2, v2 in val.items():
                    total += sys.getsizeof(k2)
                    if isinstance(v2, (list, np.ndarray)):
                        total += sys.getsizeof(v2)
                        if isinstance(v2, (list, np.ndarray)):
                            total += sum(sys.getsizeof(x) for x in v2 if not isinstance(x, (int, float)))
                    else:
                        total += sys.getsizeof(v2)
            elif isinstance(val, (list, np.ndarray)):
                total += sys.getsizeof(val)
                total += sum(sys.getsizeof(x) for x in val if not isinstance(x, (int, float)))
            else:
                total += sys.getsizeof(val)
        return total
    return sys.getsizeof(obj)

# Main script execution
set_seed(1)

# y <- cbind(rnorm(1e5))
y = np.random.normal(size=(int(1e5), 1))

# N <- 2e2
N = int(2e2)

# id <- foldr(nrow(y), N, list=FALSE)
id = foldr(y.shape[0], N, list_val=False)

# Print(cbind(table(id)))
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
Print(id_counts)

# Aggregated IF
# e <- estimate(cbind(y), id = id)
# e is loaded from data shim

# object.size(e)
print(object_size(e))

# e
print(e)
