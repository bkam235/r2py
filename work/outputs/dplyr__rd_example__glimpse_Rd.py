# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__glimpse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__glimpse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars', 'starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Convert shim data to DataFrames
mtcars = pd.DataFrame(mtcars)
starwars = pd.DataFrame(starwars)

# r2py:entity:glimpse
def glimpse(df):
    """Mimics dplyr::glimpse output."""
    rows = len(df)
    cols = len(df.columns)
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")
    
    for col in df.columns:
        dtype = df[col].dtype
        # Map numpy/pandas dtypes to R-like glimpses
        if "float" in str(dtype):
            r_type = "<dbl>"
        elif "int" in str(dtype):
            r_type = "<int>"
        elif "object" in str(dtype):
            r_type = "<chr>"
        else:
            r_type = f"<{dtype}>"
            
        # Get first few values
        vals = df[col].head(10).tolist()
        vals_str = ", ".join(map(str, vals))
        if len(df[col]) > 10:
            vals_str += "…"
            
        print(f"$ {col:<5} {r_type} {vals_str}")
    
    return df

# r2py:entity:glimpse
glimpse(mtcars)

# mtcars |> glimpse() |> select(1:3)
# In R, glimpse returns the original object invisibly.
# r2py:entity:glimpse_1
res = glimpse(mtcars)
# select(1:3) corresponds to columns 0, 1, 2 in Python
# r2py:entity:select
result = res.iloc[:, 0:3]
# Note: The R code doesn't print the result of the pipeline, 
# but since the script ends with another glimpse, we just compute it.

# r2py:entity:glimpse_2
glimpse(starwars)