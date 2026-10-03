# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import numpy as np

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    # In R lubridate, months(0:11) creates a sequence of Periods
    if isinstance(n, (int, float)):
        return [relativedelta(months=int(n))]
    return [relativedelta(months=int(i)) for i in n]

# r2py:entity:days
def days(n):
    return relativedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(dt, unit):
    if unit == "month":
        return dt.replace(day=1)
    return dt

# r2py:entity:months_2
def lubridate_add_months(start_date, rel_delta, clamp=False):
    """
    Mimics lubridate period addition.
    If clamp=False (standard +), results in NA if the day is invalid for the target month.
    If clamp=True (%m%+%), clamps to the last day of the month.
    """
    if pd.isna(start_date):
        return np.nan
        
    target_year = start_date.year + (start_date.month + rel_delta.months - 1) // 12
    target_month = (start_date.month + rel_delta.months - 1) % 12 + 1
    
    last_day_of_month = calendar.monthrange(target_year, target_month)[1]
    
    if clamp:
        day = min(start_date.day, last_day_of_month)
        return date(target_year, target_month, day)
    else:
        if start_date.day > last_day_of_month:
            return np.nan
        return date(target_year, target_month, start_date.day)

def format_r_output(dates):
    """Helper to match R's output format for dates and NAs"""
    formatted = []
    for d in dates:
        if pd.isna(d):
            formatted.append("NA")
        else:
            formatted.append(d.strftime("%Y-%m-%d"))
    
    # R's print for vectors: [1] "val1" "val2" ...
    # Split into lines of 6 elements roughly
    res = ""
    for i in range(0, len(formatted), 6):
        chunk = formatted[i:i+6]
        prefix = f"[{i+1}] " if i == 0 else f"[{i+1}] "
        res += prefix + " ".join([f'"{x}"' for x in chunk]) + "\n"
    return res.strip()

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = [lubridate_add_months(jan31, relativedelta(months=i), clamp=False) for i in range(12)]
print(format_r_output(res1))

# floor_date(jan31, "month") + months(0:11) + days(31)
res2 = []
for i in range(12):
# r2py:entity:floor_date
    # r2py:entity:floor_date
    base = floor_date(jan31, "month")
    # lubridate's months() here adds the period first
# r2py:entity:months_1
    month_added = lubridate_add_months(base, relativedelta(months=i), clamp=False)
    # then adds 31 days
    if not pd.isna(month_added):
# r2py:entity:days
        final = month_added + timedelta(days=31)
    else:
        final = np.nan
    res2.append(final)
print(format_r_output(res2))

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = [lubridate_add_months(jan31, relativedelta(months=i), clamp=True) for i in range(12)]
print(format_r_output(res3))