# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__calendar-boundary_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__calendar-boundary_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# x <- year_month_day(2019, 2:4, 5, 6)
# r2py:entity:x
years = [2019] * 3
months = [2, 3, 4]
days = [5] * 3
hours = [6] * 3

x = pd.to_datetime([
    pd.Timestamp(year=y, month=m, day=d, hour=h) 
    for y, m, d, h in zip(years, months, days, hours)
])

# r2py:entity:x_1
print("      <year_month_day<hour>[3]>")
formatted_x = " ".join([f'"{t.strftime("%Y-%m-%dT%H")}"' for t in x])
print(f"[1] {formatted_x}")

# calendar_start(x, "month")
# r2py:entity:calendar_start
res_start = x.to_period('M').to_timestamp()
print("      <year_month_day<hour>[3]>")
formatted_start = " ".join([f'"{t.strftime("%Y-%m-%dT%H")}"' for t in res_start])
print(f"[1] {formatted_start}")

# calendar_end(x, "month")
# R's calendar_end for "month" sets to the last day of the month at 23:00
# r2py:entity:calendar_end
res_end_raw = x.to_period('M').to_timestamp(how='end')
res_end = res_end_raw.floor('D') + pd.Timedelta(hours=23)
print("      <year_month_day<hour>[3]>")
formatted_end = " ".join([f'"{t.strftime("%Y-%m-%dT%H")}"' for t in res_end])
print(f"[1] {formatted_end}")