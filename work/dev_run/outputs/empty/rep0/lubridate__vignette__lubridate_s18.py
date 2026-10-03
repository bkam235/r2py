import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

def months_period(n):
    # Returns a list of month offsets
    return [int(i) for i in n]

# r2py:entity:days
def days_period(n):
    # In R, days(n) is a period of n days
    return timedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(dt, unit):
    if unit == "month":
        # Return the first day of the month
        return dt.replace(day=1)
    return dt

# Logic translation:
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# In R, adding a month period to a date that doesn't exist in the target month returns NA.
# r2py:entity:months
def r_add_months(start, m_offset):
    try:
        # Calculate target year and month
        year = start.year + (start.month + m_offset - 1) // 12
        month = (start.month + m_offset - 1) % 12 + 1
        # If the day (31) is greater than the number of days in that month, R returns NA
        if start.day > calendar.monthrange(year, month)[1]:
            return None
        return date(year, month, start.day)
    except Exception:
        return None

result1 = [r_add_months(jan31, i) for i in range(12)]
print(result1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# 1. floor_date(jan31, "month") -> 2013-01-01
# 2. + months(0:11) -> [2013-01-01, 2013-02-01, ...]
# 3. + days(31) -> add 31 days to each
# r2py:entity:months_1
start_date = floor_date(jan31, "month")
# In this sequence, adding months(0:11) to the 1st of the month always succeeds.
result2 = []
for i in range(12):
    # Add months first
    m_date = r_add_months(start_date, i)
    # Then add 31 days
    result2.append(m_date + days_period(31))
print(result2)

# jan31 %m+% months(0:11)
# The %m+% operator in lubridate handles month addition by clipping 
# the result to the last day of the month if the target day doesn't exist.
# r2py:entity:months_2
def month_add_clipped(start, delta_months):
    # relativedelta(months=n) implements the clipping behavior (Jan 31 + 1mo = Feb 28)
    return start + relativedelta(months=delta_months)

result3 = [month_add_clipped(jan31, i) for i in range(12)]
print(result3)