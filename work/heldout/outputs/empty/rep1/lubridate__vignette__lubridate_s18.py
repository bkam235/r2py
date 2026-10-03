import pandas as pd
import numpy as np
from datetime import datetime, date
from pandas.tseries.offsets import DateOffset

# r2py:entity:jan31
jan31 = pd.Timestamp("2013-01-31")

# r2py:entity:months
def r_months_add(start_date, n_months):
    """
    Implements R lubridate's base + months() behavior:
    If the resulting date is invalid (e.g., Feb 31), it returns NA.
    """
    results = []
    for i in range(n_months):
        try:
            # Calculate target year and month
            total_months = start_date.month + i
            year = start_date.year + (total_months - 1) // 12
            month = (total_months - 1) % 12 + 1
            # Try to create the date with the original day
            # This will raise ValueError if day is too high for the month
            res = pd.Timestamp(year=year, month=month, day=start_date.day)
            results.append(res)
        except ValueError:
            results.append(pd.NaT)
    return results

# r2py:entity:months_2
def r_months_add_clamp(start_date, n_months):
    """
    Implements R lubridate's %m+% behavior:
    Clamps the day to the maximum available day in the month.
    """
    results = []
    for i in range(n_months):
        # pandas DateOffset(months=i) automatically clamps to month end
        res = start_date + pd.DateOffset(months=i)
        results.append(res)
    return results

# jan31 + months(0:11)
# r2py:entity:months
res1 = r_months_add(jan31, 12)
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# floor_date(jan31, "month") results in 2013-01-01
# r2py:entity:floor_date
floor_jan31 = jan31.replace(day=1)
# r2py:entity:months_1
res2_base = r_months_add(floor_jan31, 12)
# r2py:entity:days
res2 = [d + pd.Timedelta(days=31) if pd.notnull(d) else pd.NaT for d in res2_base]
print(res2)

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = r_months_add_clamp(jan31, 12)
print(res3)