# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma

def pretty_seq(n):
    return [f"Resample{i+1}" for i in range(n)]

# r2py:entity:createDataPartition
def create_data_partition(y, times=1, p=0.5, list_out=True, groups=None):
    y = np.array(y)
    n = len(y)
    if groups is None:
        groups = min(5, n)
    
    # Logic for numeric vs factor
    if np.issubdtype(y.dtype, np.number):
        # Simple binning for numeric
        bins = np.unique(np.quantile(y, np.linspace(0, 1, groups + 1)))
        digitized = np.digitize(y, bins[1:-1])
    else:
        digitized = pd.factorize(y)[0]
    
    out = {}
    for j in range(times):
        resample_indices = []
        unique_bins = np.unique(digitized)
        for b in unique_bins:
            idx = np.where(digitized == b)[0]
            num = int(np.ceil(len(idx) * p))
            resample_indices.extend(np.random.choice(idx, size=num, replace=False))
        
        # R indices are 1-based, and returned sorted
        sorted_indices = sorted([i + 1 for i in resample_indices])
        out[f"Resample{j+1}"] = sorted_indices
        
    if not list_out:
        df = pd.DataFrame(out)
        return df
    return out

# r2py:entity:createResample
def create_resample(y, times=10, list_out=True):
    y = np.array(y)
    n = len(y)
    out = {}
    for j in range(times):
        # Bootstrap sampling (replace=True)
        indices = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out[f"Resample{j+1}"] = sorted(indices)
    
    if not list_out:
        return pd.DataFrame(out)
    return out

# r2py:entity:createFolds
def create_folds(y, k=10, list_out=True, return_train=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = max(2, min(5, n // k))
        breaks = np.unique(np.quantile(y, np.linspace(0, 1, cuts + 1)))
        digitized = np.digitize(y, breaks[1:-1])
    else:
        digitized = pd.factorize(y)[0]
    
    fold_vector = np.zeros(n, dtype=int)
    unique_bins = np.unique(digitized)
    for b in unique_bins:
        idx = np.where(digitized == b)[0]
        num_in_class = len(idx)
        min_reps = num_in_class // k
        spares = num_in_class % k
        
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
                # Indices NOT in the fold
                train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
                out[f"Fold{i}"] = train_idx.tolist()
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
    
    for i, stop in enumerate(stops):
        if fixed_window:
            start = stop - initial_window + 1
        else:
            start = 1
        
        # R: seq(start, stop)
        train[f"Training{stop}"] = list(range(start, stop + 1))
        # R: seq(stop + 1, stop + horizon)
        test[f"Testing{stop}"] = list(range(stop + 1, stop + horizon + 1))
        
    return {"train": train, "test": test}

# r2py:entity:folds
def group_k_fold(group, k=None):
    group = np.array(group)
    g_unique = np.unique(group)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    
    # Map groups to folds
    group_to_fold = {g: f for g, f in zip(g_unique, g_folds)}
    fold_vector = np.array([group_to_fold[g] for g in group])
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        # groupKFold in caret returns the TRAINING indices (excluding the fold)
        fold_idx = np.where(fold_vector == i)[0] + 1
        train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
        out[f"Fold{i}"] = train_idx.tolist()
    return out

# --- Execution ---

# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
print(create_data_partition(oilType, times=2))

# x <- rgamma(50, 3, .5)
# R shape=3, rate=0.5 => scipy shape=3, scale=1/0.5=2.0
# r2py:entity:x
x = gamma.rvs(3, scale=2.0, size=50)

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA = create_data_partition(x, times=1, list_out=False).iloc[:, 0].values

# Plotting
plt.figure(figsize=(8, 6))
# R: plot(density(x[inA]))
# Note: inA contains 1-based indices.
x_inA = x[inA - 1]
x_not_inA = np.delete(x, inA - 1)

import scipy.stats as stats
# r2py:entity:plot
kde_in = stats.gaussian_kde(x_inA)
plt.plot(np.linspace(min(x), max(x), 100), kde_in(np.linspace(min(x), max(x), 100)), color='black')
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.01, colors='black', linewidth=0.5)

# points(density(x[-inA]), type = "l", col = 4)
# r2py:entity:points
kde_out = stats.gaussian_kde(x_not_inA)
plt.plot(np.linspace(min(x), max(x), 100), kde_out(np.linspace(min(x), max(x), 100)), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.01, colors='blue', linewidth=0.5)

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
print(create_folds(np.random.randn(21), k=10)) # k defaults to 10 in R

# createTimeSlices calls
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

# Set seed and groupKFold
# r2py:entity:set.seed
np.random.seed(131)
# R letters[1:4] are 'a', 'b', 'c', 'd'
# r2py:entity:groups
groups = np.sort(np.random.choice(['a', 'b', 'c', 'd'], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = group_k_fold(groups)
# lapply(folds, function(x, y) table(y[x]), y = groups)
# r2py:entity:lapply
for fold_name, indices in folds.items():
    # R indices are 1-based
    fold_groups = groups[np.array(indices) - 1]
    print(f"{fold_name}:")
    print(pd.Series(fold_groups).value_counts().sort_index())