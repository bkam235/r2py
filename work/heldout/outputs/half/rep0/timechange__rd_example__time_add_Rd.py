import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:time_add
def time_add(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="post"):
    ts = pd.to_datetime(time)
    is_single = False
    if not isinstance(ts, pd.DatetimeIndex):
        is_single = True
        ts = pd.DatetimeIndex([ts])
    
    def vectorize(val):
        if isinstance(val, (list, np.ndarray, pd.Series)):
            return np.broadcast_to(np.array(val), ts.shape)
        return np.full(ts.shape, val)

    m_vals = vectorize(month)
    d_vals = vectorize(day)
    h_vals = vectorize(hour)
    min_vals = vectorize(minute)
    
    results = []
    for i in range(len(ts)):
        t = ts[i]
        if pd.isna(t):
            results.append(pd.NaT)
            continue
            
        m_add = int(m_vals[i])
        d_add = int(d_vals[i])
        h_add = int(h_vals[i])
        min_add = int(min_vals[i])
        
        # 1. Month/Day Addition
        if m_add != 0 or d_add != 0:
            orig_day = t.day
            if m_add != 0:
                # target date calculation
                target = t + relativedelta(months=m_add)
                if orig_day > target.day:
                    if roll_month == "postday":
                        # R's postday: if target month is shorter, add difference to the next month
                        # Jan 31 + 1 month -> Feb 29 (leap) or Feb 28. 
                        # postday: target.day is Feb 28. diff = 31 - 28 = 3. target + 3 days = March 3? 
                        # No, R's time_add(Jan 31, month=1, roll_month="postday") is 2000-03-01.
                        # Jan 31 + 1 month -> Feb 29. Diff = 2. Feb 29 + 1 = March 1.
                        # Correct logic: target is end of month, then add (orig_day - target.day)
                        last_day_target = calendar.monthrange(target.year, target.month)[1]
                        diff = orig_day - last_day_target
                        target = target.replace(day=last_day_target) + timedelta(days=diff)
                    elif roll_month == "preday":
                        pass # relativedelta already clamps to end of month (preday)
                    elif roll_month == "boundary":
                        # Snap to end of target month
                        last_day = calendar.monthrange(target.year, target.month)[1]
                        target = target.replace(day=last_day)
                    elif roll_month == "full":
                        # Similar to postday but often involves different logic for 'full' month periods
                        last_day_target = calendar.monthrange(target.year, target.month)[1]
                        diff = orig_day - last_day_target
                        target = target.replace(day=last_day_target) + timedelta(days=diff)
                    elif roll_month == "NA":
                        target = pd.NaT
            else:
                target = t
            
            if not pd.isna(target):
                target = target + timedelta(days=d_add)
            t = target

        # 2. Hour/Minute Addition and DST
        if not pd.isna(t) and (h_add != 0 or min_add != 0):
            tz_name = t.tzinfo.zone if t.tzinfo else "UTC"
            tz = pytz.timezone(tz_name)
            
            # Compute target wall-clock time
            naive = t.replace(tzinfo=None) + timedelta(hours=h_add, minutes=min_add)
            
            try:
                # Attempt localize
                t = tz.localize(naive, is_dst=None)
            except pytz.NonExistentTimeError:
                # DST GAP (Spring Forward)
                # R 'pre' in gap: result is the time just before the gap (Standard Time)
                if roll_dst == "pre":
                    t = tz.localize(naive, is_dst=False)
                elif roll_dst == "post":
                    # R 'post' in gap: result is the time after the gap (DST Time)
                    t = tz.localize(naive + timedelta(hours=1), is_dst=True)
                elif roll_dst == "boundary":
                    # Boundary is usually the exact transition
                    t = tz.localize(naive + timedelta(hours=1), is_dst=True)
                elif roll_dst == "xfirst":
                    t = tz.localize(naive, is_dst=False)
                elif roll_dst == "xlast":
                    t = tz.localize(naive + timedelta(hours=1), is_dst=True)
                else:
                    t = pd.NaT
            except pytz.AmbiguousTimeError:
                # DST OVERLAP (Fall Back)
                if roll_dst == "pre":
                    t = tz.localize(naive, is_dst=True) # First occurrence (DST)
                elif roll_dst == "post":
                    t = tz.localize(naive, is_dst=False) # Second occurrence (STD)
                elif roll_dst == "xfirst":
                    t = tz.localize(naive, is_dst=True)
                elif roll_dst == "xlast":
                    t = tz.localize(naive, is_dst=False)
                else:
                    t = tz.localize(naive, is_dst=False)

        results.append(t)
    
    res_idx = pd.DatetimeIndex(results)
    return res_idx[0] if is_single else res_idx

# r2py:entity:time_subtract
def time_subtract(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="post"):
    return time_add(time, month=-month, day=-day, hour=-hour, minute=-minute, roll_month=roll_month, roll_dst=roll_dst)

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
print(time_add(tt, hour=np.array([1, -1]), roll_dst="pre"))
# r2py:entity:time_add_14
print(time_add(tt, hour=np.array([1, -1]), roll_dst="post"))
# r2py:entity:time_add_15
print(time_add(tt, hour=np.array([1, -1]), roll_dst="xfirst"))
# r2py:entity:time_add_16
print(time_add(tt, hour=np.array([1, -1]), roll_dst="xlast"))

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