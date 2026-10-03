import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import calendar

# suppressPackageStartupMessages(library(lubridate))
# No-op in Python

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = pd.to_datetime("2013-01-31").date()

# jan31 + months(0:11)
# r2py:entity:months
def lubridate_add_months(start_date, month_vals):
    results = []
    for m in month_vals:
        total_months = start_date.year * 12 + (start_date.month - 1) + m
        year = total_months // 12
        month = (total_months % 12) + 1
        try:
            # lubridate's standard + months() returns NA if the day is out of range for the target month
            res = date(year, month, start_date.day)
            results.append(f'"{res.strftime("%Y-%m-%d")}"')
        except ValueError:
            results.append("NA")
    return results

months_res = lubridate_add_months(jan31, range(12))
# Formatting output to match R's [1] ... [6] ... [11] ...
print(f'      [1] {"  ".join(months_res[:5])}')
print(f' [6] {"  ".join(months_res[5:10])}')
print(f'[11] {"  ".join(months_res[10:])}')

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
def floor_date(d, unit):
    if unit == "month":
        return d.replace(day=1)
    return d

# r2py:entity:months_1
floor_jan31 = floor_date(jan31, "month")
res2 = []
for m in range(12):
    total_months = floor_jan31.year * 12 + (floor_jan31.month - 1) + m
    year = total_months // 12
    month = (total_months % 12) + 1
    # Start of month + 31 days
    base = date(year, month, 1)
    res = base + timedelta(days=31)
    res2.append(f'"{res.strftime("%Y-%m-%d")}"')

print(f'      [1] {"  ".join(res2[:5])}')
print(f' [6] {"  ".join(res2[5:10])}')
print(f'[11] {"  ".join(res2[10:])}')

# jan31 %m+% months(0:11)
# r2py:entity:months_2
def lubridate_m_plus_m(start_date, month_vals):
    results = []
    for m in month_vals:
        total_months = start_date.year * 12 + (start_date.month - 1) + m
        year = total_months // 12
        month = (total_months % 12) + 1
        try:
            res = date(year, month, start_date.day)
        except ValueError:
            # %m+% rolls back to the last day of the month
            last_day = calendar.monthrange(year, month)[1]
            res = date(year, month, last_day)
        results.append(f'"{res.strftime("%Y-%m-%d")}"')
    return results

months_2_res = lubridate_m_plus_m(jan31, range(12))
print(f'      [1] {"  ".join(months_2_res[:5])}')
print(f' [6] {"  ".join(months_2_res[5:10])}')
print(f'[11] {"  ".join(months_2_res[10:])}')