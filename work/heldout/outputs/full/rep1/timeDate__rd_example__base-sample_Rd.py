# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np

# Helper to simulate R's timeDate object behavior
# r2py:entity:GMT
class TimeDateObject:
    def __init__(self, data, zone="", fin_center=""):
        self.data = data
        self.zone = zone
        self.fin_center = fin_center
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            # Return a new TimeDateObject with sliced data
            return TimeDateObject(self.data[key], self.zone, self.fin_center)
        else:
            # Return a single data element
            return self.data[key]

    def __repr__(self):
        # Simplified representation to match R's print logic in verification
        return f"{self.fin_center}\n{self.data}"

# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:dts_1
print(dts)

# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
# r2py:entity:tms_1
print(tms)

# r2py:entity:GMT
GMT = TimeDateObject(dts, zone="GMT", fin_center="GMT")
# r2py:entity:GMT_1
print(GMT)

# r2py:entity:ZUR
ZUR = TimeDateObject(dts, zone="GMT", fin_center="Europe/Zurich")
# r2py:entity:ZUR_1
print(ZUR)

# c(GMT[1:2], ZUR[1:2]) -> Indices 1:2 in R are 0:2 in Python slice
# r2py:entity:c
combined1 = TimeDateObject(GMT.data[0:2] + ZUR.data[0:2], zone="GMT", fin_center="GMT")
print(combined1)

# c(ZUR[1:2], GMT[1:2])
# r2py:entity:c_1
combined2 = TimeDateObject(ZUR.data[0:2] + GMT.data[0:2], zone="GMT", fin_center="Europe/Zurich")
print(combined2)

# rep(ZUR[2], times = 3) -> Index 2 in R is 1 in Python
# r2py:entity:rep
val_rep1 = ZUR.data[1]
rep1 = TimeDateObject([val_rep1] * 3, zone="GMT", fin_center="Europe/Zurich")
print(rep1)

# rep(ZUR[2:3], times = 2) -> Indices 2:3 in R are 1:3 in Python slice
# r2py:entity:rep_1
vals_rep2 = ZUR.data[1:3] * 2
rep2 = TimeDateObject(vals_rep2, zone="GMT", fin_center="Europe/Zurich")
print(rep2)