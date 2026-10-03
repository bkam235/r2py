import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import calendar

def get_month_end(year, month):
    return calendar.monthrange(year, month)[1]

# r2py:entity:time_add
def time_add(time, periods=None, year=0, month=0, week=0, day=0, hour=0, minute=0, second=0, roll_month="preday", roll_dst="post"):
    is_scalar = not isinstance(time, (list, np.ndarray, pd.Series, pd.DatetimeIndex))
    times = pd.Series(time) if not isinstance(time, pd.Series) else time
    if isinstance(time, pd.DatetimeIndex):
        times = pd.Series(time)

    # Normalize periods
    all_periods = {}
    if periods is not None:
        all_periods.update(periods)
    
    named_args = {"year": year, "month": month, "week": week, "day": day, "hour": hour, "minute": minute, "second": second}
    for k, v in named_args.items():
        if v != 0:
            all_periods[k] = all_periods.get(k, 0) + v

    def process_single(t):
        if pd.isna(t):
            return pd.NaT
        
        current = pd.Timestamp(t)
        tz_name = current.tzinfo.zone if current.tzinfo else "UTC"
        local_tz = pytz.timezone(tz_name)
        
        # 1. Year/Month Logic
        m_add = all_periods.get("month", 0)
        y_add = all_periods.get("year", 0)
        
        if m_add != 0 or y_add != 0:
            orig_day = current.day
            orig_month = current.month
            orig_year = current.year
            
            total_months = orig_year * 12 + (orig_month - 1) + y_add * 12 + m_add
            new_year = total_months // 12
            new_month = (total_months % 12) + 1
            max_day = get_month_end(new_year, new_month)
            
            if orig_day <= max_day:
                current = current.replace(year=new_year, month=new_month)
            else:
                if roll_month == "preday":
                    current = current.replace(year=new_year, month=new_month, day=max_day)
                elif roll_month == "postday":
                    next_m = new_month + 1
                    next_y = new_year
                    if next_m > 12:
                        next_m = 1
                        next_y += 1
                    current = current.replace(year=next_y, month=next_m, day=1)
                elif roll_month == "boundary":
                    # R's roll_month="boundary" results in the 1st of the next month at 00:00:00
                    next_m = new_month + 1
                    next_y = new_year
                    if next_m > 12:
                        next_m = 1
                        next_y += 1
                    current = current.replace(year=next_y, month=next_m, day=1, hour=0, minute=0, second=0, microsecond=0)
                elif roll_month == "full":
                    temp = current.replace(year=new_year, month=new_month, day=1)
                    current = temp + pd.Timedelta(days=orig_day - 1)
                elif roll_month == "NA":
                    return pd.NaT
                else:
                    current = current.replace(year=new_year, month=new_month, day=max_day)

        # 2. Day/Week Logic
        d_add = all_periods.get("day", 0) + all_periods.get("week", 0) * 7
        if d_add != 0:
            current = current + pd.Timedelta(days=d_add)
            
        # 3. Hour/Minute/Second Logic & DST
        h_add = all_periods.get("hour", 0)
        m_add = all_periods.get("minute", 0)
        s_add = all_periods.get("second", 0)
        
        if h_add != 0 or m_add != 0 or s_add != 0:
            seconds_to_add = h_add * 3600 + m_add * 60 + s_add
            
            # Perform physical addition in UTC
            utc_t = current.astimezone(pytz.utc)
            utc_res = utc_t + pd.Timedelta(seconds=seconds_to_add)
            
            # Convert back to local
            local_res = utc_res.astimezone(local_tz)
            
            # For DST Gap/Overlap logic:
            wall_clock = local_res.replace(tzinfo=None)
            try:
                # Try to localize wall clock. If it fails, it's a gap or overlap.
                local_tz.localize(wall_clock, is_dst=None)
            except pytz.NonExistentTimeError:
                # GAP
                if roll_dst == "pre":
                    # Before the gap (Standard Time side)
                    return local_res - pd.Timedelta(hours=1) # Approximation for R 'pre' in gaps
                elif roll_dst == "boundary":
                    # The jump point (start of DST)
                    # For Chicago 2010-03-14, jump is at 02:00 -> 03:00. Boundary is 03:00.
                    return local_res.replace(minute=0, second=0, microsecond=0)
                elif roll_dst == "post":
                    return local_res
                elif roll_dst == "xfirst":
                    # If adding, xfirst is usually 'pre' (though R logic is complex)
                    return local_res - pd.Timedelta(hours=1) if seconds_to_add > 0 else local_res
                elif roll_dst == "xlast":
                    return local_res
                return local_res
            except pytz.AmbiguousTimeError:
                # OVERLAP
                if roll_dst == "pre":
                    return local_tz.localize(wall_clock, is_dst=True)
                elif roll_dst == "post":
                    return local_tz.localize(wall_clock, is_dst=False)
                elif roll_dst == "xfirst":
                    return local_tz.localize(wall_clock, is_dst=True)
                elif roll_dst == "xlast":
                    return local_tz.localize(wall_clock, is_dst=False)
                return local_res
            
            return local_res
        
        return current

    res = times.apply(process_single)
    return res.iloc[0] if is_scalar else res

# r2py:entity:time_subtract
def time_subtract(time, periods=None, year=0, month=0, week=0, day=0, hour=0, minute=0, second=0, roll_month="preday", roll_dst="pre"):
    all_periods = {}
    if periods is not None:
        all_periods = {k: -v for k, v in periods.items()}
    return time_add(time, periods=all_periods, year=-year, month=-month, week=-week, day=-day, hour=-hour, minute=-minute, second=-second, roll_month=roll_month, roll_dst=roll_dst)

# --- Translation ---

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

# r2py:entity:x_1
x = pd.Timestamp("2010-03-14 01:02:03", tz="America/Chicago")
# r2py:entity:time_add_10
print(time_add(x, hour=1, minute=50, roll_dst="pre"))
# r2py:entity:time_add_11
print(time_add(x, hour=1, minute=50, roll_dst="boundary"))
# r2py:entity:time_add_12
print(time_add(x, hour=1, minute=50, roll_dst="post"))

# r2py:entity:tt
tt = pd.to_datetime(["2014-11-02 00:15:00", "2014-11-02 02:15:00"]).tz_localize("America/New_York")
print(tt)
hours_vec = np.array([1, -1])
# r2py:entity:time_add_13
print([time_add(tt[i], hour=hours_vec[i], roll_dst="pre") for i in range(len(tt))])
# r2py:entity:time_add_14
print([time_add(tt[i], hour=hours_vec[i], roll_dst="post") for i in range(len(tt))])
# r2py:entity:time_add_15
print([time_add(tt[i], hour=hours_vec[i], roll_dst="xfirst") for i in range(len(tt))])
# r2py:entity:time_add_16
print([time_add(tt[i], hour=hours_vec[i], roll_dst="xlast") for i in range(len(tt))])

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