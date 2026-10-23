# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__group_cols_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__group_cols_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(dplyr))
# import_dplyr: simulated by using pandas

# Load iris dataset from shim
# r2py:entity:group_by
df_iris = pd.DataFrame(iris)

# gdf <- iris |> group_by(Species)
gdf = df_iris.copy()
# In R, group_by doesn't change the data, just adds metadata. 
group_cols_list = ['Species']

# gdf |> select(group_cols())
# r2py:entity:select
res_select = gdf[group_cols_list]
print(res_select.head(10))

# Remove the grouping variables from mutate selections:
# gdf |> mutate_at(vars(-group_cols()), `/`, 100)
# r2py:entity:mutate_at
cols_to_mutate = [c for c in gdf.columns if c not in group_cols_list]
gdf_mutate_at = gdf.copy()
gdf_mutate_at[cols_to_mutate] = gdf_mutate_at[cols_to_mutate] / 100
print(gdf_mutate_at.head(10))

# gdf |> mutate(across(everything(), ~ . / 100))
# r2py:entity:mutate
gdf_final = gdf.copy()
# across(everything()) applies to all columns.
# In R, dividing a factor by 100 usually results in NA for that column, 
# but the column is kept. In Python, we only divide numeric types to avoid TypeError.
numeric_cols = gdf_final.select_dtypes(include=[np.number]).columns
gdf_final[numeric_cols] = gdf_final[numeric_cols] / 100
print(gdf_final.head(10))