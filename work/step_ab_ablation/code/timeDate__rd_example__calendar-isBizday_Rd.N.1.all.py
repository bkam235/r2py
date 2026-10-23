import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/timeDate__rd_example__calendar-isBizday_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__calendar-isBizday_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Implement RmetricsOptions shim
RmetricsOptions = {
    "currentYear": 2026,
    "myFinCenter": "GMT"
}

def getRmetricsOptions(x=None, unset=""):
    if x is None:
        return {k: v for k, v in RmetricsOptions.items()}
    return RmetricsOptions.get(x, unset)

# r2py:entity:currentYear
currentYear = getRmetricsOptions("currentYear")

# r2py:entity:tS
def timeSequence(from_val, to_val=None, by="day", length_out=None, format_val=None, zone="", fin_center=""):
    # Simplified for the specific case in the R script
    ts = pd.date_range(start=from_val, end=to_val, freq='D')
    return ts

tS = timeSequence(from=f"{currentYear}-03-01", to=f"{currentYear}-04-30")
print(tS)

# Helper for NYSE holidays
def get_nth_weekday(year, month, weekday, n):
    # weekday: 0=Mon, 6=Sun
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()
    offset = (weekday - first_weekday + 7) % 7
    day = 1 + offset + (n - 1) * 7
    return date(year, month, day)

def get_easter_date(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

# r2py:entity:holidayNYSE
def holidayNYSE(year=None, type_val=""):
    if year is None:
        year = getRmetricsOptions("currentYear")
    
    years = [year] if isinstance(year, (int, float)) else year
    holidays = []
    
    for y in years:
        holidays.append(date(y, 1, 1))   # New Year
        holidays.append(date(y, 7, 4))   # Independence Day
        holidays.append(date(y, 12, 25)) # Christmas
        holidays.append(get_nth_weekday(y, 11, 3, 4)) # Thanksgiving
        holidays.append(get_nth_weekday(y, 9, 0, 1))  # Labor Day
        holidays.append(get_nth_weekday(y, 10, 0, 2)) # Columbus Day
        holidays.append(get_nth_weekday(y, 2, 0, 3))  # Presidents Day
        if y >= 1998:
            holidays.append(get_nth_weekday(y, 1, 0, 3)) # MLK
        if y >= 2022:
            holidays.append(date(y, 6, 19)) # Juneteenth
        
        # Memorial Day (Last Monday in May)
        last_may = date(y, 5, 31)
        offset = (last_may.weekday() - 0) % 7
        holidays.append(last_may - timedelta(days=offset))
        
        holidays.append(date(y, 11, 11)) # Veterans Day
        good_friday = get_easter_date(y) - timedelta(days=2)
        holidays.append(good_friday)

    # Filter out weekends as R's holidayNYSE typically does for bizdays
    biz_holidays = [h for h in holidays if h.weekday() < 5]
    unique_sorted = sorted(list(set(biz_holidays)))
    return pd.DatetimeIndex([pd.Timestamp(h) for h in unique_sorted])

# Call for R source consistency
print(holidayNYSE())

# r2py:entity:isBizday
def isBizday(x, holidays=None, wday=None):
    if holidays is None:
        holidays = holidayNYSE()
    if wday is None:
        wday = [0, 1, 2, 3, 4] # Mon-Fri
    
    # x.weekday in pandas is 0=Mon, 6=Sun
    is_weekday = x.weekday.isin(wday)
    is_not_holiday = ~x.isin(holidays)
    return is_weekday & is_not_holiday

# Execute the R sequence
biz_mask = isBizday(tS, holidayNYSE())
print(biz_mask)

# r2py:entity:isBizday_1
tS_biz = tS[biz_mask]
print(tS_biz)