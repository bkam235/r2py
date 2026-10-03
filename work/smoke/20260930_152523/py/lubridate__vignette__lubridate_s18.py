import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    if isinstance(n, (int, float)):
        return [relativedelta(months=int(n))]
    return [relativedelta(months=int(i)) for i in n]

# r2py:entity:days
def days(n):
    if isinstance(n, (int, float)):
        return [relativedelta(days=int(n))]
    return [relativedelta(days=int(i)) for i in n]

# r2py:entity:floor_date
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

# r2py:entity:months_1
def lubridate_add_period(start_date, period):
    """
    Implements lubridate's period addition: 
    If the resulting date is invalid (e.g. Feb 31), returns None (NA).
    """
    if start_date is None:
        return None
    
    m_add = period.months
    d_add = period.days
    
    total_months = start_date.year * 12 + (start_date.month - 1) + m_add
    new_year = total_months // 12
    new_month = (total_months % 12) + 1
    
    _, days_in_month = calendar.monthrange(new_year, new_month)
    if start_date.day > days_in_month:
        return None
    
    res = date(new_year, new_month, start_date.day)
    res = res + relativedelta(days=d_add)
    return res

def format_r_dates(dates):
    """Helper to format list of dates to look like R output."""
    formatted = [d.strftime("%Y-%m-%d") if d is not None else "NA" for d in dates]
    # R prints in chunks of 6 usually
    res = ""
    for i in range(0, len(formatted), 6):
        chunk = formatted[i:i+6]
        prefix = f" [{i+1}] " if i > 0 else " [1] "
        res += prefix + " ".join(f'"{x}"' if x != "NA" else x for x in chunk) + "\n"
    return res.strip()

# R: jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# R: jan31 + months(0:11)
# r2py:entity:months
m_periods = months(range(12))
res1 = [lubridate_add_period(jan31, p) for p in m_periods]
print(format_r_dates(res1))

# R: floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
f_date = floor_date(jan31, "month")
# R: months(0:11) + days(31)
# r2py:entity:months_1
res2 = []
for i in range(12):
    # Step 1: add month
    d = lubridate_add_period(f_date, relativedelta(months=i))
    # Step 2: add 31 days
    if d is not None:
        d = d + relativedelta(days=31)
    res2.append(d)
print(format_r_dates(res2))

# R: jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = []
for i in range(12):
    # %m+% caps the day to the end of the month
    d = jan31 + relativedelta(months=i)
    res3.append(d)
print(format_r_dates(res3))