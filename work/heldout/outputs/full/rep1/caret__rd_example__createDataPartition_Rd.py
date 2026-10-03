# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def prettySeq(x):
    # R: paste("Resample", gsub(" ", "0", format(seq(along.with_val= x))), sep = "")
    n = len(x) if isinstance(x, (list, np.ndarray)) else x
    return [f"Resample{i+1}" for i in range(n)]

# r2py:entity:createDataPartition
def createDataPartition(y, times=1, p=0.5, list_out=True, groups=None):
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
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]

    out = {}
    for j in range(times):
        resample = []
        unique_vals = np.unique(y_fact)
        for val in unique_vals:
            idx_val = np.where(y_fact == val)[0] + 1
            if len(idx_val) == 1:
                resample.extend(idx_val)
            else:
                num = int(np.ceil(len(idx_val) * p))
                resample.extend(np.random.choice(idx_val, size=num, replace=False))
        
        out[f"Resample{j+1}"] = sorted(resample)

    if not list_out:
        # Matrix output: columns are resamples
        res_list = [out[f"Resample{i+1}"] for i in range(times)]
        return np.array(res_list).T
    return out

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    out = {}
    for j in range(times):
        # R: sort(sample(index, size = length(index), replace = TRUE))
        resample = sorted(np.random.choice(np.arange(1, n + 1), size=n, replace=True))
        out[f"Resample{j+1}"] = resample
    
    if not list_out:
        return np.array([out[f"Resample{i+1}"] for i in range(times)]).T
    return out

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts + 1)))
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]
    
    if k < n:
        fold_vector = np.zeros(n, dtype=int)
        unique_vals = np.unique(y_fact)
        for val in unique_vals:
            idx_val = np.where(y_fact == val)[0]
            num_in_class = len(idx_val)
            min_reps = num_in_class // k
            
            if min_reps > 0:
                spares = num_in_class % k
                seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seq_vector)
                fold_vector[idx_val] = seq_vector
            else:
                fold_vector[idx_val] = np.random.choice(np.arange(1, k + 1), size=num_in_class, replace=True)
    else:
        fold_vector = np.arange(1, n + 1)

    if not list_out:
        return fold_vector
    
    out = {}
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        if returnTrain:
            out[f"Fold{i}"] = np.setdiff1d(np.arange(1, n + 1), fold_idx).tolist()
        else:
            out[f"Fold{i}"] = fold_idx.tolist()
    return out

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, n - horizon + 1, skip + 1)
    
    train = {}
    test = {}
    for stop in stops:
        start = stop - initialWindow + 1 if fixedWindow else 1
        train[f"Training{stop}"] = list(range(int(start), int(stop) + 1))
        test[f"Testing{stop}"] = list(range(int(stop) + 1, int(stop + horizon) + 1))
        
    return {"train": train, "test": test}

# r2py:entity:folds
def groupKFold(group, k=None):
    group = np.array(group)
    g_unique = np.unique(group)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"k should be less than {m}")
    
    # R: g_folds <- sample(k, size = m, replace = TRUE)
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    
    # match(group, g_unique)
    group_to_fold = {g: f for g, f in zip(g_unique, g_folds)}
    fold_vector = np.array([group_to_fold[g] for g in group])
    
    out = {}
    # R: split(seq_along(group), g_folds[match(group, g_unique)])
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        # R: lapply(out, function(z) seq_along(group)[-z]) -> returns training set
        train_idx = np.setdiff1d(np.arange(1, len(group) + 1), fold_idx)
        out[f"Fold{i}"] = train_idx.tolist()
    return out

# Execution
# r2py:entity:createDataPartition
res_dp = createDataPartition(oilType, times=2)
print(res_dp)

# r2py:entity:x
# x <- rgamma(50, 3, .5)
# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA = createDataPartition(x, times=1, list_out=False)

# Plotting
# r2py:entity:plot
plt.figure()
x_arr = np.array(x)
inA_flat = np.array(inA).flatten()
x_inA = x_arr[inA_flat - 1]
x_not_inA = np.delete(x_arr, inA_flat - 1)

# Density plots approximate R density()
density_inA = stats.gaussian_kde(x_inA)
density_not_inA = stats.gaussian_kde(x_not_inA)
xi = np.linspace(min(x_arr), max(x_arr), 200)
plt.plot(xi, density_inA(xi), color='black')
# r2py:entity:points
plt.plot(xi, density_not_inA(xi), color='blue') 
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.03, colors='black', linewidth=0.5)
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.03, colors='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
print(createResample(oilType, times=2))
# r2py:entity:createFolds
print(createFolds(oilType, k=10))
# r2py:entity:createFolds_1
print(createFolds(oilType, k=5, list_out=False))
# r2py:entity:createFolds_2
print(createFolds(np.random.randn(21)))

# r2py:entity:createTimeSlices
print(createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=False))
# r2py:entity:createTimeSlices_1
print(createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=True))
# r2py:entity:createTimeSlices_2
print(createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=True))
# r2py:entity:createTimeSlices_3
print(createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=False))
# r2py:entity:createTimeSlices_4
print(createTimeSlices(np.arange(1, 16), 5, 3))
# r2py:entity:createTimeSlices_5
print(createTimeSlices(np.arange(1, 16), 5, 3, skip=2))
# r2py:entity:createTimeSlices_6
print(createTimeSlices(np.arange(1, 16), 5, 3, skip=3))

# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = np.sort(np.random.choice(letters[:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = groupKFold(groups)
# r2py:entity:lapply
for fold_name, indices in folds.items():
    fold_groups = groups[np.array(indices) - 1]
    print(pd.Series(fold_groups).value_counts().sort_index())