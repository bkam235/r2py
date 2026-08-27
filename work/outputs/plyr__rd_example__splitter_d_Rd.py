# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/plyr__rd_example__splitter_d_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'plyr__rd_example__splitter_d_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from itertools import product

# The data shim provides mtcars as a dict, we need it as a DataFrame
if 'mtcars' in globals() and isinstance(mtcars, dict):
    mtcars = pd.DataFrame(mtcars)

def print_split_result(result):
    """Helper to mimic R's printing of a split list."""
    for key, df in result.items():
        # R split names are printed as `$`name
        print(f"      `${key}`")
        if df.empty:
            # Mimic R's empty data frame print
            cols = " ".join(df.columns)
            print(f" [1] {cols}")
            print("<0 Zeilen> (oder row.names mit Länge 0)\n")
        else:
            # Reset index to mimic R's 1-based row numbering for the group
            temp_df = df.copy()
            temp_df.index = range(1, len(temp_df) + 1)
            print(temp_df)
        print()

# r2py:entity:splitter_d
def splitter_d(data, variables, drop=True):
    """
    Python equivalent of plyr:::splitter_d.
    """
    if isinstance(variables, str):
        vars_list = [variables]
    elif isinstance(variables, (list, tuple)):
        vars_list = list(variables)
    else:
        vars_list = list(variables)
    
    df = data.copy()
    
    # Determine levels for each variable
    all_levels = []
    for var in vars_list:
        if isinstance(df[var].dtype, pd.CategoricalDtype):
            all_levels.append(df[var].cat.categories.tolist())
        else:
            # For non-categorical, get unique values excluding NA
            unique_vals = sorted([v for v in df[var].unique() if pd.notna(v)])
            all_levels.append(unique_vals)
            
    def make_key(vals):
        str_vals = []
        for v in vals:
            if pd.isna(v):
                str_vals.append("NA")
            elif isinstance(v, (float, np.floating)) and v.is_integer():
                str_vals.append(f"{int(v)}")
            elif isinstance(v, (int, np.integer)):
                str_vals.append(str(v))
            else:
                str_vals.append(str(v))
        
        if len(str_vals) == 1:
            return str_vals[0]
        return ".".join(str_vals)

    # To handle NAs in groupby, we use dropna=False
    grouped = df.groupby(vars_list, observed=True, dropna=False)
    
    result = {}
    if drop:
        for name, group in grouped:
            # Filter out groups that contain NA in the grouping variables (R's split(df, list(x)) behavior)
            name_tuple = name if isinstance(name, tuple) else (name,)
            if any(pd.isna(v) for v in name_tuple):
                continue
            key = make_key(name_tuple)
            result[key] = group
    else:
        # All combinations of levels (excluding NA unless levels contain it)
        all_combos = list(product(*all_levels))
        
        # Map observed groups
        observed_groups = {}
        for name, group in grouped:
            name_tuple = name if isinstance(name, tuple) else (name,)
            key = make_key(name_tuple)
            observed_groups[key] = group
            
        for combo in all_combos:
            key = make_key(combo)
            if key in observed_groups:
                result[key] = observed_groups[key]
            else:
                result[key] = df.iloc[0:0].copy()
                
    return result

# plyr:::splitter_d(mtcars, .(cyl))
# R's split returns groups with only original columns of the data as it existed at the call
# r2py:entity:splitter_d
res_0 = splitter_d(mtcars[['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']], 'cyl')
print_split_result(res_0)

# plyr:::splitter_d(mtcars, .(vs, am))
# r2py:entity:splitter_d_1
res_1 = splitter_d(mtcars[['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']], ['vs', 'am'])
print_split_result(res_1)

# plyr:::splitter_d(mtcars, .(am, vs))
# r2py:entity:splitter_d_2
res_2 = splitter_d(mtcars[['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']], ['am', 'vs'])
print_split_result(res_2)

# mtcars$cyl2 <- factor(mtcars$cyl, levels = c(2, 4, 6, 8, 10))
# r2py:entity:mtcars$cyl2
mtcars['cyl2'] = pd.Categorical(mtcars['cyl'], categories=[2, 4, 6, 8, 10])

# plyr:::splitter_d(mtcars, .(cyl2), drop = TRUE)
# Update cols for this call
# r2py:entity:splitter_d_3
cols_3 = ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb', 'cyl2']
res_3 = splitter_d(mtcars[cols_3], 'cyl2', drop=True)
print_split_result(res_3)

# plyr:::splitter_d(mtcars, .(cyl2), drop = FALSE)
# r2py:entity:splitter_d_4
res_4 = splitter_d(mtcars[cols_3], 'cyl2', drop=False)
print_split_result(res_4)

# mtcars$cyl3 <- ifelse(mtcars$vs == 1, NA, mtcars$cyl)
# r2py:entity:mtcars$cyl3
mtcars['cyl3'] = np.where(mtcars['vs'] == 1, np.nan, mtcars['cyl'])

# plyr:::splitter_d(mtcars, .(cyl3))
# r2py:entity:splitter_d_5
cols_5 = ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb', 'cyl2', 'cyl3']
res_5 = splitter_d(mtcars[cols_5], 'cyl3')
print_split_result(res_5)

# plyr:::splitter_d(mtcars, .(cyl3, vs))
# r2py:entity:splitter_d_6
res_6 = splitter_d(mtcars[cols_5], ['cyl3', 'vs'])
print_split_result(res_6)

# plyr:::splitter_d(mtcars, .(cyl3, vs), drop = FALSE)
# r2py:entity:splitter_d_7
res_7 = splitter_d(mtcars[cols_5], ['cyl3', 'vs'], drop=False)
print_split_result(res_7)