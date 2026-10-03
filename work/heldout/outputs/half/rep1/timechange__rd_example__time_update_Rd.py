import pandas as pd
import numpy as np
from datetime import datetime, date as py_date, timedelta
import pytz
import calendar

# r2py:entity:time_update
def time_update(time, updates=None, year=None, month=None, yday=None, 
                mday=None, wday=None, hour=None, minute=None, second=None, 
                tz=None, roll_month="preday", roll_dst=("boundary", "post"), 
                week_start=1, exact=False):
    
    if time is None:
        return None
    
    # Handle sequence types
    if isinstance(time, (list, pd.Series, np.ndarray)):
        if len(time) == 0:
            return time
        return np.array([time_update(t, updates, year, month, yday, mday, wday, hour, minute, second, tz, roll_month, roll_dst, week_start, exact) for t in time])

    # Merge updates
    updts_map = {"year": year, "month": month, "yday": yday, "mday": mday, 
                 "wday": wday, "hour": hour, "minute": minute, "second": second}
    
    final_updates = updates.copy() if updates is not None else {}
    for nm, val in updts_map.items():
        if val is not None:
            if nm not in final_updates or final_updates[nm] is None:
                final_updates[nm] = val
            else:
                final_updates[nm] = final_updates[nm] + val

    final_updates = {k: v for k, v in final_updates.items() if v is not None}

    # Convert input to datetime
    is_original_date = False
    if isinstance(time, py_date) and not isinstance(time, datetime):
        dt = datetime.combine(time, datetime.min.time()).replace(tzinfo=pytz.UTC)
        is_original_date = True
    elif isinstance(time, datetime):
        dt = time
    else:
        dt = pd.to_datetime(time).to_pydatetime()
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)

    # R's tz argument in time_update behaves like force_tz (changes label, not point in time)
    if tz:
        target_tz = pytz.timezone(tz)
        # Use replace to change the tzinfo without adjusting the hours/minutes (force_tz)
        dt = dt.replace(tzinfo=target_tz)

    # 1. Handle yday (day of year)
    if "yday" in final_updates:
        y = final_updates.get("year", dt.year)
        target_date = datetime(y, 1, 1) + timedelta(days=final_updates["yday"] - 1)
        dt = dt.replace(year=target_date.year, month=target_date.month, day=target_date.day)

    # 2. Handle year/month/mday overflow logic
    if any(k in final_updates for k in ["year", "month", "mday"]):
        y = final_updates.get("year", dt.year)
        m = final_updates.get("month", dt.month)
        d = final_updates.get("mday", dt.day)

        while m > 12:
            m -= 12
            y += 1
        while m < 1:
            m += 12
            y -= 1
        
        last_day = calendar.monthrange(y, m)[1]
        if d > last_day:
            if exact:
                return None 
            if roll_month == "preday":
                d = last_day
            elif roll_month == "boundary":
                # Boundary rolls to the first of the next month and strips time (00:00:00)
                # Need to calculate next month
                m += 1
                if m > 12:
                    m = 1
                    y += 1
                d = 1
                dt = dt.replace(year=y, month=m, day=d, hour=0, minute=0, second=0, microsecond=0)
                # Return immediately because boundary strips time
                return dt
            elif roll_month == "postday":
                diff = d - last_day
                temp_dt = datetime(y, m, last_day) + timedelta(days=diff)
                y, m, d = temp_dt.year, temp_dt.month, temp_dt.day
        
        dt = dt.replace(year=y, month=m, day=d)

    # 3. Handle time components
    if "hour" in final_updates:
        dt = dt.replace(hour=final_updates["hour"])
    if "minute" in final_updates:
        dt = dt.replace(minute=final_updates["minute"])
    if "second" in final_updates:
        dt = dt.replace(second=final_updates["second"])

    # Final Return Type
    if is_original_date:
        if not any(k in final_updates for k in ["hour", "minute", "second"]) and tz is None:
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