# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__preProcess_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['bbbDescr']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def preProcess(x, method=["center", "scale"]):
    """
    Approximate caret::preProcess.
    """
    # Identify zero-variance predictors
    # In R, preProcess removes variables with near-zero variance. 
    # For the example, we'll check if there's only one unique value.
    zv_cols = [col for col in x.columns if x[col].nunique() <= 1]
    df_filtered = x.drop(columns=zv_cols)
    
    # Caret's center and scale uses sample mean and sample sd (ddof=1)
    means = df_filtered.mean().tolist()
    stds = df_filtered.std(ddof=1).tolist()
    
    # The R output format for preProcess is a list/dict
    return {
        "mean": means,
        "std": stds,
        "removed": zv_cols,
        "columns": df_filtered.columns.tolist(),
        "dim": [x.shape[0], len(df_filtered.columns)],
        "bc": {}, "yj": {}, "et": {}, "invHyperbolicSine": {}
    }

def predict_preProcess(pre_proc, x):
    """
    Approximate predict.preProcess.
    """
    # 1. Remove the same columns that were removed during fit
    df_filtered = x.drop(columns=pre_proc["removed"])
    
    # 2. Ensure column order matches
    df_filtered = df_filtered[pre_proc["columns"]]
    
    # 3. Center and Scale: (x - mean) / std
    means = np.array(pre_proc["mean"])
    stds = np.array(pre_proc["std"])
    
    # Handle cases where std is 0 to avoid division by zero
    stds[stds == 0] = 1.0
    
    transformed_vals = (df_filtered.values - means) / stds
    return pd.DataFrame(transformed_vals, columns=pre_proc["columns"], index=x.index)

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R indexing [1:100, -3] -> rows 0 to 99, drop 3rd column (index 2)
subset_df = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(subset_df)

# Translate: training <- predict(preProc, bbbDescr[1:100,-3])
training = predict_preProcess(preProc, subset_df)

# Translate: test <- predict(preProc, bbbDescr[101:208,-3])
# R indexing [101:208, -3] -> rows 100 to 207, drop 3rd column (index 2)
test_df = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, test_df)