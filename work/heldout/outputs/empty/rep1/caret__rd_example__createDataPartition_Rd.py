import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, gaussian_kde

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(x):
    return [f"Resample{i+1}" for i in range(len(x))]

# r2py:entity:createDataPartition
def createDataPartition(y, times=1, p=0.5, list_out=True, groups=None):
    if groups is None:
        groups = min(5, len(y))
    
    y_arr = np.array(y)
    n = len(y_arr)
    if n < 2:
        raise ValueError("y must have at least 2 data points")
    if groups < 2:
        groups = 2
        
    if np.issubdtype(y_arr.dtype, np.number):
        # R: cut(y, unique(quantile(y, probs = seq(0, 1, length.out = groups))), include.lowest = TRUE)
        quantiles = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups + 1)))
        y_binned = np.digitize(y_arr, quantiles[1:-1])
    else:
        y_binned = pd.factorize(y_arr)[0]

    out = {}
    for j in range(times):
        resample = []
        unique_bins = np.unique(y_binned)
        for b in unique_bins:
            indices = np.where(y_binned == b)[0]
            if len(indices) == 1:
                resample.extend(indices)
            else:
                num = int(np.ceil(len(indices) * p))
                sampled = np.random.choice(indices, size=num, replace=False)
                resample.extend(sampled)
        
        resample = sorted([int(i + 1) for i in resample])
        out[f"Resample{j+1}"] = resample
    
    if not list_out:
        df = pd.DataFrame(out)
        return df
    return out

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    n = len(y)
    out = {}
    for j in range(times):
        resample = np.random.choice(np.arange(1, n + 1), size=n, replace=True)
        out[f"Resample{j+1}"] = sorted(resample.tolist())
    
    if not list_out:
        return pd.DataFrame(out)
    return out

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = max(2, min(5, n // k))
        quantiles = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts + 1)))
        y_binned = np.digitize(y_arr, quantiles[1:-1])
    else:
        y_binned = pd.factorize(y_arr)[0]
    
    if k < n:
        unique_bins = np.unique(y_binned)
        fold_vector = np.zeros(n, dtype=int)
        for b in unique_bins:
            indices = np.where(y_binned == b)[0]
            num_in_class = len(indices)
            min_reps = num_in_class // k
            spares = num_in_class % k
            
            if min_reps > 0:
                seq_vector = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vector = np.concatenate([seq_vector, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seq_vector)
                fold_vector[indices] = seq_vector
            else:
                fold_vector[indices] = np.random.choice(np.arange(1, k + 1), num_in_class, replace=True)
    else:
        fold_vector = np.arange(1, n + 1)
        
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_indices = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                out[f"Fold{i}"] = [idx for idx in range(1, n + 1) if idx not in fold_indices]
            else:
                out[f"Fold{i}"] = fold_indices.tolist()
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, n - horizon + 1, skip + 1)
    
    train_slices = {}
    test_slices = {}
    
    for stop in stops:
        if fixedWindow:
            start = stop - initialWindow + 1
        else:
            start = 1
        
        train_slices[f"Training{stop}"] = list(range(int(start), int(stop) + 1))
        test_slices[f"Testing{stop}"] = list(range(int(stop) + 1, int(stop) + horizon + 1))
        
    return {"train": train_slices, "test": test_slices}

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
    
    mapping = {val: fold for val, fold in zip(g_unique, g_folds)}
    fold_vector = np.array([mapping[g] for g in group_arr])
    
    out = {}
    n = len(group_arr)
    for i in range(1, k + 1):
        fold_indices = np.where(fold_vector == i)[0] + 1
        all_indices = np.arange(1, n + 1)
        train_indices = [int(idx) for idx in all_indices if idx not in fold_indices]
        out[f"Fold{i}"] = train_indices
    return out

# --- Main Execution ---

# createDataPartition(oilType, 2)
# r2py:entity:createDataPartition
dp_result = createDataPartition(oilType, times=2)
print(dp_result)

# x <- rgamma(50, 3, .5)
# r2py:entity:x
x = gamma.rvs(a=3, scale=1/0.5, size=50)

# inA <- createDataPartition(x, list = FALSE)
# r2py:entity:inA
inA_df = createDataPartition(x, times=1, list_out=False)
inA = inA_df.iloc[:, 0].values.astype(int)

# Plotting
plt.figure(figsize=(10, 6))
x_inA = np.array([x[i-1] for i in inA])
x_not_inA = np.array([x[i-1] for i in range(1, 51) if i not in inA])

kde_inA = gaussian_kde(x_inA)
kde_not_inA = gaussian_kde(x_not_inA)

xs = np.linspace(min(x), max(x), 200)
# r2py:entity:plot
plt.plot(xs, kde_inA(xs), color='black')
# r2py:entity:points
plt.plot(xs, kde_not_inA(xs), color='blue')

# r2py:entity:rug
plt.plot(x_inA, np.full_like(x_inA, -0.01), '|', color='black', markersize=10)
# r2py:entity:rug_1
plt.plot(x_not_inA, np.full_like(x_not_inA, -0.01), '|', color='blue', markersize=10)
plt.show()

# createResample(oilType, 2)
# r2py:entity:createResample
print(createResample(oilType, times=2))

# createFolds(oilType, 10)
# r2py:entity:createFolds
print(createFolds(oilType, k=10))

# createFolds(oilType, 5, FALSE)
# r2py:entity:createFolds_1
print(createFolds(oilType, k=5, list_out=False))

# createFolds(rnorm(21))
# r2py:entity:createFolds_2
print(createFolds(np.random.normal(0, 1, 21)))

# createTimeSlices
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

# Groups logic
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups_sample = np.random.choice(letters[0:4], size=20, replace=True)
groups = sorted(groups_sample)
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())

# r2py:entity:folds
folds_group = groupKFold(groups)
print(folds_group)

# r2py:entity:lapply
for fold_name, indices in folds_group.items():
    selected_groups = [groups[i-1] for i in indices]
    print(f"{fold_name}:")
    print(pd.Series(selected_groups).value_counts().sort_index())