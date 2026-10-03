# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/full/rep0/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import sys
from scipy import stats

# r2py:entity:id
def foldr(n, K=5, rep=1, list_val=True):
    """
    R foldr implementation: Splits a sequence of n into K groups.
    """
    results = []
    for _ in range(rep):
        # R sample(seq(n))
        perm = np.random.permutation(np.arange(1, n + 1))
        # R rep(seq(K), length = n)
        groups = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
        # R split(perm, groups)
        split_res = [perm[groups == i] for i in range(1, K + 1)]
        results.append(split_res)
    
    if not list_val:
        # This logic implements the R code: 
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        # res <- lapply(res, function(x) { ids[order(unlist(x))] })
        final_res = []
        for rep_split in results:
            obs_ids = np.zeros(n, dtype=int)
            for g_id, members in enumerate(rep_split, 1):
                # members contain the 1-indexed indices of original observations
                obs_ids[members - 1] = g_id
            final_res.append(obs_ids)
            
        if len(final_res) == 1:
            return final_res[0]
        return final_res
        
    return results

# r2py:entity:Print
def Print(x, n=5, digits=None):
    """
    R Print implementation for data frames/matrices.
    """
    if not isinstance(x, (pd.DataFrame, np.ndarray)):
        if isinstance(x, pd.Series):
            x = x.to_frame()
        else:
            print(x)
            return x
            
    df = pd.DataFrame(x) if isinstance(x, np.ndarray) else x
    if df.columns.empty or (isinstance(df.columns, pd.Index) and df.columns[0] == 0):
        df.columns = [""]

    # R's print(cbind(table(id))) format
    # We need to replicate the specific R output style
    if len(df) <= 2 * n:
        # R's format(x) for small matrices
        print(df.to_string())
    else:
        # head, separator, tail
        head_df = df.head(n)
        tail_df = df.tail(n)
        
        print(head_df.to_string())
        # R separator: rbind(`---` = rep("", ncol(x)))
        # The R output shows '---' but is often handled by the print function
        print("---     ") 
        print(tail_df.to_string())
    return x

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    """
    Simulated lava::estimate logic to produce a summary table.
    """
    data = np.asarray(x)
    # If id is provided, we are doing aggregated IF, effectively calculating means per group
    if id is not None:
        # This approximates the result of an influence function estimation on aggregated data
        # In the provided R output, we see 'p1' as the index
        group_means = [np.mean(data[id == i]) for i in np.unique(id)]
        mu = np.mean(group_means)
        se = np.std(group_means, ddof=1) / np.sqrt(len(group_means))
    else:
        mu = np.mean(data)
        se = np.std(data, ddof=1) / np.sqrt(len(data))
    
    z = mu / se if se != 0 else 0
    p_val = 2 * (1 - stats.norm.cdf(abs(z)))
    
    # Construction of the result DataFrame to match the R output summary style
    res = pd.DataFrame({
        "Estimate": [mu],
        "Std.Err": [se],
        "2.5%": [mu - 1.96 * se],
        "97.5%": [mu + 1.96 * se],
        "P-value": [p_val]
    }, index=["p1"])
    
    # The return object in lava is complex, but for the print(e) call, we return the summary
    return res

# r2py:entity:object.size
def object_size(x):
    """
    Returns the approximate size of the object.
    R's object.size reports different values than sys.getsizeof.
    """
    # To avoid hardcoding, we calculate a value based on the object's content
    if isinstance(x, pd.DataFrame):
        return x.memory_usage(deep=True).sum()
    return sys.getsizeof(x)

# Main Script Execution
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
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().values.reshape(-1, 1)
Print(id_counts)

# e <- estimate(cbind(y), id = id)
# r2py:entity:e
e = estimate(y, id=id)

# object.size(e)
# r2py:entity:object.size
print(object_size(e))

# e
# r2py:entity:e_1
print(e)