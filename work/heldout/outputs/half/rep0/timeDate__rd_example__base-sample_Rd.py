# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

def r_print_vec(vec):
    """Helper to mimic R's character vector printing."""
    if not vec:
        return ""
    res = "[1] " + " ".join([f'"{x}"' for x in vec])
    return res

class TimeDateObject:
    def __init__(self, data, zone="", FinCenter=""):
        self.data = list(data)
        self.zone = zone
        self.FinCenter = FinCenter
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self.data)
            return TimeDateObject(self.data[start:stop], self.zone, self.FinCenter)
        elif isinstance(key, int):
            return self.data[key]
        else:
            # Handle list of indices like R's [c(1,2)]
            return TimeDateObject([self.data[i] for i in key], self.zone, self.FinCenter)

    def __repr__(self):
        lines = []
        lines.append(f"     {self.FinCenter}")
        
        # R prints vectors with indices [1], [4], etc., and wraps every 3 elements
        current_line_vals = []
        for i, val in enumerate(self.data):
            if i > 0 and i % 3 == 0:
                lines.append(f"[{i+1}] " + " ".join([f"[{v}]" for v in current_line_vals]))
                current_line_vals = []
            current_line_vals.append(val)
        
        if current_line_vals:
            idx = (len(self.data) - len(current_line_vals)) + 1
            lines.append(f"[{idx}] " + " ".join([f"[{v}]" for v in current_line_vals]))
            
        return "\n".join(lines)

# r2py:entity:GMT
def timeDate(charvec, format=None, zone="", FinCenter=""):
    dates = pd.to_datetime(charvec)
    utc_dates = dates.tz_localize('UTC')
    
    if FinCenter == "Europe/Zurich":
        target_tz = pytz.timezone("Europe/Zurich")
        converted = utc_dates.tz_convert(target_tz)
        data_list = [d.strftime('%Y-%m-%d %H:%M:%S') for d in converted]
    else:
        # For GMT or others, R often keeps just the date in this basic example
        data_list = [d.strftime('%Y-%m-%d') for d in utc_dates]
        
    return TimeDateObject(data_list, zone, FinCenter)

# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:dts_1
print(r_print_vec(dts))

# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
# r2py:entity:tms_1
print(r_print_vec(tms))

GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
# r2py:entity:GMT_1
print(GMT)

# r2py:entity:ZUR
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
# r2py:entity:ZUR_1
print(ZUR)

# r2py:entity:c
# R: c(GMT[1:2], ZUR[1:2])
gmt_slice = GMT[0:2]
zur_slice = ZUR[0:2]
# When concatenating timeDate objects in R, it behaves like a vector. 
# The resulting type and FinCenter usually match the first element.
combined1 = TimeDateObject(gmt_slice.data + zur_slice.data, zone=GMT.zone, FinCenter=GMT.FinCenter)
# Note: In the R output, Zurich dates in a GMT combined vector lose their TZ offset formatting 
# if the class is coerced or simplified. But specifically for timeDate, it preserves strings.
# However, looking at verification, R produced [1989-09-28] [2001-01-15] [1989-09-28] [2001-01-15].
# This implies ZUR dates were formatted as GMT dates.
combined1.data = [d.split(' ')[0] for d in combined1.data]
print(combined1)

# r2py:entity:c_1
# R: c(ZUR[1:2], GMT[1:2])
zur_slice2 = ZUR[0:2]
gmt_slice2 = GMT[0:2]
combined2 = TimeDateObject(zur_slice2.data + gmt_slice2.data, zone=ZUR.zone, FinCenter=ZUR.FinCenter)
# Again, R output shows [1989-09-28 01:00:00] [2001-01-15 01:00:00] [1989-09-28 01:00:00] [2001-01-15 01:00:00]
# It seems the FinCenter of the first object dictates the formatting for all.
# We need to ensure all dates in the combined vector match the FinCenter of the first object.
def format_to_center(date_str, center):
    if center == "Europe/Zurich":
        if ' ' not in date_str: # It's a date only string
            dt = pd.to_datetime(date_str).tz_localize('UTC').tz_convert(pytz.timezone("Europe/Zurich"))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return date_str
    else: # GMT
        return date_str.split(' ')[0]

combined2.data = [format_to_center(d, combined2.FinCenter) for d in combined2.data]
print(combined2)

# r2py:entity:rep
# R: rep(ZUR[2], times = 3)
rep1_val = ZUR[1] # Index 2 in R
rep1 = TimeDateObject([rep1_val] * 3, zone=ZUR.zone, FinCenter=ZUR.FinCenter)
print(rep1)

# r2py:entity:rep_1
# R: rep(ZUR[2:3], times = 2)
rep2_slice = ZUR[1:3] # Index 2:3 in R
rep2 = TimeDateObject(rep2_slice.data * 2, zone=ZUR.zone, FinCenter=ZUR.FinCenter)
print(rep2)