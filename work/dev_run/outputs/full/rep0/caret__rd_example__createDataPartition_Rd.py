# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma, gaussian_kde

def pretty_seq(x):
    return [f"Resample{i+1}" for i in range(len(x))]

# r2py:entity:inA
def create_data_partition(y, times=1, p=0.5, list_out=True, groups=None):
    y_arr = np.array(y)
    n = len(y_arr)
    if n < 2:
        raise ValueError("y must have at least 2 data points")
    
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2

    # Stratification logic
    if np.issubdtype(y_arr.dtype, np.number):
        # Bin continuous data into 'groups' strata
        probs = np.linspace(0, 1, groups + 1)
        breaks = np.unique(np.quantile(y_arr, probs))
        # Using pandas cut to mimic R cut
        y_binned = pd.cut(y_arr, bins=breaks, include_lowest=True)
    else:
        y_binned = y_arr

    results = []
    indices = np.arange(1, n + 1)
    df = pd.DataFrame({'y': y_binned, 'index': indices})

    for _ in range(times):
        sampled_indices = []
        for name, group in df.groupby('y', observed=False):
            group_indices = group['index'].values
            if len(group_indices) == 1:
                sampled_indices.append(group_indices)
            else:
                num = int(np.ceil(len(group_indices) * p))
                sampled = np.random.choice(group_indices, size=num, replace=False)
                sampled_indices.append(sampled)
        
        resample = np.sort(np.concatenate(sampled_indices))
        results.append(resample)

    if not list_out:
        # R returns a matrix with columns named Resample1, ...
        # We return a numpy array where columns are resamples
        res_mat = np.column_stack(results)
        return res_mat
    
    res_dict = {f"Resample{i+1}": res for i, res in enumerate(results)}
    return res_dict

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    n = len(y)
    indices = np.arange(1, n + 1)
    results = []
    for _ in range(times):
        res = np.sort(np.random.choice(indices, size=n, replace=True))
        results.append(res)
    
    if not list_out:
        return np.column_stack(results)
    
    res_dict = {f"Resample{i+1}": res for i, res in enumerate(results)}
    return res_dict

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        probs = np.linspace(0, 1, cuts + 1)
        breaks = np.unique(np.quantile(y_arr, probs))
        y_binned = pd.cut(y_arr, bins=breaks, include_lowest=True)
    else:
        y_binned = y_arr
    
    if k < n:
        y_binned = pd.Series(y_binned).astype(str)
        counts = y_binned.value_counts()
        fold_vector = np.zeros(n, dtype=int)
        
        for cls, count in counts.items():
            idx = np.where(y_binned == cls)[0]
            min_reps = count // k
            spares = count % k
            
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            
            np.random.shuffle(seq_vector)
            fold_vector[idx] = seq_vector
    else:
        fold_vector = np.arange(1, n + 1)

    indices = np.arange(1, n + 1)
    if list_out:
        out = {}
        for i in range(1, k + 1):
            # R: split(seq_along(y), foldVector)
            # Foldi contains indices where fold_vector == i
            fold_idx = indices[fold_vector == i].tolist()
            if return_train:
                # return complementary set
                out[f"Fold{i}"] = indices[fold_vector != i].tolist()
            else:
                out[f"Fold{i}"] = fold_idx
        return out
    else:
        return fold_vector

