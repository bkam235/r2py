# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(x):
    if isinstance(x, (int, float)):
        return [int(x)]
    return list(x)

# r2py:entity:days
def days(x=1):
    return relativedelta(days=int(x))

# r2py:entity:floor_date
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

def lubridate_add_months(start_date, month_val, clip=False):
    """
    Implements lubridate's Period addition logic.
    If clip=False (standard + months()), it returns None (NA) if the 
    resulting day is invalid for the target month.
    If clip=True (%m+%), it clips to the last day of the month.
    """
    target_month = (start_date.month + month_val - 1) % 12 + 1
    target_year = start_date.year + (start_date.month + month_val - 1) // 12
    
    last_day_of_target = calendar.monthrange(target_year, target_month)[1]
    
    if clip:
        day = min(start_date.day, last_day_of_target)
        return date(target_year, target_month, day)
    else:
        if start_date.day > last_day_of_target:
            return None
        return date(target_year, target_month, start_date.day)

# r2py:entity:months_2
def m_plus(start_date, periods, clip=False):
    return [lubridate_add_months(start_date, p, clip=clip) for p in periods]

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = m_plus(jan31, months(range(12)), clip=False)
print([d.isoformat() if d else "NA" for d in res1])

# floor_date(jan31, "month") + months(0:11) + days(31)
res2 = []
# r2py:entity:floor_date
base_floor = floor_date(jan31, "month")
for i in range(12):
    # floor_date + months(i) is always valid (day=1)
    d_step1 = lubridate_add_months(base_floor, i, clip=False)
# r2py:entity:days
    res2.append(d_step1 + days(31))
print([d.isoformat() for d in res2])

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = m_plus(jan31, months(range(12)), clip=True)
print([d.isoformat() for d in res3])