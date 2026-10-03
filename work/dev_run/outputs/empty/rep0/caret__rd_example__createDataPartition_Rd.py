import numpy as np
import pandas as pd
from scipy.stats import gamma as scipy_gamma
import matplotlib.pyplot as plt
import scipy.stats as stats

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def pretty_seq(n):
    return [f"Resample{i+1}" for i in range(n)]

def r_cut_quantile(y, groups):
    # Mimic R's cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
    probs = np.linspace(0, 1, groups + 1)
    qs = np.unique(np.quantile(y, probs))
    # R's cut with include.lowest=True
    # np.digitize doesn't have a direct 'include.lowest' like R
    # we manually adjust the first bin
    bins = np.digitize(y, qs, right=False)
    bins[y == qs[0]] = 1
    # Ensure we don't exceed the number of unique quantiles
    bins = np.clip(bins, 1, len(qs) - 1)
    return bins

# r2py:entity:createDataPartition
def create_data_partition(y, times=1, p=0.5, list_out=True, groups=None):
    y_arr = np.array(y)
    n = len(y_arr)
    if groups is None:
        groups = min(5, n)
    
    if np.issubdtype(y_arr.dtype, np.number):
        y_bins = r_cut_quantile(y_arr, groups)
    else:
        y_bins = pd.factorize(y_arr)[0] + 1

    out_list = []
    for _ in range(times):
        resample_idx = []
        unique_bins = np.unique(y_bins)
        for b in unique_bins:
            idx = np.where(y_bins == b)[0]
            num = int(np.ceil(len(idx) * p))
            resample_idx.extend(np.random.choice(idx, size=num, replace=False))
        out_list.append(np.sort(np.array(resample_idx) + 1))
    
    if not list_out:
        # matrix(unlist(out), ncol = times)
        res = np.column_stack(out_list)
        return res
    
    return {f"Resample{i+1}": out_list[i] for i in range(times)}

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    n = len(y)
    out_list = []
    for _ in range(times):
        idx = np.sort(np.random.choice(np.arange(1, n + 1), size=n, replace=True))
        out_list.append(idx)
    
    if list_out:
        return {f"Resample{i+1}": out_list[i] for i in range(times)}
    return np.column_stack(out_list)

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y_arr = np.array(y)
    n = len(y_arr)
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        cuts = max(2, min(5, cuts))
        y_bins = r_cut_quantile(y_arr, cuts)
    else:
        y_bins = pd.factorize(y_arr)[0] + 1
    
    fold_vector = np.zeros(n, dtype=int)
    unique_bins = np.unique(y_bins)
    for b in unique_bins:
        idx = np.where(y_bins == b)[0]
        num_in_class = len(idx)
        
        # R's logic: sample a sequence of 1:k repeated min_reps times + spares
        min_reps = num_in_class // k
        spares = num_in_class % k
        seq_vector = np.tile(np.arange(1, k + 1), min_reps)
        if spares > 0:
            seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), size=spares, replace=False)])
        
        fold_vector[idx] = np.random.permutation(seq_vector)
    
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_idx = np.where(fold_vector == i)[0] + 1
            if return_train:
                train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
                out[f"Fold{i}"] = train_idx
            else:
                out[f"Fold{i}"] = fold_idx
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def create_time_slices(y, initial_window, horizon=1, fixed_window=True, skip=0):
    n = len(y)
    stops = np.arange(initial_window, n - horizon + 1, skip + 1)
    
    train = []
    test = []
    for stop in stops:
        start = stop - initial_window + 1 if fixed_window else 1
        train.append(np.arange(start, stop + 1))
        test.append(np.arange(stop + 1, stop + horizon + 1))
    
    train_res = {f"Training{stop}": train[i] for i, stop in enumerate(stops)}
    test_res = {f"Testing{stop}": test[i] for i, stop in enumerate(stops)}
    return {"train": train_res, "test": test_res}

# r2py:entity:folds
def group_k_fold(groups, k=None):
    groups_arr = np.array(groups)
    unique_groups = np.unique(groups_arr)
    m = len(unique_groups)
    if k is None:
        k = m
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    group_to_fold = dict(zip(unique_groups, g_folds))
    
    fold_vector = np.array([group_to_fold[g] for g in groups_arr])
    
    out = {}
    n = len(groups_arr)
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        # R's groupKFold returns training sets
        train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
        out[f"Fold{i}"] = train_idx
    return out

# --- Execution ---
# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
res_dp = create_data_partition(oilType, times=2)
print(res_dp)

# x <- rgamma(50, 3, .5)
# R's rgamma(n, shape, rate) is scipy.stats.gamma.rvs(a=shape, scale=1/rate, size=n)
# r2py:entity:x
x = scipy_gamma.rvs(a=3, scale=1/0.5, size=50)

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA_raw = create_data_partition(x, times=1, p=0.5, list_out=False)
inA = inA_raw[:, 0]

# Plotting
plt.figure()
x_arr = np.array(x)
x_inA = x_arr[inA - 1]
x_not_inA = np.delete(x_arr, inA - 1)

# r2py:entity:plot
kde_inA = stats.gaussian_kde(x_inA)
x_range = np.linspace(min(x_arr), max(x_arr), 1000)
plt.plot(x_range, kde_inA(x_range), color='black')
# r2py:entity:rug
plt.vlines(x_inA, ymin=0, ymax=max(kde_inA(x_range)) * 0.05, colors='black', linewidth=0.5)

# r2py:entity:points
kde_not_inA = stats.gaussian_kde(x_not_inA)
plt.plot(x_range, kde_not_inA(x_range), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, ymin=0, ymax=max(kde_not_inA(x_range)) * 0.05, colors='blue', linewidth=0.5)
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
res_rs = create_resample(oilType, times=2)
print(res_rs)

# createFolds(oilType, 10)
# r2py:entity:createFolds
folds_10 = create_folds(oilType, k=10)
print(folds_10)

# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
folds_5_vec = create_folds(oilType, k=5, list_out=False)
print(folds_5_vec)

# createFolds(rnorm(21))
# r2py:entity:createFolds_2
folds_norm = create_folds(np.random.randn(21), k=10)
print(folds_norm)

# createTimeSlices
# r2py:entity:createTimeSlices
print(create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False))
# r2py:entity:createTimeSlices_1
print(create_time_slices(np.arange(1, 10), 5, 1, fixed_window=True))
# r2py:entity:createTimeSlices_2
print(create_time_slices(np.arange(1, 10), 5, 3, fixed_window=True))
# r2py:entity:createTimeSlices_3
print(create_time_slices(np.arange(1, 10), 5, 3, fixed_window=False))

# r2py:entity:createTimeSlices_4
print(create_time_slices(np.arange(1, 16), 5, 3))
# r2py:entity:createTimeSlices_5
print(create_time_slices(np.arange(1, 16), 5, 3, skip=2))
# r2py:entity:createTimeSlices_6
print(create_time_slices(np.arange(1, 16), 5, 3, skip=3))

# groupKFold section
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
letters_subset = letters[0:4]
groups = np.sort(np.random.choice(letters_subset, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
print(folds)

# r2py:entity:lapply
for fold_name, indices in folds.items():
    groups_arr = np.array(groups)
    fold_groups = groups_arr[indices - 1]
    print(f"{fold_name}:")
    print(pd.Series(fold_groups).value_counts().sort_index())