import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

# r2py:entity:jan31
jan31 = pd.to_datetime("2013-01-31").date()

# r2py:entity:months
def lubridate_months_add(start_date, n_months):
    results = []
    for m in n_months:
        # lubridate's + months() returns NA if the day is invalid for that month
        target_date = start_date + relativedelta(months=m)
        if target_date.day != start_date.day:
            results.append(np.nan)
        else:
            results.append(target_date.strftime("%Y-%m-%d"))
    return results

# jan31 + months(0:11)
months_res = lubridate_months_add(jan31, range(12))
print(months_res)

# r2py:entity:floor_date
def floor_date(d, unit):
    if unit == "month":
        return d.replace(day=1)
    return d

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:days
def lubridate_floor_seq(start_date):
    f_date = floor_date(start_date, "month")
    results = []
    for m in range(12):
        # Step 1: + months(m)
        step1 = f_date + relativedelta(months=m)
        # Step 2: + days(31)
        step2 = step1 + timedelta(days=31)
        results.append(step2.strftime("%Y-%m-%d"))
    return results

floor_months_days_res = lubridate_floor_seq(jan31)
print(floor_months_days_res)

# r2py:entity:months_2
def m_plus_m(start_date, n_months):
    results = []
    for m in n_months:
        # %m+% clips to the last day of the month if target day doesn't exist
        res = start_date + relativedelta(months=m)
        results.append(res.strftime("%Y-%m-%d"))
    return results

# jan31 %m+% months(0:11)
m_plus_m_res = m_plus_m(jan31, range(12))
print(m_plus_m_res)