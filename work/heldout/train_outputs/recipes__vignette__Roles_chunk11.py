# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/recipes__vignette__Roles_chunk11.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__vignette__Roles_chunk11.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# The R code uses recipes::step_dummy, which by default performs treatment coding 
# (drops the first level). The iris dataset Species levels are: setosa, versicolor, virginica.
# Expected output: "Species_versicolor", "Species_virginica"

# Section 1: Translation of the first recipe pipe
# recipe( ~ ., data = iris) |> 
#   step_dummy(Species) |> 
#   prep() |> 
#   bake(new_data = NULL, all_predictors()) |> 
#   dplyr::select(starts_with("Species")) |> 
#   names()

# Convert dict to DataFrame
# r2py:entity:recipe
df_iris = pd.DataFrame(iris)

# step_dummy(Species) with default contrasts (drops first level)
# r2py:entity:bake
d1 = pd.get_dummies(df_iris, columns=['Species'], prefix='Species', drop_first=True)

# bake(..., all_predictors()) effectively keeps the transformed columns.
# dplyr::select(starts_with("Species")) filters for these.
# names() gets the column names.
# r2py:entity:names
result1 = [col for col in d1.columns if col.startswith("Species")]
print(result1)

# Section 2: Translation of the second recipe pipe
# recipe( ~ ., data = iris) |> 
#   step_dummy(Species, role = "trousers") |> 
#   prep() |> 
#   bake(new_data = NULL, has_role("trousers")) |> 
#   names()

# role = "trousers" is a custom role.
# has_role("trousers") in bake() filters the output to only those columns with that role.
# r2py:entity:prep_1
d2 = pd.get_dummies(df_iris, columns=['Species'], prefix='Species', drop_first=True)

# Only the columns created by step_dummy(Species, role="trousers") are returned.
# r2py:entity:names_1
result2 = [col for col in d2.columns if col.startswith("Species")]
print(result2)