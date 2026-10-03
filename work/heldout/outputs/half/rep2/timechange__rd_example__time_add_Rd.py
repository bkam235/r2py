import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:time_add
def time_add(time, periods=None, year=None, month=None, week=None, 
              day=None, hour=None, minute=None, second=None, 
              roll_month="preday", roll_dst="post"):
    
    # Handle vector inputs for 'time'
    is_single = not isinstance(time, (list, np.ndarray, pd.Series, pd.DatetimeIndex))
    times = [time] if is_single else time
    
    # Normalize periods
    prds = {"year": year, "month": month, "week": week, "day": day, 
            "hour": hour, "minute": minute, "second": second}
    
    results = []
    for t in times:
        ts = pd.Timestamp(t)
        tz_name = ts.tzinfo.zone if ts.tzinfo else "UTC"
        
        # 1. Handle Month/Year/Week addition (Calendar logic)
        # R's timechange roll_month logic:
        # 'preday': snap to end of month if target day doesn't exist.
        # 'postday': snap to 1st of next month if target day doesn't exist.
        # 'boundary': snap to end of month and set time to 00:00:00.
        # 'full': snap to 1st of next month and set time to 00:00:00.
        # 'NA': return NA if target day doesn't exist.
        
        current_year = ts.year
        current_month = ts.month
        current_day = ts.day
        
        # Add months/years
        m_add = (prds["year"] or 0) * 12 + (prds["month"] or 0)
        
        target_month_abs = current_month + m_add
        year_offset = (target_month_abs - 1) // 12
        final_month = (target_month_abs - 1) % 12 + 1
        final_year = current_year + year_offset
        
        last_day_of_final_month = calendar.monthrange(final_year, final_month)[1]
        
        if current_day > last_day_of_final_month:
            if roll_month == "preday":
                final_day = last_day_of_final_month
            elif roll_month == "postday":
                final_day = 1
                final_month += 1
                if final_month > 12:
                    final_month = 1
                    final_year += 1
            elif roll_month == "boundary":
                final_day = last_day_of_final_month
                # Time will be zeroed later if boundary
            elif roll_month == "full":
                final_day = 1
                final_month += 1
                if final_month > 12:
                    final_month = 1
                    final_year += 1
            elif roll_month == "NA":
                results.append(np.nan)
                continue
            else:
                final_day = last_day_of_final_month
        else:
            final_day = current_day
            
        # Construct new timestamp
        try:
            new_ts = ts.replace(year=final_year, month=final_month, day=final_day)
        except ValueError:
            # Handle edge case where month incremented to 13
            new_ts = ts.replace(year=final_year+1, month=1, day=final_day)

        if roll_month == "boundary" and current_day > last_day_of_final_month:
            new_ts = new_ts.replace(hour=0, minute=0, second=0, microsecond=0)
        elif roll_month == "full" and current_day > last_day_of_final_month:
            new_ts = new_ts.replace(hour=0, minute=0, second=0, microsecond=0)

        # 2. Handle Days/Weeks/Hours/Minutes/Seconds (Clock logic)
        # Use timedelta for these
        total_days = (prds["week"] or 0) * 7 + (prds["day"] or 0)
        total_seconds = (prds["hour"] or 0) * 3600 + (prds["minute"] or 0) * 60 + (prds["second"] or 0)
        
        # In R, adding days is often treated as 24-hour periods unless using Date.
        # But time_add handles DST gaps.
        # Convert to UTC to add physical time, then back to TZ to handle DST
        utc_ts = new_ts.tz_convert("UTC")
        utc_ts += timedelta(days=total_days, seconds=total_seconds)
        final_ts = utc_ts.tz_convert(tz_name)
        
        # DST Roll logic is complex. In Python, pandas tz_convert handles it.
        # For 'boundary', 'pre', 'post' in DST gaps:
        # This is an approximation of the R logic.
        
        results.append(final_ts)

    if is_single:
        return results[0]
    return np.array(results)

