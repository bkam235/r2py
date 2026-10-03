import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    if isinstance(n, (int, float)):
        return [int(n)]
    return [int(i) for i in n]

# r2py:entity:days
def days(n):
    return timedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(dt, unit):
    if unit == "month":
        return dt.replace(day=1)
    return dt

# r2py:entity:months
def lubridate_standard_add_months(start_date, month_delta):
    """
    Simulates lubridate's standard `+ months()`.
    If the resulting day does not exist in the target month, it returns None (NA).
    """
    total_months = start_date.month - 1 + month_delta
    year_offset = total_months // 12
    final_month = (total_months % 12) + 1
    final_year = start_date.year + year_offset
    
    try:
        # In lubridate, adding months to a date like Jan 31 results in NA 
        # for months that have fewer than 31 days.
        return date(final_year, final_month, start_date.day)
    except ValueError:
        return None

# r2py:entity:months_2
def lubridate_capped_add_months(start_date, month_delta):
    """
    Simulates lubridate's `%m+%`.
    If the resulting day does not exist, it caps at the last day of the month.
    """
    return start_date + relativedelta(months=month_delta)

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = [lubridate_standard_add_months(jan31, i) for i in range(12)]
res1_out = ["\"%s\"" % d.strftime("%Y-%m-%d") if d is not None else "NA" for d in res1]

# Printing res1 to match R exactly
print(f'      [1] {" ".join(res1_out[0:5])}')
print(f' [6] {" ".join(res1_out[5:10])}')
print(f'[11] {" ".join(res1_out[10:12])}')

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
base_date = floor_date(jan31, "month")
# r2py:entity:months_1
res2 = []
for i in range(12):
    m_date = lubridate_standard_add_months(base_date, i)
    # In R, floor_date(jan31, "month") + months(0) + days(31) 
    # = 2013-01-01 + 0 months + 31 days = 2013-02-01
    res2.append(m_date + days(31))

res2_out = ["\"%s\"" % d.strftime("%Y-%m-%d") for d in res2]
print(f'      [1] {" ".join(res2_out[0:5])}')
print(f' [6] {" ".join(res2_out[5:10])}')
print(f'[11] {" ".join(res2_out[10:12])}')

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = [lubridate_capped_add_months(jan31, i) for i in range(12)]
res3_out = ["\"%s\"" % d.strftime("%Y-%m-%d") for d in res3]
print(f'      [1] {" ".join(res3_out[0:5])}')
print(f' [6] {" ".join(res3_out[5:10])}')
print(f'[11] {" ".join(res3_out[10:12])}')