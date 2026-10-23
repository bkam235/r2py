# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__distinct_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__distinct_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:nrow_1
def distinct(df, *args, keep_all=False):
    """
    Mimics dplyr::distinct.
    If args are provided, it returns only those columns (or all if keep_all=True) 
    that are unique based on the provided columns.
    """
    # Handle grouped dataframes
    if hasattr(df, '_group_by_cols'):
        group_cols = df._group_by_cols
        if not args:
            # distinct() on grouped df: distinctness across all columns, but preserve groups
            # In dplyr, distinct() on grouped df uses all variables.
            return df.drop_duplicates().reset_index(drop=True)
        
        subset = list(args)
        # Grouped distinct: unique based on subset within each group
        # We keep group_cols and the subset columns
        all_subset = group_cols + subset
        res = df.drop_duplicates(subset=all_subset)
        
        if keep_all:
            return res.reset_index(drop=True)
        else:
            # Return only grouping columns and the distinct columns specified
            # Deduplicate the column list to avoid duplicates if group_cols were in args
            final_cols = []
            for c in all_subset:
                if c not in final_cols:
                    final_cols.append(c)
            return res[final_cols].reset_index(drop=True)

    # Ungrouped case
    if not args:
        return df.drop_duplicates().reset_index(drop=True)
    
    subset = list(args)
    res = df.drop_duplicates(subset=subset)
    
    if keep_all:
        return res.reset_index(drop=True)
    else:
        return res[subset].reset_index(drop=True)

# r2py:entity:group_by
def group_by(df, *cols):
    """Mimics dplyr::group_by by attaching metadata to the dataframe."""
    df_grouped = df.copy()
    df_grouped._group_by_cols = list(cols)
    return df_grouped

# Initial data setup
# Note: R's sample(10, 100, rep = TRUE)
# r2py:entity:df
np.random.seed(42) 
df = pd.DataFrame({
    'x': np.random.choice(np.arange(1, 11), 100),
    'y': np.random.choice(np.arange(1, 11), 100)
})

# r2py:entity:nrow
print(f"[1] {len(df)}")
# r2py:entity:nrow_1
print(f"[1] {len(distinct(df))}")
# r2py:entity:nrow_2
print(f"[1] {len(distinct(df, 'x', 'y'))}")

# r2py:entity:distinct
print(distinct(df, 'x'))
# r2py:entity:distinct_1
print(distinct(df, 'y'))

# You can choose to keep all other variables as well
# r2py:entity:distinct_2
print(distinct(df, 'x', keep_all=True))
# r2py:entity:distinct_3
print(distinct(df, 'y', keep_all=True))

# You can also use distinct on computed variables
# distinct(df, diff = abs(x - y))
# r2py:entity:distinct_4
df_computed = df.assign(diff=lambda d: (d['x'] - d['y']).abs())
print(distinct(df_computed, 'diff'))

# Use `pick()` to select columns with tidy-select
# distinct(starwars, pick(contains("color")))
# r2py:entity:distinct_5
starwars_df = pd.DataFrame(starwars)
color_cols = [col for col in starwars_df.columns if 'color' in col]
print(distinct(starwars_df[color_cols]))

# Grouping -------------------------------------------------

# r2py:entity:df_1
df_grouped_data = pd.DataFrame({
    'g': [1, 1, 2, 2, 2],
    'x': [1, 1, 2, 1, 2],
    'y': [3, 2, 1, 3, 1]
})

# r2py:entity:df_2
df_grouped = group_by(df_grouped_data, 'g')

# With grouped data frames, distinctness is computed within each group
# r2py:entity:distinct_6
print(distinct(df_grouped, 'x'))

# When `...` are omitted, `distinct()` still computes distinctness using
# all variables in the data frame
# r2py:entity:distinct_7
print(distinct(df_grouped))