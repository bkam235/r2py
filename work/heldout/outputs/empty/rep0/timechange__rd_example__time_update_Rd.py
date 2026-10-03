# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 17

import pandas as pd
import numpy as np
from datetime import datetime, date as py_date, timedelta
import pytz
from dateutil.relativedelta import relativedelta

# r2py:entity:time_update
def time_update(time_val, updates=None, year=None, month=None, yday=None, 
                mday=None, wday=None, hour=None, minute=None, second=None, 
                tz=None, roll_month="preday", roll_dst="boundary", 
                week_start=1, exact=False):
    
    if time_val is None:
        return None

    # Merge updates logic from R source
    updts = {"year": year, "month": month, "yday": yday, "mday": mday, 
             "wday": wday, "hour": hour, "minute": minute, "second": second}
    
    final_updates = {}
    if updates is not None:
        final_updates = updates.copy()
    
    for nm, val in updts.items():
        if val is not None:
            if nm not in final_updates or final_updates[nm] is None:
                final_updates[nm] = val
            else:
                final_updates[nm] = final_updates[nm] + val

    # Handle input types
    is_date_input = isinstance(time_val, py_date) and not isinstance(time_val, datetime)
    
    if is_date_input:
        dt = datetime.combine(time_val, datetime.min.time()).replace(tzinfo=pytz.UTC)
    elif isinstance(time_val, datetime):
        dt = time_val
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
    else:
        raise TypeError(f"Unsupported date-time class {type(time_val)}")

    # 1. Apply timezone "force"
    if tz is not None:
        target_tz = pytz.timezone(tz)
        dt = target_tz.localize(dt.replace(tzinfo=None))

    # 2. Process updates
    if "year" in final_updates:
        dt = dt.replace(year=final_updates["year"])
    
    if "month" in final_updates:
        m = final_updates["month"]
        # Handle month overflow
        while m > 12:
            dt = dt + relativedelta(years=1)
            m -= 12
        while m < 1:
            dt = dt - relativedelta(years=1)
            m += 12
        dt = dt.replace(month=m)

    if "mday" in final_updates:
        d = final_updates["mday"]
        try:
            dt = dt.replace(day=d)
        except ValueError:
            if exact:
                return None 
            
            # R timechange roll_month logic
            if roll_month == "preday":
                # Last day of the current month
                next_month = dt.replace(day=1) + relativedelta(months=1)
                dt = next_month - timedelta(days=1)
            elif roll_month == "boundary":
                # For boundary, R often returns the 1st of next month for overflows
                next_month = dt.replace(day=1) + relativedelta(months=1)
                dt = next_month.replace(hour=0, minute=0, second=0, microsecond=0)
            elif roll_month == "postday":
                # 1st of next month + (d - last_day_of_month)
                last_day_of_month = (dt.replace(day=1) + relativedelta(months=1)) - timedelta(days=1)
                days_over = d - last_day_of_month.day
                dt = (last_day_of_month + timedelta(days=1)) + timedelta(days=days_over - 1)

    if "yday" in final_updates:
        start_of_year = dt.replace(month=1, day=1)
        dt = start_of_year + timedelta(days=final_updates["yday"] - 1)

    if "wday" in final_updates:
        current_wday = dt.isoweekday()
        diff = final_updates["wday"] - current_wday
        dt = dt + timedelta(days=diff)

    if "hour" in final_updates:
        dt = dt.replace(hour=final_updates["hour"])
    if "minute" in final_updates:
        dt = dt.replace(minute=final_updates["minute"])
    if "second" in final_updates:
        dt = dt.replace(second=final_updates["second"])

    if is_date_input:
        no_time_updates = all(final_updates.get(k) is None for k in ["hour", "minute", "second"])
        if no_time_updates and tz is None:
            return dt.date()

    return dt

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