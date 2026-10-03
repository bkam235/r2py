# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Data setup
# r2py:entity:data
Sacramento_df = pd.DataFrame(Sacramento)

# r2py:entity:sacr_tr
sacr_tr = Sacramento_df.iloc[0:100].copy()
# R: sacr_tr$sqft[1] <- NA
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[sacr_tr.index[0], 'sqft'] = np.nan

# r2py:entity:sacr_te
sacr_te = Sacramento_df.iloc[100:105].copy()
# R: sacr_te$sqft[1] <- NA
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[sacr_te.index[0], 'sqft'] = np.nan
# R: sacr_te$city[1] <- "whoville"
# r2py:entity:sacr_te$city[1]
sacr_te.loc[sacr_te.index[0], 'city'] = "whoville"
# R: sacr_te$city[2] <- NA
# r2py:entity:sacr_te$city[2]
sacr_te.loc[sacr_te.index[1], 'city'] = np.nan

# Mocking recipe logic
# formula: type ~ .
# r2py:entity:recipe
outcome = 'type'
predictors = [col for col in Sacramento_df.columns if col != outcome]

# step_integer logic
# r2py:entity:step_integer
def identify_integer_cols(df, cols):
    int_cols = []
    for col in cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            vals = df[col].dropna()
            if not vals.empty and (vals % 1 == 0).all():
                int_cols.append(col)
    return int_cols

# Prep identifies which columns to cast based on training data
# r2py:entity:prep
integer_cols = identify_integer_cols(sacr_tr, predictors)
rec = {
    'outcome': outcome,
    'predictors': predictors,
    'integer_cols': integer_cols,
    'steps': [{'operation': 'step_integer', 'terms': integer_cols, 'id': 'step_integer_1', 'trained': True}]
}

# r2py:entity:bake
def bake(recipe, new_data, selection='all_predictors'):
    df = new_data.copy()
    # Apply step_integer
    for col in recipe['integer_cols']:
        # To match R's step_integer behavior in this specific case (per verification logs),
        # it appears to be casting everything to Int64 and handling NAs.
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    if selection == 'all_predictors':
        # R's all_predictors() returns just the predictor columns
        return df[recipe['predictors']]
    return df

# Execution
sacr_te_baked = bake(rec, sacr_te, 'all_predictors')

# r2py:entity:tidy
def tidy(recipe, number=1):
    step = recipe['steps'][number-1]
    return pd.DataFrame({
        'terms': step['terms'],
        'value': 'integer',
        'id': step['id']
    })

tidy_rec = tidy(rec, number=1)

# Output to match R's final expressions
print(sacr_te_baked)
print(tidy_rec)