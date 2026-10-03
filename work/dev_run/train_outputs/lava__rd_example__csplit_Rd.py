# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__csplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd

# Ensure iris is a DataFrame
if 'iris' in globals() and isinstance(iris, dict):
    iris = pd.DataFrame(iris)

# r2py:entity:foldr
def foldr(n, K=5, rep=1, list_val=True):
    results = []
    for _ in range(rep):
        # sample(seq(n))
        perm = np.random.permutation(np.arange(1, n + 1))
        # rep(seq(K), length = n)
        groups = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
        
        # split(perm, groups)
        fold = {}
        for g in range(1, K + 1):
            fold[g] = perm[groups == g].tolist()
        results.append(fold)
    
    if not list_val:
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        first_fold = results[0]
        lengths = [len(first_fold[g]) for g in sorted(first_fold.keys())]
        ids = np.repeat(np.arange(1, len(first_fold) + 1), lengths)
        
        processed = []
        for fold in results:
            # unlist(x)
            flat_x = []
            for g in sorted(fold.keys()):
                flat_x.extend(fold[g])
            # ids[order(unlist(x))]
            order_idx = np.argsort(flat_x)
            processed.append(ids[order_idx].tolist())
        
        if len(processed) == 1:
            return processed[0]
        return processed

    if rep == 1:
        return results[0]
    return results

# r2py:entity:csplit
def csplit(x, p=None, replace=False, return_index=False, k=2, **kwargs):
    # if (length(x) == 1 && is.numeric(x)) x <- seq(x)
    if isinstance(x, (int, float, np.integer)) and np.ndim(x) == 0:
        x = np.arange(1, int(x) + 1)
    
    # N <- NROW(x)
    if isinstance(x, pd.DataFrame):
        N = x.shape[0]
    elif isinstance(x, (list, np.ndarray)):
        N = len(x)
    else:
        N = 1

    if p is None:
        # K <- base::round(N/k)
        K = int(round(N / k))
        # idx <- split(seq(N), sort(rep(seq(k), length.out = N, each = K)))
        groups = np.repeat(np.arange(1, k + 1), K)[:N]
        # split(seq(N), groups)
        idx = {}
        seq_N = np.arange(1, N + 1)
        for g in range(1, k + 1):
            idx[g] = seq_N[groups == g]
    else:
        if p < 1:
            # idx1 <- base::sample(N, base::round(p * N), replace = replace)
            n_idx1 = int(round(p * N))
            idx1 = np.random.choice(np.arange(1, N + 1), n_idx1, replace=replace)
            # idx <- list(idx1, base::sample(setdiff(seq(N), idx1), replace = replace))
            remaining = np.setdiff1d(np.arange(1, N + 1), idx1)
            idx2 = np.random.choice(remaining, len(remaining), replace=replace)
            idx = {1: idx1, 2: idx2}
        else:
            # idx <- split(sample(seq(N)), rep(seq(p), length = N))
            perm = np.random.permutation(np.arange(1, N + 1))
            groups = np.tile(np.arange(1, int(p) + 1), int(np.ceil(N / int(p))))[:N]
            idx = {}
            for g in range(1, int(p) + 1):
                idx[g] = perm[groups == g]

    if return_index:
        return idx

    # Return data based on index
    res = {}
    for g, ii in idx.items():
        ii_0based = np.array(ii) - 1
        if isinstance(x, pd.DataFrame):
            res[g] = x.iloc[ii_0based]
        elif isinstance(x, (list, np.ndarray)):
            res[g] = np.array(x)[ii_0based]
        else:
            res[g] = x[ii_0based]
    return res

# Execution
# r2py:entity:foldr
print(foldr(5, 2, rep=2))

# r2py:entity:csplit
print(csplit(10, 3))

# csplit(iris[1:10,])
# r2py:entity:csplit_1
print(csplit(iris.iloc[0:10]))

# csplit(iris[1:10,], 0.5)
# r2py:entity:csplit_2
print(csplit(iris.iloc[0:10], 0.5))