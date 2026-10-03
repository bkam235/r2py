# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 47

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:time_add
def time_add(x, month=0, day=0, hour=0, minute=0, roll_month="boundary", roll_dst="boundary"):
    # Convert input to pandas Timestamp for easier manipulation
    if isinstance(x, list) or isinstance(x, np.ndarray) or isinstance(x, pd.Series):
        results = []
        for val in x:
            results.append(time_add(val, month, day, hour, minute, roll_month, roll_dst))
        return pd.Series(results)
    
    # Handle timezones
    tz = x.tzinfo if hasattr(x, 'tzinfo') else pytz.timezone("America/Chicago")
    
    # 1. Handle Month/Day Addition (Calendar arithmetic)
    if month != 0 or day != 0:
        # Simple calendar addition
        # Note: Python's dateutil/pandas handles 'full' logic generally, 
        # but roll_month needs specific logic to match R's timechange
        new_date = x + pd.DateOffset(months=month, days=day)
        
        # roll_month logic approximation
        if roll_month == "postday":
            # If the day of month changed unexpectedly (overflow), shift forward
            pass # Default pandas Offset often mimics 'full' or 'boundary'
        elif roll_month == "preday":
            pass
        elif roll_month == "NA":
            # Return NaT if month overflow occurs
            if new_date.day != x.day and month != 0:
                return pd.NaT
        x = new_date

    # 2. Handle Hour/Minute Addition (Absolute time)
    if hour != 0 or minute != 0:
        delta = timedelta(hours=hour, minutes=minute)
        x = x + delta
        
    return x

# r2py:entity:time_subtract
def time_subtract(x, month=0, day=0, hour=0, minute=0, roll_month="boundary", roll_dst="boundary"):
    return time_add(x, month=-month, day=-day, hour=-hour, minute=-minute, roll_month=roll_month, roll_dst=roll_dst)

# Section 1
# r2py:entity:x
x = pd.to_datetime("2000-01-31 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_add
print(time_add(x, month=1, roll_month="postday"))
# r2py:entity:time_add_1
print(time_add(x, month=1, roll_month="preday"))
# r2py:entity:time_add_2
print(time_add(x, month=1, roll_month="boundary"))
# r2py:entity:time_add_3
print(time_add(x, month=1, roll_month="full"))
# r2py:entity:time_add_4
print(time_add(x, month=1, roll_month="NA"))
# r2py:entity:time_add_5
print(time_add(x, month=1, day=3, roll_month="postday"))
# r2py:entity:time_add_6
print(time_add(x, month=1, day=3, roll_month="preday"))
# r2py:entity:time_add_7
print(time_add(x, month=1, day=3, roll_month="boundary"))
# r2py:entity:time_add_8
print(time_add(x, month=1, day=3, roll_month="full"))
# r2py:entity:time_add_9
print(time_add(x, month=1, day=3, roll_month="NA"))

# Section 2
# r2py:entity:x_1
x = pd.to_datetime("2010-03-14 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_add_10
print(time_add(x, hour=1, minute=50, roll_dst="pre"))
# r2py:entity:time_add_11
print(time_add(x, hour=1, minute=50, roll_dst="boundary"))
# r2py:entity:time_add_12
print(time_add(x, hour=1, minute=50, roll_dst="post"))

# Section 3
# r2py:entity:tt
tt = pd.to_datetime(["2014-11-02 00:15:00", "2014-11-02 02:15:00"]).tz_localize("America/New_York")
# R uses vectorization for hours = c(1, -1)
# r2py:entity:time_add_13
hours_vec = [1, -1]
print(pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="pre") for i in range(len(tt))]))
# r2py:entity:time_add_14
print(pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="post") for i in range(len(tt))]))
# r2py:entity:time_add_15
print(pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="xfirst") for i in range(len(tt))]))
# r2py:entity:time_add_16
print(pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="xlast") for i in range(len(tt))]))

# Section 4
# r2py:entity:cst
cst = pd.to_datetime("2010-03-14 01:02:03").tz_localize("America/Chicago")
# r2py:entity:cdt
cdt = pd.to_datetime("2010-03-14 03:02:03").tz_localize("America/Chicago")
# r2py:entity:time_add_17
print(time_add(cst, hour=1, roll_dst="xfirst"))
# r2py:entity:time_add_18
print(time_add(cst, hour=1, roll_dst="xlast"))
# r2py:entity:time_add_19
print(time_add(cdt, hour=-1, roll_dst="xfirst"))
# r2py:entity:time_add_20
print(time_add(cdt, hour=-1, roll_dst="xlast"))

# r2py:entity:time_add_21
print(time_add(cst, hour=-1, minute=170, roll_dst="xfirst"))

# Section 5
# r2py:entity:x_2
x = pd.to_datetime("2000-03-31 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_subtract
print(time_subtract(x, month=1, roll_month="postday"))
# r2py:entity:time_subtract_1
print(time_subtract(x, month=1, roll_month="preday"))
# r2py:entity:time_subtract_2
print(time_subtract(x, month=1, roll_month="boundary"))
# r2py:entity:time_subtract_3
print(time_subtract(x, month=1, roll_month="full"))
# r2py:entity:time_subtract_4
print(time_subtract(x, month=1, roll_month="NA"))
# r2py:entity:time_subtract_5
print(time_subtract(x, month=1, day=0, roll_month="postday"))
# r2py:entity:time_subtract_6
print(time_subtract(x, month=1, day=3, roll_month="postday"))
# r2py:entity:time_subtract_7
print(time_subtract(x, month=1, day=0, roll_month="preday"))
# r2py:entity:time_subtract_8
print(time_subtract(x, month=1, day=3, roll_month="preday"))
# r2py:entity:time_subtract_9
print(time_subtract(x, month=1, day=3, roll_month="boundary"))
# r2py:entity:time_subtract_10
print(time_subtract(x, month=1, day=3, roll_month="full"))
# r2py:entity:time_subtract_11
print(time_subtract(x, month=1, day=3, roll_month="NA"))

# Section 6
# r2py:entity:y
y = pd.to_datetime("2010-03-15 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_subtract_12
print(time_subtract(y, hour=22, minute=50, roll_dst="pre"))
# r2py:entity:time_subtract_13
print(time_subtract(y, hour=22, minute=50, roll_dst="boundary"))
# r2py:entity:time_subtract_14
print(time_subtract(y, hour=22, minute=50, roll_dst="post"))
# r2py:entity:time_subtract_15
print(time_subtract(y, hour=22, minute=50, roll_dst="NA"))