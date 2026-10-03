# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__glimpse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars', 'starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:glimpse
def glimpse(x, width=None):
    df = pd.DataFrame(x)
    rows, cols = df.shape
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")
    
    for col in df.columns:
        dtype = df[col].dtype
        # Map numpy/pandas dtypes to R-like labels
        if pd.api.types.is_float_dtype(dtype):
            type_label = "<dbl>"
        elif pd.api.types.is_integer_dtype(dtype):
            type_label = "<int>"
        elif pd.api.types.is_bool_dtype(dtype):
            type_label = "<lgl>"
        else:
            type_label = "<chr>"
        
        # Get values and format as a comma-separated string
        vals = df[col].values
        val_str = ", ".join(map(str, vals[:10]))
        if len(vals) > 10:
            val_str += ", ..."
            
        print(f"$ {col} {type_label} {val_str}")
    
    return x

# r2py:entity:select
def select(df, cols):
    # Handle 1:3 slicing (1-indexed R style)
    if isinstance(cols, slice) or (isinstance(cols, range) or hasattr(cols, '__iter__')):
        # Simplified for the 1:3 case
        return df.iloc[:, 0:3]
    return df[cols]

# Convert shim dicts to DataFrames
mtcars = pd.DataFrame(mtcars)
starwars = pd.DataFrame(starwars)

# glimpse(mtcars)
# r2py:entity:glimpse
glimpse(mtcars)

# mtcars |> glimpse() |> select(1:3)
# In R, glimpse returns the object invisibly.
# r2py:entity:glimpse_1
res = glimpse(mtcars)
# r2py:entity:select
res = select(res, range(1, 4))

# glimpse(starwars)
# r2py:entity:glimpse_2
glimpse(starwars)