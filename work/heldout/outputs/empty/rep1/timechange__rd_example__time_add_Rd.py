import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:time_add
def time_add(time, periods=None, year=0, month=0, week=0, day=0, hour=0, minute=0, second=0, roll_month="preday", roll_dst="post"):
    # Handle vectorized input
    is_single = False
    if not isinstance(time, (pd.Series, np.ndarray, list)):
        is_single = True
        time = [time]
    
    # Handle periods list
    effective_periods = {"year": year, "month": month, "week": week, "day": day, "hour": hour, "minute": minute, "second": second}
    if periods is not None:
        for k, v in periods.items():
            effective_periods[k] = effective_periods.get(k, 0) + v

    results = []
    for t in time:
        if pd.isna(t):
            results.append(pd.NaT)
            continue
        
        current_tz = t.tzinfo if hasattr(t, 'tzinfo') else pytz.UTC
        dt = t
        
        # 1. Calendar additions
        m_add = effective_periods.get("month", 0)
        y_add = effective_periods.get("year", 0)
        
        if m_add != 0 or y_add != 0:
            old_day = dt.day
            # In R timechange, month addition logic is specific:
            # 'preday' (default): if day > max(new_month), cap at max(new_month)
            # 'postday': if day > max(new_month), overflow into next month
            # 'boundary': if day > max(new_month), cap at max(new_month) AND time = 00:00:00
            # 'full': if day > max(new_month), overflow AND add 1 day
            # 'NA': if day > max(new_month), return NA
            
            # Calculate target year and month
            target_month = dt.month + m_add
            target_year = dt.year + y_add + (target_month - 1) // 12
            target_month = (target_month - 1) % 12 + 1
            
            max_day_in_new = calendar.monthrange(target_year, target_month)[1]
            
            if old_day <= max_day_in_new:
                dt = dt.replace(year=target_year, month=target_month)
            else:
                if roll_month == "NA":
                    dt = pd.NaT
                elif roll_month == "preday":
                    dt = dt.replace(year=target_year, month=target_month, day=max_day_in_new)
                elif roll_month == "boundary":
                    dt = dt.replace(year=target_year, month=target_month, day=max_day_in_new, hour=0, minute=0, second=0, microsecond=0)
                elif roll_month == "postday":
                    # Overflow into next month: start at 1st of target_month and add old_day-1 days
                    base = dt.replace(year=target_year, month=target_month, day=1)
                    dt = base + timedelta(days=old_day - 1)
                elif roll_month == "full":
                    # Overflow + 1 day
                    base = dt.replace(year=target_year, month=target_month, day=1)
                    dt = base + timedelta(days=old_day)

        # Week/Day addition
        dt = dt + timedelta(weeks=effective_periods.get("week", 0), days=effective_periods.get("day", 0))
        
        if pd.isna(dt):
            results.append(pd.NaT)
            continue

        # 2. Clock additions
        h_add = effective_periods.get("hour", 0)
        mi_add = effective_periods.get("minute", 0)
        s_add = effective_periods.get("second", 0)
        
        if h_add != 0 or mi_add != 0 or s_add != 0:
            # To handle DST gaps/overlaps as R does, we work with UTC absolute time
            utc_dt = dt.astimezone(pytz.UTC)
            utc_dt = utc_dt + timedelta(hours=h_add, minutes=mi_add, seconds=s_add)
            
            # Convert back to local. We use the wall clock time of the UTC result.
            res_local_naive = utc_dt.astimezone(current_tz).replace(tzinfo=None)
            
            # roll_dst logic
            # 'pre': before gap/overlap (UTC result might land in gap, then shift back)
            # 'post': after gap/overlap
            # 'xfirst': first occurrence of wall clock time
            # 'xlast': last occurrence of wall clock time
            # 'boundary': transition point
            
            try:
                if roll_dst == "xfirst":
                    dt = current_tz.localize(res_local_naive, is_dst=True)
                elif roll_dst == "xlast":
                    dt = current_tz.localize(res_local_naive, is_dst=False)
                elif roll_dst == "pre":
                    # Standard normalize often shifts post-gap; we try to force pre
                    dt = current_tz.normalize(current_tz.localize(res_local_naive, is_dst=True))
                elif roll_dst == "post":
                    dt = current_tz.normalize(current_tz.localize(res_local_naive, is_dst=False))
                elif roll_dst == "boundary":
                    # R's boundary for DST is the exact transition wall-clock time
                    # Simplified: we use the converted UTC time
                    dt = utc_dt.astimezone(current_tz)
                else:
                    dt = utc_dt.astimezone(current_tz)
            except:
                dt = utc_dt.astimezone(current_tz)

        results.append(dt)

    res = pd.Series(results)
    return res[0] if is_single else res

