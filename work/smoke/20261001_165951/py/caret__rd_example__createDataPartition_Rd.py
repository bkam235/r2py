# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/caret__rd_example__createDataPartition_Rd.py'
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
def createDataPartition(y, times=1, p=0.5, list_out=True, groups=None):
    y = np.array(y)
    n = len(y)
    if n < 2:
        raise ValueError("y must have at least 2 data points")
    
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2
        
    if np.issubdtype(y.dtype, np.number):
        # Bin numeric data into groups
        quantiles = np.unique(np.quantile(y, np.linspace(0, 1, groups + 1)))
        y_fact = np.digitize(y, quantiles[1:-1])
    else:
        y_fact = pd.factorize(y)[0]

    resamples = {}
    indices = np.arange(n)
    
    for j in range(times):
        sample_indices = []
        unique_classes = np.unique(y_fact)
        for cls in unique_classes:
            cls_indices = indices[y_fact == cls]
            num_to_sample = int(np.ceil(len(cls_indices) * p))
            sampled = np.random.choice(cls_indices, size=num_to_sample, replace=False)
            sample_indices.extend(sampled)
        
        resamples[f"Resample{j+1}"] = sorted([int(i + 1) for i in sample_indices])
    
    if not list_out:
        # Convert to matrix-like DataFrame
        df = pd.DataFrame(resamples)
        return df
    return resamples

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    indices = np.arange(1, n + 1)
    resamples = {}
    for j in range(times):
        resamples[f"Resample{j+1}"] = sorted(np.random.choice(indices, size=n, replace=True).tolist())
    
    if list_out:
        return pd.DataFrame(resamples)
    return pd.DataFrame(resamples)

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y = np.array(y)
    n = len(y)
    if np.issubdtype(y.dtype, np.number):
        cuts = max(2, min(5, n // k))
        breaks = np.unique(np.quantile(y, np.linspace(0, 1, cuts + 1)))
        y_fact = np.digitize(y, breaks[1:-1])
    else:
        y_fact = pd.factorize(y)[0]

    fold_vector = np.zeros(n, dtype=int)
    unique_classes = np.unique(y_fact)
    for cls in unique_classes:
        cls_indices = np.where(y_fact == cls)[0]
        num_in_class = len(cls_indices)
        min_reps = num_in_class // k
        spares = num_in_class % k
        
        if min_reps > 0:
            seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
            if spares > 0:
                seq_vector = np.append(seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False))
            np.random.shuffle(seq_vector)
            fold_vector[cls_indices] = seq_vector
        else:
            fold_vector[cls_indices] = np.random.choice(np.arange(1, k + 1), num_in_class, replace=True)

    if list_out:
        out = {}
        for i in range(1, k + 1):
            out[f"Fold{i}"] = np.where(fold_vector == i)[0] + 1
        if returnTrain:
            all_idx = np.arange(1, n + 1)
            out = {k_fold: np.setdiff1d(all_idx, v) for k_fold, v in out.items()}
        return out
    return fold_vector + 1

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, n - horizon + 1, skip + 1)
    
    train = {}
    test = {}
    
    for i, stop in enumerate(stops):
        if fixedWindow:
            start = stop - initialWindow + 1
        else:
            start = 1
        
        train_idx = list(range(int(start), int(stop) + 1))
        test_idx = list(range(int(stop) + 1, int(stop + horizon) + 1))
        
        name = f"Training{str(stop).replace(' ', '0')}"
        test_name = f"Testing{str(stop).replace(' ', '0')}"
        train[name] = train_idx
        test[test_name] = test_idx
        
    return {"train": train, "test": test}

# r2py:entity:folds
def groupKFold(group, k=None):
    group = np.array(group)
    g_unique = np.unique(group)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
        
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    
    # Map each group to a fold
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    member_folds = np.array([group_to_fold[g] for g in group])
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        # R: lapply(out, function(z) seq_along(group)[-z]) -> return training set
        val_indices = np.where(member_folds == i)[0] + 1
        train_indices = np.setdiff1d(np.arange(1, n + 1), val_indices)
        out[f"Fold{i}"] = train_indices.tolist()
    return out

