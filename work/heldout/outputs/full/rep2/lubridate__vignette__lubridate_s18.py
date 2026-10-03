# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str)

# r2py:entity:months
def months(n):
    # In R, months(0:11) creates a period of months. 
    # In Python, we handle this as a list of relativedeltas for vectorization.
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [relativedelta(months=int(i)) for i in n]
    return relativedelta(months=int(n))

# r2py:entity:days
def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [relativedelta(days=int(i)) for i in n]
    return relativedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(x, unit):
    if unit == "month":
        return x.replace(day=1)
    return x

# r2py:entity:months
def apply_period(start_date, periods):
    if isinstance(periods, list):
        return pd.Series([start_date + p for p in periods])
    return start_date + periods

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = apply_period(jan31, months(np.arange(0, 12)))
print(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# R's days(31) is added to the result of (floor_date + months)
# r2py:entity:floor_date
base_date = floor_date(jan31, "month")
months_seq = months(np.arange(0, 12))
res2 = pd.Series([base_date + m + relativedelta(days=31) for m in months_seq])
print(res2)

# jan31 %m+% months(0:11)
# %m+% is the "month-modulo" addition which keeps the day within the valid range of the month
# (e.g., Jan 31 + 1 month = Feb 28/29, not March 3)
# r2py:entity:months_2
def month_modulo_add(start_date, periods):
    results = []
    for p in periods:
        # Calculate target month and year
        target = start_date + p
        # If the day shifted (e.g. 31 -> 28), we need to cap it at the end of that month
        # relativedelta already handles this by clamping to the last valid day of the month
        # whereas standard datetime arithmetic might roll over.
        # pd.to_datetime + relativedelta(months=n) mimics %m+% behavior.
        results.append(target)
    return pd.Series(results)

# r2py:entity:months_2
res3 = month_modulo_add(jan31, months(np.arange(0, 12)))
print(res3)