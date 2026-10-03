# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/clock__rd_example__iso-year-week-day-getters_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__iso-year-week-day-getters_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
from datetime import datetime, date

# r2py:entity:x
class IsoYearWeekDay:
    """Mimics clock::iso_year_week_day object."""
    def __init__(self, year, week, day):
        self.year = year
        self.week = week
        self.day = day
    
    def __repr__(self):
        return f'"{self.year}-W{self.week:02d}-{self.day}"'
    
    def __str__(self):
        return f"{self.year}-W{self.week:02d}-{self.day}"

def iso_year_week_day(year, week=None, day=None, hour=None, minute=None, second=None, subsecond=None, subsecond_precision=None):
    years = np.atleast_1d(year)
    weeks = np.atleast_1d(week) if week is not None else None
    days = np.atleast_1d(day) if day is not None else None
    
    # Determine result length based on recycling
    lengths = [len(years)]
    if weeks is not None: lengths.append(len(weeks))
    if days is not None: lengths.append(len(days))
    res_len = max(lengths)
    
    res = []
    for i in range(res_len):
        y = years[i % len(years)]
        w = weeks[i % len(weeks)] if weeks is not None else 1
        d = days[i % len(days)] if days is not None else 1
        res.append(IsoYearWeekDay(int(y), int(w), int(d)))
    
    return res if res_len > 1 else res[0]

# r2py:entity:get_week
def get_week(x):
    if isinstance(x, list):
        return [obj.week for obj in x]
    if isinstance(x, IsoYearWeekDay):
        return x.week
    return x

# r2py:entity:get_day
def get_day(x):
    if isinstance(x, list):
        return [obj.day for obj in x]
    if isinstance(x, IsoYearWeekDay):
        return x.day
    return x

# r2py:entity:ymd
def as_year_month_day(iso_obj):
    # ISO year, week, day to Gregorian date
    # Python's date.fromisocalendar is available in 3.8+
    return date.fromisocalendar(iso_obj.year, iso_obj.week, iso_obj.day)

# r2py:entity:get_year
def get_year(x):
    if isinstance(x, list):
        return [get_year(i) for i in x]
    if isinstance(x, IsoYearWeekDay):
        return x.year
    if hasattr(x, 'year'): # Handle date/datetime
        return x.year
    return None

# x <- iso_year_week_day(2019, 50:52, 1:3)
# r2py:entity:x
x = iso_year_week_day(2019, range(50, 53), range(1, 4))

# x
# r2py:entity:x_1
print(f' <iso_year_week_day<day>[3]>\n[1] {" ".join([str(i) for i in x])}')

# get_week(x)
# r2py:entity:get_week
print(f'[1] {" ".join(map(str, get_week(x)))}')

# get_day(x)
# r2py:entity:get_day
print(f'[1] {" ".join(map(str, get_day(x)))}')

# iso <- iso_year_week_day(2019, 1, 1)
# r2py:entity:iso
iso = iso_year_week_day(2019, 1, 1)

# ymd <- as_year_month_day(iso)
# r2py:entity:ymd
ymd = as_year_month_day(iso)

# get_year(iso)
# r2py:entity:get_year
print(f'[1] {get_year(iso)}')

# get_year(ymd)
# r2py:entity:get_year_1
print(f'[1] {get_year(ymd)}')