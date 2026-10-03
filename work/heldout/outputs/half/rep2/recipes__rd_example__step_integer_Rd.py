# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Load data
# r2py:entity:data
Sacramento = pd.DataFrame(Sacramento)

# r2py:entity:sacr_tr
sacr_tr = Sacramento.iloc[0:100].copy()
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[sacr_tr.index[0], 'sqft'] = np.nan

# r2py:entity:sacr_te
sacr_te = Sacramento.iloc[100:105].copy()
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[sacr_te.index[0], 'sqft'] = np.nan
# r2py:entity:sacr_te$city[1]
sacr_te.loc[sacr_te.index[0], 'city'] = "whoville"
# r2py:entity:sacr_te$city[2]
sacr_te.loc[sacr_te.index[1], 'city'] = np.nan

# Translation of recipe(type ~ ., data = sacr_tr) |> step_integer(all_predictors())
# r2py:entity:rec
predictors = [col for col in sacr_tr.columns if col != 'type']

# step_integer: identify numeric predictors to be cast to integer
# In R, step_integer typically targets numeric variables.
# r2py:entity:step_integer
numeric_predictors = [col for col in predictors if pd.api.types.is_numeric_dtype(sacr_tr[col])]

# prep() effectively 'trains' the recipe. For step_integer, it identifies the columns.
# r2py:entity:prep
rec = {
    'predictors': predictors,
    'numeric_predictors': numeric_predictors,
    'steps': [{'operation': 'step_integer', 'terms': numeric_predictors}]
}

# bake applies the transformation to new data.
# r2py:entity:bake
sacr_te_baked = sacr_te[predictors].copy()
for col in rec['numeric_predictors']:
    # We use pd.to_numeric then cast to Int64 to handle NaNs and ensure it's treated as integer
    # However, if the data is not numeric (like 'city'), step_integer wouldn't target it.
    try:
        sacr_te_baked[col] = pd.to_numeric(sacr_te_baked[col], errors='coerce').astype('Int64')
    except:
        pass

# tidy(rec, number = 1) returns information about the first step.
# r2py:entity:tidy
step1 = rec['steps'][0]
tidy_rec = pd.DataFrame({
    'number': [1],
    'operation': [step1['operation']],
    'type': ['integer'],
    'trained': [True],
    'skip': [False],
    'id': ['step_integer_1']
})

# To match R's behavior of printing the results of bake() and tidy()
print(sacr_te_baked)
print(tidy_rec)