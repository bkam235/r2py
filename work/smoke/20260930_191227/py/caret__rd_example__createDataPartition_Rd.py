import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import random

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_191227/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(x):
    # R: paste("Resample", gsub(" ", "0", format(seq(along.with = x))), sep = "")
    # Since x is often a list or range, we use the length.
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
        
    # Handle numeric y (stratification via cut)
    if np.issubdtype(y_arr.dtype, np.number):
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        probs = np.linspace(0, 1, groups + 1)
        breaks = np.unique(np.quantile(y_arr, probs))
        # digitize mimics cut
        y_bins = np.digitize(y_arr, breaks[1:-1])
    else:
        # Factor/Character: use unique categories
        y_bins = pd.factorize(y_arr)[0]

    out_list = []
    for j in range(times):
        resample = []
        unique_bins = np.unique(y_bins)
        for bin_val in unique_bins:
            bin_idx = np.where(y_bins == bin_val)[0] + 1
            if len(bin_idx) == 1:
                resample.append(bin_idx[0])
            else:
                num = int(np.ceil(len(bin_idx) * p))
                # R sample() without replace
                resample.extend(np.random.choice(bin_idx, size=num, replace=False))
        out_list.append(sorted(resample))
        
    if not list_out:
        return np.array(out_list).T
    
    return {f"Resample{i+1}": out_list[i] for i in range(times)}

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    indices = np.arange(1, n + 1)
    out_cols = []
    for j in range(times):
        # R: sample(index, size = length(index), replace = TRUE)
        resample = np.random.choice(indices, size=n, replace=True)
        out_cols.append(sorted(resample))
    
    if list_out:
        df = pd.DataFrame(np.array(out_cols).T, columns=prettySeq(range(times)))
        # R: attributes(out) <- NULL removes df attributes, but keep it as DataFrame
        return df
    else:
        return np.array(out_cols).T

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts + 1)))
        y_bins = np.digitize(y_arr, breaks[1:-1])
    else:
        y_bins = pd.factorize(y_arr)[0]
        
    fold_vector = np.zeros(n, dtype=int)
    unique_bins = np.unique(y_bins)
    
    for bin_val in unique_bins:
        bin_idx = np.where(y_bins == bin_val)[0]
        num_in_class = len(bin_idx)
        
        min_reps = num_in_class // k
        if min_reps > 0:
            spares = num_in_class % k
            seq_vector = list(range(1, k + 1)) * min_reps
            if spares > 0:
                seq_vector.extend(np.random.choice(range(1, k + 1), size=spares, replace=False))
            
            np.random.shuffle(seq_vector)
            fold_vector[bin_idx] = seq_vector
        else:
            fold_vector[bin_idx] = np.random.choice(range(1, k + 1), size=num_in_class, replace=True)
            
    if list_out:
        out = {}
        for f in range(1, k + 1):
            indices = np.where(fold_vector == f)[0] + 1
            if returnTrain:
                out[f"Fold{f}"] = np.setdiff1d(np.arange(1, n + 1), indices)
            else:
                out[f"Fold{f}"] = indices
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    y_len = len(y)
    # R: seq(initialWindow, (length(y) - horizon), by = skip + 1)
    stops = np.arange(initialWindow, (y_len - horizon) + 1, skip + 1)
    
    train = {}
    test = {}
    
    for stop in stops:
        start = (stop - initialWindow + 1) if fixedWindow else 1
        train[f"Training{stop}"] = np.arange(start, stop + 1)
        test[f"Testing{stop}"] = np.arange(stop + 1, stop + horizon + 1)
    
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
        
    g_folds = np.random.choice(range(1, k + 1), size=m, replace=True)
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    fold_vector = np.array([group_to_fold[g] for g in group])
    
    out = {}
    n = len(group)
    for f in range(1, k + 1):
        fold_idx = np.where(fold_vector == f)[0] + 1
        # R: lapply(out, function(z) seq_along(group)[-z]) -> return complements
        train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
        out[f"Fold{f}"] = train_idx
    return out

# --- Execution ---

# r2py:entity:createDataPartition
print(createDataPartition(oilType, times=2))

# rgamma(50, 3, .5) -> shape=3, rate=0.5 -> scale=1/0.5=2
# r2py:entity:x
x = np.random.gamma(3, 2, 50)

# r2py:entity:inA
inA = createDataPartition(x, times=1, list_out=False)

# r2py:entity:plot
plt.figure()
inA_indices = inA.flatten().astype(int)
x_inA = np.array(x)[inA_indices - 1]
kde_inA = gaussian_kde(x_inA)
xs = np.linspace(min(x), max(x), 200)
plt.plot(xs, kde_inA(xs), color='black')
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.01, colors='black', linewidth=0.5)

# r2py:entity:points
inA_set = set(inA_indices)
x_not_inA = np.array([val for i, val in enumerate(x, 1) if i not in inA_set])
kde_not_inA = gaussian_kde(x_not_inA)
plt.plot(xs, kde_not_inA(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.01, colors='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
print(createResample(oilType, times=2))
# r2py:entity:createFolds
print(createFolds(oilType, k=10))
# r2py:entity:createFolds_1
print(createFolds(oilType, k=5, list_out=False))
# r2py:entity:createFolds_2
print(createFolds(np.random.randn(21), k=10))

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
random.seed(131)
# r2py:entity:groups
sample_letters = letters[0:4]
groups = sorted(np.random.choice(sample_letters, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = groupKFold(groups)
# r2py:entity:lapply
for f_name, indices in folds.items():
    sub_groups = [groups[i-1] for i in indices]
    print(pd.Series(sub_groups).value_counts().sort_index())