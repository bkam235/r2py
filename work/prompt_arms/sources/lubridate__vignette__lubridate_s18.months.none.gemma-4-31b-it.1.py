import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def ymd(date_str):
    return pd.to_datetime(date_str).date()

def months(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(months=int(i)) for i in n]
    return relativedelta(months=int(n))

def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(days=int(i)) for i in n]
    return relativedelta(days=int(n))

def floor_date(x, unit="month"):
    if unit == "month":
        return x.replace(day=1)
    return x

def lubridate_add_months(start_date, month_deltas):
    results = []
    for delta in month_deltas:
        target = start_date + delta
        # R's months() returns NA if the day of the month is not preserved
        if target.day != start_date.day:
            results.append(None)
        else:
            results.append(target)
    return results

def lubridate_mplus_months(start_date, month_deltas):
    # %m+% snaps to the end of the month, which is dateutil.relativedelta's default
    results = []
    for delta in month_deltas:
        results.append(start_date + delta)
    return results

# jan31 <- ymd("2013-01-31")
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# Use the strict addition for the first call
res1 = lubridate_add_months(jan31, months(range(12)))
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# floor_date returns 2013-01-01. 0:11 months preserves day 1. Then add 31 days.
base_dates = lubridate_add_months(floor_date(jan31, "month"), months(range(12)))
res2 = [(d + relativedelta(days=31)) if d is not None else None for d in base_dates]
print(res2)

# jan31 %m+% months(0:11)
# Use the snapping addition
res3 = lubridate_mplus_months(jan31, months(range(12)))
print(res3)
