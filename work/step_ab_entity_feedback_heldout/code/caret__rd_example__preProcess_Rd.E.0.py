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

# Note: bbbDescr is provided by the shim. 
# The R code uses data(BloodBrain), and bbbDescr is a matrix/dataframe in that dataset.
# The shim loads bbbDescr.

def preProcess(x, method=["center", "scale"]):
    # 1. Zero Variance Filter (zv)
    # caret's preProcess by default removes columns with zero variance
    # x is expected to be a DataFrame
    zv_cols = [col for col in x.columns if x[col].nunique() <= 1]
    df_filtered = x.drop(columns=zv_cols)
    
    # 2. Center and Scale
    # R's scale() uses sample sd (ddof=1)
    means = df_filtered.mean()
    stds = df_filtered.std(ddof=1)
    
    # To handle columns with zero variance that might have slipped through or become 0
    # caret generally removes them. We only keep columns where std > 0 for scaling.
    # However, for this specific example, we follow the basic center/scale logic.
    
    return {
        "mean": means.tolist(),
        "std": stds.tolist(),
        "removed": zv_cols,
        "columns": df_filtered.columns.tolist(),
        "dim": [x.shape[0], x.shape[1]],
        "bc": {}, "yj": {}, "et": {}, "invHyperbolicSine": {} # Placeholders for other caret methods
    }

def predict_preProcess(pre_proc, x):
    # Remove the same columns that were removed during fit
    df_filtered = x.drop(columns=pre_proc["removed"])
    # Ensure column order
    df_filtered = df_filtered[pre_proc["columns"]]
    
    # Apply centering and scaling using the stored means and stds
    means = np.array(pre_proc["mean"])
    stds = np.array(pre_proc["std"])
    
    transformed = (df_filtered.values - means) / stds
    return pd.DataFrame(transformed, columns=pre_proc["columns"], index=x.index)

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R [1:100, -3] -> rows 0:100, drop 3rd column (index 2)
subset_train = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(subset_train)

# Translate: training <- predict(preProc, bbbDescr[1:100,-3])
training = predict_preProcess(preProc, subset_train)

# Translate: test <- predict(preProc, bbbDescr[101:208,-3])
# R [101:208, -3] -> rows 100:208, drop 3rd column (index 2)
subset_test = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, subset_test)