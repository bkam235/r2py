# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__when-any-all_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__when-any-all_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['countries']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:x
x = pd.Series([True, True, True, False, False, False, pd.NA, pd.NA, pd.NA], dtype='boolean')
# r2py:entity:y
y = pd.Series([True, False, pd.NA, True, False, pd.NA, True, False, pd.NA], dtype='boolean')

def format_bool(val):
    if pd.isna(val): return "NA"
    return "TRUE" if val is True else "FALSE" if val is False else str(val).upper()

# r2py:entity:any
def r_any(*args):
    if not args: return False
    vals = []
    for a in args:
        if isinstance(a, pd.Series): vals.extend(a.tolist())
        else: vals.append(a)
    found_true = any(v is True for v in vals)
    if found_true: return True
    if any(pd.isna(v) for v in vals): return pd.NA
    return False

# r2py:entity:all
def r_all(*args):
    if not args: return True
    vals = []
    for a in args:
        if isinstance(a, pd.Series): vals.extend(a.tolist())
        else: vals.append(a)
    found_false = any(v is False for v in vals)
    if found_false: return False
    if any(pd.isna(v) for v in vals): return pd.NA
    return True

# r2py:entity:any
print(f"[1] {format_bool(r_any(x, y))}")
# r2py:entity:all
print(f"[1] {format_bool(r_all(x, y))}")

# r2py:entity:when_any
def when_any(*args, na_rm=False, size=None):
    if not args:
        if size is not None:
            return pd.Series([False] * size, dtype='boolean')
        return pd.Series([], dtype='boolean')
    series_list = [pd.Series(a, dtype='boolean') if not isinstance(a, pd.Series) else a.astype('boolean') for a in args]
    if na_rm:
        res = pd.Series(False, index=series_list[0].index, dtype='boolean')
        for s in series_list:
            res = res | s.fillna(False)
        return res
    else:
        res = series_list[0].copy()
        for s in series_list[1:]:
            res = res | s
        return res

# r2py:entity:when_all
def when_all(*args, na_rm=False, size=None):
    if not args:
        if size is not None:
            return pd.Series([True] * size, dtype='boolean')
        return pd.Series([], dtype='boolean')
    series_list = [pd.Series(a, dtype='boolean') if not isinstance(a, pd.Series) else a.astype('boolean') for a in args]
    if na_rm:
        res = pd.Series(True, index=series_list[0].index, dtype='boolean')
        for s in series_list:
            res = res & s.fillna(True)
        return res
    else:
        res = series_list[0].copy()
        for s in series_list[1:]:
            res = res & s
        return res

def print_r_vec(s):
    if s.empty: return
    vals = s.tolist()
    formatted = [format_bool(v) for v in vals]
    # Adjusted spacing to match R's [1]  TRUE  TRUE...
    print(f"[1]  {'  '.join(formatted)}")

# r2py:entity:when_any
print_r_vec(when_any(x, y))
print_r_vec(x | y)

# r2py:entity:when_all
print_r_vec(when_all(x, y))
print_r_vec(x & y)

# r2py:entity:tibble
def print_tibble(df):
    # Handle numeric formatting to avoid .0
    df_display = df.copy()
    for col in df_display.columns:
        if pd.api.types.is_float_dtype(df_display[col]):
            df_display[col] = df_display[col].apply(lambda x: f"{int(x)}" if pd.notna(x) and x == int(x) else x)

    print(f"# A tibble: {len(df)} × {len(df.columns)}")
    cols = df.columns.tolist()
    # R's tibble has specific column widths. 
    # For the first few examples, they are roughly 13 chars
    header = "  " + " ".join(f"{c:13}" for c in cols)
    print(header)
    types = ["<lgl>" if df[c].dtype == 'boolean' else "<chr>" if df[c].dtype == 'object' else "<dbl>" for c in cols]
    print("  " + " ".join(f"{t:13}" for t in types))
    for i, row in enumerate(df_display.itertuples(index=False), 1):
        row_vals = []
        for val in row:
            if pd.isna(val):
                row_vals.append(f"{'NA':13}")
            elif isinstance(val, (bool, np.bool_)):
                row_vals.append(f"{str(val).upper():13}")
            else:
                row_vals.append(f"{str(val):13}")
        print(f"{i} {' '.join(row_vals)}")

# r2py:entity:tibble
df_logic = pd.DataFrame({
    'x': x,
    'y': y,
    'any_propagate': when_any(x, y),
    'any_remove': when_any(x, y, na_rm=True),
    'all_propagate': when_all(x, y),
    'all_remove': when_all(x, y, na_rm=True)
})
print_tibble(df_logic)

# ---------------------------------------------------------------------------
# With `filter()` and `filter_out()`

# r2py:entity:countries
countries = pd.DataFrame(countries)
# R prints countries here
# r2py:entity:countries_1
print_tibble(countries)

# r2py:entity:filter
def between(s, left, right):
    return (s >= left) & (s <= right)

cond1 = (countries['name'].isin(["US", "CA"])) & (between(countries['score'], 200, 300))
cond2 = (countries['name'].isin(["PR", "RU"])) & (between(countries['score'], 100, 200))

# filter() logic
res_filter = countries[cond1 | cond2].reset_index(drop=True)
print_tibble(res_filter)

# r2py:entity:filter_1
res_any = when_any(cond1, cond2)
res_filter_any = countries[res_any.fillna(False)].reset_index(drop=True)
print_tibble(res_filter_any)

# r2py:entity:filter_out
res_filter_out = countries[~res_any.fillna(False)].reset_index(drop=True)
print_tibble(res_filter_out)

# ---------------------------------------------------------------------------
# Programming with `when_any()` and `when_all()`

# r2py:entity:size
size = len(x)

# Two inputs
# r2py:entity:inputs
inputs = [x, y]
# r2py:entity:when_all_1
print_r_vec(when_all(*inputs, size=size))

# One input
# r2py:entity:inputs_1
inputs_1 = [x]
# r2py:entity:when_all_2
print_r_vec(when_all(*inputs_1, size=size))

# Zero inputs
# r2py:entity:inputs_2
inputs_2 = []
# r2py:entity:when_all_3
print_r_vec(when_all(*inputs_2, size=size))

# When no inputs are provided, these functions are consistent with `any()`
# and `all()`
# r2py:entity:any_1
print(f"[1] {format_bool(r_any())}")
# r2py:entity:when_any_1
print_r_vec(when_any(size=1))

# r2py:entity:all_1
print(f"[1] {format_bool(r_all())}")
# r2py:entity:when_all_4
print_r_vec(when_all(size=1))