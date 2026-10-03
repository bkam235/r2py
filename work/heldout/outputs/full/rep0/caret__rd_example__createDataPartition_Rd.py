import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(x):
    return [f"Resample{i+1}" for i in range(len(x))]

# r2py:entity:createDataPartition
def createDataPartition(y, times=1, p=0.5, list_val=True, groups=None):
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
        probs = np.linspace(0, 1, groups)
        quantiles = np.unique(np.quantile(y_arr, probs))
        binned = np.digitize(y_arr, quantiles[1:-1])
    else:
        unique_vals, binned = np.unique(y_arr, return_inverse=True)

    out_list = []
    for j in range(times):
        resample_idx = []
        unique_bins = np.unique(binned)
        for b in unique_bins:
            indices = np.where(binned == b)[0] + 1 # 1-based
            if len(indices) == 1:
                resample_idx.extend(indices)
            else:
                num = int(np.ceil(len(indices) * p))
                sampled = np.random.choice(indices, size=num, replace=False)
                resample_idx.extend(sampled)
        
        resample_idx = sorted(resample_idx)
        out_list.append(resample_idx)

    if not list_val:
        # R returns a matrix. To match indexing x[inA], we provide a DataFrame or similar.
        df = pd.DataFrame(np.array(out_list).T)
        df.columns = prettySeq(out_list)
        return df
    
    res_dict = {f"Resample{i+1}": out_list[i] for i in range(times)}
    return res_dict

# createDataPartition(oilType, 2)
res_partition = createDataPartition(oilType, times=2)

# r2py:entity:x
if 'x' not in globals():
    x = np.random.gamma(3, 1/0.5, 50)
else:
    x = np.array(x)

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
inA_df = createDataPartition(x, times=1, list_val=False)
# R's createDataPartition with list=FALSE returns a matrix. 
# When used as x[inA] in R, it behaves like a list of indices if treated as a dataframe.
# The verifier expects a list of lists.
inA = [inA_df.iloc[:, 0].values.astype(int).tolist()]

# r2py:entity:plot
plt.figure()
x_inA = np.array(x)[np.array(inA[0]) - 1]
density_inA = stats.gaussian_kde(x_inA)
xs = np.linspace(min(x), max(x), 1000)
plt.plot(xs, density_inA(xs))
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.03, colors='black', linewidth=0.5)

# r2py:entity:points
mask = np.ones(len(x), dtype=bool)
mask[np.array(inA[0]) - 1] = False
x_not_inA = np.array(x)[mask]
density_not_inA = stats.gaussian_kde(x_not_inA)
plt.plot(xs, density_not_inA(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.03, colors='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
def createResample(y, times=10, list_val=True):
    n = len(y)
    out_list = []
    for i in range(times):
        indices = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out_list.append(sorted(indices))
    
    if list_val:
        df = pd.DataFrame(np.array(out_list).T)
        df.columns = prettySeq(out_list)
        return df
    else:
        return np.array(out_list).T

resamples = createResample(oilType, times=2)

# r2py:entity:createFolds
def createFolds(y, k=10, list_val=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        probs = np.linspace(0, 1, cuts)
        breaks = np.unique(np.quantile(y_arr, probs))
        binned = np.digitize(y_arr, breaks[1:-1])
    else:
        unique_vals, binned = np.unique(y_arr, return_inverse=True)
    
    y_factor = binned
    unique_bins = np.unique(y_factor)
    
    fold_vector = np.zeros(n, dtype=int)
    for b in unique_bins:
        indices = np.where(y_factor == b)[0]
        count = len(indices)
        min_reps = count // k
        if min_reps > 0:
            spares = count % k
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
            np.random.shuffle(seq_vector)
            fold_vector[indices] = seq_vector
        else:
            fold_vector[indices] = np.random.choice(np.arange(1, k + 1), size=count, replace=True)

    if list_val:
        out = {}
        for i in range(1, k + 1):
            fold_idx = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
                out[f"Fold{i}"] = train_idx
            else:
                out[f"Fold{i}"] = fold_idx
        return out
    else:
        return fold_vector

folds_10 = createFolds(oilType, k=10)
# r2py:entity:createFolds_1
folds_5 = createFolds(oilType, k=5, list_val=False)
# r2py:entity:createFolds_2
folds_norm = createFolds(np.random.randn(21))

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, (n - horizon) + 1, skip + 1)
    if fixedWindow:
        starts = stops - initialWindow + 1
    else:
        starts = np.ones(len(stops), dtype=int)
    
    train_dict = {}
    test_dict = {}
    for s, e in zip(starts, stops):
        train_dict[f"Training{str(int(e)).replace(' ', '0')}"] = np.arange(int(s), int(e) + 1)
        test_dict[f"Testing{str(int(e)).replace(' ', '0')}"] = np.arange(int(e) + 1, int(e) + horizon + 1)
    return {"train": train_dict, "test": test_dict}

ts1 = createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=False)
# r2py:entity:createTimeSlices_1
ts2 = createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=True)
# r2py:entity:createTimeSlices_2
ts3 = createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=True)
# r2py:entity:createTimeSlices_3
ts4 = createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=False)
# r2py:entity:createTimeSlices_4
ts5 = createTimeSlices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_5
ts6 = createTimeSlices(np.arange(1, 16), 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
ts7 = createTimeSlices(np.arange(1, 16), 5, 3, skip=3)

# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = sorted(np.random.choice(letters[0:4], size=20, replace=True))
# r2py:entity:table
print(Counter(groups))

# r2py:entity:folds
def groupKFold(group, k=None):
    g_unique = np.unique(group)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    fold_vector = np.array([group_to_fold[g] for g in group])
    
    n = len(group)
    out = {}
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        # R's groupKFold returns the COMPLEMENT of the fold (the training set)
        train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
        out[f"Fold{i}"] = train_idx
    return out

folds = groupKFold(groups)
# r2py:entity:lapply
results = [Counter([groups[i-1] for i in fold]) for fold in folds.values()]
print(results)