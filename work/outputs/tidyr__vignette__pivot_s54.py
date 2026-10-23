# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/tidyr__vignette__pivot_s54.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__vignette__pivot_s54.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['spec1', 'us_rent_income']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:spec1
def build_wider_spec(data, names_from, values_from, names_prefix="", names_sep="_", names_glue=None, names_sort=False, names_vary="fastest", names_expand=False):
    df = pd.DataFrame(data)
    
    # Handle names_from and values_from as lists
    if isinstance(names_from, str):
        names_from_cols = [names_from]
    else:
        names_from_cols = names_from
        
    if isinstance(values_from, str):
        values_from_cols = [values_from]
    else:
        values_from_cols = values_from

    # Get unique combinations of names_from columns
    row_ids = df[names_from_cols].drop_duplicates().reset_index(drop=True)
    if names_sort:
        row_ids = row_ids.sort_values(by=names_from_cols).reset_index(drop=True)
    
    # Create the base row names
    row_names = row_ids.astype(str).agg(names_sep.join, axis=1)
    
    # Initialize result dataframe
    out = pd.DataFrame({' .name': names_prefix + row_names})
    
    if len(values_from_cols) == 1:
        out['.value'] = values_from_cols[0]
    else:
        n_rows = len(row_ids)
        if names_vary == "fastest":
            # Repeat the whole block for each value column
            out = pd.concat([out] * len(values_from_cols), ignore_index=True)
            # Each block gets one value column name
            out['.value'] = np.repeat(values_from_cols, n_rows)
        else: # slowest
            # Repeat each row for all value columns
            out = out.loc[out.index.repeat(len(values_from_cols))].reset_index(drop=True)
            # Each row gets the list of value column names
            out['.value'] = np.tile(values_from_cols, n_rows)
            
        # Update .name to be .value + sep + .name
        out[' .name'] = out['.value'] + names_sep + out[' .name']

    # Combine with original IDs
    if names_vary == "fastest":
        row_ids_rep = pd.concat([row_ids] * len(values_from_cols), ignore_index=True)
        out = pd.concat([out, row_ids_rep], axis=1)
    elif names_vary == "slowest" and len(values_from_cols) > 1:
        row_ids_rep = row_ids.loc[row_ids.index.repeat(len(values_from_cols))].reset_index(drop=True)
        out = pd.concat([out, row_ids_rep], axis=1)
    else:
        out = pd.concat([out, row_ids], axis=1)

    # R's build_wider_spec result has specific column order and naming
    # The R output shows columns: .name, .value, variable
    # We need to ensure we only return the requested columns if it's a simple spec
    
    # For the specific case of the vignette:
    # We just need to return the dataframe.
    return out

# (tidyr is handled by the logic in build_wider_spec)

# (No-op in Python)

# In the R code: spec1 <- us_rent_income |> build_wider_spec(names_from = variable, values_from = c(estimate, moe))
df_rent = pd.DataFrame(us_rent_income)
spec1 = build_wider_spec(
    df_rent, 
    names_from="variable", 
    values_from=["estimate", "moe"]
)

# The final expression in R is spec1, which prints the tibble.
# The output requires .name, .value, and the variable column.
# r2py:entity:spec1_1
print(spec1[[' .name', '.value', 'variable']].to_string(index=False))