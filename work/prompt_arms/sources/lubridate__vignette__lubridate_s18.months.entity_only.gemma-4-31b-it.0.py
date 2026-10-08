import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:ymd
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

# r2py:entity:days
def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

# r2py:entity:floor_date
def floor_date(x, unit="month"):
    if unit == "month":
        return x.replace(day=1)
    return x

def add_months_strict(start_date, m):
    if isinstance(m, list):
        return [add_months_strict(start_date, i) for i in m]
    
    total_months = start_date.year * 12 + start_date.month - 1 + m
    new_year = total_months // 12
    new_month = (total_months % 12) + 1
    
    try:
        return date(new_year, new_month, start_date.day)
    except ValueError:
        return np.nan

def add_months_modulo(start_date, m):
    if isinstance(m, list):
        return [add_months_modulo(start_date, i) for i in m]
    return start_date + relativedelta(months=m)

def add_days(start_date, d):
    if isinstance(d, list):
        return [add_days(start_date, i) for i in d]
    return start_date + relativedelta(days=d)

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = add_months_strict(jan31, months(np.arange(0, 12)))
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
base_dates = add_months_strict(floor_date(jan31, "month"), months(np.arange(0, 12)))
# r2py:entity:days
res2 = [add_days(d, 31) if d is not np.nan else np.nan for d in base_dates]
print(res2)

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = add_months_modulo(jan31, months(np.arange(0, 12)))
print(res3)