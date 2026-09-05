# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__rd_example__vec-rep_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__vec-rep_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x', 'y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def r_print_df(df):
    """Helper to mimic R's data frame printing style more closely."""
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        return ""
    if not isinstance(df, pd.DataFrame):
        return str(df)
    header = " " + " ".join(df.columns)
    rows = []
    for i in range(len(df)):
        row_vals = " ".join(map(lambda x: f"{x:g}" if pd.notna(x) else "NA", df.iloc[i].values))
        rows.append(f"{i+1} {row_vals}")
    return header + "\n" + "\n".join(rows)

# r2py:entity:vec_rep
def vec_rep(x, times):
    if isinstance(x, pd.DataFrame):
        # Repeat rows of data frame
        res = pd.concat([x] * times, ignore_index=True)
        res.index = np.arange(1, len(res) + 1)
        return res
    return np.tile(x, times)

# r2py:entity:vec_rep_each
def vec_rep_each(x, times):
    if isinstance(x, pd.DataFrame):
        # Repeat rows of data frame each
        res = x.loc[x.index.repeat(times)].reset_index(drop=True)
        res.index = np.arange(1, len(res) + 1)
        return res
    return np.repeat(x, times)

# r2py:entity:vec_unrep
def vec_unrep(x):
    vals = np.array(x)
    if len(vals) == 0:
        return pd.DataFrame()
    
    mask = []
    for i in range(len(vals) - 1):
        a, b = vals[i], vals[i+1]
        if pd.isna(a) and pd.isna(b):
            mask.append(False) # R's vec_unrep treats NAs as equivalent
        elif pd.isna(a) or pd.isna(b):
            mask.append(True)
        else:
            mask.append(a != b)
    
    indices = [i + 1 for i, changed in enumerate(mask) if changed]
    indices = [0] + indices + [len(vals)]
    
    lengths = []
    values = []
    for i in range(len(indices) - 1):
        start, end = indices[i], indices[i+1]
        lengths.append(end - start)
        values.append(vals[start])
        
    df = pd.DataFrame({'key': values, 'times': lengths})
    df.index = np.arange(1, len(df) + 1)
    return df

# r2py:entity:rle
def rle(x):
    vals = np.array(x)
    if len(vals) == 0:
        return {"lengths": np.array([]), "values": vals}
    
    lengths = []
    values = []
    curr_val = vals[0]
    count = 0
    for v in vals:
        # rle treats adjacent missing values as different
        if (pd.isna(curr_val) or pd.isna(v) or curr_val != v):
            if count > 0:
                lengths.append(count)
                values.append(curr_val)
            curr_val = v
            count = 1
        else:
            count += 1
    lengths.append(count)
    values.append(curr_val)
    return {"lengths": np.array(lengths), "values": np.array(values)}

# r2py:entity:rep
def rep_r(df, each=None):
    """
    In R, rep(df, each=2) on a data frame repeats the data frame itself, 
    effectively returning a list of repeated data frames or columns.
    The specific output for rep(df, each=2) where df is data.frame(x=1:2, y=3:4)
    is a list with elements $x, $x, $y, $y containing 1 2, 1 2, 3 4, 3 4.
    """
    result = {}
    # To match the R output: $x [1] 1 2, $x [1] 1 2, $y [1] 3 4, $y [1] 3 4
    # Since Python dicts don't allow duplicate keys, we'll return a list of tuples
    res_list = []
    for col in df.columns:
        for _ in range(each if each else 1):
            res_list.append((col, df[col].values))
    return res_list

# Execution
# vec_rep(1:2, 3)
# r2py:entity:vec_rep
res1 = vec_rep(np.array([1, 2]), 3)
print(f"[1] {' '.join(map(str, res1))}")

# vec_rep_each(1:2, 3)
# r2py:entity:vec_rep_each
res2 = vec_rep_each(np.array([1, 2]), 3)
print(f"[1] {' '.join(map(str, res2))}")

# x <- vec_rep_each(1:2, c(3, 4))
# r2py:entity:x
x = vec_rep_each(np.array([1, 2]), np.array([3, 4]))
# x (printed in R)
print(f"[1] {' '.join(map(str, x))}")

# vec_unrep(x)
# r2py:entity:vec_unrep
print(r_print_df(vec_unrep(x)))

# df <- data.frame(x = 1:2, y = 3:4)
# r2py:entity:df
df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
df.index = np.arange(1, 3)

# rep(df, each = 2)
# r2py:entity:rep
rep_res = rep_r(df, each=2)
for k, v in rep_res:
    print(f"${k}")
    print(f"[1] {' '.join(map(str, v))}\n")

# vec_rep(df, 2)
# r2py:entity:vec_rep_1
print(r_print_df(vec_rep(df, 2)))

# vec_rep_each(df, 2)
# r2py:entity:vec_rep_each_1
print(r_print_df(vec_rep_each(df, 2)))

# y <- c(1, NA, NA, 2)
# r2py:entity:y
y = np.array([1, np.nan, np.nan, 2])

# rle(y)
# r2py:entity:rle
rle_y = rle(y)
print("Run Length Encoding")
print(f"  lengths: int [1:4] {' '.join(map(str, rle_y['lengths']))}")
vals_str = ' '.join(map(lambda v: 'NA' if pd.isna(v) else f"{v:g}", rle_y['values']))
print(f"  values : num [1:4] {vals_str}")

# vec_unrep(y)
# r2py:entity:vec_unrep_1
print(r_print_df(vec_unrep(y)))