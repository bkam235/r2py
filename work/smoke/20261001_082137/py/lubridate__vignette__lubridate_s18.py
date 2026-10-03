import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np
import calendar

# r2py:entity:jan31
def ymd(x):
    return pd.to_datetime(x).date()

# r2py:entity:months
def months(x):
    # In R, months(0:11) creates a Period object.
    # Adding a Period of months to a date in lubridate results in NA 
    # if the resulting day is invalid for that month.
    if isinstance(x, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(months=int(i)) for i in x]
    return relativedelta(months=int(x))

# r2py:entity:days
def days(x=1):
    if isinstance(x, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(days=int(i)) for i in x]
    return relativedelta(days=int(x))

# r2py:entity:floor_date
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

# Implementation of lubridate's period addition (the + operator)
# r2py:entity:months
def lubridate_add_period(start_date, period):
    # lubridate's + operator returns NA if the day of month is not valid in target month
    target_date = start_date + period
    # Check if the day shifted (e.g., Jan 31 + 1 month -> March 3 or Feb 28 depending on lib)
    # dateutil.relativedelta typically clips or overflows. 
    # Lubridate's + months() specifically returns NA if the day is not the same.
    if target_date.day != start_date.day:
        return None
    return target_date

# r2py:entity:months_2
def m_plus(date_val, period_val):
    # %m+% clips to the end of the month instead of returning NA
    target_date = date_val + period_val
    # If the day changed, it means we overflowed the target month's length.
    # We must clip to the last day of the intended month.
    if target_date.day != date_val.day:
        # Find the last day of the target month
        year = target_date.year
        month = target_date.month
        # If it overflowed into the next month, we need the previous month's end
        # However, relativedelta(months=1) on Jan 31 results in Feb 28.
        # But R's %m+% logic for Jan 31 + 1 month is Feb 28.
        # In dateutil, Jan 31 + relativedelta(months=1) is Feb 28. 
        # We need to ensure we are at the end of the month.
        last_day = calendar.monthrange(year, month)[1]
        return target_date.replace(day=last_day)
    return target_date

# Translation of the script logic
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# R: jan31 + months(0:11)
# r2py:entity:months
res1 = [lubridate_add_period(jan31, months(i)) for i in range(12)]
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# floor_date(jan31, "month") is 2013-01-01.
# + months(i) makes it the 1st of the month.
# + days(31) adds 31 days.
# r2py:entity:months_1
res2 = []
for i in range(12):
# r2py:entity:floor_date
    d = floor_date(jan31, "month")
    d = lubridate_add_period(d, months(i))
# r2py:entity:days
    d = d + days(31)
    res2.append(d)
print(res2)

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = [m_plus(jan31, months(i)) for i in range(12)]
print(res3)