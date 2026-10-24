import numpy as np
import pandas as pd
import random

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__csplit_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__csplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:foldr
def foldr(n, K=5, rep_val=1, list_out=True):
    res_list = []
    for _ in range(rep_val):
        # sample(seq(n))
        s = list(range(1, n + 1))
        random.shuffle(s)
        
        # rep(seq(K), length = n)
        groups = []
        for i in range(n):
            groups.append((i % K) + 1 if (i // 1) < 0 else ((i // (n // K)) if (n // K) > 0 else 0)) 
        # Correction: R's rep(seq(K), length = n) is 1,2,3,4,5,1,2,3,4,5...
        groups = [((i % K) + 1) for i in range(n)]
        
        # split(sample, groups)
        split_res = {}
        for val, g in zip(s, groups):
            if g not in split_res: split_res[g] = []
            split_res[g].append(val)
        
        res_list.append({g: split_res[g] for g in sorted(split_res.keys())})

    if not list_out:
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        # This is a very specific R operation to create a mapping for ordering
        first_split = res_list[0]
        ids = []
        for g in sorted(first_split.keys()):
            ids.extend([g] * len(first_split[g]))
        
        final_res = []
        for split_set in res_list:
            # unlist(x)
            flat_x = []
            for g in sorted(split_set.keys()):
                flat_x.extend(split_set[g])
            
            # ids[order(unlist(x))]
            sorted_indices = np.argsort(flat_x)
            final_res.append([ids[i] for i in sorted_indices])
            
        if len(final_res) == 1:
            return final_res[0]
        return final_res
        
    return res_list

# r2py:entity:csplit
def csplit(x, p=None, replace=False, return_index=False, k=2, **kwargs):
    if isinstance(x, (int, float)) and not isinstance(x, (list, np.ndarray, pd.DataFrame, pd.Series)):
        seq_x = list(range(1, int(x) + 1))
    else:
        seq_x = x

    if isinstance(seq_x, pd.DataFrame):
        N = seq_x.shape[0]
    elif isinstance(seq_x, (list, np.ndarray, pd.Series)):
        N = len(seq_x)
    else:
        N = 0

    if p is None:
        # K <- base::round(N/k)
        K_val = int(round(N / k))
        # rep(seq(k), length.out = N, each = K)
        groups = []
        for i in range(1, k + 1):
            groups.extend([i] * K_val)
        groups = groups[:N]
        if len(groups) < N:
            groups.extend([k] * (N - len(groups)))
        
        # split(seq(N), sort(groups))
        idx_dict = {}
        for i, g in enumerate(groups):
            if g not in idx_dict: idx_dict[g] = []
            idx_dict[g].append(i + 1)
        idx = [idx_dict[g] for g in sorted(idx_dict.keys())]
    else:
        if p < 1:
            # sample(N, round(p*N), replace=replace)
            all_indices = list(range(1, N + 1))
            n_sample = int(round(p * N))
            if replace:
                idx1 = [random.choice(all_indices) for _ in range(n_sample)]
            else:
                idx1 = random.sample(all_indices, n_sample)
            
            # sample(setdiff(seq(N), idx1), replace=replace)
            diff = [i for i in all_indices if i not in idx1]
            if replace:
                idx2 = [random.choice(diff) for _ in range(len(diff))] if diff else []
            else:
                idx2 = random.sample(diff, len(diff)) if diff else []
            idx = [idx1, idx2]
        else:
            # split(sample(seq(N)), rep(seq(p), length = N))
            s = list(range(1, N + 1))
            random.shuffle(s)
            groups = [((i % int(p)) + 1) for i in range(N)]
            idx_dict = {}
            for val, g in zip(s, groups):
                if g not in idx_dict: idx_dict[g] = []
                idx_dict[g].append(val)
            idx = [idx_dict[g] for g in sorted(idx_dict.keys())]

    if return_index:
        return idx
    
    if isinstance(seq_x, pd.DataFrame):
        return [seq_x.iloc[np.array(ii) - 1] for ii in idx]
    
    if isinstance(seq_x, (list, np.ndarray, pd.Series)):
        return [[seq_x[i-1] for i in ii] for ii in idx]
    else:
        return [[i for i in ii] for ii in idx]

# Executing the script logic
# foldr(5,2,rep=2)
# r2py:entity:foldr
print(foldr(5, 2, rep_val=2))

# csplit(10,3)
# r2py:entity:csplit
print(csplit(10, 3))

# csplit(iris[1:10,])
# r2py:entity:csplit_1
print(csplit(iris.iloc[0:10]))

# csplit(iris[1:10,],0.5)
# r2py:entity:csplit_2
print(csplit(iris.iloc[0:10], 0.5))