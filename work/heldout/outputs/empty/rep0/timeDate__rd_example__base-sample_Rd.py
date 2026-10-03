# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
from datetime import datetime

# r2py:entity:ZUR
class timeDate:
    def __init__(self, charvec, format=None, zone="", FinCenter=""):
        self.zone = zone
        self.FinCenter = FinCenter
        self.data = []
        for item in charvec:
            # Handle strings or timeDate objects
            date_str = item.data[0] if isinstance(item, timeDate) else str(item)
            
            try:
                if ' ' in date_str:
                    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                else:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                # Fallback for other formats if necessary
                dt = datetime.fromisoformat(date_str)
            self.data.append(dt)

    def __repr__(self):
        # Mimic R output: Header then bracketed dates
        header = self.FinCenter if self.FinCenter else self.zone
        dates = " ".join([f"[{d.strftime('%Y-%m-%d' if d.hour==0 and d.minute==0 and d.second==0 else '%Y-%m-%d %H:%M:%S')}]" for d in self.data])
        return f"{header}\n[1] {dates}"

    def __getitem__(self, key):
        # Support R-style slicing (1-based) and index
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self.data)
            # Adjust for R 1-based indexing in the source call GMT[1:2]
            # The shim provides data, but the R code does c(GMT[1:2], ZUR[1:2])
            # We assume slice is provided as 0-based by Python logic if converted, 
            # but here we must handle the logic carefully.
            subset = [self.data[i] for i in range(start, stop)]
            new_obj = timeDate([])
            new_obj.zone = self.zone
            new_obj.FinCenter = self.FinCenter
            new_obj.data = subset
            return new_obj
        else:
            # Single index
            val = self.data[key]
            new_obj = timeDate([])
            new_obj.zone = self.zone
            new_obj.FinCenter = self.FinCenter
            new_obj.data = [val]
            return new_obj

# r2py:entity:c
def r_c(*args):
    # Concatenate timeDate objects or lists
    combined_data = []
    fin_center = ""
    zone = ""
    for arg in args:
        if isinstance(arg, timeDate):
            combined_data.extend(arg.data)
            fin_center = arg.FinCenter
            zone = arg.zone
        elif isinstance(arg, list):
            combined_data.extend(arg)
        else:
            combined_data.append(arg)
    
    res = timeDate(combined_data)
    res.FinCenter = fin_center
    res.zone = zone
    return res

# r2py:entity:rep
def r_rep(x, times=1):
    # Replicate timeDate objects
    if isinstance(x, timeDate):
        data = x.data * times
        res = timeDate(data)
        res.FinCenter = x.FinCenter
        res.zone = x.zone
        return res
    else:
        return np.tile(x, times)

# Execute the R script logic
# r2py:entity:dts_1
print(dts)

# r2py:entity:tms_1
print(tms)

# R: GMT = timeDate(dts, zone = "GMT", FinCenter = "GMT")
# r2py:entity:GMT_1
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
print(GMT)

# R: ZUR = timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
# r2py:entity:ZUR_1
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
print(ZUR)

# R: c(GMT[1:2], ZUR[1:2])
# In R, [1:2] means indices 1 and 2. In Python [0:2]
# r2py:entity:c
print(r_c(GMT[0:2], ZUR[0:2]))

# R: c(ZUR[1:2], GMT[1:2])
# r2py:entity:c_1
print(r_c(ZUR[0:2], GMT[0:2]))

# R: rep(ZUR[2], times = 3)
# r2py:entity:rep
print(r_rep(ZUR[1], times=3))

# R: rep(ZUR[2:3], times = 2)
# r2py:entity:rep_1
print(r_rep(ZUR[1:3], times=2))