# r2py:entity:time_subtract
def time_subtract(time, periods=None, year=0, month=0, week=0, day=0, hour=0, minute=0, second=0, roll_month="preday", roll_dst="pre"):
    effective_periods = {}
    if periods is not None:
        effective_periods = {k: -v for k, v in periods.items()}
    
    # Subtract provided arguments
    for k, v in {"year": year, "month": month, "week": week, "day": day, "hour": hour, "minute": minute, "second": second}.items():
        effective_periods[k] = effective_periods.get(k, 0) - v
        
    return time_add(time, periods=effective_periods, roll_month=roll_month, roll_dst=roll_dst)

# Setup timezone
tz_chi = pytz.timezone("America/Chicago")
tz_ny = pytz.timezone("America/New_York")

# r2py:entity:x
x = tz_chi.localize(datetime(2000, 1, 31, 1, 2, 3))
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

# r2py:entity:x_1
x = tz_chi.localize(datetime(2010, 3, 14, 1, 2, 3))
# r2py:entity:time_add_10
print(time_add(x, hour=1, minute=50, roll_dst="pre"))
# r2py:entity:time_add_11
print(time_add(x, hour=1, minute=50, roll_dst="boundary"))
# r2py:entity:time_add_12
print(time_add(x, hour=1, minute=50, roll_dst="post"))

# r2py:entity:tt
tt = pd.Series([
    tz_ny.localize(datetime(2014, 11, 2, 0, 15, 0)),
    tz_ny.localize(datetime(2014, 11, 2, 2, 15, 0))
])
print(tt)
hours_vec = [1, -1]
# r2py:entity:time_add_13
res_pre = pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="pre") for i in range(len(tt))])
print(res_pre)
# r2py:entity:time_add_14
res_post = pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="post") for i in range(len(tt))])
print(res_post)
# r2py:entity:time_add_15
res_xfirst = pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="xfirst") for i in range(len(tt))])
print(res_xfirst)
# r2py:entity:time_add_16
res_xlast = pd.Series([time_add(tt[i], hour=hours_vec[i], roll_dst="xlast") for i in range(len(tt))])
print(res_xlast)

# r2py:entity:cst
cst = tz_chi.localize(datetime(2010, 3, 14, 1, 2, 3))
# r2py:entity:cdt
cdt = tz_chi.localize(datetime(2010, 3, 14, 3, 2, 3))
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

# r2py:entity:x_2
x = tz_chi.localize(datetime(2000, 3, 31, 1, 2, 3))
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

# r2py:entity:y
y = tz_chi.localize(datetime(2010, 3, 15, 1, 2, 3))
# r2py:entity:time_subtract_12
print(time_subtract(y, hour=22, minute=50, roll_dst="pre"))
# r2py:entity:time_subtract_13
print(time_subtract(y, hour=22, minute=50, roll_dst="boundary"))
# r2py:entity:time_subtract_14
print(time_subtract(y, hour=22, minute=50, roll_dst="post"))
# r2py:entity:time_subtract_15
print(time_subtract(y, hour=22, minute=50, roll_dst="NA"))