import numpy as np
import pandas as pd
from scipy.stats import gamma, gaussian_kde
import matplotlib.pyplot as plt
from collections import Counter

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(x):
    return [f"Resample{i+1}" for i in range(len(x))]

# r2py:entity:inA
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
        quantiles = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups)))
        y_fact = np.digitize(y_arr, quantiles[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]
    
    out_list = []
    indices = np.arange(1, n + 1)
    
    for j in range(times):
        resample_indices = []
        unique_levels = np.unique(y_fact)
        for level in unique_levels:
            idx_level = indices[y_fact == level]
            if len(idx_level) == 1:
                resample_indices.append(int(idx_level[0]))
            else:
                num = int(np.ceil(len(idx_level) * p))
                resample_indices.extend(np.random.choice(idx_level, size=num, replace=False).tolist())
        
        out_list.append(sorted([int(i) for i in resample_indices]))
    
    if not list_out:
        # R's matrix(unlist(out), ncol = times)
        res_matrix = np.array(out_list).T
        return res_matrix.tolist()
    
    res_dict = {f"Resample{i+1}": out_list[i] for i in range(times)}
    return res_dict

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    indices = np.arange(1, n + 1)
    out_list = []
    for i in range(times):
        resample = sorted(np.random.choice(indices, size=n, replace=True).tolist())
        out_list.append([int(x) for x in resample])
    
    if list_out:
        res_dict = {f"Resample{i+1}": out_list[i] for i in range(times)}
        return res_dict
    else:
        return np.array(out_list).T.tolist()

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = max(2, min(5, n // k))
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts)))
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]
        
    if k < n:
        unique_levels = np.unique(y_fact)
        fold_vector = np.zeros(n, dtype=int)
        for level in unique_levels:
            indices = np.where(y_fact == level)[0]
            num_in_class = len(indices)
            min_reps = num_in_class // k
            spares = num_in_class % k
            
            if min_reps > 0:
                seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), size=spares, replace=False)])
                np.random.shuffle(seq_vector)
                fold_vector[indices] = seq_vector
            else:
                fold_vector[indices] = np.random.choice(np.arange(1, k + 1), size=num_in_class, replace=True)
    else:
        fold_vector = np.arange(1, n + 1)
        
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_indices = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices)
                out[f"Fold{i}"] = train_indices.tolist()
            else:
                out[f"Fold{i}"] = fold_indices.tolist()
        return out
    else:
        return fold_vector.tolist()

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, (n - horizon) + 1, skip + 1)
    
    if fixedWindow:
        starts = stops - initialWindow + 1
    else:
        starts = np.ones(len(stops), dtype=int)
        
    train = {}
    test = {}
    for s, stop in zip(starts, stops):
        train_idx = list(range(int(s), int(stop) + 1))
        test_idx = list(range(int(stop) + 1, int(stop) + horizon + 1))
        label = f"Training{int(stop)}"
        train[label] = train_idx
        test[f"Testing{int(stop)}"] = test_idx
        
    return {"train": train, "test": test}

# r2py:entity:folds
def groupKFold(group, k=None):
    group_arr = np.array(group)
    g_unique, g_inverse = np.unique(group_arr, return_inverse=True)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    fold_vector = g_folds[g_inverse]
    
    out = {}
    n = len(group_arr)
    for i in range(1, k + 1):
        fold_indices = np.where(fold_vector == i)[0] + 1
        # R: lapply(out, function(z) seq_along(group)[-z])
        train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices).tolist()
        out[f"Fold{i}"] = train_indices
    return out

# Execution
oilType = np.array(oilType)
# r2py:entity:createDataPartition
print(createDataPartition(oilType, 2))

# r2py:entity:x
# Use provided x from shim if available, otherwise generate
if 'x' in globals() and isinstance(x, list):
    x = np.array(x)
else:
    x = np.random.gamma(3, 2.0, 50)

# r2py:entity:inA
inA_res = createDataPartition(x, list_out=False)
# inA should be a list of lists (matrix)
inA = inA_res

# For plotting we need a flat index for one resample
flat_inA = np.array(inA).flatten().astype(int) if isinstance(inA, list) else inA.flatten().astype(int)
inA_mask = np.zeros(len(x), dtype=bool)
if flat_inA.size > 0:
    inA_mask[flat_inA - 1] = True

# r2py:entity:plot
plt.figure()
kde_in = gaussian_kde(x[inA_mask])
xs = np.linspace(min(x), max(x), 100)
plt.plot(xs, kde_in(xs))
# r2py:entity:rug
plt.vlines(x[inA_mask], ymin=0, ymax=0.01, color='black', linewidth=0.5)

# r2py:entity:points
kde_out = gaussian_kde(x[~inA_mask])
plt.plot(xs, kde_out(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x[~inA_mask], ymin=0, ymax=0.01, color='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
print(createResample(oilType, 2))
# r2py:entity:createFolds
print(createFolds(oilType, 10))
# r2py:entity:createFolds_1
print(createFolds(oilType, 5, list_out=False))
# r2py:entity:createFolds_2
print(createFolds(np.random.normal(size=21)))

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
letters_list = list('abcdefghijklmnopqrstuvwxyz')
groups = sorted(np.random.choice(letters_list[0:4], size=20, replace=True))
# r2py:entity:table
print(Counter(groups))

# r2py:entity:folds
folds = groupKFold(groups)
# r2py:entity:lapply
for fold_name, indices in folds.items():
    fold_groups = [groups[i-1] for i in indices]
    print(f"{fold_name}: {Counter(fold_groups)}")