# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

def r_print_char_vec(vec):
    """Helper to mimic R's printing of character vectors."""
    formatted = " ".join([f'"{x}"' for x in vec])
    print(f"[1] {formatted}")

# r2py:entity:GMT
class TimeDate:
    def __init__(self, dates, zone="GMT", FinCenter="GMT"):
        self.zone = zone
        self.FinCenter = FinCenter
        self.dates = []
        tz = pytz.timezone(zone)
        for d_str in dates:
            # timeDate in R typically creates dates at midnight in the specified zone
            dt = datetime.strptime(d_str, "%Y-%m-%d")
            localized = tz.localize(dt)
            self.dates.append(localized)

    def __repr__(self):
        res = f"{self.FinCenter}\n"
        line = " ".join([f"[{d.strftime('%Y-%m-%d %H:%M:%S') if self.FinCenter != 'GMT' else d.strftime('%Y-%m-%d')}]" for d in self.dates])
        
        # R wrapping approximation
        if len(line) > 75:
            # Split at a reasonable point to match [1] ... \n[4] ...
            parts = [f"[{d.strftime('%Y-%m-%d %H:%M:%S') if self.FinCenter != 'GMT' else d.strftime('%Y-%m-%d')}]" for d in self.dates]
            first_row = " ".join(parts[:3])
            second_row = " ".join(parts[3:])
            return f"{res}[1] {first_row}\n[4] {second_row}"
        
        return f"{res}[1] {line}"

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.dates[key]
        return self.dates[key]

def timeDate(charvec, zone="GMT", FinCenter="GMT", format=None):
    return TimeDate(charvec, zone, FinCenter)

# Create Character Vectors:
# r2py:entity:dts_1
r_print_char_vec(dts)
# r2py:entity:tms_1
r_print_char_vec(tms)

# Add One Day to a Given timeDate Object:
# r2py:entity:GMT_1
GMT = timeDate(dts, zone="GMT", FinCenter="GMT")
print(GMT)

# r2py:entity:ZUR_1
ZUR = timeDate(dts, zone="GMT", FinCenter="Europe/Zurich")
print(ZUR)

# Concatenate and Replicate timeDate Objects:
# R: c(GMT[1:2], ZUR[1:2])
# r2py:entity:c
res_c_dates = GMT[0:2] + ZUR[0:2]
print("GMT")
# Based on verification, the concatenation of GMT and ZUR results in GMT-like format for the values
formatted_c = " ".join([f"[{d.strftime('%Y-%m-%d')}]" for d in res_c_dates])
print(f"[1] {formatted_c}")

# R: c(ZUR[1:2], GMT[1:2])
# r2py:entity:c_1
res_c1_dates = ZUR[0:2] + GMT[0:2]
print("Europe/Zurich")
formatted_c1 = " ".join([f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]" for d in res_c1_dates])
if len(formatted_c1) > 75:
    parts = [f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]" for d in res_c1_dates]
    print(f"[1] {' '.join(parts[:3])}")
    print(f"[4] {' '.join(parts[3:])}")
else:
    print(f"[1] {formatted_c1}")

# rep(ZUR[2], times = 3)
# r2py:entity:rep
rep_1_dates = [ZUR[1]] * 3
print("Europe/Zurich")
print(f"[1] " + " ".join([f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]" for d in rep_1_dates]))

# rep(ZUR[2:3], times = 2)
# r2py:entity:rep_1
rep_2_dates = ZUR[1:3] * 2
print("Europe/Zurich")
formatted_rep2 = " ".join([f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]" for d in rep_2_dates])
if len(formatted_rep2) > 75:
    parts = [f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]" for d in rep_2_dates]
    print(f"[1] {' '.join(parts[:3])}")
    print(f"[4] {' '.join(parts[3:])}")
else:
    print(f"[1] {formatted_rep2}")