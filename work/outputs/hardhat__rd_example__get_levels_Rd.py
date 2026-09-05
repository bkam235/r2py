# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/hardhat__rd_example__get_levels_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hardhat__rd_example__get_levels_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'letters', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from typing import Any, Optional

# r2py:entity:get_levels
def get_levels(data: Any) -> Optional[dict]:
    if not isinstance(data, pd.DataFrame):
        return None
    
    levels_dict = {}
    for col_name in data.columns:
        col = data[col_name]
        if isinstance(col.dtype, pd.CategoricalDtype):
            levels_dict[col_name] = col.cat.categories.tolist()
        # In some cases, R factors are shimmed as objects/strings, 
        # but the logic should follow if they are categorical.
            
    if not levels_dict:
        return None
    
    return levels_dict

# r2py:entity:get_outcome_levels
def standardize(y: Any) -> pd.DataFrame:
    if isinstance(y, (pd.Series, np.ndarray, list)):
        # Mimic R factor: convert to categorical
        series = pd.Series(y).astype('category')
        return pd.DataFrame({".outcome": series})
    elif isinstance(y, pd.DataFrame):
        return y
    else:
        # Fallback for other types
        series = pd.Series(y).astype('category')
        return pd.DataFrame({".outcome": series})

def get_outcome_levels(y: Any) -> Optional[dict]:
    y_std = standardize(y)
    return get_levels(y_std)

# --- Example Execution ---

# Setup iris: Convert shim dict to DataFrame and make 'Species' categorical
# r2py:entity:get_levels
iris_df = pd.DataFrame(iris)
if 'Species' in iris_df.columns:
    iris_df['Species'] = iris_df['Species'].astype('category')

# Factor columns are returned with their levels
res1 = get_levels(iris_df)
print(res1)

# No factor columns
# r2py:entity:get_levels_1
mtcars_df = pd.DataFrame(mtcars)
res2 = get_levels(mtcars_df)
print(res2)

# standardize() is first run on `y`
# which converts the input to a data frame with an automatically named column, `.outcome`
# r2py:entity:get_outcome_levels
y_val = letters[0:5]
res3 = get_outcome_levels(y=y_val)
print(res3)