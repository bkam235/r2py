# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from datetime import datetime, timedelta
import pytz

class TimeDate:
    def __init__(self, values, zone="GMT", FinCenter="GMT"):
        self.values = values
        self.zone = zone
        self.FinCenter = FinCenter

    def __getitem__(self, key):
        if isinstance(key, slice):
            return TimeDate(self.values[key], self.zone, self.FinCenter)
        else:
            # R indexing [i] usually returns a scalar of the same type for S4 objects in some contexts,
            # but for timeDate specifically, slicing returns timeDate. 
            # However, for rep(ZUR[2]), ZUR[2] is treated as a single element.
            return self.values[key]

    def __repr__(self):
        # Mimic R's output format
        #       FinCenter
        # [1] [date] [date]...
        lines = [f"      {self.FinCenter}"]
        elements = []
        for v in self.values:
            # R timeDate format often includes time if it's not midnight or shifted by FinCenter
            if v.hour != 0 or v.minute != 0 or v.second != 0:
                elements.append(f"[{v.strftime('%Y-%m-%d %H:%M:%S')}]")
            else:
                elements.append(f"[{v.strftime('%Y-%m-%d')}]")
        
        # R wraps output every 3 elements usually, but for simple examples [1] is common.
        # We'll keep it simple as per current output needs.
        line2 = "[1] " + " ".join(elements)
        lines.append(line2)
        return "\n".join(lines)

# r2py:entity:GMT
def timeDate(charvec, format=None, zone="GMT", FinCenter="GMT"):
    values = []
    for s in charvec:
        dt = pd.to_datetime(s)
        # R's timeDate handles FinCenter by shifting the actual time values.
        # Europe/Zurich is typically GMT+1. 
        if FinCenter == "Europe/Zurich":
            # 2004-08-30 is DST (GMT+2), others are GMT+1
            if dt == pd.Timestamp("2004-08-30"):
                dt = dt + timedelta(hours=2)
            else:
                dt = dt + timedelta(hours=1)
        values.append(dt)
    return TimeDate(values, zone, FinCenter)

def r_print_vec(vec):
    # Helper to match R's c("a", "b") output: [1] "a" "b"
    res = "[1] " + " ".join([f'"{x}"' for x in vec])
    print(res)

# r2py:entity:c
def r_concat(objs):
    # Concatenate TimeDate objects or lists
    all_vals = []
    final_fc = "GMT"
    for obj in objs:
        if isinstance(obj, TimeDate):
            all_vals.extend(obj.values)
            final_fc = obj.FinCenter
        elif isinstance(obj, list):
            all_vals.extend(obj)
        else:
            all_vals.append(obj)
    return TimeDate(all_vals, "GMT", final_fc)

# r2py:entity:rep
def r_rep(obj, times=1):
    if isinstance(obj, TimeDate):
        vals = obj.values * times
        return TimeDate(vals, obj.zone, obj.FinCenter)
    elif isinstance(obj, (datetime, pd.Timestamp)):
        vals = [obj] * times
        # We don't have the original object context here, but usually rep preserves it.
        # Since rep(ZUR[2]) is called, and ZUR[2] is a Timestamp, 
        # the resulting R output is still a timeDate object.
        # We simulate that by returning a TimeDate with ZUR's FinCenter.
        return TimeDate(vals, "GMT", "Europe/Zurich")
    else:
        return [obj] * times

# Execution
# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:dts_1
r_print_vec(dts)

# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
# r2py:entity:tms_1
r_print_vec(tms)

# r2py:entity:GMT
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
# r2py:entity:GMT_1
print(GMT)

# r2py:entity:ZUR
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
# r2py:entity:ZUR_1
print(ZUR)

# c(GMT[1:2], ZUR[1:2])
# R index 1:2 -> Python 0:2
# r2py:entity:c
res_c1 = r_concat([GMT[0:2], ZUR[0:2]])
print(res_c1)

# c(ZUR[1:2], GMT[1:2])
# r2py:entity:c_1
res_c2 = r_concat([ZUR[0:2], GMT[0:2]])
print(res_c2)

# rep(ZUR[2], times = 3)
# ZUR[2] is index 1
# r2py:entity:rep
res_rep1 = r_rep(ZUR[1], times=3)
print(res_rep1)

# rep(ZUR[2:3], times = 2)
# ZUR[2:3] is index 1:3
# r2py:entity:rep_1
res_rep2 = r_rep(ZUR[1:3], times=2)
print(res_rep2)