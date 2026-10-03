# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/recipes__rd_example__step_integer_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_integer_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:is_installed
from modeldata import Sacramento # Assuming modeldata is available or loaded as a CSV

# data(Sacramento, package = "modeldata")
# r2py:entity:data
d = Sacramento.copy()

# sacr_tr <- Sacramento[1:100, ]
# sacr_tr$sqft[1] <- NA
# r2py:entity:sacr_tr
sacr_tr = d.iloc[0:100].copy()
# r2py:entity:sacr_tr$sqft[1]
sacr_tr.loc[sacr_tr.index[0], 'sqft'] = np.nan

# sacr_te <- Sacramento[101:105, ]
# sacr_te$sqft[1] <- NA
# sacr_te$city[1] <- "whoville"
# sacr_te$city[2] <- NA
# r2py:entity:sacr_te
sacr_te = d.iloc[100:105].copy()
# r2py:entity:sacr_te$sqft[1]
sacr_te.loc[sacr_te.index[0], 'sqft'] = np.nan
# r2py:entity:sacr_te$city[1]
sacr_te.loc[sacr_te.index[0], 'city'] = "whoville"
# r2py:entity:sacr_te$city[2]
sacr_te.loc[sacr_te.index[1], 'city'] = np.nan

# recipe(type ~ ., data = sacr_tr) |> step_integer(all_predictors())
# In R, step_integer converts doubles to integers. 
# We identify predictors (excluding target 'type') and apply conversion.
# r2py:entity:rec
target = 'type'
predictors = [col for col in sacr_tr.columns if col != target]

# prep(training = sacr_tr)
# We store the logic for conversion (similar to how a recipe prep stores state)
# For step_integer, the operation is a type cast.
# r2py:entity:prep
def apply_step_integer(df, cols):
    df_copy = df.copy()
    for col in cols:
        # To mimic R's step_integer, we convert to Int64 (nullable integer) 
        # to handle the NAs present in the data.
        df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype('Int64')
    return df_copy

# bake(rec, sacr_te, all_predictors())
# r2py:entity:bake
baked_te = apply_step_integer(sacr_te[predictors], predictors)
print(baked_te)

# tidy(rec, number = 1)
# step_integer typically just reports the columns it operated on.
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'term': 'step_integer',
    'columns': predictors
})
print(tidy_rec)