# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__vignette__Skipping_chunk2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__vignette__Skipping_chunk2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Convert shim data to DataFrame
mtcars = pd.DataFrame(mtcars)

# r2py:entity:recipe
# mpg ~ . means mpg is target, others are predictors
target = 'mpg'
predictors = [col for col in mtcars.columns if col != target]

# r2py:entity:step_log
# step_log(disp, skip = TRUE) means 'disp' is identified but not transformed.
# In recipes, if a step is skipped, the column remains in the data but is not modified.
skipped_cols = ['disp']

# r2py:entity:step_center
# all_numeric_predictors() includes all predictors since all in mtcars (except mpg) are numeric.
# step_center centers the data (subtracts mean).
numeric_predictors = [col for col in predictors if mtcars[col].dtype in [np.float64, np.int64]]

# r2py:entity:prep
# Prep calculates the means for centering.
scaler = StandardScaler(with_mean=True, with_std=False)
scaler.fit(mtcars[numeric_predictors])

# r2py:entity:bake
# Define a bake function to mimic the behavior of recipes::bake
def bake(recipe_scaler, new_data=None):
    if new_data is None:
        # bake(recipe, new_data = NULL) returns processed training data
        data = mtcars.copy()
    else:
        # bake(recipe, new_data = mtcars) returns processed new_data
        data = new_data.copy()
    
    # Apply centering to numeric predictors
    data[numeric_predictors] = recipe_scaler.transform(data[numeric_predictors])
    
    # Note: step_log(disp, skip=TRUE) means disp is NOT transformed.
    # If we were doing a log, we would do it here. Since skip=TRUE, we do nothing.
    
    return data

# First call: bake(car_recipe, new_data = NULL) |> head() |> select(disp, hp)
res1 = bake(scaler, new_data=None)
# r2py:entity:head
res1_head = res1.head(6)
# r2py:entity:select
print(res1_head[['disp', 'hp']])

# Second call: bake(car_recipe, new_data = mtcars) |> head() |> select(disp, hp)
# r2py:entity:bake_1
res2 = bake(scaler, new_data=mtcars)
# r2py:entity:head_1
res2_head = res2.head(6)
# r2py:entity:select_1
print(res2_head[['disp', 'hp']])