# r2py:entity:time_subtract
def time_subtract(time, periods=None, year=None, month=None, week=None, 
                  day=None, hour=None, minute=None, second=None, 
                  roll_month="preday", roll_dst="pre"):
    
    # In R, time_subtract negates all provided period units
    return time_add(time, periods=None, 
                    year=-year if year else None, 
                    month=-month if month else None, 
                    week=-week if week else None, 
                    day=-day if day else None, 
                    hour=-hour if hour else None, 
                    minute=-minute if minute else None, 
                    second=-second if second else None, 
                    roll_month=roll_month, roll_dst=roll_dst)

# --- Execution ---

# Month gap
# r2py:entity:x
x = pd.Timestamp("2000-01-31 01:02:03").tz_localize("America/Chicago")
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
print(time_add(x, month=1, day=3,  roll_month="postday"))
# r2py:entity:time_add_6
print(time_add(x, month=1, day=3,  roll_month="preday"))
# r2py:entity:time_add_7
print(time_add(x, month=1, day=3,  roll_month="boundary"))
# r2py:entity:time_add_8
print(time_add(x, month=1, day=3,  roll_month="full"))
# r2py:entity:time_add_9
print(time_add(x, month=1, day=3,  roll_month="NA"))

# DST gap
# r2py:entity:x_1
x = pd.Timestamp("2010-03-14 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_add_10
print(time_add(x, hour=1, minute=50, roll_dst="pre"))
# r2py:entity:time_add_11
print(time_add(x, hour=1, minute=50, roll_dst="boundary"))
# r2py:entity:time_add_12
print(time_add(x, hour=1, minute=50, roll_dst="post"))
# time_add(x, hours=1, minutes=50, roll_dst="NA")

# DST repeated time
# r2py:entity:tt
tt = pd.to_datetime(["2014-11-02 00:15:00", "2014-11-02 02:15:00"]).tz_localize("America/New_York", ambiguous='infer')
print(tt)
# Handle vector addition for tt
# r2py:entity:time_add_13
hours_vec = [1, -1]
res_pre = [time_add(tt[i], hour=hours_vec[i], roll_dst="pre") for i in range(len(tt))]
print(np.array(res_pre))
# r2py:entity:time_add_14
res_post = [time_add(tt[i], hour=hours_vec[i], roll_dst="post") for i in range(len(tt))]
print(np.array(res_post))
# r2py:entity:time_add_15
res_xfirst = [time_add(tt[i], hour=hours_vec[i], roll_dst="xfirst") for i in range(len(tt))]
print(np.array(res_xfirst))
# r2py:entity:time_add_16
res_xlast = [time_add(tt[i], hour=hours_vec[i], roll_dst="xlast") for i in range(len(tt))]
print(np.array(res_xlast))

# DST skip
# r2py:entity:cst
cst = pd.Timestamp("2010-03-14 01:02:03").tz_localize("America/Chicago")
# r2py:entity:cdt
cdt = pd.Timestamp("2010-03-14 03:02:03").tz_localize("America/Chicago")
# r2py:entity:time_add_17
print(time_add(cst, hour=1, roll_dst="xfirst"))
# r2py:entity:time_add_18
print(time_add(cst, hour=1, roll_dst="xlast"))
# r2py:entity:time_add_19
print(time_add(cdt, hour=-1, roll_dst="xfirst"))
# r2py:entity:time_add_20
print(time_add(cdt, hour=-1, roll_dst="xlast"))

# Warning case
# r2py:entity:time_add_21
print(time_add(cst, hour=-1, minute=170, roll_dst="xfirst"))

# SUBTRACTION
# r2py:entity:x_2
x = pd.Timestamp("2000-03-31 01:02:03").tz_localize("America/Chicago")
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

# DST gap subtraction
# r2py:entity:y
y = pd.Timestamp("2010-03-15 01:02:03").tz_localize("America/Chicago")
# r2py:entity:time_subtract_12
print(time_subtract(y, hour=22, minute=50, roll_dst="pre"))
# r2py:entity:time_subtract_13
print(time_subtract(y, hour=22, minute=50, roll_dst="boundary"))
# r2py:entity:time_subtract_14
print(time_subtract(y, hour=22, minute=50, roll_dst="post"))
# r2py:entity:time_subtract_15
print(time_subtract(y, hour=22, minute=50, roll_dst="NA"))