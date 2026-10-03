# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/tidyr__rd_example__complete_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__rd_example__complete_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['df']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# Setup initial dataframe
# r2py:entity:df
df = pd.DataFrame(df)
print(df)

# Combinations --------------------------------------------------------------
# r2py:entity:df_1
# df |> complete(group, item_id, item_name)
# Generate all possible combinations of `group`, `item_id`, and `item_name`
# r2py:entity:complete
cols = ['group', 'item_id', 'item_name']
unique_vals = [df[c].unique() for c in cols]
full_grid = pd.DataFrame(list(itertools.product(*unique_vals)), columns=cols)
res1 = pd.merge(full_grid, df, on=cols, how='left')
print(res1)

# df |> complete(group, nesting(item_id, item_name))
# Cross all possible `group` values with the unique pairs of `(item_id, item_name)`
# r2py:entity:complete_1
nest_cols = ['item_id', 'item_name']
groups = df['group'].unique()
unique_pairs = df[nest_cols].drop_duplicates()
full_grid_nest = pd.merge(pd.DataFrame({'group': groups}), unique_pairs, how='cross')
res2 = pd.merge(full_grid_nest, df, on=['group'] + nest_cols, how='left')
print(res2)

# r2py:entity:group_by
# df |> dplyr::group_by(group) |> complete(item_id, item_name)
# Within each `group`, generate all possible combinations of `item_id` and `item_name` that occur in that group
# r2py:entity:complete_2
res3_list = []
for group_val, group_df in df.groupby('group'):
    cols_to_complete = ['item_id', 'item_name']
    unique_vals_in_group = [group_df[c].unique() for c in cols_to_complete]
    grid_in_group = pd.DataFrame(list(itertools.product(*unique_vals_in_group)), columns=cols_to_complete)
    grid_in_group['group'] = group_val
    merged_group = pd.merge(grid_in_group, group_df, on=['group'] + cols_to_complete, how='left')
    res3_list.append(merged_group)
res3 = pd.concat(res3_list, ignore_index=True)
print(res3)

# Supplying values for new rows ---------------------------------------------
# df |> complete(group, nesting(item_id, item_name), fill = list(value1 = 0, value2 = 99))
# Use `fill` to replace NAs with some value. Affects both new and pre-existing missing values.
# r2py:entity:complete_3
fill_vals = {'value1': 0, 'value2': 99}
nest_cols = ['item_id', 'item_name']
groups = df['group'].unique()
unique_pairs = df[nest_cols].drop_duplicates()
full_grid_fill = pd.merge(pd.DataFrame({'group': groups}), unique_pairs, how='cross')
res4 = pd.merge(full_grid_fill, df, on=['group'] + nest_cols, how='left')
res4 = res4.fillna(value=fill_vals)
print(res4)

# df |> complete(group, nesting(item_id, item_name), fill = list(value1 = 0, value2 = 99), explicit = FALSE)
# Limit the fill to only the newly created (i.e. previously implicit) missing values
# r2py:entity:complete_4
nest_cols = ['item_id', 'item_name']
groups = df['group'].unique()
unique_pairs = df[nest_cols].drop_duplicates()
full_grid_exp = pd.merge(pd.DataFrame({'group': groups}), unique_pairs, how='cross')
# To identify "implicit" NAs, we track which rows existed in the original df
merged_exp = pd.merge(full_grid_exp, df, on=['group'] + nest_cols, how='left', indicator=True)
# indicator='_merge' tells us if the row was in 'both' (explicit) or 'left_only' (implicit)
res5 = merged_exp.copy()
for col, val in fill_vals.items():
    # Fill only if the row was implicit (left_only)
    res5.loc[res5['_merge'] == 'left_only', col] = res5.loc[res5['_merge'] == 'left_only', col].fillna(val)
res5 = res5.drop(columns=['_merge'])
print(res5)