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
    
    updts_args = {'year': year, 'month': month, 'yday': yday, 'mday': mday, 
                  'wday': wday, 'hour': hour, 'minute': minute, 'second': second}
    
    final_updates = updates.copy() if updates is not None else {}
    for nm, val in updts_args.items():
        if val is not None:
            if nm not in final_updates or final_updates[nm] is None:
                final_updates[nm] = val
            else:
                final_updates[nm] = final_updates[nm] + val

    final_updates = {k: v for k, v in final_updates.items() if v is not None}

    is_date_only = False
    if isinstance(time_val, py_date) and not isinstance(time_val, datetime):
        is_date_only = True
        dt = datetime.combine(time_val, datetime.min.time())
        current_tz = pytz.UTC
    elif isinstance(time_val, pd.Timestamp):
        dt = time_val.to_pydatetime()
        current_tz = dt.tzinfo if dt.tzinfo else pytz.UTC
    elif isinstance(time_val, datetime):
        dt = time_val
        current_tz = dt.tzinfo if dt.tzinfo else pytz.UTC
    else:
        raise TypeError(f"Unsupported date-time class '{type(time_val)}'")

    # R's tz argument in time_update is like force_tz: it changes the zone without changing wall-clock time.
    if tz is not None:
        target_tz = pytz.timezone(tz)
        if dt.tzinfo is None:
            dt = target_tz.localize(dt)
        else:
            # force_tz behavior: replace tzinfo
            dt = dt.replace(tzinfo=None)
            dt = target_tz.localize(dt)
        current_tz = target_tz

    # 1. Handle yday
    if 'yday' in final_updates:
        y = final_updates.get('year', dt.year)
        # Construct date at start of year with current time
        start_of_year = datetime(y, 1, 1, dt.hour, dt.minute, dt.second, dt.microsecond)
        if dt.tzinfo:
            start_of_year = current_tz.localize(start_of_year) if start_of_year.tzinfo is None else start_of_year.replace(tzinfo=current_tz)
        dt = start_of_year + timedelta(days=final_updates['yday'] - 1)

    # 2. Year
    if 'year' in final_updates and 'yday' not in final_updates:
        dt = dt.replace(year=final_updates['year'])

    # 3. Month and Day logic
    if 'month' in final_updates or 'mday' in final_updates:
        m = final_updates.get('month', dt.month)
        d = final_updates.get('mday', dt.day)
        
        # Month overflow logic (R style)
        if m < 1 or m > 12:
            year_offset = (m - 1) // 12
            m = ((m - 1) % 12) + 1
            dt = dt.replace(year=dt.year + year_offset)

        try:
            dt = dt.replace(month=m, day=d)
        except ValueError:
            if exact:
                return None
            
            last_day = calendar.monthrange(dt.year, m)[1]
            if roll_month == "preday" or roll_month == "boundary":
                dt = dt.replace(month=m, day=last_day)
            elif roll_month == "postday":
                # Roll into next month: d=31 for Feb (28 days) becomes Mar 3.
                # Use a reference date at the start of the month to calculate overflow
                ref = datetime(dt.year, m, 1, dt.hour, dt.minute, dt.second, dt.microsecond)
                if dt.tzinfo:
                    ref = current_tz.localize(ref)
                dt = ref + timedelta(days=d - 1)

    # 4. Time components
    if 'hour' in final_updates:
        dt = dt.replace(hour=final_updates['hour'])
    if 'minute' in final_updates:
        dt = dt.replace(minute=final_updates['minute'])
    if 'second' in final_updates:
        dt = dt.replace(second=final_updates['second'])

    if is_date_only and not any(k in final_updates for k in ['hour', 'minute', 'second']) and tz is None:
        return dt.date()
    
    return dt

# --- Main Script ---

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
time = pd.Timestamp("2015-02-03 01:02:03", tz="America/New_York")
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
time = pd.Timestamp("2015-02-03 01:02:03", tz="America/New_York")
# r2py:entity:time_update_9
print(time_update(time, year=2016, yday=10))
# r2py:entity:time_update_10
print(time_update(time, year=2016, yday=10, tz="Europe/Amsterdam"))
# r2py:entity:time_update_11
print(time_update(time, second=30, tz="America/New_York"))