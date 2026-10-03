# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def pretty_seq(n):
    return [f"Resample{i+1}" for i in range(n)]

# r2py:entity:createDataPartition
def create_data_partition(y, times=1, p=0.5, list_out=True, groups=None):
    y = np.array(y)
    n = len(y)
    if n < 2:
        raise ValueError("y must have at least 2 data points")
    
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2
        
    if np.issubdtype(y.dtype, np.number):
        # Logic matching R's cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))))
        qs = np.quantile(y, np.linspace(0, 1, groups + 1))
        breaks = np.unique(qs)
        # np.digitize is equivalent to cut
        y_fact = np.digitize(y, breaks[1:-1])
    else:
        y_fact = y

    resamples = []
    for j in range(times):
        indices = np.arange(n)
        sample_indices = []
        unique_vals = np.unique(y_fact)
        for val in unique_vals:
            idx_val = indices[y_fact == val]
            num = int(np.ceil(len(idx_val) * p))
            if len(idx_val) > 0:
                sampled = np.random.choice(idx_val, size=num, replace=False)
                sample_indices.extend(sampled)
        
        resamples.append(sorted(list(sample_indices)))

    if not list_out:
        # R's matrix(unlist(out), ncol=times)
        # return as 2D numpy array (indices 1-based to match R's matrix output)
        mat = np.array(resamples).T
        return mat + 1
    
    out_dict = {f"Resample{i+1}": resamples[i] for i in range(times)}
    # Correcting to 1-based indices for output consistency if returned as list
    for k in out_dict:
        out_dict[k] = [idx + 1 for idx in out_dict[k]]
    return out_dict

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    y = np.array(y)
    n = len(y)
    resamples = []
    for j in range(times):
        idx = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        resamples.append(sorted(idx.tolist()))
    
    if not list_out:
        return np.array(resamples).T
    
    out_dict = {f"Resample{i+1}": resamples[i] for i in range(times)}
    return out_dict

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = max(2, min(5, n // k))
        breaks = np.unique(np.quantile(y, np.linspace(0, 1, cuts + 1)))
        y_fact = np.digitize(y, breaks[1:-1])
    else:
        y_fact = y

    fold_vector = np.zeros(n, dtype=int)
    unique_vals = np.unique(y_fact)
    for val in unique_vals:
        idx_val = np.where(y_fact == val)[0]
        num_in_class = len(idx_val)
        min_reps = num_in_class // k
        spares = num_in_class % k
        
        if min_reps > 0:
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            np.random.shuffle(seq_vector)
            fold_vector[idx_val] = seq_vector
        else:
            fold_vector[idx_val] = np.random.choice(np.arange(1, k + 1), size=num_in_class, replace=True)

    if list_out:
        out = {}
        for i in range(1, k + 1):
            if return_train:
                indices = np.where(fold_vector != i)[0] + 1
            else:
                indices = np.where(fold_vector == i)[0] + 1
            out[f"Fold{i}"] = sorted(indices.tolist())
        return out
    else:
        return fold_vector

# r2py:entity:createTimeSlices
def create_time_slices(y, initial_window, horizon=1, fixed_window=True, skip=0):
    n = len(y)
    stops = np.arange(initial_window, n - horizon + 1, skip + 1)
    
    train = {}
    test = {}
    
    for stop in stops:
        start = (stop - initial_window + 1) if fixed_window else 1
        train_indices = list(range(start, stop + 1))
        test_indices = list(range(stop + 1, stop + horizon + 1))
        
        stop_str = str(stop).replace(" ", "0")
        train[f"Training{stop_str}"] = train_indices
        test[f"Testing{stop_str}"] = test_indices
        
    return {"train": train, "test": test}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group = np.array(group)
    g_unique, g_inv = np.unique(group, return_inverse=True)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    fold_vector = g_folds[g_inv]
    
    out = {}
    for i in range(1, k + 1):
        # caret's groupKFold returns the TRAINING set
        train_indices = np.where(fold_vector != i)[0] + 1
        out[f"Fold{i}"] = sorted(train_indices.tolist())
    return out

# --- Execution ---

# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
print(create_data_partition(oilType, times=2))

# r2py:entity:x
# x <- rgamma(50, 3, .5) (handled by shim)
# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA = create_data_partition(x, times=1, list_out=False)
# inA is now a 2D array (since times=1, it's (50, 1)). First column is indices.
inA_indices = inA[:, 0].astype(int) - 1

# Plotting
x_arr = np.array(x)
x_inA = x_arr[inA_indices]
x_not_inA = np.delete(x_arr, inA_indices)

# r2py:entity:plot
plt.figure(figsize=(8, 6))
if len(x_inA) > 1:
    kde_in = gaussian_kde(x_inA)
    x_range = np.linspace(min(x_arr), max(x_arr), 200)
    plt.plot(x_range, kde_in(x_range), color='black')
# r2py:entity:rug
    plt.plot(x_inA, np.zeros_like(x_inA), '|', color='black')

if len(x_not_inA) > 1:
# r2py:entity:points
    kde_out = gaussian_kde(x_not_inA)
    plt.plot(x_range, kde_out(x_range), color='blue')
# r2py:entity:rug_1
    plt.plot(x_not_inA, np.zeros_like(x_not_inA), '|', color='blue')
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
print(create_resample(oilType, times=2))

# createFolds(oilType, 10)
# r2py:entity:createFolds
print(create_folds(oilType, k=10))

# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
print(create_folds(oilType, k=5, list_out=False))

# createFolds(rnorm(21))
# r2py:entity:createFolds_2
print(create_folds(np.random.normal(0, 1, 21), k=10))

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

# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = np.sort(np.random.choice(letters[0:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
print(folds)

# lapply(folds, function(x, y) table(y[x]), y = groups)
# r2py:entity:lapply
res_lapply = []
for f_name in sorted(folds.keys()):
    indices = np.array(folds[f_name]) - 1
    subset_groups = np.array(groups)[indices]
    res_lapply.append(pd.Series(subset_groups).value_counts().sort_index())

for i, tab in enumerate(res_lapply):
    print(f"Fold{i+1}:")
    print(tab)