# r2py:entity:createTimeSlices
def create_time_slices(y, initial_window, horizon=1, fixed_window=True, skip=0):
    n = len(y)
    stops = np.arange(initial_window, (n - horizon) + 1, skip + 1)
    
    train_slices = []
    test_slices = []
    
    for stop in stops:
        start = (stop - initial_window + 1) if fixed_window else 1
        train_slices.append(list(range(start, stop + 1)))
        test_slices.append(list(range(stop + 1, stop + horizon + 1)))
    
    train_dict = {f"Training{str(stop).replace(' ', '0')}": s for stop, s in zip(stops, train_slices)}
    test_dict = {f"Testing{str(stop).replace(' ', '0')}": s for stop, s in zip(stops, test_slices)}
    
    return {'train': train_dict, 'test': test_dict}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group_arr = np.array(group)
    u_groups = np.unique(group_arr)
    m = len(u_groups)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    # R: g_folds <- sample(k, size = m, replace = TRUE)
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    group_to_fold = dict(zip(u_groups, g_folds))
    
    fold_assignments = np.array([group_to_fold[g] for g in group_arr])
    indices = np.arange(1, len(group_arr) + 1)
    
    # R groupKFold returns the complementary indices
    out = {}
    # To ensure we have keys Fold1, Fold2... even if some weren't sampled
    # but R's split(..., g_folds[match(...)]) only creates folds that exist
    unique_assigned_folds = np.unique(fold_assignments)
    for i, fold_val in enumerate(unique_assigned_folds, 1):
        out[f"Fold{i}"] = indices[fold_assignments != fold_val].tolist()
    return out

# r2py:entity:data
# data(oil) handled by shim

# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
createDataPartition_res = create_data_partition(oilType, times=2)

# r2py:entity:x
# x handled by shim

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA_raw = create_data_partition(x, times=1, list_out=False)
inA = inA_raw[:, 0]

# plot(density(x[inA]))
# rug(x[inA])
x_arr = np.array(x)
x_inA = x_arr[inA.astype(int) - 1]
x_not_inA = x_arr[np.setdiff1d(np.arange(1, len(x_arr)+1), inA) - 1]

# r2py:entity:plot
plt.figure()
density_inA = gaussian_kde(x_inA)
x_range = np.linspace(min(x_arr), max(x_arr), 100)
plt.plot(x_range, density_inA(x_range))
# r2py:entity:rug
plt.plot(x_inA, np.zeros_like(x_inA), '|', color='black', markerfacecolor='black', markeredgecolor='black')

# points(density(x[-inA]), type = "l", col = 4)
# r2py:entity:points
density_not_inA = gaussian_kde(x_not_inA)
plt.plot(x_range, density_not_inA(x_range), color='blue')

# rug(x[-inA], col = 4)
# r2py:entity:rug_1
plt.plot(x_not_inA, np.zeros_like(x_not_inA), '|', color='blue', markerfacecolor='blue', markeredgecolor='blue')
plt.show()

# r2py:entity:createResample
createResample_res = create_resample(oilType, times=2)

# r2py:entity:createFolds
createFolds_res = create_folds(oilType, k=10)

# r2py:entity:createFolds_1
createFolds_res_1 = create_folds(oilType, k=5, list_out=True)

# r2py:entity:createFolds_2
createFolds_res_2 = create_folds(np.random.randn(21), k=10)

# r2py:entity:createTimeSlices
createTimeSlices_res = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False)

# r2py:entity:createTimeSlices_1
createTimeSlices_res_1 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False)
# r2py:entity:createTimeSlices_2
createTimeSlices_res_2 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=True)
# r2py:entity:createTimeSlices_3
createTimeSlices_res_3 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=True)
# r2py:entity:createTimeSlices_4
createTimeSlices_res_4 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=False)

# r2py:entity:createTimeSlices_5
createTimeSlices_res_5 = create_time_slices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_6
createTimeSlices_res_6 = create_time_slices(np.arange(1, 16), 5, 3, skip=2)
createTimeSlices_res_7 = create_time_slices(np.arange(1, 16), 5, 3, skip=3)

# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = np.sort(np.random.choice(letters[:4], size=20, replace=True))

# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)

# r2py:entity:lapply
for fold_name, indices in folds.items():
    # R: table(y[x]) where y=groups, x=indices
    subset = np.array(groups)[np.array(indices) - 1]
    print(f"${fold_name}")
    print(pd.Series(subset).value_counts().sort_index())