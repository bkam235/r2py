import pandas as pd
import numpy as np
from datetime import datetime, date as py_date
import pytz
import calendar

# r2py:entity:time_update
def time_update(time, updates=None, year=None, month=None, yday=None, 
                mday=None, wday=None, hour=None, minute=None, second=None, 
                tz=None, roll_month="preday", roll_dst=("boundary", "post"), 
                week_start=1, exact=False):
    
    if time is None:
        return None

    # Normalize input to pandas Timestamp
    is_date_input = False
    if isinstance(time, py_date) and not isinstance(time, datetime):
        dt = pd.Timestamp(time).tz_localize('UTC')
        is_date_input = True
    elif isinstance(time, datetime):
        dt = pd.Timestamp(time)
        if dt.tzinfo is None:
            dt = dt.tz_localize('UTC')
    else:
        dt = pd.to_datetime(time)
        if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
            dt = dt.tz_localize('UTC')

    # Consolidate updates
    actual_updates = {}
    if updates is not None:
        actual_updates.update(updates)
    
    fields = {'year': year, 'month': month, 'yday': yday, 'mday': mday, 
              'wday': wday, 'hour': hour, 'minute': minute, 'second': second}
    
    for field, val in fields.items():
        if val is not None:
            if field in actual_updates:
                actual_updates[field] += val
            else:
                actual_updates[field] = val

    # Timezone update (force_tz behavior: change TZ without changing wall clock)
    if tz is not None:
        new_tz = pytz.timezone(tz)
        dt = dt.tz_localize(None).tz_localize(new_tz)

    # Handle yday (day of year) - must preserve time
    if 'yday' in actual_updates:
        yday_val = actual_updates['yday']
        target_year = actual_updates.get('year', dt.year)
        year_start = pd.Timestamp(year=target_year, month=1, day=1, 
                                  hour=dt.hour, minute=dt.minute, second=dt.second, 
                                  microsecond=dt.microsecond, tz=dt.tz)
        dt = year_start + pd.Timedelta(days=yday_val - 1)
        actual_updates.pop('yday')

    # Handle month and mday rolling logic
    if 'month' in actual_updates or 'mday' in actual_updates:
        target_month = actual_updates.get('month', dt.month)
        target_day = actual_updates.get('mday', dt.day)
        target_year = actual_updates.get('year', dt.year)

        # Handle month overflow (e.g., month=13)
        while target_month > 12:
            target_year += 1
            target_month -= 12
        while target_month < 1:
            target_year -= 1
            target_month += 12
        
        # Validate day of month
        try:
            dt = dt.replace(year=target_year, month=target_month, day=target_day)
        except ValueError:
            if exact:
                return None
            
            last_day = calendar.monthrange(target_year, target_month)[1]
            if roll_month == "preday":
                dt = dt.replace(year=target_year, month=target_month, day=last_day)
            elif roll_month == "boundary":
                next_month = target_month + 1
                next_year = target_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                dt = dt.replace(year=next_year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            elif roll_month == "postday":
                next_month = target_month + 1
                next_year = target_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                dt = dt.replace(year=next_year, month=next_month, day=1)
        else:
            # If replace succeeded, ensure the overflowed year is used
            dt = dt.replace(year=target_year)

    # Apply remaining replacements (year is already handled in month logic if present)
    if 'year' in actual_updates and 'month' not in actual_updates:
        dt = dt.replace(year=actual_updates['year'])
    if 'hour' in actual_updates:
        dt = dt.replace(hour=actual_updates['hour'])
    if 'minute' in actual_updates:
        dt = dt.replace(minute=actual_updates['minute'])
    if 'second' in actual_updates:
        dt = dt.replace(second=actual_updates['second'])

    # Return format
    if is_date_input and hour is None and minute is None and second is None and tz is None:
        return dt.date()
    
    # For boundary case in R, the output is often just the date part if time was reset
    if roll_month == "boundary" and dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt.date().strftime('%Y-%m-%d') if is_date_input else dt.strftime('%Y-%m-%d')
    
    return dt

# r2py:entity:date
date = pd.to_datetime("2009-02-10").date()
# r2py:entity:time_update
print(time_update(date, year=2010, month=1, mday=1))
# r2py:entity:time_update_1
print(time_update(date, year=2010, month=13, mday=1))
# r2py:entity:time_update_2
print(time_update(date, minute=10, second=3))
# r2py:entity:time_update_3
print(time_update(date, minute=10, second=3, tz="America/New_York"))

# r2py:entity:time
time = pd.to_datetime("2015-02-03 01:02:03").tz_localize("America/New_York")
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
time = pd.to_datetime("2015-02-03 01:02:03").tz_localize("America/New_York")
# r2py:entity:time_update_9
print(time_update(time, year=2016, yday=10))
# r2py:entity:time_update_10
print(time_update(time, year=2016, yday=10, tz="Europe/Amsterdam"))
# r2py:entity:time_update_11
print(time_update(time, second=30, tz="America/New_York"))