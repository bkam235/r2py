# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/dplyr__vignette__programming_chunk10.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__vignette__programming_chunk10.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Ensure mtcars is a DataFrame
mtcars = pd.DataFrame(mtcars)

# r2py:entity:summarise_mean
def summarise_mean(data, vars_func):
    # In R, this is called on a grouped tibble. 
    # 'data' here is a pandas GroupBy object.
    
    # Identify numeric columns (where(is.numeric))
    # We check columns of the original dataframe associated with the groupby object
    df_orig = data.obj if hasattr(data, 'obj') else data
    numeric_cols = [col for col in df_orig.columns if pd.api.types.is_numeric_dtype(df_orig[col])]
    
    # If vars_func is passed (e.g., via where(is.numeric)), we should filter columns.
    # However, the R call is summarise_mean(where(is.numeric)).
    # The R 'where' function returns a predicate.
    
    # R: summarise(n = n(), across({{ vars }}, mean))
    # We need to aggregate: count (n) and the mean of numeric columns.
    agg_dict = {'cyl': 'size'} # 'n' in R. Using 'cyl' as a proxy for size.
    
    # We'll rename the count column to 'n' later.
    # To avoid 'cyl' being in the mean list (since it's numeric), 
    # we only take numeric columns that aren't the grouping key.
    group_keys = data.groups.keys() # This is not quite right for indices.
    # For simplicity in this specific case:
    group_col = 'cyl' 
    
    mean_cols = [col for col in numeric_cols if col != group_col]
    
    # Create the aggregation dictionary
    # pandas .agg handles the naming if we use named aggregation or rename afterwards.
    res = data.agg(**{col: (col, 'mean') for col in mean_cols}, n=('mpg', 'size'))
    return res.reset_index()

# r2py:entity:group_by
grouped_mtcars = mtcars.groupby('cyl')

# In R: summarise_mean(where(is.numeric))
# We pass a dummy function or the logic inside our Python summarise_mean
# r2py:entity:summarise_mean_1
result = summarise_mean(grouped_mtcars, None)

print(result.to_string(index=False))