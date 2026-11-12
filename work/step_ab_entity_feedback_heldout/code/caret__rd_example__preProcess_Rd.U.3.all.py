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

# r2py:entity:preProc
def preProcess(x, method=["center", "scale"]):
    """
    Approximate caret::preProcess.
    In R, scale() uses the sample standard deviation (ddof=1).
    """
    # 1. Zero Variance Filter (zv)
    # caret's preProcess defaults to removing near-zero variance predictors.
    # Here we identify columns with only 1 unique value.
    zv_cols = [col for col in x.columns if x[col].nunique() <= 1]
    df_filtered = x.drop(columns=zv_cols)
    
    # 2. Center and Scale (Sample Std Dev)
    means = df_filtered.mean()
    stds = df_filtered.std(ddof=1) # R uses ddof=1
    
    return {
        "mean": means, 
        "std": stds, 
        "removed": zv_cols, 
        "columns": df_filtered.columns.tolist()
    }

def predict_preProcess(pre_proc, x):
    """
    Approximate predict.preProcess.
    """
    # Remove the same columns that were removed during preProcess fit
    df_filtered = x.drop(columns=pre_proc["removed"])
    
    # Ensure column order matches the training set
    df_filtered = df_filtered[pre_proc["columns"]]
    
    # Apply scaling: (x - mean) / std
    transformed = (df_filtered - pre_proc["mean"]) / pre_proc["std"]
    
    return transformed

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R [1:100, -3] means rows 1-100 and all columns EXCEPT the 3rd.
# Python: iloc[0:100] for rows, and drop index 2 for columns.
# r2py:entity:preProc_1
bbbDescr_subset = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(bbbDescr_subset)

# Translate: training <- predict(preProc, bbbDescr[1:100, -3])
# r2py:entity:training
training = predict_preProcess(preProc, bbbDescr_subset)

# Translate: test <- predict(preProc, bbbDescr[101:208, -3])
# R [101:208, -3] means rows 101 to 208 and all columns EXCEPT the 3rd.
# r2py:entity:test
bbbDescr_test = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, bbbDescr_test)