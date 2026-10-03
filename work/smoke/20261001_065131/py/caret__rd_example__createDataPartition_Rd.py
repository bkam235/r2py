import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma
from collections import Counter
import scipy.stats as stats

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(n):
    return [f"Resample{i+1}" for i in range(n)]

# r2py:entity:createDataPartition
def createDataPartition(y, times=1, p=0.5, list_out=True, groups=None):
    y_arr = np.array(y)
    n = len(y_arr)
    if groups is None:
        groups = min(5, n)
    if groups < 2:
        groups = 2
    
    if np.issubdtype(y_arr.dtype, np.number):
        breaks = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups)))
        y_fact = np.digitize(y_arr, breaks[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]
    
    out = []
    for _ in range(times):
        indices = np.arange(n)
        sample_indices = []
        unique_classes = np.unique(y_fact)
        for cls in unique_classes:
            cls_indices = indices[y_fact == cls]
            if len(cls_indices) == 1:
                sample_indices.append(cls_indices)
            else:
                num = int(np.ceil(len(cls_indices) * p))
                sample_indices.append(np.random.choice(cls_indices, size=num, replace=False))
        
        res = np.sort(np.concatenate(sample_indices))
        out.append(res + 1) # 1-based

    if not list_out:
        mat = np.array(out).T
        df = pd.DataFrame(mat, columns=prettySeq(times))
        return df
    
    res_dict = {prettySeq(times)[i]: out[i] for i in range(times)}
    return res_dict

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    y_arr = np.array(y)
    n = len(y_arr)
    out = {}
    for i in range(times):
        res = np.sort(np.random.choice(np.arange(1, n + 1), size=n, replace=True))
        out[f"Resample{i+1}"] = res
    
    if list_out:
        return pd.DataFrame(out)
    return np.array(list(out.values())).T

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
        fold_vector = np.zeros(n, dtype=int)
        unique_classes = np.unique(y_fact)
        for cls in unique_classes:
            idx = np.where(y_fact == cls)[0]
            num_in_cls = len(idx)
            min_reps = num_in_cls // k
            spares = num_in_cls % k
            
            if min_reps > 0:
                seq_vec = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vec = np.concatenate([seq_vec, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seq_vec)
                fold_vector[idx] = seq_vec
            else:
                fold_vector[idx] = np.random.choice(np.arange(1, k + 1), num_in_cls, replace=True)
    else:
        fold_vector = np.arange(1, n + 1)
            
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_idx = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                train_idx = np.delete(np.arange(1, n + 1), fold_idx - 1)
                out[f"Fold{i}"] = train_idx
            else:
                out[f"Fold{i}"] = fold_idx
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, n - horizon + 1, skip + 1)
    
    train_list = []
    test_list = []
    
    for stop in stops:
        if fixedWindow:
            start = stop - initialWindow + 1
        else:
            start = 1
        train_list.append(np.arange(start, stop + 1))
        test_list.append(np.arange(stop + 1, stop + horizon + 1))
    
    train_dict = {f"Training{str(stop).replace(' ', '0')}": train_list[i] for i, stop in enumerate(stops)}
    test_dict = {f"Testing{str(stop).replace(' ', '0')}": test_list[i] for i, stop in enumerate(stops)}
    
    return {"train": train_dict, "test": test_dict}

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
    group_to_fold = dict(zip(g_unique, g_folds))
    fold_vector = np.array([group_to_fold[g] for g in group])
    
    out = {}
    n = len(group)
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        train_idx = np.delete(np.arange(1, n + 1), fold_idx - 1)
        out[f"Fold{i}"] = train_idx
    return out

# Logic execution
# r2py:entity:createDataPartition
res_partition = createDataPartition(oilType, times=2)
print(res_partition)

# r2py:entity:x
x = gamma.rvs(a=3, scale=1/0.5, size=50)
# r2py:entity:inA
inA_df = createDataPartition(x, times=1, p=0.5, list_out=False)
inA = inA_df.iloc[:, 0].values.astype(int)

# r2py:entity:plot
plt.figure()
x_inA = np.array(x)[inA - 1]
kde_inA = stats.gaussian_kde(x_inA)
x_vals = np.linspace(min(x), max(x), 200)
plt.plot(x_vals, kde_inA(x_vals), color='black')
# r2py:entity:rug
plt.vlines(x_inA, 0, 0.03, colors='black', linewidth=0.5)

# r2py:entity:points
mask_not_inA = np.ones(len(x), dtype=bool)
mask_not_inA[inA - 1] = False
x_not_inA = np.array(x)[mask_not_inA]
kde_not_inA = stats.gaussian_kde(x_not_inA)
plt.plot(x_vals, kde_not_inA(x_vals), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA, 0, 0.03, colors='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
res_resample = createResample(oilType, times=2)
print(res_resample)

# r2py:entity:createFolds
folds_10 = createFolds(oilType, k=10)
print(folds_10)

# r2py:entity:createFolds_1
folds_5_no_list = createFolds(oilType, k=5, list_out=False)
print(folds_5_no_list)

# r2py:entity:createFolds_2
folds_norm = createFolds(np.random.randn(21), k=10)
print(folds_norm)

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
groups = np.sort(np.random.choice(letters, size=20, replace=True))
# r2py:entity:table
print(Counter(groups))

# r2py:entity:folds
folds = groupKFold(groups)
print(folds)

# r2py:entity:lapply
for fold_name, train_idx in folds.items():
    subset = np.array(groups)[train_idx - 1]
    print(f"{fold_name}:")
    print(Counter(subset))