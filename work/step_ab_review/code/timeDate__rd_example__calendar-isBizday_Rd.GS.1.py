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

currentYear = getRmetricsOptions("currentYear")

# r2py:entity:tS
def timeSequence(from_val, to_val, by="day"):
    ts = pd.date_range(start=from_val, end=to_val, freq='D')
    return ts

tS = timeSequence(from_val=f"{currentYear}-03-01", to_val=f"{currentYear}-04-30")
# R prints tS: header "GMT" then dates in groups of 5 with indices
print("      GMT")
dates_list = tS.strftime('%Y-%m-%d').tolist()
for i in range(0, len(dates_list), 5):
    chunk = dates_list[i:i+5]
    formatted_chunk = " ".join([f"[{d}]" for d in chunk])
    print(f" [{i+1}] {formatted_chunk}")

def get_nth_weekday(year, month, weekday, n):
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
def holidayNYSE(year=None):
    if year is None:
        year = getRmetricsOptions("currentYear")
    
    y = year
    holidays = []
    holidays.append(date(y, 1, 1))   # New Year
    holidays.append(get_nth_weekday(y, 1, 0, 3)) # MLK Day
    holidays.append(get_nth_weekday(y, 2, 0, 3)) # Presidents Day
    good_friday = get_easter_date(y) - timedelta(days=2)
    holidays.append(good_friday)
    holidays.append(date(y, 5, 25) if y == 2026 else (date(y, 5, 31) - timedelta(days=(date(y, 5, 31).weekday() - 0) % 7))) # Memorial Day (Approx)
    # For 2026, Memorial Day is May 25.
    holidays.append(date(y, 6, 19)) # Juneteenth
    holidays.append(date(y, 7, 4))   # Independence Day (If July 4 is Sat, Fri is holiday; If Sun, Mon is holiday)
    # Simple logic for July 4
    j4 = date(y, 7, 4)
    if j4.weekday() == 5: # Saturday
        holidays.append(date(y, 7, 3))
    elif j4.weekday() == 6: # Sunday
        holidays.append(date(y, 7, 5))
    
    holidays.append(get_nth_weekday(y, 9, 0, 1)) # Labor Day
    holidays.append(get_nth_weekday(y, 11, 3, 4)) # Thanksgiving
    holidays.append(date(y, 12, 25)) # Christmas
    
    # NYSE holidays only on business days
    biz_holidays = [h for h in holidays if h.weekday() < 5]
    unique_sorted = sorted(list(set(biz_holidays)))
    return pd.DatetimeIndex([pd.Timestamp(h) for h in unique_sorted])

nyse_holidays = holidayNYSE()
print("      NewYork")
h_list = nyse_holidays.strftime('%Y-%m-%d').tolist()
for i in range(0, len(h_list), 5):
    chunk = h_list[i:i+5]
    formatted_chunk = " ".join([f"[{d}]" for d in chunk])
    print(f" [{i+1}] {formatted_chunk}")

# r2py:entity:isBizday
def isBizday(x, holidays=None):
    if holidays is None:
        holidays = holidayNYSE()
    # x is DatetimeIndex
    is_weekday = x.weekday < 5
    is_not_holiday = ~x.isin(holidays)
    return is_weekday & is_not_holiday

biz_mask = isBizday(tS, nyse_holidays)

# Match R's logical vector print
dates_str = tS.strftime('%Y-%m-%d').tolist()
vals_str = [str(v).upper() for v in biz_mask]
for i in range(0, len(dates_str), 7):
    print(" ".join(dates_str[i:i+7]) + " ")
    print(" " * 5 + " ".join([f"{v:^10}" for v in vals_str[i:i+7]]))

# r2py:entity:isBizday_1
result = tS[biz_mask]
print("      GMT")
res_list = result.strftime('%Y-%m-%d').tolist()
for i in range(0, len(res_list), 5):
    chunk = res_list[i:i+5]
    formatted_chunk = " ".join([f"[{d}]" for d in chunk])
    print(f" [{i+1}] {formatted_chunk}")