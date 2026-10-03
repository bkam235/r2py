# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/f3of4/rep0/timeDate__rd_example__base-sample_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__base-sample_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['GMT', 'ZUR', 'dts', 'tms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:dts_1
print(dts)

# r2py:entity:tms_1
print(tms)

# timeDate translation: Creating timezone-aware datetimes
# R's timeDate for these parameters behaves like converting a date string to a specific zone
# r2py:entity:GMT
GMT_zone = pytz.timezone("GMT")
# r2py:entity:ZUR
ZUR_zone = pytz.timezone("Europe/Zurich")

# r2py:entity:GMT_1
print(GMT)

# r2py:entity:ZUR_1
print(ZUR)

# c(GMT[1:2], ZUR[1:2])
# r2py:entity:c
print(GMT[0:2] + ZUR[0:2])

# c(ZUR[1:2], GMT[1:2])
# r2py:entity:c_1
print(ZUR[0:2] + GMT[0:2])

# rep(ZUR[2], times = 3)
# r2py:entity:rep
print([ZUR[1]] * 3)

# rep(ZUR[2:3], times = 2)
# r2py:entity:rep_1
print(ZUR[1:3] * 2)