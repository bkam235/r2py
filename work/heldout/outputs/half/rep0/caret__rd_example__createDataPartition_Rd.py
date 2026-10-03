# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def pretty_seq(x):
    # R: paste("Resample", gsub(" ", "0", format(seq(along.with_val= x))), sep = "")
    return [f"Resample{i+1}" for i in range(len(x))]

# r2py:entity:createDataPartition
def create_data_partition(y, times=1, p=0.5, list_out=True, groups=None):
    y_arr = np.array(y)
    n = len(y_arr)
    if n < 2:
        raise ValueError("y must have at least 2 data points")
    
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2
        
    if np.issubdtype(y_arr.dtype, np.number):
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups + 1)))
        y_cat = np.digitize(y_arr, breaks[1:-1])
    else:
        # Ensure y_cat is handled as a factor (categorical)
        y_cat = pd.factorize(y_arr)[0]
    
    out_list = []
    for j in range(times):
        resample_idx = []
        unique_cats = np.unique(y_cat)
        for cat in unique_cats:
            cat_indices = np.where(y_cat == cat)[0] + 1
            if len(cat_indices) == 1:
                resample_idx.extend(cat_indices)
            else:
                num = int(np.ceil(len(cat_indices) * p))
                resample_idx.extend(np.random.choice(cat_indices, size=num, replace=False))
        
        out_list.append(sorted(resample_idx))
        
    if not list_out:
        # R: matrix(unlist(out), ncol = times)
        max_len = max(len(v) for v in out_list)
        padded = [v + [np.nan] * (max_len - len(v)) for v in out_list]
        df = pd.DataFrame(np.array(padded).T, columns=pretty_seq(out_list))
        return df
    
    res_dict = {f"Resample{i+1}": v for i, v in enumerate(out_list)}
    return res_dict

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    y_arr = np.array(y)
    n = len(y_arr)
    out_list = []
    for j in range(times):
        idx = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out_list.append(sorted(idx.tolist()))
        
    if not list_out:
        df = pd.DataFrame(np.array(out_list).T, columns=pretty_seq(out_list))
        return df
    
    res_dict = {f"Resample{i+1}": v for i, v in enumerate(out_list)}
    return res_dict

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y_arr = np.array(y)
    n = len(y_arr)
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = int(np.floor(n / k))
        cuts = max(2, min(5, cuts))
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts + 1)))
        y_cat = np.digitize(y_arr, breaks[1:-1])
    else:
        y_cat = pd.factorize(y_arr)[0]
        
    num_in_class = pd.Series(y_cat).value_counts().sort_index()
    fold_vector = np.zeros(n, dtype=int)
    
    for cat, count in num_in_class.items():
        indices = np.where(y_cat == cat)[0]
        min_reps = count // k
        spares = count % k
        if min_reps > 0:
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            
            assigned = np.random.permutation(seq_vector)
            fold_vector[indices] = assigned.astype(int)
        else:
            fold_vector[indices] = np.random.choice(np.arange(1, k + 1), size=count, replace=True)
            
    if list_out:
        out = {}
        all_indices = np.arange(1, n + 1)
        for i in range(1, k + 1):
            fold_idx = all_indices[fold_vector == i]
            if return_train:
                out[f"Fold{i}"] = np.setdiff1d(all_indices, fold_idx).tolist()
            else:
                out[f"Fold{i}"] = fold_idx.tolist()
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def create_time_slices(y, initial_window, horizon=1, fixed_window=True, skip=0):
    n = len(y)
    stops = np.arange(initial_window, n - horizon + 1, skip + 1)
    
    train = {}
    test = {}
    
    for stop in stops:
        start = stop - initial_window + 1 if fixed_window else 1
        train[f"Training{stop}"] = list(range(int(start), int(stop) + 1))
        test[f"Testing{stop}"] = list(range(int(stop) + 1, int(stop + horizon) + 1))
        
    return {"train": train, "test": test}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group = np.array(group)
    g_unique, g_inverse = np.unique(group, return_inverse=True)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
        
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    fold_vector = g_folds[g_inverse]
    
    out = {}
    all_indices = np.arange(1, len(group) + 1)
    for i in range(1, k + 1):
        fold_indices = all_indices[fold_vector == i]
        # R: lapply(out, function(z) seq_along(group)[-z])
        out[f"Fold{i}"] = np.setdiff1d(all_indices, fold_indices).tolist()
        
    return out

# Execution
# suppressPackageStartupMessages(library(caret))
oil_type_data = np.array(oilType)
# r2py:entity:createDataPartition
res_partition = create_data_partition(oil_type_data, times=2)
print(res_partition)

# x <- rgamma(50, 3, .5)
# r2py:entity:x
x_data = np.array(x)

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA_matrix = create_data_partition(x_data, times=1, list_out=False)
inA_vec = inA_matrix.iloc[:, 0].dropna().astype(int).values
inA = [[int(i)] for i in inA_vec]

# plotting
# r2py:entity:plot
plt.figure()
inA_idx = (inA_vec - 1).astype(int)
kde_in = stats.gaussian_kde(x_data[inA_idx])
xs = np.linspace(min(x_data), max(x_data), 100)
plt.plot(xs, kde_in(xs))
# r2py:entity:rug
plt.vlines(x_data[inA_idx], -0.01, 0, colors='black', linewidth=0.5)

# r2py:entity:points
not_inA_idx = np.setdiff1d(np.arange(len(x_data)), inA_idx)
kde_out = stats.gaussian_kde(x_data[not_inA_idx])
plt.plot(xs, kde_out(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x_data[not_inA_idx], -0.01, 0, colors='blue', linewidth=0.5)
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
resamples = create_resample(oil_type_data, times=2)

# createFolds(oilType, 10)
# r2py:entity:createFolds
folds_10 = create_folds(oil_type_data, k=10)
# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
folds_5_vec = create_folds(oil_type_data, k=5, list_out=False)
# createFolds(rnorm(21))
# r2py:entity:createFolds_2
folds_norm = create_folds(np.random.randn(21))

# createTimeSlices
# r2py:entity:createTimeSlices
ts1 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False)
# r2py:entity:createTimeSlices_1
ts2 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=True)
# r2py:entity:createTimeSlices_2
ts3 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=True)
# r2py:entity:createTimeSlices_3
ts4 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=False)
# r2py:entity:createTimeSlices_4
ts5 = create_time_slices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_5
ts6 = create_time_slices(np.arange(1, 16), 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
ts7 = create_time_slices(np.arange(1, 16), 5, 3, skip=3)

# Final block
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups_sample = np.random.choice(letters[0:4], size=20, replace=True)
groups = np.sort(groups_sample)
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
# r2py:entity:lapply
for fold_name, indices in folds.items():
    subset_groups = [groups[i-1] for i in indices]
    print(pd.Series(subset_groups).value_counts().sort_index())