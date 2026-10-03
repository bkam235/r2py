# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/recipes__rd_example__step_integer_Rd.py'
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
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[sacr_tr.index[0], 'sqft'] = np.nan

# r2py:entity:sacr_te
sacr_te = Sacramento_df.iloc[100:105].copy()
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[sacr_te.index[0], 'sqft'] = np.nan
# r2py:entity:sacr_te$city[1]
sacr_te.loc[sacr_te.index[0], 'city'] = "whoville"
# r2py:entity:sacr_te$city[2]
sacr_te.loc[sacr_te.index[1], 'city'] = np.nan

# Recipe logic emulation
# In R: recipe(type ~ ., data = sacr_tr)
# r2py:entity:recipe
outcome = 'type'
predictors = [col for col in sacr_tr.columns if col != outcome]

# step_integer(all_predictors()) - identifies numeric predictors to convert to integer
# In R, prep() evaluates the recipe on the training data. 
# step_integer identifies which numeric columns should be converted.
# r2py:entity:prep
integer_cols = []
for col in predictors:
    if pd.api.types.is_numeric_dtype(sacr_tr[col]):
        integer_cols.append(col)

# Create a representation of the recipe object for tidy()
rec = {
    'steps': [
        {'operation': 'step_integer', 'type': 'integer', 'trained': True, 'skip': False, 'id': 'step_integer_1', 'vars': integer_cols}
    ],
    'predictors': predictors,
    'integer_cols': integer_cols
}

# bake(rec, sacr_te, all_predictors())
# r2py:entity:bake
sacr_te_baked = sacr_te[predictors].copy()
for col in integer_cols:
    # Only cast if the data in the test set is also numeric/convertible
    # R's step_integer will convert numeric to integer; non-numeric stays as is or becomes NA if forced
    # To match R's behavior where it simply casts the numeric columns identified in prep:
    try:
        sacr_te_baked[col] = pd.to_numeric(sacr_te_baked[col], errors='coerce').astype('Int64')
    except:
        pass

print(sacr_te_baked)

# tidy(rec, number = 1)
# Returns info about the first step
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'number': [1],
    'operation': ['step_integer'],
    'type': ['integer'],
    'trained': [True],
    'skip': [False],
    'id': ['step_integer_1']
})

print(tidy_rec)