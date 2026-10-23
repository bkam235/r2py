# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__summary_tidiers_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__summary_tidiers_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['s', 'v']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:s
class Summary:
    """Mimics the object returned by R's summary() for a numeric vector."""
    def __init__(self, data):
        self.data = np.array(data)
        self.clean_data = self.data[~pd.isna(self.data)]
        
        self.stats_dict = {
            "minimum": np.min(self.clean_data) if len(self.clean_data) > 0 else np.nan,
            "q1": np.percentile(self.clean_data, 25) if len(self.clean_data) > 0 else np.nan,
            "median": np.median(self.clean_data) if len(self.clean_data) > 0 else np.nan,
            "mean": np.mean(self.clean_data) if len(self.clean_data) > 0 else np.nan,
            "q3": np.percentile(self.clean_data, 75) if len(self.clean_data) > 0 else np.nan,
            "maximum": np.max(self.clean_data) if len(self.clean_data) > 0 else np.nan,
        }
        self.nas = np.sum(pd.isna(self.data))

    def __repr__(self):
        # R's summary(numeric) prints a table with headers and values on two lines
        headers = "      Min.   1st Qu.    Median      Mean   3rd Qu.      Max. "
        vals = f"{self.stats_dict['minimum']:10.6f} {self.stats_dict['q1']:10.6f} {self.stats_dict['median']:10.6f} {self.stats_dict['mean']:10.6f} {self.stats_dict['q3']:10.6f} {self.stats_dict['maximum']:10.6f}"
        res = f"{headers}\n{vals}"
        if self.nas > 0:
            res += f"\nNA's   : {int(self.nas)}"
        return res

def summary(v):
    return Summary(v)

# r2py:entity:tidy
def tidy(x):
    if isinstance(x, Summary):
        df = pd.DataFrame([x.stats_dict])
        if x.nas > 0:
            df['na'] = int(x.nas)
        df.index = [1]
        return df
    raise TypeError(f"No tidy method for objects of class {type(x)}")

# r2py:entity:glance
def glance(x):
    if isinstance(x, Summary):
        return tidy(x)
    raise TypeError(f"No glance method for objects of class {type(x)}")

# r2py:entity:v
# v is provided by data_shim

# r2py:entity:s
s = summary(v)
# r2py:entity:s_1
print(s)

# r2py:entity:tidy
res_tidy = tidy(s)
print(res_tidy)

# r2py:entity:glance
res_glance = glance(s)
print(res_glance)

# r2py:entity:v2
v2 = np.append(v, np.nan)

# r2py:entity:tidy_1
res_tidy_v2 = tidy(summary(v2))
print(res_tidy_v2)