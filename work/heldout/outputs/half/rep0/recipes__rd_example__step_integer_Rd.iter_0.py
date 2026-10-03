# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:is_installed
from modeldata import Sacramento # Assuming modeldata package is available via a python port or csv

# Load data
# r2py:entity:data
d = Sacramento
# r2py:entity:sacr_tr
sacr_tr = d.iloc[0:100].copy()
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[0, 'sqft'] = np.nan

# r2py:entity:sacr_te
sacr_te = d.iloc[100:105].copy()
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[0, 'sqft'] = np.nan
# r2py:entity:sacr_te$city[1]
sacr_te.loc[0, 'city'] = "whoville"
# r2py:entity:sacr_te$city[2]
sacr_te.loc[1, 'city'] = np.nan

# Emulating 'recipe' and 'step_integer'
# step_integer in R converts doubles to integers. 
# In Python, we identify numeric columns and handle them.
# r2py:entity:recipe
predictors = [col for col in sacr_tr.columns if col != 'type']

# Prep phase: Identify columns to be treated as integers based on training data
# recipes' step_integer typically targets numeric types
# r2py:entity:prep
integer_cols = []
for col in predictors:
    if pd.api.types.is_numeric_dtype(sacr_tr[col]):
        integer_cols.append(col)

# Bake phase: Apply the transformation to test data
# step_integer essentially casts to int (handling NAs by leaving them or casting to Float/Int64)
# r2py:entity:bake
sacr_te_baked = sacr_te[predictors].copy()
for col in integer_cols:
    sacr_te_baked[col] = pd.to_numeric(sacr_te_baked[col], errors='coerce').astype('Int64')

print(sacr_te_baked)

# Tidy phase: Emulate tidy(rec, number = 1) which describes the first step
# r2py:entity:tidy
tidy_rec_1 = pd.DataFrame({
    'term': ['step_integer'],
    'all_predictors': [integer_cols]
})
print(tidy_rec_1)