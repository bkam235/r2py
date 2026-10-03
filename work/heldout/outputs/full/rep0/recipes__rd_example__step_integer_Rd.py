# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:data
from modeldata import Sacramento # Assuming modeldata is available or data is loaded

# Load data

# r2py:entity:sacr_tr
sacr_tr = Sacramento.iloc[0:100].copy()
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[0, 'sqft'] = np.nan

# r2py:entity:sacr_te
sacr_te = Sacramento.iloc[100:105].copy()
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[0, 'sqft'] = np.nan
# r2py:entity:sacr_te$city[1]
sacr_te.loc[0, 'city'] = "whoville"
# r2py:entity:sacr_te$city[2]
sacr_te.loc[1, 'city'] = np.nan

# recipe(type ~ ., data = sacr_tr)
# step_integer(all_predictors())
# prep(training = sacr_tr)
# r2py:entity:recipe
predictors = [col for col in sacr_tr.columns if col != 'type']
rec_state = {}

# r2py:entity:prep
for col in predictors:
    if pd.api.types.is_numeric_dtype(sacr_tr[col]):
        # Store the logic of step_integer: typically ensuring integer type
        # In recipes, step_integer converts to integer, often handling NAs
        rec_state[col] = 'integer'

# bake(rec, sacr_te, all_predictors())
# r2py:entity:bake
baked_te = sacr_te[predictors].copy()
for col, dtype in rec_state.items():
    # Approximating step_integer: convert to Int64 to support NaNs
    baked_te[col] = pd.to_numeric(baked_te[col], errors='coerce').astype('Int64')

print(baked_te)

# tidy(rec, number = 1)
# Since step_integer is the first step, we simulate the tidy output
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'term': predictors,
    'result': ['integer'] * len(predictors)
})
print(tidy_rec)