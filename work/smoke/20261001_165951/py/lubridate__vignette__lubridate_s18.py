# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
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
def m_plus(dt, period):
    return dt + period

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1_fmt = []
for i in range(12):
    target = jan31 + relativedelta(months=i)
    if target.day != 31:
        res1_fmt.append("NA")
    else:
        res1_fmt.append(f'"{target.strftime("%Y-%m-%d")}"')

print(f'[1] {"  ".join(res1_fmt[0:5])}')
print(f'[6] {"  ".join(res1_fmt[5:10])}')
print(f'[11] {"  ".join(res1_fmt[10:])}')

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:days
floor_jan = floor_date(jan31, "month")
res2_fmt = []
for i in range(12):
    # R: floor_date(jan31, "month") is 2013-01-01
    # Then add months(i) and then add 31 days
    d = floor_jan + relativedelta(months=i) + relativedelta(days=31)
    res2_fmt.append(f'"{d.strftime("%Y-%m-%d")}"')

print(f'[1] {"  ".join(res2_fmt[0:5])}')
print(f'[6] {"  ".join(res2_fmt[5:10])}')
print(f'[11] {"  ".join(res2_fmt[10:])}')

# jan31 %m+% months(0:11)
# %m+% in lubridate ensures the day of the month is capped at the last day of the month
# r2py:entity:months_2
res3_fmt = []
for i in range(12):
    target = jan31 + relativedelta(months=i)
    res3_fmt.append(f'"{target.strftime("%Y-%m-%d")}"')

print(f'[1] {"  ".join(res3_fmt[0:5])}')
print(f'[6] {"  ".join(res3_fmt[5:10])}')
print(f'[11] {"  ".join(res3_fmt[10:])}')