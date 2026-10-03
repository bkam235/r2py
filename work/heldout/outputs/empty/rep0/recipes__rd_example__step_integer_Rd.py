# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:is_installed
from modeldata import Sacramento # Assuming modeldata is available or loaded via pandas
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

# Load data
# r2py:entity:data
d = Sacramento.copy()

# Data splitting and manipulation
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

# Define the target and predictors
# r2py:entity:rec
target = 'type'
predictors = [col for col in sacr_tr.columns if col != target]

# Implementation of step_integer: converting to integer (handling NaNs by keeping as float/nan)
# In R's recipes, step_integer converts numeric predictors to integers.
# r2py:entity:step_integer
def step_integer_func(X):
    X_out = X.copy()
    for col in X_out.columns:
        if np.issubdtype(X_out[col].dtype, np.number):
            # Use pandas' Int64 to allow nullable integers
            X_out[col] = X_out[col].astype('Int64')
    return X_out

# Create the pipeline (Equivalent to recipe |> step_integer |> prep)
# r2py:entity:recipe
rec = Pipeline([
    ('step_integer', FunctionTransformer(step_integer_func))
])

# 'prep' in this context is essentially fitting the pipeline
# r2py:entity:prep
rec.fit(sacr_tr[predictors])

# bake(rec, sacr_te, all_predictors())
# r2py:entity:bake
baked_data = rec.transform(sacr_te[predictors])

# tidy(rec, number = 1)
# In recipes, tidy returns information about the step. 
# Here we simulate the metadata for the first step (step_integer).
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'term': ['all_predictors()'],
    'result': ['integer'],
    'step': [1]
})

print(baked_data)
print(tidy_rec)