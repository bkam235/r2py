# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:data
from modeldata import Sacramento # Assuming modeldata is available as a python package or loaded via pd.read_csv

# Data splitting and NA injection
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

# Recipe emulation: step_integer(all_predictors())
# In R's recipes, step_integer converts numeric predictors to integer.
# In Python, we identify numeric columns and cast them to Int64 (nullable integer)
# r2py:entity:prep
predictors = [col for col in sacr_tr.columns if col != 'type']
numeric_cols = sacr_tr[predictors].select_dtypes(include=[np.number]).columns

# Prep: Fit the recipe (store the column types/names)
rec_prep = {
    'predictors': predictors,
    'numeric_cols': numeric_cols
}

# Bake: Apply transformations to sacr_te
# We simulate the "all_predictors()" selection and the integer conversion
# r2py:entity:bake
baked_te = sacr_te[predictors].copy()
for col in rec_prep['numeric_cols']:
    baked_te[col] = pd.to_numeric(baked_te[col], errors='coerce').astype('Int64')

print(baked_te)

# Tidy: Display metadata about the first step (step_integer)
# Emulating the output of tidy(rec, number = 1)
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'term': 'step_integer',
    'selection': 'all_predictors()',
    'columns': list(rec_prep['numeric_cols'])
})

print(tidy_rec)