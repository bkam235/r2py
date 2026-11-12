# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:entity:data
# r2py:data_shim managed by the harness (loads R's input data) - do not write it
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
    Removes zero-variance predictors and applies centering/scaling.
    """
    # Convert to DataFrame if not already
    df = pd.DataFrame(x)
    
    # Zero Variance Filter (zv) - identify columns with only 1 unique value
    # caret's preProcess removes columns with zero variance by default
    zv_cols = [col for col in df.columns if df[col].nunique() <= 1]
    df_filtered = df.drop(columns=zv_cols)
    
    means = df_filtered.mean().tolist()
    # R's scale() uses sample standard deviation (ddof=1)
    stds = df_filtered.std().tolist()
    
    # The returned object in R is a list containing these attributes
    res = {
        "dim": [df_filtered.shape[0], df_filtered.shape[1]],
        "mean": means,
        "std": stds,
        "removed": zv_cols,
        "columns": df_filtered.columns.tolist(),
        "bc": {}, "yj": {}, "et": {}, "invHyperbolicSine": {} # Placeholders for other methods
    }
    return res

def predict_preProcess(pre_proc, x):
    """
    Approximate predict.preProcess.
    """
    df = pd.DataFrame(x)
    # Remove columns that were removed during fit
    df_filtered = df.drop(columns=pre_proc["removed"])
    # Ensure correct column order
    df_filtered = df_filtered[pre_proc["columns"]]
    
    # Apply centering and scaling
    # formula: (x - mean) / std
    means = np.array(pre_proc["mean"])
    stds = np.array(pre_proc["std"])
    
    # Handle cases where std is 0 to avoid division by zero
    stds_fixed = np.where(stds == 0, 1.0, stds)
    
    transformed = (df_filtered.values - means) / stds_fixed
    
    return pd.DataFrame(transformed, columns=pre_proc["columns"], index=df.index)

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R [1:100, -3] means rows 1-100 and all columns except the 3rd.
# In Python, rows 0:100, and drop column index 2.
bbbDescr_subset = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(bbbDescr_subset)

# Translate: training <- predict(preProc, bbbDescr[1:100,-3])
training = predict_preProcess(preProc, bbbDescr_subset)

# Translate: test <- predict(preProc, bbbDescr[101:208,-3])
# R [101:208, -3] means rows 101 to 208 and all columns except the 3rd.
bbbDescr_test = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, bbbDescr_test)