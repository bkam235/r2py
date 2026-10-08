# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np

# r2py:entity:months
def months(n):
    # R's months() returns an integer vector representing months
    # When used with + operator, it produces NAs for some cases
    # When used with %m+%, it preserves the day of month
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

# r2py:entity:days
def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

# r2py:entity:floor_date
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

def format_date(d):
    """Format date as R does: YYYY-MM-DD"""
    if d is None or (isinstance(d, float) and np.isnan(d)):
        return "NA"
    return d.strftime("%Y-%m-%d")

def print_date_vector(dates, title=""):
    """Print dates in R format"""
    if title:
        print(f"[{title}]")
    # Format as R does: [1] "date1" "date2" etc.
    formatted = [format_date(d) if d is not None else "NA" for d in dates]
    output = '[1] ' + ' '.join(f'"{d}"' for d in formatted[:5])
    if len(formatted) > 5:
        output += '\n [6] ' + ' '.join(f'"{d}"' for d in formatted[5:10])
    if len(formatted) > 10:
        output += '\n[11] ' + ' '.join(f'"{d}"' for d in formatted[10:])
    print(output)

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jam31 = pd.to_datetime("2013-01-31").date()

# jan31 + months(0:11)
# In R's lubridate, adding months to a date with + operator produces NAs for some months
# This is because some intermediate dates don't exist (e.g., Feb 31)
# r2py:entity:months
res1 = []
for m in months(np.arange(0, 12)):
    try:
        result_date = jan31 + relativedelta(months=m)
        # Check if day exists in the target month
        res1.append(result_date)
    except:
        res1.append(None)
print_date_vector(res1)

# floor_date(jan31, "month") + months(0:11) + days(31)
# floor_date(jan31, "month") is 2013-01-01.
# r2py:entity:floor_date
base = floor_date(jan31, "month")
res2 = []
for m in months(np.arange(0, 12)):
    try:
        result_date = base + relativedelta(months=m, days=31)
        res2.append(result_date)
    except:
        res2.append(None)
print_date_vector(res2)

# jan31 %m+% months(0:11)
# The %m+% operator in lubridate preserves the day of month, capped at the last day
# r2py:entity:months_2
res3 = []
for m in months(np.arange(0, 12)):
    result_date = jan31 + relativedelta(months=m)
    res3.append(result_date)
print_date_vector(res3)
