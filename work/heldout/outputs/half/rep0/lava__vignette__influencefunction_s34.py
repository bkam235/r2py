# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/lava__vignette__influencefunction_s34.py'
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
def foldr_custom(n, K=5, rep_val=1, list_val=True):
    # R: replicate(rep, split(sample(seq(n)), rep(seq(K), length = n)), simplify = FALSE)
    all_reps = []
    for _ in range(rep_val):
        perm = np.random.permutation(np.arange(1, n + 1))
        groups = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
        # split(sample(seq(n)), groups)
        res_list = [perm[groups == k] for k in range(1, K + 1)]
        all_reps.append(res_list)
    
    if not list_val:
        # res_first = all_reps[0]
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        # res <- lapply(res, function(x) { ids[order(unlist(x))] })
        res_first = all_reps[0]
        lengths = [len(x) for x in res_first]
        ids_base = np.repeat(np.arange(1, len(lengths) + 1), lengths)
        
        # For each group in res_first, find the positions of its elements in the original sequence
        # and map them to the group ID.
        # In R: ids[order(unlist(x))] where x is a group of indices.
        # This is essentially recreating the 'groups' vector but mapped to the sampled order.
        # Actually, the R code: res <- lapply(res, function(x) { ids[order(unlist(x))] })
        # with list=FALSE returns res[[1]], which is a vector of group IDs for each observation.
        
        # Simplified: the group ID for each observation in the sampled sequence.
        final_ids = np.zeros(n, dtype=int)
        for group_idx, member_indices in enumerate(res_first, 1):
            # member_indices are 1-based indices from the sample(seq(n))
            # We want the group ID (group_idx) at the position specified by the index
            final_ids[member_indices - 1] = group_idx
        return final_ids
        
    return all_reps[0] if rep_val == 1 else all_reps

# r2py:entity:Print
def Print_custom(x, n=5, digits=3):
    if not hasattr(x, 'shape') or len(x.shape) < 2:
        df = pd.DataFrame(x)
    else:
        df = pd.DataFrame(x)
    
    if len(df) <= 2 * n:
        print(df.to_string())
    else:
        head = df.head(n).to_string()
        tail = df.tail(n).to_string()
        sep = "---"
        print(f"{head}\n{sep}\n{tail}")
    return x

# r2py:entity:e
def estimate_custom(y, id_val):
    # lava::estimate for simple mean: 
    # Estimate = mean(y)
    # Std.Err = Robust SE of the mean
    # For a simple mean, the IF is (y - mean(y))
    # Grouped IF: e_i = (1/N) * sum_{j in group i} (y_j - global_mean)
    
    df = pd.DataFrame({'y': y.flatten(), 'id': id_val})
    global_mean = df['y'].mean()
    
    # Group means
    group_means = df.groupby('id')['y'].mean()
    
    # robust SE for mean: sqrt( var(group_means) / num_groups )
    # But lava's estimate usually provides the overall mean's SE across groups
    # For the specific output 'p1 -0.002244 0.00332 ...', it is an estimate of a parameter.
    # In this vignette, e = estimate(cbind(y), id=id) is likely estimating the mean of y.
    
    est = global_mean
    # Robust SE across clusters
    cluster_means = df.groupby('id')['y'].mean()
    std_err = np.std(cluster_means, ddof=1) / np.sqrt(len(cluster_means))
    
    # Confidence intervals
    z = 1.96
    low = est - z * std_err
    high = est + z * std_err
    p_val = 2 * (1 - stats.norm.cdf(abs(est / std_err))) if std_err != 0 else 1.0
    
    # The output is a dataframe-like object 'e'
    res = pd.DataFrame({
        'Estimate': [est],
        'Std.Err': [std_err],
        '2.5%': [low],
        '97.5%': [high],
        'P-value': [p_val]
    }, index=['p1'])
    
    # To match object.size, we create a dict mimicking the lava object
    return {
        'coef': res,
        'print': res,
        'id': id_val,
        'ncluster': len(cluster_means)
    }

# Execution
# r2py:entity:set.seed
np.random.seed(1)
# r2py:entity:y
y = np.random.normal(size=(100000, 1))
# r2py:entity:N
N = 200
# r2py:entity:id
id = foldr_custom(len(y), K=N, list_val=False)
# r2py:entity:Print
Print_custom(pd.DataFrame(pd.Series(id).value_counts().sort_index()))

# r2py:entity:e
e = estimate_custom(y, id)
# r2py:entity:object.size
print(f"{sys.getsizeof(e)} bytes")
# r2py:entity:e_1
print(e['print'])