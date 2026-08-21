# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 12

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Helper function to simulate set_day logic
# r2py:entity:set_day
def set_day(dt, day, invalid="error"):
    if isinstance(day, (list, np.ndarray, range)):
        return [set_day(dt, d, invalid) for d in day]
    
    if day == "last":
        # Get the first day of next month, then subtract one day
        next_month = dt.replace(day=1) + relativedelta(months=1)
        return next_month - timedelta(days=1)
    
    try:
        return dt.replace(day=day)
    except ValueError:
        if invalid == "previous":
            # Find the last valid day of the current month
            next_month = dt.replace(day=1) + relativedelta(months=1)
            return next_month - timedelta(days=1)
        raise

# Helper function to simulate set_hour logic for DST transitions
# r2py:entity:set_hour
def set_hour(dt, hour, nonexistent="error"):
    try:
        return dt.replace(hour=hour)
    except (ValueError, OSError):
        if nonexistent == "roll-forward":
            # Roll forward: move to the start of the next valid time (usually +1 hour)
            return dt.replace(hour=hour) + timedelta(hours=1)
        elif nonexistent == "roll-backward":
            # Roll backward: move to the last valid time before the gap
            return dt.replace(hour=hour) - timedelta(hours=1)
        raise

# x <- as.POSIXct("2019-02-01", tz = "America/New_York")
# r2py:entity:x
x = pd.to_datetime("2019-02-01").tz_localize("America/New_York")

# set_day(x, 12:14)
# r2py:entity:set_day
print(set_day(x, range(12, 15)))

# set_day(x, "last")
# r2py:entity:set_day_1
print(set_day(x, "last"))

# try(set_day(x, 31))
# r2py:entity:try
try:
    print(set_day(x, 31))
except ValueError as e:
    print(f"Caught expected error: {e}")

# set_day(as_year_month_day(x), 31) 
# (Since Python's date objects still validate days, this will still fail for Feb)
# r2py:entity:set_day_2
try:
    print(set_day(x.date(), 31))
except ValueError as e:
    print(f"Caught expected error: {e}")

# set_day(x, 31, invalid = "previous")
# r2py:entity:set_day_3
print(set_day(x, 31, invalid="previous"))

# y <- as.POSIXct("2020-03-08 01:30:00", tz = "America/New_York")
# r2py:entity:y
y = pd.to_datetime("2020-03-08 01:30:00").tz_localize("America/New_York")

# try(set_hour(y, 2))
# r2py:entity:try_1
try:
    print(set_hour(y, 2))
except Exception as e:
    print(f"Caught expected error: {e}")

# set_hour(y, 2, nonexistent = "roll-forward")
# r2py:entity:set_hour
print(set_hour(y, 2, nonexistent="roll-forward"))

# set_hour(y, 2, nonexistent = "roll-backward")
# r2py:entity:set_hour_1
print(set_hour(y, 2, nonexistent="roll-backward"))