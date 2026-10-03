import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta
import calendar

# r2py:entity:jan31
jan31 = pd.to_datetime("2013-01-31").date()

# jan31 + months(0:11)
# lubridate's + months() returns NA if the day is not valid in the target month.
# r2py:entity:months
def lubridate_add_months(start_date, n_months):
    results = []
    for i in n_months:
        # Calculate target year and month
        total_months = start_date.year * 12 + start_date.month + i
        year = total_months // 12
        month = total_months % 12
        if month == 0:
            year -= 1
            month = 12
        
        # Check if the day exists in the target month
        last_day_of_month = calendar.monthrange(year, month)[1]
        if start_date.day <= last_day_of_month:
            results.append(pd.Timestamp(year, month, start_date.day).date())
        else:
            results.append(np.nan)
    return results

res1 = lubridate_add_months(jan31, range(12))
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:months_1
jan31_floor = jan31.replace(day=1)
# In R: floor_date(jan31, "month") + months(0:11) 
# Since it's the 1st of the month, it will never be NA.
# Then add 31 days.
res2 = []
for i in range(12):
    total_months = jan31_floor.year * 12 + jan31_floor.month + i
    year = total_months // 12
    month = total_months % 12
    if month == 0:
        year -= 1
        month = 12
    # The 1st of the month always exists
    dt = pd.Timestamp(year, month, 1)
    # r2py:entity:days
# r2py:entity:days
    res2.append((dt + pd.Timedelta(days=31)).date())
print(res2)

# jan31 %m+% months(0:11)
# %m+% clamps the day to the maximum available in that month.
# r2py:entity:months_2
def lubridate_mplus_months(start_date, n_months):
    results = []
    for i in n_months:
        total_months = start_date.year * 12 + start_date.month + i
        year = total_months // 12
        month = total_months % 12
        if month == 0:
            year -= 1
            month = 12
        
        last_day_of_month = calendar.monthrange(year, month)[1]
        day = min(start_date.day, last_day_of_month)
        results.append(pd.Timestamp(year, month, day).date())
    return results

res3 = lubridate_mplus_months(jan31, range(12))
print(res3)