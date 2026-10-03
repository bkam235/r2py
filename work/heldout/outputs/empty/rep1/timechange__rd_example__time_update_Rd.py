# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 17

import pandas as pd
import numpy as np
from datetime import datetime, date as py_date, timedelta
import pytz
import calendar

# r2py:entity:time_update
def time_update(time_val, updates=None, year=None, month=None, yday=None, 
                mday=None, wday=None, hour=None, minute=None, second=None, 
                tz=None, roll_month="preday", roll_dst=("boundary", "post"), 
                week_start=1, exact=False):
    
    if time_val is None:
        return None
    
    # Merge updates
    updts_dict = {"year": year, "month": month, "yday": yday, "mday": mday, 
                  "wday": wday, "hour": hour, "minute": minute, "second": second}
    
    final_updates = {}
    if updates:
        final_updates = updates.copy()
    
    for nm, val in updts_dict.items():
        if val is not None:
            if nm not in final_updates or final_updates[nm] is None:
                final_updates[nm] = val
            else:
                final_updates[nm] = final_updates[nm] + val

    # Convert input to datetime object and identify original TZ
    if isinstance(time_val, py_date) and not isinstance(time_val, datetime):
        # Date objects in R are implicitly UTC midnight
        dt = datetime.combine(time_val, datetime.min.time()).replace(tzinfo=pytz.UTC)
        original_is_date = True
    elif isinstance(time_val, datetime):
        dt = time_val
        original_is_date = False
    elif isinstance(time_val, pd.Timestamp):
        dt = time_val.to_pydatetime()
        original_is_date = False
    else:
        raise TypeError(f"Unsupported date-time class '{type(time_val)}'")

    # Handle TZ: If tz is provided, it acts like force_tz (changes tz without changing wall clock)
    if tz:
        target_tz = pytz.timezone(tz)
        if dt.tzinfo is None:
            dt = target_tz.localize(dt)
        else:
            dt = dt.replace(tzinfo=None)
            dt = target_tz.localize(dt)
    elif dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)

    # Extract current components
    curr_year = dt.year
    curr_month = dt.month
    curr_day = dt.day
    curr_hour = dt.hour
    curr_min = dt.minute
    curr_sec = dt.second

    # Apply updates
    if "year" in final_updates: curr_year = final_updates["year"]
    if "month" in final_updates: curr_month = final_updates["month"]
    if "mday" in final_updates: curr_day = final_updates["mday"]
    if "hour" in final_updates: curr_hour = final_updates["hour"]
    if "minute" in final_updates: curr_min = final_updates["minute"]
    if "second" in final_updates: curr_sec = final_updates["second"]

    # Handle yday (day of year) - overrides mday if both provided
    if "yday" in final_updates:
        # R's yday is 1-indexed
        dummy_dt = datetime(curr_year, 1, 1) + timedelta(days=final_updates["yday"] - 1)
        curr_month = dummy_dt.month
        curr_day = dummy_dt.day

    # Handle month rolling
    if curr_month > 12 or curr_month < 1:
        while curr_month > 12:
            curr_year += 1
            curr_month -= 12
        while curr_month < 1:
            curr_year -= 1
            curr_month += 12

    # Handle mday rolling
    try:
        # Try to create the datetime in a naive way first to check validity
        new_dt_naive = datetime(curr_year, curr_month, curr_day, curr_hour, curr_min, curr_sec)
    except ValueError:
        if exact:
            return None # R returns NA
        
        if roll_month == "preday":
            # Roll back to the last day of the month
            last_day = calendar.monthrange(curr_year, curr_month)[1]
            new_dt_naive = datetime(curr_year, curr_month, last_day, curr_hour, curr_min, curr_sec)
        elif roll_month == "postday":
            # Roll forward to the first day of the next month
            if curr_month == 12:
                new_dt_naive = datetime(curr_year + 1, 1, 1, curr_hour, curr_min, curr_sec)
            else:
                new_dt_naive = datetime(curr_year, curr_month + 1, 1, curr_hour, curr_min, curr_sec)
        else: # boundary
            # Boundary behavior in timechange: if day > max, it rolls to first of next month
            # If day < 1, it rolls to last of prev month. 
            # Since we only catch ValueError here, it's usually day > max.
            if curr_day > calendar.monthrange(curr_year, curr_month)[1]:
                if curr_month == 12:
                    new_dt_naive = datetime(curr_year + 1, 1, 1, curr_hour, curr_min, curr_sec)
                else:
                    new_dt_naive = datetime(curr_year, curr_month + 1, 1, curr_hour, curr_min, curr_sec)
            else: # curr_day < 1
                if curr_month == 1:
                    prev_year = curr_year - 1
                    prev_month = 12
                else:
                    prev_year = curr_year
                    prev_month = curr_month - 1
                last_day = calendar.monthrange(prev_year, prev_month)[1]
                new_dt_naive = datetime(prev_year, prev_month, last_day, curr_hour, curr_min, curr_sec)

    # Re-apply timezone
    # We use localize to maintain the wall clock time we just computed
    if dt.tzinfo:
        new_dt = dt.tzinfo.localize(new_dt_naive)
    else:
        new_dt = pytz.UTC.localize(new_dt_naive)

    # If original was Date and no time updates were made, return as Date
    if original_is_date:
        has_time_upd = any(k in final_updates for k in ["hour", "minute", "second"]) or tz is not None
        if not has_time_upd:
            return new_dt.date()

    return new_dt

# --- Execution ---

# r2py:entity:date
date = py_date(2009, 2, 10)
# r2py:entity:time_update
print(time_update(date, year=2010, month=1, mday=1))
# r2py:entity:time_update_1
print(time_update(date, year=2010, month=13, mday=1))
# r2py:entity:time_update_2
print(time_update(date, minute=10, second=3))
# r2py:entity:time_update_3
print(time_update(date, minute=10, second=3, tz="America/New_York"))

# r2py:entity:time
time = pytz.timezone("America/New_York").localize(datetime(2015, 2, 3, 1, 2, 3))
# r2py:entity:time_update_4
print(time_update(time, month=2, mday=31, roll_month="preday"))
# r2py:entity:time_update_5
print(time_update(time, month=2, mday=31, roll_month="boundary"))
# r2py:entity:time_update_6
print(time_update(time, month=2, mday=31, roll_month="postday"))
# r2py:entity:time_update_7
print(time_update(time, month=2, mday=31, exact=True))
# r2py:entity:time_update_8
print(time_update(time, month=2, mday=31, exact=False))

## DST skipped
# r2py:entity:time_1
time = pytz.timezone("America/New_York").localize(datetime(2015, 2, 3, 1, 2, 3))
# r2py:entity:time_update_9
print(time_update(time, year=2016, yday=10))
# r2py:entity:time_update_10
print(time_update(time, year=2016, yday=10, tz="Europe/Amsterdam"))
# r2py:entity:time_update_11
print(time_update(time, second=30, tz="America/New_York"))