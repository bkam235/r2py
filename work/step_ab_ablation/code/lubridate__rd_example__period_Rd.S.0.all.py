import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# Helper constructors to match lubridate style
def days(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(days=int(x)) for x in n]
    return relativedelta(days=int(n))

def hours(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(hours=int(x)) for x in n]
    return relativedelta(hours=int(n))

def minutes(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(minutes=int(x)) for x in n]
    return relativedelta(minutes=int(n))

def months(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(months=int(x)) for x in n]
    return relativedelta(months=int(n))

def years(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(years=int(x)) for x in n]
    return relativedelta(years=int(n))

def ddays(n):
    # lubridate::ddays is essentially a duration of 24*60*60 seconds
    if isinstance(n, (list, tuple, np.ndarray)):
        return [timedelta(days=int(x)) for x in n]
    return timedelta(days=int(n))

def is_period(x):
    return isinstance(x, relativedelta)

def period(*args, **kwargs):
    # Lubridate periods are complex. We use relativedelta as the Python equivalent.
    
    # Case 1: Lubridate/ISO parsing (single string argument)
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        res = relativedelta()
        # ISO 8601: P[nY][nM][nD][T[nH][nM][nS]]
        if s.startswith('P'):
            m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if m:
                groups = m.groups()
                if groups[0]: res += relativedelta(years=int(groups[0]))
                if groups[1]: res += relativedelta(months=int(groups[1]))
                if groups[2]: res += relativedelta(days=int(groups[2]))
                if groups[3]: res += relativedelta(hours=int(groups[3]))
                if groups[4]: res += relativedelta(minutes=int(groups[4]))
                if groups[5]: res += relativedelta(seconds=int(groups[5]))
                return res
        
        # Lubridate style parsing (simplified)
        # "2M 1sec", "2hours 2minutes 1second", etc.
        # Extract numbers and units
        tokens = re.findall(r'(\d+)\s*([a-zA-Z]+)', s)
        if not tokens:
            # Handle cases like "day day" (Missing numerals default to 1)
            words = re.findall(r'[a-zA-Z]+', s)
            for w in words:
                if w.lower().startswith('day'): res += relativedelta(days=1)
                elif w.lower().startswith('hour'): res += relativedelta(hours=1)
                elif w.lower().startswith('min'): res += relativedelta(minutes=1)
                elif w.lower().startswith('sec'): res += relativedelta(seconds=1)
            return res
        
        for val, unit in tokens:
            u = unit.lower()
            if u.startswith('year'): res += relativedelta(years=int(val))
            elif u.startswith('month') or (u == 'm' and 'P' not in s): res += relativedelta(months=int(val))
            elif u.startswith('day') or u == 'd': res += relativedelta(days=int(val))
            elif u.startswith('hour') or u == 'h': res += relativedelta(hours=int(val))
            elif u.startswith('min') or u == 'm': res += relativedelta(minutes=int(val))
            elif u.startswith('sec') or u == 's': res += relativedelta(seconds=int(val))
        return res

    # Case 2: Vectors for values and units
    if len(args) >= 2 and isinstance(args[0], (list, tuple, np.ndarray)):
        vals = args[0]
        units = args[1]
        # lubridate: period(c(90, 5), c("second", "minute")) -> "5M 90S"
        # It sums them into one period object
        res = relativedelta()
        for v, u in zip(vals, units):
            u = u.lower()
            if u.startswith('year'): res += relativedelta(years=v)
            elif u.startswith('month'): res += relativedelta(months=v)
            elif u.startswith('day'): res += relativedelta(days=v)
            elif u.startswith('hour'): res += relativedelta(hours=v)
            elif u.startswith('minute'): res += relativedelta(minutes=v)
            elif u.startswith('second'): res += relativedelta(seconds=v)
        
        # If named args are also provided, add them
        if kwargs:
            mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks'}
            for k, v in kwargs.items():
                py_k = mapping.get(k, k)
                if isinstance(v, (list, tuple, np.ndarray)):
                    # Simplification: only add first element if vector provided in kwargs
                    res += relativedelta(**{py_k: v[0]})
                else:
                    res += relativedelta(**{py_k: v})
        return res

    # Case 3: Single value and unit
    if len(args) == 2 and not isinstance(args[0], (list, tuple, np.ndarray)):
        val = args[0]
        unit = args[1].lower()
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks'}
        # Strip trailing 's' for mapping
        key = unit.rstrip('s') if unit.rstrip('s') in mapping else unit
        py_key = mapping.get(key, unit)
        return relativedelta(**{py_key: val})

    # Case 4: Named arguments
    if kwargs:
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        final_kwargs = {mapping.get(k, k): v for k, v in kwargs.items()}
        res = relativedelta()
        for k, v in final_kwargs.items():
            if isinstance(v, (list, tuple, np.ndarray)):
                # Handle vector named args by summing (approximate lubridate)
                res += relativedelta(**{k: sum(v)})
            else:
                res += relativedelta(**{k: v})
        return res

    return relativedelta()

