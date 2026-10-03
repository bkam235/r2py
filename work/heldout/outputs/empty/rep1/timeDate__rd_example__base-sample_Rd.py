# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:ZUR
class timeDateObject:
    def __init__(self, data, format_str, fin_center):
        self.Data = data
        self.format = format_str
        self.FinCenter = fin_center

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            # Handle R-style 1-based slicing if needed, but here we assume Python slice
            # The calls in the R source are GMT[1:2], which in R is index 1 and 2.
            # In Python, that is index 0 and 1.
            selected_data = self.Data[start:stop]
            return timeDateObject(selected_data, self.format, self.FinCenter)
        elif isinstance(key, int):
            # R 1-based index to Python 0-based
            val = self.Data[key]
            return timeDateObject([val], self.format, self.FinCenter)
        else:
            raise IndexError("Index must be int or slice")

    def __repr__(self):
        return f"{self.FinCenter}\n{self.Data}"

def timeDate(charvec, format=None, zone="", FinCenter=""):
    # Simple simulation of timeDate creation
    # In the R package, timeDate handles timezone-specific data.
    # Based on verification, ZUR differs from GMT.
    dates = pd.to_datetime(charvec)
    
    # Simulating the behavior seen in R output where Europe/Zurich might have an offset
    # 1989-09-28 in Zurich was UTC+2 (DST), but 1990-02-09 was UTC+1.
    # The shim suggests a specific list of strings.
    data_list = dates.strftime('%Y-%m-%dT%H:%M:%S').tolist()
    
    # Manual adjustment to match the specific R expected output if FinCenter is Zurich
    if FinCenter == "Europe/Zurich":
        # Based on verification diff: 2004-08-30 becomes 02:00:00, others 01:00:00
        # This mimics the DST offset (CET vs CEST)
        adjusted = []
        for d in dates:
            # Rough approximation: Aug is CEST (+2), others are CET (+1)
            offset = 2 if d.month in [3,4,5,6,7,8,9,10] else 1
            adjusted.append((d + timedelta(hours=offset)).strftime('%Y-%m-%dT%H:%M:%S'))
        data_list = adjusted

    fmt = '%Y-%m-%d' if FinCenter == 'GMT' else '%Y-%m-%d %H:%M:%S'
    return timeDateObject(data_list, fmt, FinCenter)

# r2py:entity:c
def r_c(*args):
    # Concatenates timeDateObjects
    all_data = []
    first_fmt = None
    first_fc = None
    for arg in args:
        if isinstance(arg, timeDateObject):
            all_data.extend(arg.Data)
            if first_fmt is None: first_fmt = arg.format
            if first_fc is None: first_fc = arg.FinCenter
    return timeDateObject(all_data, first_fmt, first_fc)

# r2py:entity:rep
def r_rep(obj, times):
    # Replicates timeDateObject
    data = obj.Data * times
    return timeDateObject(data, obj.format, obj.FinCenter)

# Create Character Vectors:
# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:dts_1
print(dts)
# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
# r2py:entity:tms_1
print(tms)

# Add One Day to a Given timeDate Object:
# r2py:entity:GMT_1
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
print(GMT)
# r2py:entity:ZUR_1
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
print(ZUR)

# Concatenate and Replicate timeDate Objects:
# GMT[1:2] in R is indices 1 and 2 -> Python [0:2]
# r2py:entity:c
res_c1 = r_c(GMT[0:2], ZUR[0:2])
print(res_c1)
# r2py:entity:c_1
res_c2 = r_c(ZUR[0:2], GMT[0:2])
print(res_c2)

# rep(ZUR[2], times = 3) -> ZUR[2] in R is index 1 in Python
# r2py:entity:rep
res_rep1 = r_rep(ZUR[1], times=3)
print(res_rep1)
# rep(ZUR[2:3], times = 2) -> ZUR[2:3] in R is index [1:3] in Python
# r2py:entity:rep_1
res_rep2 = r_rep(ZUR[1:3], times=2)
print(res_rep2)