import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import pytz

# r2py:entity:time_add
def time_add(time, month=0, day=0, hour=0, minute=0, second=0, year=0, week=0, roll_month="preday", roll_dst="post"):
    time_val = np.atleast_1d(time)
    
    def to_array(val):
        if isinstance(val, (list, np.ndarray, pd.Series)):
            return np.array(val)
        return np.full(len(time_val), val)

    months = to_array(month)
    days = to_array(day)
    hours = to_array(hour)
    minutes = to_array(minute)
    seconds = to_array(second)
    years = to_array(year)
    weeks = to_array(week)

    results = []
    
    for i in range(len(time_val)):
        ts = pd.Timestamp(time_val[i])
        if ts.tz is None:
            ts = ts.tz_localize('UTC')
        
        original_tz = ts.tz
        
        # 1. Month/Year Addition
        if months[i] != 0 or years[i] != 0:
            start_day = ts.day
            # Calculate target month/year
            target_ts = ts + relativedelta(years=int(years[i]), months=int(months[i]))
            end_of_target_month = calendar.monthrange(target_ts.year, target_ts.month)[1]
            
            if start_day > end_of_target_month:
                if roll_month == "NA":
                    results.append(np.nan)
                    continue
                elif roll_month == "postday" or roll_month == "boundary":
                    # R postday/boundary: if overflow, move to 1st of next month
                    # Example: Jan 31 + 1 month -> Mar 1
                    # We can achieve this by adding 1 day to the last day of the target month
                    ts = pd.Timestamp(year=target_ts.year, month=target_ts.month, day=end_of_target_month, 
                                      hour=ts.hour, minute=ts.minute, second=ts.second, tz=original_tz) + timedelta(days=1)
                    if roll_month == "boundary":
                        ts = ts.replace(hour=0, minute=0, second=0)
                elif roll_month == "full":
                    # R full: add the difference in days
                    diff = start_day - end_of_target_month
                    ts = pd.Timestamp(year=target_ts.year, month=target_ts.month, day=end_of_target_month, 
                                      hour=ts.hour, minute=ts.minute, second=ts.second, tz=original_tz) + timedelta(days=diff)
                elif roll_month == "preday":
                    ts = target_ts
            else:
                ts = target_ts

        # 2. Day/Week Addition
        ts = ts + timedelta(days=int(days[i]) + int(weeks[i])*7)
        
        # 3. Hour/Minute/Second Addition
        total_seconds = int(hours[i])*3600 + int(minutes[i])*60 + int(seconds[i])
        
        # To handle DST, we add the duration in UTC and then convert back to local
        utc_ts = ts.tz_convert('UTC')
        utc_res = utc_ts + timedelta(seconds=total_seconds)
        res_local = utc_res.tz_convert(original_tz)
        
        # Determine if the resulting wall-clock time is valid/ambiguous
        wall_clock = res_local.tz_localize(None)
        
        try:
            # Use pytz to check validity
            tz_obj = pytz.timezone(str(original_tz))
            tz_obj.localize(wall_clock, is_dst=None)
            is_ambiguous = False
            is_nonexistent = False
        except pytz.AmbiguousTimeError:
            is_ambiguous = True
            is_nonexistent = False
        except pytz.NonExistentTimeError:
            is_ambiguous = False
            is_nonexistent = True
        except Exception:
            is_ambiguous = False
            is_nonexistent = False

        if is_nonexistent:
            # DST Gap
            if roll_dst == "pre":
                # return wall clock just before the gap
                res_ts = (wall_clock - timedelta(hours=1)).tz_localize(original_tz)
            elif roll_dst == "boundary":
                # start of gap (e.g. 03:00:00 CDT)
                res_ts = wall_clock.tz_localize(original_tz, nonexistent='shifted')
            elif roll_dst == "post":
                res_ts = res_local
            elif roll_dst == "xfirst":
                # For positive addition, xfirst is 'post', for negative it is 'pre'
                res_ts = res_local if total_seconds >= 0 else (wall_clock - timedelta(hours=1)).tz_localize(original_tz)
            elif roll_dst == "xlast":
                # For positive addition, xlast is 'pre', for negative it is 'post'
                res_ts = (wall_clock - timedelta(hours=1)).tz_localize(original_tz) if total_seconds >= 0 else res_local
            else:
                res_ts = res_local
        elif is_ambiguous:
            # DST Fold
            if roll_dst == "pre":
                res_ts = wall_clock.tz_localize(original_tz, ambiguous=False)
            elif roll_dst == "post":
                res_ts = wall_clock.tz_localize(original_tz, ambiguous=True)
            elif roll_dst == "xfirst":
                res_ts = wall_clock.tz_localize(original_tz, ambiguous=False) if total_seconds >= 0 else wall_clock.tz_localize(original_tz, ambiguous=True)
            elif roll_dst == "xlast":
                res_ts = wall_clock.tz_localize(original_tz, ambiguous=True) if total_seconds >= 0 else wall_clock.tz_localize(original_tz, ambiguous=False)
            else:
                res_ts = res_local
        else:
            res_ts = res_local

        results.append(res_ts)

    if isinstance(time, (list, np.ndarray, pd.Series)):
        return pd.Series(results)
    return results[0] if len(results) == 1 else results

# r2py:entity:time_subtract
def time_subtract(time, month=0, day=0, hour=0, minute=0, second=0, year=0, week=0, roll_month="preday", roll_dst="pre"):
    return time_add(time, month=-month, day=-day, hour=-hour, minute=-minute, second=-second, year=-year, week=-week, roll_month=roll_month, roll_dst=roll_dst)

# --- START TRANSLATION ---

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
tt = pd.Series(pd.to_datetime(["2014-11-02 00:15:00", "2014-11-02 02:15:00"]).tz_localize("America/New_York"))
print(tt)
# r2py:entity:time_add_13
print(time_add(tt, hour=[1, -1], roll_dst="pre"))
# r2py:entity:time_add_14
print(time_add(tt, hour=[1, -1], roll_dst="post"))
# r2py:entity:time_add_15
print(time_add(tt, hour=[1, -1], roll_dst="xfirst"))
# r2py:entity:time_add_16
print(time_add(tt, hour=[1, -1], roll_dst="xlast"))

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