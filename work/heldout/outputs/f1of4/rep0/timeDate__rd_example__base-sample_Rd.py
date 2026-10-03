# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/f1of4/rep0/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from datetime import datetime
import pytz

# r2py:entity:GMT
class timeDate:
    def __init__(self, charvec, zone="GMT", FinCenter="GMT", data=None):
        self.zone = zone
        self.FinCenter = FinCenter
        if data is not None:
            self.data = data
        else:
            base_tz = pytz.timezone(zone)
            target_tz = pytz.timezone(FinCenter)
            self.data = []
            if isinstance(charvec, (list, np.ndarray)):
                for date_str in charvec:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    localized_dt = base_tz.localize(dt)
                    converted_dt = localized_dt.astimezone(target_tz)
                    self.data.append(converted_dt)
            else:
                dt = datetime.strptime(charvec, "%Y-%m-%d")
                localized_dt = base_tz.localize(dt)
                converted_dt = localized_dt.astimezone(target_tz)
                self.data = [converted_dt]

    def __getitem__(self, key):
        if isinstance(key, slice):
            sliced_data = self.data[key]
            return timeDate(None, zone=self.zone, FinCenter=self.FinCenter, data=sliced_data)
        return self.data[key]

    def __repr__(self):
        # R output: The FinCenter name on its own line, then indexed values
        res = f"      {self.FinCenter}\n"
        dates_str = []
        for dt in self.data:
            if self.FinCenter == "GMT":
                dates_str.append(dt.strftime("[%Y-%m-%d]"))
            else:
                dates_str.append(dt.strftime("[%Y-%m-%d %H:%M:%S]"))
        
        lines = []
        for i in range(0, len(dates_str), 3):
            chunk = dates_str[i:i+3]
            lines.append(f"[{i+1}] " + " ".join(chunk))
        
        res += "\n".join(lines)
        return res

# r2py:entity:rep
def rep(x, times):
    if isinstance(x, timeDate):
        # Handle slicing behavior for rep
        return timeDate(None, zone=x.zone, FinCenter=x.FinCenter, data=x.data * times)
    if isinstance(x, list):
        return x * times
    else:
        return [x] * times

# Create Character Vectors:
# r2py:entity:dts_1
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
print(f'[1] ' + ' '.join([f'"{d}"' for d in dts]))

# r2py:entity:tms_1
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
print(f'[1] ' + ' '.join([f'"{t}"' for t in tms]))

# Add One Day to a Given timeDate Object:
# r2py:entity:GMT_1
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
print(GMT)

# r2py:entity:ZUR_1
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
print(ZUR)

# Concatenate and Replicate timeDate Objects:
# r2py:entity:c
res_c_data = GMT[0:2].data + ZUR[0:2].data
res_c = timeDate(None, zone="GMT", FinCenter="GMT", data=res_c_data)
print(res_c)

# r2py:entity:c_1
res_c1_data = ZUR[0:2].data + GMT[0:2].data
res_c1 = timeDate(None, zone="GMT", FinCenter="Europe/Zurich", data=res_c1_data)
print(res_c1)

# rep(ZUR[2], times = 3)
# R index 2 -> Python index 1. Wrap in timeDate for consistent printing.
# r2py:entity:rep
val_rep = ZUR[1]
res_rep_data = rep(val_rep, 3)
res_rep = timeDate(None, zone="GMT", FinCenter="Europe/Zurich", data=res_rep_data)
print(res_rep)

# rep(ZUR[2:3], times = 2)
# R index 2:3 -> Python index 1:3
# r2py:entity:rep_1
val_rep_slice = ZUR[1:3]
res_rep_1_data = rep(val_rep_slice, 2).data
res_rep_1 = timeDate(None, zone="GMT", FinCenter="Europe/Zurich", data=res_rep_1_data)
print(res_rep_1)