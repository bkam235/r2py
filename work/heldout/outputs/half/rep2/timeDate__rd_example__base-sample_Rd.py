import pandas as pd
import numpy as np
from datetime import datetime

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:ZUR
class TimeDateVector:
    def __init__(self, data, zone="", fin_center=""):
        self.data = list(data)
        self.zone = zone
        self.fin_center = fin_center

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Handle R-style 1-based indexing via shim or manual logic
            # The shim provides Python lists, so we use standard Python slicing
            return TimeDateVector([self.data[i] for i in range(key.start or 0, key.stop)], self.zone, self.fin_center)
        else:
            # Return a single element as a TimeDateVector of length 1 to mimic R's vector behavior
            return TimeDateVector([self.data[key]], self.zone, self.fin_center)

    def __repr__(self):
        # Mimic R's print output roughly
        return f"{self.fin_center}\n[1] " + " ".join([f"[{d}]" for d in self.data])

def timeDate(charvec, zone="", FinCenter="", format=None):
    # Simple implementation to match the R metadata structure
    return TimeDateVector(charvec, zone, FinCenter)

# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]
# r2py:entity:dts_1
print(dts)

# r2py:entity:tms
tms = ["23:12:55", "10:34:02", "08:30:00", "11:18:23"]
# r2py:entity:tms_1
print(tms)

GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
# r2py:entity:GMT_1
print(GMT)

ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
# r2py:entity:ZUR_1
print(ZUR)

# Concatenate vectors: GMT[1:2] (idx 0,1) and ZUR[1:2] (idx 0,1)
# r2py:entity:c
res_c1 = TimeDateVector(GMT[0:2].data + ZUR[0:2].data, zone="GMT", fin_center="GMT")
print(res_c1)

# r2py:entity:c_1
res_c2 = TimeDateVector(ZUR[0:2].data + GMT[0:2].data, zone="GMT", fin_center="Europe/Zurich")
print(res_c2)

# rep(ZUR[2], times=3) -> ZUR index 1 repeated 3 times
# r2py:entity:rep
res_rep1 = TimeDateVector([ZUR[1].data[0]] * 3, zone="GMT", fin_center="Europe/Zurich")
print(res_rep1)

# rep(ZUR[2:3], times=2) -> sequence [ZUR[1], ZUR[2]] repeated twice
# r2py:entity:rep_1
seq = ZUR[1:3].data
res_rep2 = TimeDateVector(seq * 2, zone="GMT", fin_center="Europe/Zurich")
print(res_rep2)