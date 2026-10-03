# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma, norm
import scipy.stats as stats

def prettySeq(x):
    # R: paste("Resample", gsub(" ", "0", format(seq(along.with_val= x))), sep = "")
    # x can be a list or an integer indicating the number of columns
    n = len(x) if hasattr(x, '__len__') else x
    return [f"Resample{i+1}" for i in range(n)]

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
        probs = np.linspace(0, 1, groups)
        breaks = np.unique(np.quantile(y_arr, probs))
        # Mimic R's cut: include_lowest=True
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]

    out_list = []
    for j in range(times):
        resample_indices = []
        unique_groups = np.unique(y_fact)
        for g in unique_groups:
            group_idx = np.where(y_fact == g)[0]
            if len(group_idx) == 1:
                resample_indices.append(group_idx[0])
            else:
                num = int(np.ceil(len(group_idx) * p))
                sampled = np.random.choice(group_idx, size=num, replace=False)
                resample_indices.extend(sampled)
        
        # R indices are 1-based, sorted
        sorted_indices = sorted([i + 1 for i in resample_indices])
        out_list.append(sorted_indices)
    
    if not list_out:
        # R: matrix(unlist(out), ncol = times)
        # Note: R's unlist on a list of varying lengths is complex; 
        # however, createDataPartition in R often produces balanced samples.
        # If lengths differ, R's matrix() would recycle or error. 
        # We assume balanced for the matrix conversion.
        data = np.array(out_list).T
        df = pd.DataFrame(data, columns=prettySeq(times))
        return df
    
    res_dict = {f"Resample{i+1}": out_list[i] for i in range(times)}
    return res_dict

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    out_list = []
    for j in range(times):
        indices = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out_list.append(sorted(indices.tolist()))
    
    if not list_out:
        data = np.array(out_list).T
        df = pd.DataFrame(data, columns=prettySeq(times))
        return df
    
    # R: as.data.frame(out, stringsAsFactors = TRUE)
    data = np.array(out_list).T
    df = pd.DataFrame(data, columns=prettySeq(times))
    return df

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = n // k
        if cuts < 2: cuts = 2
        if cuts > 5: cuts = 5
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts)))
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]
    
    if k < n:
        unique_classes = np.unique(y_fact)
        foldVector = np.zeros(n, dtype=int)
        for cls in unique_classes:
            idx = np.where(y_fact == cls)[0]
            num_in_cls = len(idx)
            min_reps = num_in_cls // k
            if min_reps > 0:
                spares = num_in_cls % k
                seqVector = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seqVector = np.concatenate([seqVector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seqVector)
                foldVector[idx] = seqVector - 1
            else:
                foldVector[idx] = np.random.choice(np.arange(0, k), size=num_in_cls, replace=True)
    else:
        foldVector = np.arange(n)
    
    if not list_out:
        return foldVector + 1

    indices = np.arange(1, n + 1)
    unique_folds = np.unique(foldVector)
    out = {}
    for i, f_val in enumerate(sorted(unique_folds), 1):
        if returnTrain:
            out[f"Fold{i}"] = indices[foldVector != f_val].tolist()
        else:
            out[f"Fold{i}"] = indices[foldVector == f_val].tolist()
    return out

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, n - horizon + 1, skip + 1)
    
    train = []
    test = []
    for stop in stops:
        start = stop - initialWindow + 1 if fixedWindow else 1
        train.append(list(range(start, stop + 1)))
        test.append(list(range(stop + 1, stop + horizon + 1)))
    
    nums = [str(s) for s in stops]
    train_dict = {f"Training{nums[i]}": train[i] for i in range(len(nums))}
    test_dict = {f"Testing{nums[i]}": test[i] for i in range(len(nums))}
    
    return {"train": train_dict, "test": test_dict}

# r2py:entity:folds
def groupKFold(group, k=None):
    group_arr = np.array(group)
    g_unique = np.unique(group_arr)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(np.arange(1, k + 1), size=m, replace=True)
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    fold_assignment = np.array([group_to_fold[g] for g in group_arr])
    
    n = len(group_arr)
    indices = np.arange(1, n + 1)
    
    final_out = {}
    # R's groupKFold creates k folds based on the sampled fold IDs
    # and then returns the indices NOT in that fold (Training set)
    for i in range(1, k + 1):
        z_indices = indices[fold_assignment == i]
        train_idx = np.setdiff1d(indices, z_indices)
        final_out[f"Fold{i}"] = train_idx.tolist()
        
    return final_out

# --- Execution ---
# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
res_dp = createDataPartition(oilType, 2)
for k, v in res_dp.items():
    print(f"${k}")
    print(np.array(v))
print()

# x <- rgamma(50, 3, .5)
# r2py:entity:x
x_val = np.array(x) 

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA_df = createDataPartition(x_val, 1, p=0.7, list_out=False)
inA = inA_df.iloc[:, 0].values.astype(int)

# Plotting
# r2py:entity:plot
plt.figure(figsize=(8, 6))
x_inA = x_val[inA - 1]
density_inA = stats.gaussian_kde(x_inA)
xs = np.linspace(min(x_val), max(x_val), 200)
plt.plot(xs, density_inA(xs), color='black')
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.01, colors='black', linewidth=0.5)

not_inA = np.setdiff1d(np.arange(1, len(x_val)+1), inA)
x_not_inA = x_val[not_inA - 1]
density_not_inA = stats.gaussian_kde(x_not_inA)
# r2py:entity:points
plt.plot(xs, density_not_inA(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.01, colors='blue', linewidth=0.5)
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
res_rs = createResample(oilType, 2)
print(res_rs)
print()

# createFolds(oilType, 10)
# r2py:entity:createFolds
print(createFolds(oilType, 10))
print()

# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
print(createFolds(oilType, 5, list_out=False))
print()

# createFolds(rnorm(21))
# r2py:entity:createFolds_2
print(createFolds(norm.rvs(size=21)))
print()

# createTimeSlices(1:9, 5, 1, fixedWindow = FALSE)
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
groups = np.sort(np.random.choice(letters[0:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())
# r2py:entity:folds
folds = groupKFold(groups)
# r2py:entity:lapply
res_lapply = {name: pd.Series(groups)[np.array(indices)-1].value_counts().sort_index() 
       for name, indices in folds.items()}
for name, tab in res_lapply.items():
    print(f"${name}")
    print(tab)