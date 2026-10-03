import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def pretty_seq(n_items, prefix="Resample"):
    return [f"{prefix}{i+1}" for i in range(n_items)]

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
        # Quantile-based grouping for continuous
        quantiles = np.unique(np.quantile(y, np.linspace(0, 1, groups + 1)))
        y_grouped = np.digitize(y, quantiles[1:-1])
    else:
        y_grouped = y

    unique_vals, counts = np.unique(y_grouped, return_counts=True)
    
    resamples = []
    for _ in range(times):
        indices = []
        for val in unique_vals:
            idx = np.where(y_grouped == val)[0]
            num_to_sample = int(np.ceil(len(idx) * p))
            sampled = np.random.choice(idx, size=num_to_sample, replace=False)
            indices.extend(sampled)
        indices.sort()
        # R's indices are 1-based
        resamples.append(np.array(indices) + 1)

    if not list_out:
        mat = np.array(resamples)
        df = pd.DataFrame(mat, index=pretty_seq(times)).T
        return df
    else:
        return {name: resample for name, resample in zip(pretty_seq(times), resamples)}

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    y = np.array(y)
    n = len(y)
    resamples = []
    for _ in range(times):
        # Bootstrap sampling (replace=True)
        resamples.append(np.sort(np.random.choice(np.arange(1, n + 1), size=n, replace=True)))
    
    if list_out:
        return {name: resample for name, resample in zip(pretty_seq(times), resamples)}
    else:
        return pd.DataFrame(np.array(resamples), index=pretty_seq(times)).T

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = max(2, min(5, n // k))
        breaks = np.unique(np.quantile(y, np.linspace(0, 1, cuts + 1)))
        y_grouped = np.digitize(y, breaks[1:-1])
    else:
        y_grouped = y

    unique_vals, counts = np.unique(y_grouped, return_counts=True)
    fold_vector = np.zeros(n, dtype=int)
    
    for val, count in zip(unique_vals, counts):
        idx = np.where(y_grouped == val)[0]
        min_reps = count // k
        spares = count % k
        
        seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
        if spares > 0:
            seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
        
        np.random.shuffle(seq_vector)
        fold_vector[idx] = seq_vector

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
    else:
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
    
    train_dict = {f"Training{str(stop).replace(' ', '0')}": t for stop, t in zip(stops, train)}
    test_dict = {f"Testing{str(stop).replace(' ', '0')}": t for stop, t in zip(stops, test)}
    return {"train": train_dict, "test": test_dict}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group = np.array(group)
    unique_groups = np.unique(group)
    m = len(unique_groups)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    group_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    group_map = {val: fold for val, fold in zip(unique_groups, group_folds)}
    
    fold_vector = np.array([group_map[g] for g in group])
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        out[f"Fold{i}"] = np.setdiff1d(np.arange(1, n + 1), fold_idx)
    return out

# Execution
# r2py:entity:createDataPartition
print(create_data_partition(oilType, 2))

# r2py:entity:x
# x is already in shim, but let's ensure it's a numpy array
x_arr = np.array(x)
# r2py:entity:inA
inA = create_data_partition(x_arr, list_out=False)
# In R, createDataPartition(x, list=FALSE) returns a matrix. 
# The first column is the training set.
inA_vec = inA.iloc[:, 0].values.astype(int) - 1 
not_inA_vec = np.setdiff1d(np.arange(len(x_arr)), inA_vec)

# r2py:entity:plot
plt.figure()
# R's density(x[inA])
density_inA, bins_inA = stats.gaussian_kde(x_arr[inA_vec]).evaluate(np.linspace(min(x_arr), max(x_arr), 1000)), np.linspace(min(x_arr), max(x_arr), 1000)
plt.plot(bins_inA, density_inA, color='black')
# r2py:entity:rug
plt.plot(x_arr[inA_vec], np.zeros_like(x_arr[inA_vec]), '|', color='black')

# r2py:entity:points
density_not_inA, bins_not_inA = stats.gaussian_kde(x_arr[not_inA_vec]).evaluate(np.linspace(min(x_arr), max(x_arr), 1000)), np.linspace(min(x_arr), max(x_arr), 1000)
plt.plot(bins_not_inA, density_not_inA, color='blue')
# r2py:entity:rug_1
plt.plot(x_arr[not_inA_vec], np.zeros_like(x_arr[not_inA_vec]), '|', color='blue')
plt.show()

# r2py:entity:createResample
print(create_resample(oilType, 2))
# r2py:entity:createFolds
print(create_folds(oilType, 10))
# r2py:entity:createFolds_1
print(create_folds(oilType, 5, list_out=False))
# r2py:entity:createFolds_2
print(create_folds(np.random.normal(0, 1, 21)))

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
letters_list = np.array(letters[:4])
groups = np.sort(np.random.choice(letters_list, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
# r2py:entity:lapply
lapply_res = {fold_name: pd.Series(groups[idx - 1]).value_counts().sort_index() for fold_name, idx in folds.items()}
print(lapply_res)