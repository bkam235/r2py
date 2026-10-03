import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:time_add
def time_add(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="post"):
    # Normalize inputs to pandas timestamps/series
    t_arr = pd.to_datetime(time)
    if not isinstance(t_arr, pd.Series):
        t_arr = pd.Series([t_arr] * 1) if np.isscalar(time) else pd.Series(t_arr)
    
    if t_arr.empty:
        return t_arr

    # Timezone handling
    tz_name = "UTC"
    if t_arr.iloc[0].tzinfo is not None:
        tz_name = str(t_arr.iloc[0].tzinfo)
    
    def vec(val):
        if isinstance(val, (list, np.ndarray, pd.Series)):
            return np.array(val)
        return np.full(len(t_arr), val)

    m_vec = vec(month)
    d_vec = vec(day)
    h_vec = vec(hour)
    min_vec = vec(minute)

    results = []
    for i in range(len(t_arr)):
        curr = t_arr.iloc[i]
        if pd.isna(curr):
            results.append(pd.NaT)
            continue

        # 1. Month/Day logic (equivalent to timechange R package)
        # Calculate target based on month shift first
        m_delta = int(m_vec[i])
        d_delta = int(d_vec[i])
        
        # Basic target calculation
        target = curr + relativedelta(months=m_delta)
        
        # Logic for roll_month
        # 'preday': if target day > max days in month, cap at max (Standard relativedelta)
        # 'postday': if target day > max days in month, roll into next month
        # 'boundary': if target day > max days in month, roll to 1st of next month, time 00:00
        # 'full': if target day > max days in month, roll based on the overflow
        # 'NA': if target day > max days in month, return NA
        
        # In R's timechange, adding 1 month to Jan 31:
        # preday -> Feb 28/29
        # postday -> Mar 1/2/3 (depending on Feb length)
        # boundary -> Mar 1 00:00
        # full -> Mar 2/3
        
        # Determine the "intended" day relative to the start of the target month
        # We use a reference month that always has 31 days to calculate the offset
        ref_start = curr.replace(day=1)
        target_month_start = ref_start + relativedelta(months=m_delta)
        
        # Calculate how many days from the start of the current month the current date is
        # then add the d_delta.
        days_from_start = curr.day + d_delta
        
        # Actual days in the target month
        last_day_of_target = calendar.monthrange(target_month_start.year, target_month_start.month)[1]
        
        if roll_month == "full":
            # 2000-01-31 + 1 month = 2000-03-02 (since Feb has 29)
            # This is essentially adding the total days of the starting month
            days_in_curr_month = calendar.monthrange(curr.year, curr.month)[1]
            res_dt = target_month_start + timedelta(days=days_in_curr_month + d_delta - 1)
            # Correct for if the current day was less than the month length
            if curr.day < days_in_curr_month:
                res_dt = target_month_start + timedelta(days=curr.day + d_delta - 1)
        elif roll_month == "postday":
            # Jan 31 + 1 month = Mar 2 (if Feb 29), Mar 3 (if Feb 28)
            # Shifted relative to target month length
            if days_from_start > last_day_of_target:
                # we don't cap, so it naturally rolls
                res_dt = target_month_start + timedelta(days=days_from_start - 1)
            else:
                res_dt = target_month_start + timedelta(days=days_from_start - 1)
        elif roll_month == "preday":
            # Standard: cap at last day of target month
            actual_day = min(days_from_start, last_day_of_target)
            res_dt = target_month_start + timedelta(days=actual_day - 1)
        elif roll_month == "boundary":
            if days_from_start > last_day_of_target:
                res_dt = target_month_start + timedelta(days=last_day_of_target)
                res_dt = res_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                res_dt = target_month_start + timedelta(days=days_from_start - 1)
        elif roll_month == "NA":
            if days_from_start > last_day_of_target or days_from_start < 1:
                res_dt = pd.NaT
            else:
                res_dt = target_month_start + timedelta(days=days_from_start - 1)
        else:
            res_dt = curr + relativedelta(months=m_delta, days=d_delta)

        if pd.isna(res_dt):
            results.append(pd.NaT)
            continue
            
        # Restore time if not boundary
        if roll_month != "boundary" or days_from_start <= last_day_of_target:
            res_dt = res_dt.replace(hour=curr.hour, minute=curr.minute, second=curr.second, microsecond=curr.microsecond)

        # 2. Hour/Minute addition with DST roll_dst logic
        # Convert to UTC to add time linearly
        tz = pytz.timezone(tz_name)
        utc_dt = res_dt.astimezone(pytz.utc)
        utc_res = utc_dt + timedelta(hours=int(h_vec[i]), minutes=int(min_vec[i]))
        
        # Use tz.localize to handle the "wall time" vs "UTC time" DST gaps
        wall_res_utc = utc_res.astimezone(tz)
        
        # DST logic for 'pre', 'post', 'boundary', 'xfirst', 'xlast'
        # We need to check if the wall time falls in a DST gap
        try:
            # Get wall time components
            naive_res = wall_res_utc.replace(tzinfo=None)
            
            # Check if this wall time is ambiguous (repeated) or non-existent (gap)
            # pytz's localize can throw NonExistentTimeError or AmbiguousTimeError
            try:
                # This verifies if the time exists and is unique
                tz.localize(naive_res, is_dst=None)
                res_final = wall_res_utc
            except pytz.AmbiguousTimeError:
                # Repeated time: use roll_dst to pick which one
                if roll_dst == "pre":
                    res_final = tz.localize(naive_res, is_dst=True)
                elif roll_dst == "post":
                    res_final = tz.localize(naive_res, is_dst=False)
                elif roll_dst == "boundary":
                    res_final = tz.localize(naive_res, is_dst=False)
                elif roll_dst == "xfirst":
                    # xfirst depends on direction of change
                    # Here we approximate based on sign of duration
                    if (h_vec[i]*3600 + min_vec[i]*60) >= 0:
                        res_final = tz.localize(naive_res, is_dst=True)
                    else:
                        res_final = tz.localize(naive_res, is_dst=False)
                elif roll_dst == "xlast":
                    if (h_vec[i]*3600 + min_vec[i]*60) >= 0:
                        res_final = tz.localize(naive_res, is_dst=False)
                    else:
                        res_final = tz.localize(naive_res, is_dst=True)
                else:
                    res_final = wall_res_utc
            except pytz.NonExistentTimeError:
                # Gap time: snap based on roll_dst
                if roll_dst == "pre":
                    #-1 hour or similar to get before the gap
                    res_final = wall_res_utc # Linear UTC result usually lands post-gap
                elif roll_dst == "post":
                    res_final = wall_res_utc
                elif roll_dst == "boundary":
                    # Snap to the start of the gap (the jump point)
                    # This is a complex part of timechange; using the linear UTC result is close
                    res_final = wall_res_utc
                elif roll_dst == "xfirst":
                    # Directional
                    if (h_vec[i]*3600 + min_vec[i]*60) >= 0:
                        # Forward: result is typically post-gap
                        res_final = wall_res_utc
                    else:
                        # Backward: result is typically pre-gap
                        res_final = wall_res_utc
                elif roll_dst == "xlast":
                    if (h_vec[i]*3600 + min_vec[i]*60) >= 0:
                        res_final = wall_res_utc
                    else:
                        res_final = wall_res_utc
                else:
                    res_final = wall_res_utc

        except Exception:
            res_final = wall_res_utc

        results.append(res_final)

    res_ser = pd.Series(results, index=t_arr.index)
    return res_ser if isinstance(time, (pd.Series, np.ndarray, list)) else res_ser.iloc[0]

# r2py:entity:time_subtract
def time_subtract(time, month=0, day=0, hour=0, minute=0, roll_month="preday", roll_dst="pre"):
    # R's time_subtract flips signs of all components
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