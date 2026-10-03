import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def prettySeq(x):
    # R's prettySeq: paste("Resample", gsub(" ", "0", format(seq(along.with_val= x))), sep = "")
    n = len(x) if hasattr(x, '__len__') else 1
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
        qs = np.unique(np.quantile(y_arr, np.linspace(0, 1, groups)))
        y_fact = np.digitize(y_arr, qs[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]

    resamples = []
    for j in range(times):
        sample_idx = []
        unique_groups = np.unique(y_fact)
        for g in unique_groups:
            g_idx = np.where(y_fact == g)[0]
            if len(g_idx) == 1:
                sample_idx.extend(g_idx)
            else:
                num = int(np.ceil(len(g_idx) * p))
                sample_idx.extend(np.random.choice(g_idx, size=num, replace=False))
        resamples.append(np.sort(np.array(sample_idx)) + 1)

    if not list_out:
        data = np.array(resamples).T
        df = pd.DataFrame(data, columns=prettySeq(resamples))
        return df
    else:
        # R returns a list of vectors
        return {f"Resample{i+1}": resamples[i].tolist() for i in range(times)}

# r2py:entity:createResample
def createResample(y, times=10, list_out=True):
    y_arr = np.array(y)
    n = len(y_arr)
    resamples = []
    for j in range(times):
        idx = np.sort(np.random.choice(np.arange(1, n + 1), size=n, replace=True))
        resamples.append(idx)
    
    if list_out:
        # R: as.data.frame(out, stringsAsFactors = TRUE); names(out) <- prettySeq(out)
        data = np.array(resamples).T
        df = pd.DataFrame(data, columns=prettySeq(resamples))
        return df
    else:
        data = np.array(resamples).T
        df = pd.DataFrame(data, columns=prettySeq(resamples))
        return df

# r2py:entity:createFolds
def createFolds(y, k=10, list_out=True, returnTrain=False):
    y_arr = np.array(y)
    n = len(y_arr)
    
    if np.issubdtype(y_arr.dtype, np.number):
        cuts = max(2, min(5, n // k))
        qs = np.unique(np.quantile(y_arr, np.linspace(0, 1, cuts)))
        y_fact = np.digitize(y_arr, qs[1:-1])
    else:
        y_fact = pd.factorize(y_arr)[0]

    if k < n:
        fold_vector = np.zeros(n, dtype=int)
        unique_vals = np.unique(y_fact)
        for val in unique_vals:
            idx = np.where(y_fact == val)[0]
            num_in_class = len(idx)
            min_reps = num_in_class // k
            spares = num_in_class % k
            if min_reps > 0:
                seq_vec = np.repeat(np.arange(1, k + 1), min_reps)
                if spares > 0:
                    seq_vec = np.concatenate([seq_vec, np.random.choice(np.arange(1, k + 1), spares, replace=False)])
                np.random.shuffle(seq_vec)
                fold_vector[idx] = seq_vec
            else:
                fold_vector[idx] = np.random.choice(np.arange(1, k + 1), num_in_class, replace=True)
    else:
        fold_vector = np.arange(1, n + 1)

    if list_out:
        out = {}
        # R: split(seq(along.with_val= y), foldVector)
        for i in range(1, k + 1):
            fold_idx = np.where(fold_vector == i)[0] + 1
            if returnTrain:
                train_idx = np.setdiff1d(np.arange(1, n + 1), fold_idx)
                out[f"Fold{i}"] = train_idx.tolist()
            else:
                out[f"Fold{i}"] = fold_idx.tolist()
        return out
    return fold_vector

# r2py:entity:createTimeSlices
def createTimeSlices(y, initialWindow, horizon=1, fixedWindow=True, skip=0):
    n = len(y)
    stops = np.arange(initialWindow, (n - horizon) + 1, skip + 1)
    train = {}
    test = {}
    for stop in stops:
        start = stop - initialWindow + 1 if fixedWindow else 1
        train_seq = list(range(int(start), int(stop) + 1))
        test_seq = list(range(int(stop) + 1, int(stop + horizon) + 1))
        stop_str = str(int(stop)).replace(" ", "0")
        train[f"Training{stop_str}"] = train_seq
        test[f"Testing{stop_str}"] = test_seq
    return {"train": train, "test": test}

# r2py:entity:folds
def groupKFold(group, k=None):
    group_arr = np.array(group)
    g_unique = np.unique(group_arr)
    m = len(g_unique)
    if k is None:
        k = m
    if k > m:
        raise ValueError(f"`k` should be less than {m}")
    
    g_folds = np.random.choice(k, size=m, replace=True) + 1
    group_to_fold = {val: fold for val, fold in zip(g_unique, g_folds)}
    fold_vector = np.array([group_to_fold[g] for g in group_arr])
    
    out = {}
    # R: split(seq_along(group), g_folds[match(group, g_unique)])
    # and then lapply(out, function(z) seq_along(group)[-z])
    # This means the output is the training set for each fold
    for i in range(1, k + 1):
        fold_idx = np.where(fold_vector == i)[0] + 1
        train_idx = np.setdiff1d(np.arange(1, len(group_arr) + 1), fold_idx)
        out[f"Fold{i}"] = train_idx.tolist()
    return out

# --- Execution ---

# r2py:entity:createDataPartition
createDataPartition(oilType, times=2)

# r2py:entity:x
if 'x' not in globals():
    np.random.seed(None)
    x = np.random.gamma(shape=3, scale=2.0, size=50)

# r2py:entity:inA
inA_res = createDataPartition(x, times=1, list_out=True)
inA = inA_res["Resample1"] # R: inA <- createDataPartition(x, list = FALSE) actually returns a vector of indices if list=FALSE

# r2py:entity:plot
plt.figure()
x_vals = np.array(x)
x_inA_vals = x_vals[np.array(inA) - 1]
kde_inA = gaussian_kde(x_inA_vals)
xs = np.linspace(min(x_vals), max(x_vals), 100)
plt.plot(xs, kde_inA(xs))
# r2py:entity:rug
plt.vlines(x_inA_vals, ymin=0, ymax=0.01, colors='black', linewidth=0.5)

# r2py:entity:points
x_not_inA_idx = np.setdiff1d(np.arange(1, len(x_vals) + 1), np.array(inA))
x_not_inA_vals = x_vals[x_not_inA_idx - 1]
kde_not_inA = gaussian_kde(x_not_inA_vals)
plt.plot(xs, kde_not_inA(xs), color='blue')
# r2py:entity:rug_1
plt.vlines(x_not_inA_vals, ymin=0, ymax=0.01, colors='blue', linewidth=0.5)
plt.show()

# r2py:entity:createResample
createResample(oilType, times=2)
# r2py:entity:createFolds
createFolds(oilType, k=10)
# r2py:entity:createFolds_1
createFolds(oilType, k=5, list_out=False)
# r2py:entity:createFolds_2
createFolds(np.random.randn(21))

# r2py:entity:createTimeSlices
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
groups = np.sort(np.random.choice(letters[0:4], size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts().sort_index())
# r2py:entity:folds
folds = groupKFold(groups)

# r2py:entity:lapply
for fold_name, indices in folds.items():
    fold_groups = [groups[i-1] for i in indices]
    print(pd.Series(fold_groups).value_counts().sort_index())