# --- START TRANSLATION ---

# period(c(90, 5), c("second", "minute"))
period([90, 5], ["second", "minute"])
# period(-1, "days")
period(-1, "days")
# period(c(3, 1, 2, 13, 1), c("second", "minute", "hour", "day", "week"))
period([3, 1, 2, 13, 1], ["second", "minute", "hour", "day", "week"])
# period(c(1, -60), c("hour", "minute"))
period([1, -60], ["hour", "minute"])
# period(0, "second")
period(0, "second")

# period(second = 90, minute = 5)
period(second=90, minute=5)
# period(day = -1)
period(day=-1)
# period(second = 3, minute = 1, hour = 2, day = 13, week = 1)
period(second=3, minute=1, hour=2, day=13, week=1)
# period(hour = 1, minute = -60)
period(hour=1, minute=-60)
# period(second = 0)
period(second=0)
# period(c(1, -60), c("hour", "minute"), hour = c(1, 2), minute = c(3, 4))
period([1, -60], ["hour", "minute"], hour=[1, 2], minute=[3, 4])

# period("2M 1sec")
period("2M 1sec")
# period("2hours 2minutes 1second")
period("2hours 2minutes 1second")
# period("2d 2H 2M 2S")
period("2d 2H 2M 2S")
# period("2days 2hours 2mins 2secs")
period("2days 2hours 2mins 2secs")
# period("2 days, 2 hours, 2 mins, 2 secs")
period("2 days, 2 hours, 2 mins, 2 secs")
# period("day day")
period("day day")

# period("P10M23DT23H")
period("P10M23DT23H")
# period("10DT10M")
period("10DT10M")
# period("P3Y6M4DT12H30M5S")
period("P3Y6M4DT12H30M5S")
# period("P23DT60H 20min 100 sec")
period("P23DT60H 20min 100 sec")

# period("day 2 sec") > "day 1sec"
# Since relativedelta doesn't support string comparison, we compare their string representation
p1 = period("day 2 sec")
p2 = period("day 1sec")
print(str(p1) > str(p2))

# x <- ymd("2009-08-03")
x = pd.to_datetime("2009-08-03")
# x + days(1) + hours(6) + minutes(30)
x + days(1) + hours(6) + minutes(30)
# x + days(100) - hours(8)
x + days(100) - hours(8)

# class(as.Date("2009-08-09") + days(1))
date_obj = pd.to_datetime("2009-08-09").date()
res_date = date_obj + timedelta(days=1)
print(type(res_date))

# as.Date("2009-08-09") + hours(12)
res_hours = pd.to_datetime("2009-08-09") + hours(12)
# class(as.Date("2009-08-09") + hours(12))
print(type(res_hours))

# years(1) - months(7)
years(1) - months(7)
# c(1:3) * hours(1)
# R: c(1:3) * hours(1) multiplies the period by the vector
[i * hours(1) for i in range(1, 4)] # This is logically what happens in R
# hours(1:3)
hours(range(1, 4))

# y <- ymd(090101)
y = pd.to_datetime("2009-01-01")
# y + months(0:11)
[y + months(i) for i in range(12)]

# boundary <- ymd_hms("2009-03-08 01:59:59", tz = "America/Chicago")
boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
# boundary + days(1)
boundary + days(1)
# boundary + ddays(1)
boundary + ddays(1)

# is.period(as.Date("2009-08-03"))
is_period(pd.to_datetime("2009-08-03").date())
# is.period(period(months = 1, days = 15))
is_period(period(months=1, days=15))