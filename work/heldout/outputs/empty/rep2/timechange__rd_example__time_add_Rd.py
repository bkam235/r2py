import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import calendar

# r2py:entity:time_add
def time_add(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="post"):
    # Handle vector inputs
    if isinstance(time, (pd.Series, pd.DatetimeIndex, np.ndarray, list)):
        time_vals = pd.to_datetime(time)
        results = []
        for i in range(len(time_vals)):
            m = month[i] if isinstance(month, (list, np.ndarray, pd.Series)) else month
            d = day[i] if isinstance(day, (list, np.ndarray, pd.Series)) else day
            h = hour[i] if isinstance(hour, (list, np.ndarray, pd.Series)) else hour
            mi = minute[i] if isinstance(minute, (list, np.ndarray, pd.Series)) else minute
            results.append(time_add(time_vals[i], m, d, h, mi, roll_month, roll_dst))
        return pd.DatetimeIndex(results)

    dt = pd.Timestamp(time)
    tz_name = dt.tzinfo.zone if dt.tzinfo else "UTC"
    tz = pytz.timezone(tz_name)
    
    # 1. Month Addition
    if month != 0:
        orig_day = dt.day
        total_months = dt.year * 12 + (dt.month - 1) + month
        target_year = total_months // 12
        target_month = (total_months % 12) + 1
        
        last_day_of_target = calendar.monthrange(target_year, target_month)[1]
        
        if orig_day <= last_day_of_target:
            dt = dt.replace(year=target_year, month=target_month)
        else:
            if roll_month == "preday":
                dt = dt.replace(year=target_year, month=target_month, day=last_day_of_target)
            elif roll_month == "postday":
                next_month = target_month + 1
                next_year = target_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                dt = dt.replace(year=next_year, month=next_month, day=1)
            elif roll_month == "boundary":
                # R boundary for months usually means the end of that month, 
                # but the R output for time_add(x, month=1, roll_month="boundary") on Jan 31 is Mar 1.
                # This implies 'boundary' in timechange behaves like 'postday' (1st of next month) when overflow occurs.
                next_month = target_month + 1
                next_year = target_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                dt = dt.replace(year=next_year, month=next_month, day=1)
            elif roll_month == "full":
                diff = orig_day - last_day_of_target
                temp_dt = dt.replace(year=target_year, month=target_month, day=last_day_of_target)
                dt = temp_dt + pd.Timedelta(days=diff)
            elif roll_month == "NA":
                return np.nan

    # 2. Day Addition
    dt = dt + pd.Timedelta(days=day)
    
    # 3. Hour and Minute Addition with DST handling
    # Convert to UTC to add absolute time
    utc_dt = dt.tz_convert('UTC') + pd.Timedelta(hours=hour, minutes=minute)
    
    # Convert back to local and resolve DST
    # Using pytz.localize handles non-existent and ambiguous times
    local_dt_naive = utc_dt.tz_convert(tz).replace(tzinfo=None)
    
    # Check if the resulting local time is a gap or fold
    try:
        # Try to localize normally
        dt = tz.localize(local_dt_naive, is_dst=None)
    except pytz.NonExistentTimeError:
        # In a gap: roll_dst logic
        if roll_dst == "pre":
            # Time just before the gap
            dt = tz.localize(local_dt_naive - timedelta(seconds=1), is_dst=False)
        elif roll_dst == "boundary":
            # Exact start of gap (usually the jump)
            dt = tz.localize(local_dt_naive, is_dst=False) # fallback
        elif roll_dst == "post":
            dt = tz.localize(local_dt_naive, is_dst=True)
        elif roll_dst in ["xfirst", "xlast"]:
            # For gaps, xfirst/xlast typically behaves like pre/post
            dt = tz.localize(local_dt_naive, is_dst=True)
        else:
            dt = tz.localize(local_dt_naive, is_dst=True)
    except pytz.AmbiguousTimeError:
        # In a fold (repeated time)
        if roll_dst == "pre" or roll_dst == "xfirst":
            dt = tz.localize(local_dt_naive, is_dst=True) # First occurrence (DST)
        elif roll_dst == "post" or roll_dst == "xlast":
            dt = tz.localize(local_dt_naive, is_dst=False) # Second occurrence (Std)
        elif roll_dst == "boundary":
            dt = tz.localize(local_dt_naive, is_dst=True)
        else:
            dt = tz.localize(local_dt_naive, is_dst=False)

    return pd.Timestamp(dt)

# r2py:entity:time_subtract
def time_subtract(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="pre"):
    return time_add(time, month=-month, day=-day, hour=-hour, minute=-minute, roll_month=roll_month, roll_dst=roll_dst)

# Section 1
# r2py:entity:x
x = pd.Timestamp("2000-01-31 01:02:03", tz="America/Chicago")
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
x = pd.Timestamp("2010-03-14 01:02:03", tz="America/Chicago")
# r2py:entity:time_add_10
print(time_add(x, hour=1, minute=50, roll_dst="pre"))
# r2py:entity:time_add_11
print(time_add(x, hour=1, minute=50, roll_dst="boundary"))
# r2py:entity:time_add_12
print(time_add(x, hour=1, minute=50, roll_dst="post"))

# Section 3
# r2py:entity:tt
tt = pd.to_datetime(["2014-11-02 00:15:00", "2014-11-02 02:15:00"]).tz_localize("America/New_York", ambiguous='infer')
print(tt)
# r2py:entity:time_add_13
hours_vec = [1, -1]
print(time_add(tt, hour=hours_vec, roll_dst="pre"))
# r2py:entity:time_add_14
print(time_add(tt, hour=hours_vec, roll_dst="post"))
# r2py:entity:time_add_15
print(time_add(tt, hour=hours_vec, roll_dst="xfirst"))
# r2py:entity:time_add_16
print(time_add(tt, hour=hours_vec, roll_dst="xlast"))

# Section 4
# r2py:entity:cst
cst = pd.Timestamp("2010-03-14 01:02:03", tz="America/Chicago")
# r2py:entity:cdt
cdt = pd.Timestamp("2010-03-14 03:02:03", tz="America/Chicago")
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
x = pd.Timestamp("2000-03-31 01:02:03", tz="America/Chicago")
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
y = pd.Timestamp("2010-03-15 01:02:03", tz="America/Chicago")
# r2py:entity:time_subtract_12
print(time_subtract(y, hour=22, minute=50, roll_dst="pre"))
# r2py:entity:time_subtract_13
print(time_subtract(y, hour=22, minute=50, roll_dst="boundary"))
# r2py:entity:time_subtract_14
print(time_subtract(y, hour=22, minute=50, roll_dst="post"))
# r2py:entity:time_subtract_15
print(time_subtract(y, hour=22, minute=50, roll_dst="NA"))