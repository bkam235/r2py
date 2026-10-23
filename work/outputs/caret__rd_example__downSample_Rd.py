# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/caret__rd_example__downSample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__downSample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['fattyAcids', 'oilType']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:downSample
def downSample(x, y, list_val=False, yname="Class"):
    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)
    
    y = np.array(y)
    counts = pd.Series(y).value_counts()
    min_class = counts.min()
    
    df = x.copy()
    df['_outcome'] = y
    
    sampled_list = []
    labels = sorted(counts.index)
    for label in labels:
        subset = df[df['_outcome'] == label]
        sampled_subset = subset.sample(n=min_class)
        sampled_list.append(sampled_subset)
    
    result_df = pd.concat(sampled_list).reset_index(drop=True)
    y_out = result_df['_outcome']
    x_out = result_df.drop(columns=['_outcome'])
    
    if list_val:
        return {'x': x_out, 'y': y_out}
    else:
        x_out[yname] = y_out
        return x_out

# r2py:entity:upSample
def upSample(x, y, list_val=False, yname="Class"):
    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)
    
    y = np.array(y)
    counts = pd.Series(y).value_counts()
    max_class = counts.max()
    
    df = x.copy()
    df['_outcome'] = y
    
    sampled_list = []
    labels = sorted(counts.index)
    for label in labels:
        subset = df[df['_outcome'] == label]
        if len(subset) < max_class:
            diff = max_class - len(subset)
            extra = subset.sample(n=diff, replace=True)
            sampled_subset = pd.concat([subset, extra])
        else:
            sampled_subset = subset.sample(n=max_class)
        sampled_list.append(sampled_subset)
        
    result_df = pd.concat(sampled_list).reset_index(drop=True)
    y_out = result_df['_outcome']
    x_out = result_df.drop(columns=['_outcome'])
    
    if list_val:
        return {'x': x_out, 'y': y_out}
    else:
        x_out[yname] = y_out
        return x_out

fattyAcids = pd.DataFrame(fattyAcids)
oilType = np.array(oilType)

# r2py:entity:table
def r_table_print(y):
    counts = pd.Series(y).value_counts().sort_index()
    print("      oilType")
    print(" " + "  ".join(counts.index))
    print(" ".join(map(str, counts.values)))

r_table_print(oilType)

# Setup pandas output to match R's style more closely (1-based index, no scientific notation)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.precision', 1)

def print_r_style(df):
    # R dataframes start index at 1
    df_copy = df.copy()
    df_copy.index = df_copy.index + 1
    print(df_copy)

# r2py:entity:downSample
down_sampled = downSample(fattyAcids, oilType)
print_r_style(down_sampled)

# r2py:entity:upSample
up_sampled = upSample(fattyAcids, oilType)
print_r_style(up_sampled)