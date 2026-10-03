import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma, norm

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def pretty_seq(x):
    return [f"Resample{i+1}" for i in range(len(x))]

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
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        quantiles = np.unique(np.quantile(y, np.linspace(0, 1, groups)))
        # Manually implement R's cut behavior
        y_binned = np.digitize(y, quantiles[1:-1])
    else:
        y_binned = pd.factorize(y)[0]

    out = []
    for j in range(times):
        indices = np.arange(n)
        resample = []
        unique_bins = np.unique(y_binned)
        for b in unique_bins:
            bin_indices = indices[y_binned == b]
            if len(bin_indices) == 1:
                resample.append(bin_indices[0])
            else:
                num = int(np.ceil(len(bin_indices) * p))
                resample.extend(np.random.choice(bin_indices, size=num, replace=False))
        out.append(sorted(np.array(resample) + 1))

    if not list_out:
        return np.array(out).T
    
    return {f"Resample{i+1}": out[i] for i in range(times)}

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    y = np.array(y)
    n = len(y)
    out = []
    for j in range(times):
        # R: sort(sample(index, size = length(index), replace = TRUE))
        resample = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out.append(sorted(resample))
    
    if list_out:
        return {f"Resample{i+1}": out[i] for i in range(times)}
    return np.array(out).T

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = max(2, min(5, n // k))
        quantiles = np.unique(np.quantile(y, np.linspace(0, 1, cuts)))
        y_binned = np.digitize(y, quantiles[1:-1])
    else:
        y_binned = pd.factorize(y)[0]

    if k < n:
        unique_bins = np.unique(y_binned)
        fold_vector = np.zeros(n, dtype=int)
        for b in unique_bins:
            idx = np.where(y_binned == b)[0]
            num_in_class = len(idx)
            min_reps = num_in_class // k
            spares = num_in_class % k
            
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            
            perm = np.random.permutation(seq_vector)
            fold_vector[idx] = perm
    else:
        fold_vector = np.arange(1, n + 1)

    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_indices = np.where(fold_vector == i)[0] + 1
            if return_train:
                out[f"Fold{i}"] = np.setdiff1d(np.arange(1, n + 1), fold_indices)
            else:
                out[f"Fold{i}"] = fold_indices
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def create_time_slices(y, initial_window, horizon=1, fixed_window=True, skip=0):
    n = len(y)
    stops = np.arange(initial_window, (n - horizon) + 1, skip + 1)
    
    train = []
    test = []
    for stop in stops:
        start = (stop - initial_window + 1) if fixed_window else 1
        train.append(np.arange(start, stop + 1))
        test.append(np.arange(stop + 1, stop + horizon + 1))
    
    train_dict = {f"Training{str(s).replace(' ', '0')}": train[i] for i, s in enumerate(stops)}
    test_dict = {f"Testing{str(s).replace(' ', '0')}": test[i] for i, s in enumerate(stops)}
    return {"train": train_dict, "test": test_dict}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group = np.array(group)
    g_unique, g_inverse = np.unique(group, return_inverse=True)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    # R: g_folds <- sample(k, size = m, replace = TRUE)
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    
    # R: split(seq_along(group), g_folds[match(group, g_unique)])
    fold_vector = g_folds[g_inverse]
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        # Find indices belonging to fold i
        fold_indices = np.where(fold_vector == i)[0] + 1
        # R's groupKFold returns the training indices (the complement)
        train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices)
        out[f"Fold{i}"] = train_indices
    return out

# --- Execution ---

# r2py:entity:createDataPartition
# createDataPartition(oilType, 2)
print(create_data_partition(oilType, times=2))

# r2py:entity:x
# x <- rgamma(50, 3, .5)
# Using the shim 'x' if available, otherwise generating
if 'x' not in globals():
    x = gamma.rvs(a=3, scale=1/0.5, size=50)
else:
    x = np.array(x)

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA = create_data_partition(x, times=1, list_out=False).flatten()

# r2py:entity:plot
# Plotting
plt.figure(figsize=(8, 6))
x_arr = np.array(x)
inA_idx = inA - 1
x_inA = x_arr[inA_idx]
pd.Series(x_inA).plot(kind='kde', color='blue')
# r2py:entity:rug
plt.plot(x_inA, np.full_like(x_inA, -0.01), '|', color='blue')

# r2py:entity:points
not_inA_idx = np.setdiff1d(np.arange(len(x)), inA_idx)
x_not_inA = x_arr[not_inA_idx]
pd.Series(x_not_inA).plot(kind='kde', color='blue') 
# r2py:entity:rug_1
plt.plot(x_not_inA, np.full_like(x_not_inA, -0.01), '|', color='blue')
plt.show()

# r2py:entity:createResample
# createResample(oilType, 2)
print(create_resample(oilType, times=2))

# r2py:entity:createFolds
# createFolds(oilType, 10)
print(create_folds(oilType, k=10))
# r2py:entity:createFolds_1
# createFolds(oilType, 5, FALSE)
print(create_folds(oilType, k=5, list_out=False))

# r2py:entity:createFolds_2
# createFolds(rnorm(21))
print(create_folds(norm.rvs(size=21), k=10))

# Time Slices
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

# GroupKFold section
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
letters_subset = letters[0:4]
groups = np.sort(np.random.choice(letters_subset, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
# r2py:entity:lapply
for fold_name, indices in folds.items():
    subset = groups[indices - 1]
    print(f"{fold_name}:")
    print(pd.Series(subset).value_counts().sort_index())