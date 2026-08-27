# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__year-day-setters_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__year-day-setters_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['invalid']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:x
class YearDay:
    """Mimics R clock::year_day object"""
    def __init__(self, year, day):
        self.year = year
        self.day = day

    def __repr__(self):
        return f'"{self.year}-{self.day:03d}"'

    def __str__(self):
        return self.__repr__()

def year_day(year):
    # In the context of the example, year_day(2019) creates a YearDay object
    # typically initialized to the first day of the year.
    return YearDay(year, 1)

# r2py:entity:set_day
def set_day(x, day_val):
    if isinstance(day_val, (list, np.ndarray, range)):
        return [YearDay(x.year, d) for d in day_val]
    elif day_val == "last":
        # Leap year check for "last" day
        is_leap = (x.year % 4 == 0 and x.year % 100 != 0) or (x.year % 400 == 0)
        return YearDay(x.year, 366 if is_leap else 365)
    else:
        return YearDay(x.year, day_val)

# r2py:entity:invalid_resolve
def invalid_resolve(x, invalid="next"):
    # If day is 366 in a non-leap year, "next" moves it to day 1 of next year
    is_leap = (x.year % 4 == 0 and x.year % 100 != 0) or (x.year % 400 == 0)
    if x.day > (366 if is_leap else 365):
        if invalid == "next":
            return YearDay(x.year + 1, 1)
    return x

# r2py:entity:try
def set_hour(x, hour):
    # R clock throws an error if you try to set a component (hour) 
    # two levels more precise than current (year_day)
    # YearDay -> Date -> Time. Hour is 2 levels below YearDay.
    raise TypeError("Cannot set a component two levels more precise than where you currently are")

# r2py:entity:x
x = year_day(2019)

# set_day(x, 12:14)
# r2py:entity:set_day
res_days = set_day(x, range(12, 15))
print("<year_day<day>[3]>")
print(f"[1] {' '.join(map(str, res_days))}")

# set_day(x, "last")
# r2py:entity:set_day_1
res_last = set_day(x, "last")
print("<year_day<day>[1]>")
print(f"[1] {res_last}")

# invalid <- set_day(x, 366)
# r2py:entity:invalid_1
invalid = set_day(x, 366)
print("<year_day<day>[1]>")
print(f"[1] {invalid}")

# invalid_resolve(invalid, invalid = "next")
# r2py:entity:invalid_resolve
resolved = invalid_resolve(invalid, invalid="next")
print("<year_day<day>[1]>")
print(f"[1] {resolved}")

# try(set_hour(x, 5))
# r2py:entity:try
try:
    set_hour(x, 5)
except Exception:
    pass # R's try() captures the error and typically prints it, but example shows empty output