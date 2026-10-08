# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np

# Suppress library startup messages (no-op in Python)
pass

# Create ymd function to parse dates
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# Create months function that returns relativedelta objects
def months(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(months=int(i)) for i in n]
    return relativedelta(months=int(n))

# Create days function that returns relativedelta objects
def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [relativedelta(days=int(i)) for i in n]
    return relativedelta(days=int(n))

# Create floor_date function
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

# Helper function to format date vector output like R
def format_date_vector(dates):
    # Format dates and add NA markers for None values
    formatted = []
    for d in dates:
        if d is None:
            formatted.append("NA")
        else:
            formatted.append(f'"{d}"')
    
    # Print in R-style vector format with line breaks every 5 elements
    result = "[1] " + " ".join(formatted[:5])
    for i in range(5, len(formatted), 5):
        result += "\n[" + str(i+1) + "] " + " ".join(formatted[i:i+5])
    return result

# jan31 <- ymd("2013-01-31")
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# In R, adding months to day-31 dates produces NA for months with < 31 days
# This is the standard + operator behavior in lubridate
periods = months(range(0, 12))
res1 = []
for period in periods:
    try:
        result_date = jan31 + period
        # Check if the resulting day is valid for the month
        # Jan 31 + 1 month should be Feb 28/29, but + operator gives NA
        # We need to simulate this: if day of month is 31 and target month has < 31 days, return NA
        if jan31.day == 31:
            # Check if result month has fewer than 31 days
            test_date = jan31 + period
            # Get last day of the result month
            next_month = test_date.replace(day=1) + relativedelta(months=1)
            last_day = (next_month - relativedelta(days=1)).day
            if last_day < 31:
                res1.append(None)  # NA value
            else:
                res1.append(test_date)
        else:
            res1.append(jan31 + period)
    except:
        res1.append(None)

print(format_date_vector(res1))

# floor_date(jan31, "month") + months(0:11) + days(31)
base = floor_date(jan31, "month")
periods_m = months(range(0, 12))
res2 = []
for period in periods_m:
    intermediate = base + period
    res2.append(intermediate + relativedelta(days=31))

print(format_date_vector(res2))

# jan31 %m+% months(0:11)
# The %m+% operator uses month arithmetic that preserves/rolls to last valid day
# This is equivalent to relativedelta behavior
periods_mm = months(range(0, 12))
res3 = [jan31 + period for period in periods_mm]

print(format_date_vector(res3))
