import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from pandas.tseries.offsets import DateOffset

# r2py:entity:time_add
def time_add(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="post"):
    # Ensure time is a pandas Timestamp or DatetimeIndex
    if isinstance(time, (list, np.ndarray, pd.Index)):
        time = pd.DatetimeIndex(time)
    else:
        time = pd.to_datetime(time)
    
    # Handle vectorization for parameters
    def to_vec(val):
        if isinstance(val, (list, np.ndarray, pd.Series)):
            return np.array(val)
        return np.full(len(time) if hasattr(time, '__len__') else 1, val)

    months = to_vec(month)
    days = to_vec(day)
    hours = to_vec(hour)
    minutes = to_vec(minute)

    results = []
    time_vals = time if hasattr(time, '__iter__') else [time]
    
    for i in range(len(time_vals)):
        t = time_vals[i]
        m = months[i]
        d = days[i]
        h = hours[i]
        mi = minutes[i]
        
        # 1. Month Addition Logic
        if m != 0:
            orig_day = t.day
            # Use DateOffset to move months
            res = t + pd.DateOffset(months=int(m))
            target_day = res.day
            
            if roll_month == "boundary":
                # boundary: Jan 31 + 1 month -> Feb 28/29 (pandas default)
                # But we must ensure the time is preserved exactly.
                pass
            elif roll_month == "postday":
                # postday: Jan 31 + 1 month -> Mar 2/3 (days overflow)
                if target_day < orig_day:
                    res = res + pd.Timedelta(days=orig_day - target_day)
            elif roll_month == "preday":
                # preday: Jan 31 + 1 month -> Feb 28/29 (pandas default)
                pass
            elif roll_month == "full":
                # full: Jan 31 + 1 month -> Mar 2/3
                if target_day < orig_day:
                    res = res + pd.Timedelta(days=orig_day - target_day)
            elif roll_month == "NA":
                if target_day != orig_day:
                    res = pd.NaT
        else:
            res = t

        if pd.isna(res):
            results.append(pd.NaT)
            continue

        # 2. Days, Hours, Minutes
        # R adds these sequentially.
        res = res + pd.Timedelta(days=int(d), hours=int(h), minutes=int(mi))

        # 3. DST Handling (roll_dst)
        # This is the hardest part to mimic without C_time_add.
        # We use tz_localize with 'nonexistent' and 'ambiguous' flags.
        tz_name = res.tz.zone if res.tz else "UTC"
        naive = res.tz_localize(None)
        
        try:
            if roll_dst == "pre":
                # Shift to the time before the gap
                res = tz_name_localize(naive, tz_name, nonexistent="shift_backward", ambiguous="infer")
            elif roll_dst == "post":
                # Shift to the time after the gap
                res = tz_name_localize(naive, tz_name, nonexistent="shift_forward", ambiguous="infer")
            elif roll_dst == "boundary":
                # Usually the gap edge
                res = tz_name_localize(naive, tz_name, nonexistent="shift_forward", ambiguous="infer")
            elif roll_dst == "xfirst":
                # For overlap, pick first instance (DST)
                res = tz_name_localize(naive, tz_name, nonexistent="shift_forward", ambiguous=True)
            elif roll_dst == "xlast":
                # For overlap, pick last instance (STD)
                res = tz_name_localize(naive, tz_name, nonexistent="shift_forward", ambiguous=False)
        except:
            res = res.tz_convert(res.tz)
            
        results.append(res)

    if hasattr(time, '__iter__'):
        return pd.DatetimeIndex(results)
    return results[0]

def tz_name_localize(naive, tz_name, nonexistent, ambiguous):
    return pd.Timestamp(naive).tz_localize(tz_name, nonexistent=nonexistent, ambiguous=ambiguous)

# r2py:entity:time_subtract
def time_subtract(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="pre"):
    return time_add(time, month=-month, day=-day, hour=-hour, minute=-minute, 
                    roll_month=roll_month, roll_dst=roll_dst)

# --- Translation Starts Here ---

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
print(tt)
# r2py:entity:time_add_13
print(time_add(tt, hour=[1, -1], roll_dst="pre"))
# r2py:entity:time_add_14
print(time_add(tt, hour=[1, -1], roll_dst="post"))
# r2py:entity:time_add_15
print(time_add(tt, hour=[1, -1], roll_dst="xfirst"))
# r2py:entity:time_add_16
print(time_add(tt, hour=[1, -1], roll_dst="xlast"))

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