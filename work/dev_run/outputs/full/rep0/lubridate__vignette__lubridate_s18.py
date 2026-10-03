import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# No-op

# Handled by imports above

# r2py:entity:jan31
jan31 = pd.Timestamp("2013-01-31").date()

# lubridate's + months(n) returns NA if the day is not valid for the target month
# r2py:entity:months
def r_months_add(start_date, months_list):
    results = []
    for m in months_list:
        # Calculate target date using relativedelta (which normally clamps)
        target = start_date + relativedelta(months=m)
        # lubridate behavior: if original day is 31 but target month only has 28, result is NA
        if target.day != start_date.day:
            results.append(np.nan)
        else:
            results.append(target)
    return results

# lubridate's %m+% clamps the day to the maximum possible for that month
# r2py:entity:months_2
def r_m_plus_m(start_date, months_list):
    results = []
    for m in months_list:
        # relativedelta(months=m) automatically handles the clamping (e.g., Jan 31 + 1mo = Feb 28)
        res = start_date + relativedelta(months=m)
        results.append(res)
    return results

# Expression 1: jan31 + months(0:11)
# r2py:entity:months
res1 = r_months_add(jan31, range(12))
print(res1)

# Expression 2: floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
floor_jan31 = jan31.replace(day=1)
# r2py:entity:months_1
res2 = []
for i in range(12):
    # First floor to month, add i months, then add 31 days
    d = floor_jan31 + relativedelta(months=i)
# r2py:entity:days
    d = d + relativedelta(days=31)
    res2.append(d)
print(res2)

# Expression 3: jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = r_m_plus_m(jan31, range(12))
print(res3)