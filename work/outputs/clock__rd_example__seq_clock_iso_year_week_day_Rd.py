# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__seq_clock_iso_year_week_day_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__seq_clock_iso_year_week_day_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:set_week
def get_iso_week_count(year):
    # ISO year has 53 weeks if Jan 1 is Thursday OR Jan 1 is Wed and it's a leap year.
    jan1_weekday = datetime(year, 1, 1).weekday()  # Monday=0, Sunday=6
    # R's clock/ISO: Thursday is weekday 3 in Python's 0-6 (Mon-Sun)
    if (jan1_weekday == 3) or \
       (jan1_weekday == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))):
        return 53
    return 52

# R: x <- seq(iso_year_week_day(2020), iso_year_week_day(2026), by = 2)
# r2py:entity:x
x = np.arange(2020, 2027, 2)

# R printing: x
# r2py:entity:x_1
print("<iso_year_week_day<year>[4]>")
formatted_x = ' '.join([f'"{year}"' for year in x])
print(f'[1] {formatted_x}')

# R: set_week(x, "last")
# r2py:entity:set_week
res_weeks = []
for year in x:
    last_week = get_iso_week_count(year)
    res_weeks.append(f"{year}-W{last_week}")

# R printing: set_week(x, "last")
print("<iso_year_week_day<week>[4]>")
formatted_weeks = ' '.join([f'"{w}"' for w in res_weeks])
print(f'[1] {formatted_weeks}')