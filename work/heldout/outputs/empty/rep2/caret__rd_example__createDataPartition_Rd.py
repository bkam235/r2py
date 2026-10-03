# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/caret__rd_example__createDataPartition_Rd.py'
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
    n = len(x) if isinstance(x, (list, np.ndarray, pd.Series)) else x
    if isinstance(n, int):
        return [f"Resample{i+1}" for i in range(n)]
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
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        qs = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups + 1)))
        # To emulate R's cut with include.lowest=TRUE
        y_bins = np.digitize(y_arr, qs[1:-1])
    else:
        y_bins = pd.factorize(y_arr)[0]

    out_list = []
    for j in range(times):
        all_sampled_indices = []
        unique_bins = np.unique(y_bins)
        for b in unique_bins:
            bin_indices = np.where(y_bins == b)[0] + 1 # 1-based indices
            if len(bin_indices) == 1:
                sampled = bin_indices
            else:
                num = int(np.ceil(len(bin_indices) * p))
                sampled = np.random.choice(bin_indices, size=num, replace=False)
            all_sampled_indices.extend(sampled)
        
        out_list.append(sorted(all_sampled_indices))

    if not list_out:
        # R: matrix(unlist(out), ncol = times)
        data_matrix = np.array(out_list).T
        df = pd.DataFrame(data_matrix, columns=prettySeq(times))
        return df
    
    res_dict = {f"Resample{i+1}": out_list[i] for i in range(times)}
    return res_dict

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    y_arr = np.array(y)
    n = len(y_arr)
    indices = np.arange(1, n + 1)
    out_list = []
    for j in range(times):
        resample = np.random.choice(indices, size=n, replace=True)
        out_list.append(sorted(resample.tolist()))
    
    if list_out:
        df = pd.DataFrame(out_list).T
        df.columns = prettySeq(times)
        return df
    else:
        return np.array(out_list).T

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts)))
        y_bins = np.digitize(y_arr, breaks[1:-1])
    else:
        y_bins = pd.factorize(y_arr)[0]
    
    if k < n:
        unique_bins = np.unique(y_bins)
        fold_vector = np.zeros(n, dtype=int)
        for b in unique_bins:
            idx = np.where(y_bins == b)[0]
            num_in_class = len(idx)
            min_reps = num_in_class // k
            
            if min_reps > 0:
                spares = num_in_class % k
                seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seq_vector)
                fold_vector[idx] = seq_vector
            else:
                fold_vector[idx] = np.random.choice(np.arange(1, k + 1), size=num_in_class, replace=True)
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
        return fold_vector

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, (n - horizon) + 1, skip + 1)
    
    train_list = []
    test_list = []
    
    for stop in stops:
        start = (stop - initialWindow + 1) if fixedWindow else 1
        train_list.append(list(range(int(start), int(stop) + 1)))
        test_list.append(list(range(int(stop) + 1, int(stop + horizon) + 1)))
    
    train_dict = {f"Training{int(stop)}": t for stop, t in zip(stops, train_list)}
    test_dict = {f"Testing{int(stop)}": t for stop, t in zip(stops, test_list)}
    
    return {"train": train_dict, "test": test_dict}

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
    fold_assignments = g_folds[g_inverse]
    
    n = len(group_arr)
    out = {}
    for i in range(1, k + 1):
        fold_members = np.where(fold_assignments == i)[0] + 1
        # R: lapply(out, function(z) seq_along(group)[-z])
        train_indices = np.setdiff1d(np.arange(1, n + 1), fold_members)
        out[f"Fold{i}"] = train_indices.tolist()
    return out

# --- Execute Script ---

# r2py:entity:data
# data(oil) handled by shim: oilType is provided
# r2py:entity:createDataPartition
print(createDataPartition(oilType, times=2))

# r2py:entity:x
# x <- rgamma(50, 3, .5) handled by shim: x is provided
# r2py:entity:inA
inA_res = createDataPartition(x, times=1, list_out=False)
inA = inA_res.iloc[:, 0].values.astype(int)

# Plotting
x_np = np.array(x)
x_inA = x_np[inA - 1]
x_not_inA = np.delete(x_np, inA - 1)

# r2py:entity:plot
plt.figure()
kde_inA = stats.gaussian_kde(x_inA)
xs = np.linspace(min(x_np), max(x_np), 200)
plt.plot(xs, kde_inA(xs), color='black')
# r2py:entity:rug
plt.plot(x_inA, np.zeros_like(x_inA), '|', color='black', markeredgewidth=1)

# r2py:entity:points
kde_not_inA = stats.gaussian_kde(x_not_inA)
plt.plot(xs, kde_not_inA(xs), color='blue')
# r2py:entity:rug_1
plt.plot(x_not_inA, np.zeros_like(x_not_inA), '|', color='blue', markeredgewidth=1)
plt.show()

# r2py:entity:createResample
print(createResample(oilType, times=2))
# r2py:entity:createFolds
print(createFolds(oilType, k=10))
# r2py:entity:createFolds_1
print(createFolds(oilType, k=5, list_out=False))
# r2py:entity:createFolds_2
print(createFolds(np.random.normal(0, 1, 21)))

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
letters_subset = letters[:4]
groups = sorted(np.random.choice(letters_subset, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds = groupKFold(groups)
# r2py:entity:lapply
for f_name, indices in folds.items():
    fold_groups = [groups[i-1] for i in indices]
    print(pd.Series(fold_groups).value_counts().sort_index())