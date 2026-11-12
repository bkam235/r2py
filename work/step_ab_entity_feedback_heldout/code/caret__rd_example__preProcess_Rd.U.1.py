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

# Convert shim data to DataFrame if not already (the shim usually does)
bbbDescr = pd.DataFrame(bbbDescr)

# r2py:entity:preProc
def preProcess(x, method=["center", "scale"]):
    """
    Approximate caret::preProcess.
    R's scale() uses sample standard deviation (ddof=1).
    """
    # Zero Variance Filter: remove columns with 1 unique value
    zv_cols = [col for col in x.columns if x[col].nunique() <= 1]
    df_filtered = x.drop(columns=zv_cols)
    
    # Calculate mean and sample std (ddof=1)
    means = df_filtered.mean()
    stds = df_filtered.std(ddof=1)
    
    return {
        "mean": means.tolist(),
        "std": stds.tolist(),
        "removed": zv_cols,
        "columns": df_filtered.columns.tolist()
    }

def predict_preProcess(pre_proc, x):
    """
    Approximate predict.preProcess.
    """
    # Remove the same columns that were removed during fit
    df_filtered = x.drop(columns=pre_proc["removed"])
    # Ensure column order matches
    df_filtered = df_filtered[pre_proc["columns"]]
    
    # Manual centering and scaling using sample std
    means = np.array(pre_proc["mean"])
    stds = np.array(pre_proc["std"])
    
    # (x - mean) / std
    transformed = (df_filtered.values - means) / stds
    
    return pd.DataFrame(transformed, columns=pre_proc["columns"], index=x.index)

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R [1:100, -3] -> Rows 0-100, exclude 3rd column (index 2)
# Note: bbbDescr in R typically includes a response variable 'logBBB' as the last col.
# The index -3 removes the 3rd column.
bbbDescr_subset = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(bbbDescr_subset)

# Translate: training <- predict(preProc, bbbDescr[1:100,-3])
training = predict_preProcess(preProc, bbbDescr_subset)

# Translate: test <- predict(preProc, bbbDescr[101:208,-3])
# R [101:208, -3] -> Rows 100-208, exclude 3rd column (index 2)
bbbDescr_test = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, bbbDescr_test)