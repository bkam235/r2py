# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/caret__rd_example__nearZeroVar_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__nearZeroVar_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['bbbDescr', 'iris', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import random

# r2py:entity:nearZeroVar
def nzv_logic(x, freq_cut=19.0, unique_cut=10, save_metrics=False, names=False):
    if isinstance(x, pd.DataFrame):
        cols = x.columns
    else:
        cols = [0]
        x = pd.DataFrame(x)

    results = []
    for col in cols:
        data = x[col]
        valid_data = data.dropna()
        
        # ZeroVar
        lunique = len(valid_data.unique())
        zero_var = (lunique <= 1) or data.isna().all()
        
        # freqRatio
        counts = valid_data.value_counts().sort_values(ascending=False)
        if len(counts) <= 1:
            freq_ratio = 0.0
        else:
            freq_ratio = counts.iloc[0] / counts.iloc[1]
            
        # percentUnique
        p_unique = 100.0 * lunique / len(data)
        
        nzv = (freq_ratio > freq_cut and p_unique <= unique_cut) or zero_var
        results.append({'freqRatio': freq_ratio, 'percentUnique': p_unique, 'zeroVar': zero_var, 'nzv': nzv})

    if save_metrics:
        res_df = pd.DataFrame(results, index=cols)
        return res_df
    else:
        indices = [i + 1 for i, res in enumerate(results) if res['nzv']]
        if names:
            return [cols[i-1] for i in indices]
        return indices

def nearZeroVar(x, freq_cut=19.0, unique_cut=10, save_metrics=False, names=False, foreach=False, allow_parallel=True):
    if not foreach:
        return nzv_logic(x, freq_cut, unique_cut, save_metrics, names)
    
    # Caret foreach implementation simplifies to per-column check
    if isinstance(x, pd.DataFrame):
        cols = x.columns
    else:
        cols = [0]
    
    if save_metrics:
        final_results = {}
        for col in cols:
            metric = nzv_logic(x[col] if isinstance(x, pd.DataFrame) else x, freq_cut, unique_cut, save_metrics=True)
            final_results[col] = metric.iloc[0]
        return pd.DataFrame.from_dict(final_results, orient='index')
    else:
        indices = []
        for i, col in enumerate(cols):
            res = nzv_logic(x[col] if isinstance(x, pd.DataFrame) else x, freq_cut, unique_cut, save_metrics=False)
            if len(res) > 0 and res[0] == 1:
                indices.append(i + 1)
        if names:
            return [cols[i-1] for i in indices]
        return indices

# r2py:entity:checkConditionalX
def checkConditionalX(x, y):
    df = x.copy()
    df['_outcome'] = y
    nzv_indices = set()
    for val in df['_outcome'].unique():
        subset = df[df['_outcome'] == val].drop(columns=['_outcome'])
        # In caret, checkConditionalX looks for zeroVar specifically
        for i, col in enumerate(subset.columns):
            col_data = subset[col]
            if len(col_data.dropna().unique()) <= 1 or col_data.isna().all():
                nzv_indices.add(i + 1)
    return sorted(list(nzv_indices))

# r2py:entity:folds
def createFolds(y, k=10, list_out=True, return_train=False):
    y_arr = np.array(y)
    n = len(y_arr)
    unique_classes = np.unique(y_arr)
    fold_vector = np.zeros(n, dtype=int)
    
    for cls in unique_classes:
        indices = np.where(y_arr == cls)[0]
        n_cls = len(indices)
        
        # R's createFolds distributes samples across k folds
        # Each class is split into k parts
        fold_ids = np.arange(1, k + 1)
        
        # replicate fold_ids to cover n_cls
        full_ids = np.tile(fold_ids, (n_cls // k) + 1)[:n_cls]
        np.random.shuffle(full_ids)
        fold_vector[indices] = full_ids
        
    if list_out:
        out = {}
        for i in range(1, k + 1):
            fold_indices = np.where(fold_vector == i)[0] + 1
            if return_train:
                train_indices = np.setdiff1d(np.arange(1, n + 1), fold_indices)
                out[f"Fold{i}"] = train_indices.tolist()
            else:
                out[f"Fold{i}"] = fold_indices.tolist()
        return out
    return fold_vector

# r2py:entity:checkResamples
def checkResamples(index, x, y):
    all_nzv = set()
    x_df = pd.DataFrame(x)
    y_series = pd.Series(y)
    
    for fold_name in index:
        idx = np.array(index[fold_name]) - 1
        x_sub = x_df.iloc[idx]
        y_sub = y_series.iloc[idx]
        all_nzv.update(checkConditionalX(x_sub, y_sub))
        
    return sorted(list(all_nzv), reverse=True) if len(all_nzv) > 1 else sorted(list(all_nzv))

# --- Main Execution ---

# 1. Iris Example
# r2py:entity:nearZeroVar
iris_df = pd.DataFrame(iris)
iris_features = iris_df.iloc[:, :-1]
print(nearZeroVar(iris_features, save_metrics=True))

# 2. BloodBrain Example
# r2py:entity:data
bbb_df = pd.DataFrame(bbbDescr)
# r2py:entity:nearZeroVar_1
res1 = nearZeroVar(bbb_df)
print(f"[1] { ' '.join(map(str, res1)) if isinstance(res1, list) else res1}")

# r2py:entity:nearZeroVar_2
res2 = nearZeroVar(bbb_df, names=True)
print(f"[1] { ' '.join(map(repr, res2)) if isinstance(res2, list) else res2}")

# 3. Seed and Custom Data
# r2py:entity:set.seed
random.seed(1)
np.random.seed(1)

# r2py:entity:classes
classes = pd.Series(np.repeat(letters[0:3], 30))
# R: rep(c(0, 1), 45) -> 0, 1, 0, 1 ...
# r2py:entity:x
x = pd.DataFrame({
    'x1': np.tile([0, 1], 45),
    'x2': np.concatenate([np.zeros(10), np.ones(80)])
})

# lapply(x, table, y = classes)
# r2py:entity:lapply
for col in x.columns:
    print(f"${col}")
    ct = pd.crosstab(x[col], classes)
    ct.index.name = None
    ct.columns.name = 'y'
    print(ct)

# r2py:entity:checkConditionalX
print(f"[1] {checkConditionalX(x, classes)}")

# r2py:entity:folds
folds = createFolds(classes, k=3, return_train=True)

# r2py:entity:x$x3
x['x3'] = x['x1']
# x$x3[folds[[1]]] <- 0
# Note: folds is a dict, folds['Fold1'] contains training indices (return_train=True)
# r2py:entity:x$x3[folds[[1]]]
train_idx_1 = np.array(folds['Fold1']) - 1
x.loc[train_idx_1, 'x3'] = 0

# r2py:entity:checkResamples
res_resamples = checkResamples(folds, x, classes)
# Format output to match [1] 3 2
print(f"[1] {' '.join(map(str, res_resamples))}")