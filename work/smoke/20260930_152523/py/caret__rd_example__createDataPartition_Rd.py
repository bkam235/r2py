# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Helper: prettySeq
def prettySeq(x):
    # R's format(seq) with gsub(" ", "0", ...) basically formats integers
    return [f"Resample{int(i+1)}" for i in range(len(x))]

# r2py:entity:createDataPartition
def createDataPartition(y, times=1, p=0.5, list_out=True, groups=None):
    y = np.array(y)
    n = len(y)
    if n < 2: raise ValueError("y must have at least 2 data points")
    
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2
    
    # Stratification logic
    if np.issubdtype(y.dtype, np.number):
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        # Use np.nanquantile for safety, though data is usually clean here
        probs = np.linspace(0, 1, groups)
        breaks = np.unique(np.quantile(y, probs))
        # Handle the include.lowest = TRUE logic of R's cut
        y_bins = np.digitize(y, breaks[1:-1])
    else:
        # For factors/characters, R uses table() to identify classes
        y_bins = pd.factorize(y)[0]
        
    out = []
    for j in range(times):
        resample_indices = []
        unique_bins = np.unique(y_bins)
        for b in unique_bins:
            idx = np.where(y_bins == b)[0] + 1
            if len(idx) == 1:
                resample_indices.extend(idx)
            else:
                num = int(np.ceil(len(idx) * p))
                # R's sample(idx, size=num) is random choice without replacement
                resample_indices.extend(np.random.choice(idx, size=num, replace=False))
        out.append(sorted(resample_indices))
        
    if not list_out:
        res = np.array(out).T
        return pd.DataFrame(res, columns=prettySeq(range(times)))
    
    res_dict = {f"Resample{i+1}": out[i] for i in range(times)}
    return res_dict

# R: createDataPartition(oilType, 2)
createDataPartition_res = createDataPartition(oilType, 2)
print(createDataPartition_res)

# r2py:entity:x
x = np.array(x)

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA_df = createDataPartition(x, times=1, p=0.5, list_out=False)
inA = inA_df.iloc[:, 0].values.astype(int)

# Plotting logic
# r2py:entity:plot
plt.figure(figsize=(8, 6))
# plot(density(x[inA]))
x_in = x[inA - 1]
kde_in = stats.gaussian_kde(x_in)
xs = np.linspace(min(x), max(x), 200)
plt.plot(xs, kde_in(xs), color='black')
# r2py:entity:rug
# rug(x[inA])
plt.vlines(x_in, ymin=0, ymax=0.03, color='black', linewidth=0.5)

# r2py:entity:points
# points(density(x[-inA]), type = "l", col = 4)
mask_out = np.ones(len(x), dtype=bool)
mask_out[inA - 1] = False
x_out = x[mask_out]
kde_out = stats.gaussian_kde(x_out)
plt.plot(xs, kde_out(xs), color='blue') # col=4 is blue
# r2py:entity:rug_1
# rug(x[-inA], col = 4)
plt.vlines(x_out, ymin=0, ymax=0.03, color='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    y = np.array(y)
    n = len(y)
    out = []
    for i in range(times):
        # R: sort(sample(index, size = length(index), replace = TRUE))
        out.append(sorted(np.random.choice(np.arange(1, n + 1), size=n, replace=True)))
    
    if list_out:
        df = pd.DataFrame(np.array(out).T, columns=prettySeq(range(times)))
        return df
    return np.array(out).T

createResample(oilType, 2)

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        probs = np.linspace(0, 1, cuts)
        breaks = np.unique(np.quantile(y, probs))
        y_bins = np.digitize(y, breaks[1:-1])
    else:
        y_bins = pd.factorize(y)[0]
    
    fold_vector = np.zeros(n, dtype=int)
    unique_bins = np.unique(y_bins)
    for b in unique_bins:
        idx = np.where(y_bins == b)[0]
        num_in_class = len(idx)
        min_reps = num_in_class // k
        spares = num_in_class % k
        
        if min_reps > 0:
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            np.random.shuffle(seq_vector)
            fold_vector[idx] = seq_vector
        else:
            fold_vector[idx] = np.random.choice(np.arange(1, k + 1), num_in_class, replace=True)
            
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_indices = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices)
                out[f"Fold{i}"] = train_indices
            else:
                out[f"Fold{i}"] = fold_indices
        return out
    return fold_vector

createFolds(oilType, 10)
# r2py:entity:createFolds_1
createFolds(oilType, 5, list_out=False)
# r2py:entity:createFolds_2
createFolds(np.random.randn(21))

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, (n - horizon) + 1, skip + 1)
    if fixedWindow:
        starts = stops - initialWindow + 1
    else:
        starts = np.ones(len(stops), dtype=int)
        
    train = []
    test = []
    for s, e in zip(starts, stops):
        train.append(np.arange(s, e + 1))
        test.append(np.arange(e + 1, e + horizon + 1))
        
    res = {'train': train, 'test': test}
    return res

createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=False)
# r2py:entity:createTimeSlices_1
createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=True)
# r2py:entity:createTimeSlices_2
createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=True)
# r2py:entity:createTimeSlices_3
createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=False)
# r2py:entity:createTimeSlices_4
createTimeSlices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_5
createTimeSlices(np.arange(1, 16), 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
createTimeSlices(np.arange(1, 16), 5, 3, skip=3)

# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
# R: groups <- sort(sample(letters[1:4], size = 20, replace = TRUE))
groups = np.sort(np.random.choice(letters[:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
def groupKFold(group, k=None):
    group = np.array(group)
    g_unique = np.unique(group)
    m = len(g_unique)
    if k is None: k = m
    if k > m: raise ValueError(f"k should be less than {m}")
    
    # R: g_folds <- sample(k, size = m, replace = TRUE)
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    # R: out <- split(seq_along(group), g_folds[match(group, g_unique)])
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    folds_vector = np.array([group_to_fold[g] for g in group])
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        fold_indices = np.where(folds_vector == i)[0] + 1
        # R: lapply(out, function(z) seq_along(group)[-z])
        # This returns the complement (training set)
        train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices)
        out[f"Fold{i}"] = train_indices
    return out

folds = groupKFold(groups)

# r2py:entity:lapply
for fold_name, indices in folds.items():
    fold_groups = groups[indices - 1]
    print(pd.Series(fold_groups).value_counts().sort_index())