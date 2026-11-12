# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

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

def preProcess(df):
    """
    Approximate caret::preProcess(method='center', 'scale').
    R's scale() uses sample std (ddof=1).
    """
    # Identify zero-variance predictors (only 1 unique value)
    # caret::preProcess by default handles zv.
    zv_cols = [col for col in df.columns if df[col].nunique() <= 1]
    df_filtered = df.drop(columns=zv_cols)
    
    means = df_filtered.mean().tolist()
    stds = df_filtered.std(ddof=1).tolist()
    
    return {
        'mean': means,
        'std': stds,
        'removed': zv_cols,
        'columns': df_filtered.columns.tolist(),
        'dim': [df.shape[0], df_filtered.shape[1]],
        'bc': {}, 'yj': {}, 'et': {}, 'invHyperbolicSine': {}
    }

def predict_preProcess(pre_proc, df):
    """
    Approximate predict.preProcess.
    """
    # Remove columns identified as zero-variance during fitting
    df_filtered = df.drop(columns=pre_proc['removed'])
    # Ensure column order matches
    df_filtered = df_filtered[pre_proc['columns']]
    
    # Center and Scale: (x - mean) / std
    means = np.array(pre_proc['mean'])
    stds = np.array(pre_proc['std'])
    
    # Avoid division by zero if std is 0
    stds[stds == 0] = 1.0
    
    scaled_values = (df_filtered.values - means) / stds
    return pd.DataFrame(scaled_values, columns=pre_proc['columns'], index=df.index)

# Translate: preProc <- preProcess(bbbDescr)
preProc = preProcess(bbbDescr)

# Translate: preProc <- preProcess(bbbDescr[1:100,-3])
# R [1:100, -3] -> Python rows 0:100, drop column index 2
bbbDescr_subset = bbbDescr.iloc[0:100].drop(bbbDescr.columns[2], axis=1)
preProc = preProcess(bbbDescr_subset)

# Translate: training <- predict(preProc, bbbDescr[1:100,-3])
training = predict_preProcess(preProc, bbbDescr_subset)

# Translate: test <- predict(preProc, bbbDescr[101:208,-3])
# R [101:208, -3] -> Python rows 100:208, drop column index 2
bbbDescr_test = bbbDescr.iloc[100:208].drop(bbbDescr.columns[2], axis=1)
test = predict_preProcess(preProc, bbbDescr_test)