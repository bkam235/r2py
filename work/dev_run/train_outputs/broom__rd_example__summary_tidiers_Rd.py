import numpy as np
import pandas as pd

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/train_outputs/broom__rd_example__summary_tidiers_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__summary_tidiers_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['s', 'v']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# v is provided by shim, but we ensure it is a numpy array for calculations
# r2py:entity:v
v = np.array(v)

# r2py:entity:s
def summary_numeric(x):
    x = np.array(x)
    mask = ~np.isnan(x)
    clean = x[mask]
    
    # R's summary(numeric) output format
    res = {
        "Min.": np.min(clean) if len(clean) > 0 else np.nan,
        "1st Qu.": np.quantile(clean, 0.25) if len(clean) > 0 else np.nan,
        "Median": np.median(clean) if len(clean) > 0 else np.nan,
        "Mean": np.mean(clean) if len(clean) > 0 else np.nan,
        "3rd Qu.": np.quantile(clean, 0.75) if len(clean) > 0 else np.nan,
        "Max.": np.max(clean) if len(clean) > 0 else np.nan,
    }
    na_count = np.sum(~mask)
    if na_count > 0:
        res["NA's"] = na_count
    return res

s = summary_numeric(v)
# R prints summary(v) which looks like:
#      Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# -2.70839 -0.68727 -0.01152 -0.01759  0.68458  3.66985
# We simulate this output format
summary_cols = ["Min.", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max."]
vals = [s[c] for c in summary_cols]
print(f"      {'  '.join(summary_cols)}")
print(f"{'  '.join([f'{val: .5f}' if not np.isnan(val) else 'NA' for val in vals])}")

# r2py:entity:tidy
def tidy(x):
    # broom::tidy.summary.numeric (or tidy.numeric)
    # transforms summary into a 1-row tibble
    mapping = {
        "Min.": "minimum",
        "1st Qu.": "q1",
        "Median": "median",
        "Mean": "mean",
        "3rd Qu.": "q3",
        "Max.": "maximum",
        "NA's": "na"
    }
    data = {mapping[k]: v for k, v in x.items() if k in mapping}
    return pd.DataFrame([data])

print(tidy(s))

# r2py:entity:glance
def glance(x):
    # For summary(numeric), glance returns the same as tidy in broom
    return tidy(x)

print(glance(s))

# r2py:entity:v2
v2 = np.append(v, np.nan)

# r2py:entity:tidy_1
print(tidy(summary_numeric(v2)))