# --- Execution ---

# suppressPackageStartupMessages(library(caret))
# data(oil)
# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
res_partition = createDataPartition(oilType, times=2)
print(res_partition)

# x <- rgamma(50, 3, .5)
# (x is provided by data shim)

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA = createDataPartition(x, times=1, list_out=False)
inA_vec = inA.iloc[:, 0].values.astype(int)

# Plotting
# plot(density(x[inA]))
# rug(x[inA])
x_arr = np.array(x)
# R indexing is 1-based, so subtract 1
inA_indices = inA_vec - 1
x_inA = x_arr[inA_indices]
# r2py:entity:plot
kde_inA = gaussian_kde(x_inA)
x_plot = np.linspace(min(x_inA), max(x_inA), 100)
plt.plot(x_plot, kde_inA(x_plot))
# r2py:entity:rug
plt.plot(x_inA, np.zeros_like(x_inA), '|', color='black', markersize=10)

# points(density(x[-inA]), type = "l", col = 4)
# rug(x[-inA], col = 4)
not_inA_indices = np.setdiff1d(np.arange(len(x_arr)), inA_indices)
x_not_inA = x_arr[not_inA_indices]
# r2py:entity:points
kde_not_inA = gaussian_kde(x_not_inA)
x_plot_not = np.linspace(min(x_not_inA), max(x_not_inA), 100)
plt.plot(x_plot_not, kde_not_inA(x_plot_not), color='blue')
# r2py:entity:rug_1
plt.plot(x_not_inA, np.zeros_like(x_not_inA), '|', color='blue', markersize=10)
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
resample_out = createResample(oilType, times=2)
print(resample_out)

# createFolds(oilType, 10)
# r2py:entity:createFolds
folds_10 = createFolds(oilType, k=10)
print(folds_10)

# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
folds_5 = createFolds(oilType, k=5, list_out=False)
print(folds_5)

# createFolds(rnorm(21))
# r2py:entity:createFolds_2
x_norm = np.random.normal(0, 1, 21)
folds_norm = createFolds(x_norm)
print(folds_norm)

# createTimeSlices
# r2py:entity:createTimeSlices
ts1 = createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=False)
print(ts1)
# r2py:entity:createTimeSlices_1
ts2 = createTimeSlices(np.arange(1, 10), 5, 1, fixedWindow=True)
print(ts2)
# r2py:entity:createTimeSlices_2
ts3 = createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=True)
print(ts3)
# r2py:entity:createTimeSlices_3
ts4 = createTimeSlices(np.arange(1, 10), 5, 3, fixedWindow=False)
print(ts4)

# r2py:entity:createTimeSlices_4
ts5 = createTimeSlices(np.arange(1, 16), 5, 3)
print(ts5)
# r2py:entity:createTimeSlices_5
ts6 = createTimeSlices(np.arange(1, 16), 5, 3, skip=2)
print(ts6)
# r2py:entity:createTimeSlices_6
ts7 = createTimeSlices(np.arange(1, 16), 5, 3, skip=3)
print(ts7)

# set.seed(131)
# r2py:entity:set.seed
np.random.seed(131)
# groups <- sort(sample(letters[1:4], size = 20, replace = TRUE))
# r2py:entity:groups
groups = sorted(np.random.choice(letters[0:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# folds <- groupKFold(groups)
# r2py:entity:folds
folds = groupKFold(groups)
print(folds)

# lapply(folds, function(x, y) table(y[x]), y = groups)
# r2py:entity:lapply
groups_arr = np.array(groups)
for fold_name, idxs in folds.items():
    # idxs are 1-based
    fold_data = groups_arr[np.array(idxs) - 1]
    print(f"{fold_name}:")
    print(pd.Series(fold_data).value_counts().sort_index())