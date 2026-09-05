# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/purrr__vignette__base_s19.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__vignette__base_s19.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# suppressPackageStartupMessages(library(purrr)) -> handled by imports

# Convert shim dict to DataFrame
mtcars_df = pd.DataFrame(mtcars)

# R code:
# mtcars |>
#   split(mtcars$cyl) |> 
#   map(\(df) lm(mpg ~ wt, data = df))|> 
#   map(coef) |> 
#   map_dbl(1)

# split(mtcars$cyl) creates a list of dataframes indexed by cyl
# r2py:entity:split
grouped = mtcars_df.groupby('cyl')

# map(\(df) lm(mpg ~ wt, data = df))
# r2py:entity:map
models = {name: smf.ols('mpg ~ wt', data=group).fit() for name, group in grouped}

# map(coef)
# r2py:entity:map_1
coeffs = {name: model.params for name, model in models.items()}

# map_dbl(1) extracts the first element (intercept) of each coefficient vector
# In R, this returns a named numeric vector.
# r2py:entity:map_dbl
result_series = pd.Series({name: params.iloc[0] for name, params in coeffs.items()})

# To match R's print output format exactly:
# R output shows the group names (4, 6, 8) and the intercept values.
print(f"      { '        '.join(map(str, result_series.index))}")
print(f"{' '.join(f'{val:.5f}' for val in result_series.values)}")