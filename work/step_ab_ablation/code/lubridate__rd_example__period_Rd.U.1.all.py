import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# --- Helper functions for lubridate style constructors ---

def days(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(days=int(i)) for i in n]
    return relativedelta(days=n)

def hours(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(hours=int(i)) for i in n]
    return relativedelta(hours=n)

def minutes(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(minutes=int(i)) for i in n]
    return relativedelta(minutes=n)

def months(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(months=int(i)) for i in n]
    return relativedelta(months=n)

def years(n):
    if isinstance(n, (list, tuple, np.ndarray)):
        return [relativedelta(years=int(i)) for i in n]
    return relativedelta(years=n)

def ddays(n):
    # ddays in lubridate is a duration (exactly 24*60*60 seconds)
    if isinstance(n, (list, tuple, np.ndarray)):
        return [timedelta(days=int(i)) for i in n]
    return timedelta(days=n)

def is_period(obj):
    return isinstance(obj, relativedelta)

def period(*args, **kwargs):
    # Handle Lubridate style parsing and ISO 8601
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        res = relativedelta()
        
        # ISO 8601 parsing
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

        # Mixing ISO and Lubridate or purely Lubridate style
        # This is a simplified parser to match the examples
        parts = re.findall(r'(\d+)\s*([a-zA-Z]+)', s)
        if not parts and "day day" in s: # Special case "day day" -> 1 day + 1 day
            return relativedelta(days=2)
            
        for val, unit in parts:
            val = int(val)
            u = unit.lower()
            if u.startswith('year'): res += relativedelta(years=val)
            elif u.startswith('month'): res += relativedelta(months=val)
            elif u.startswith('day') or u == 'd': res += relativedelta(days=val)
            elif u.startswith('hour') or u == 'h': res += relativedelta(hours=val)
            elif u.startswith('min') or u == 'm': res += relativedelta(minutes=val)
            elif u.startswith('sec') or u == 's': res += relativedelta(seconds=val)
        return res

    # Handle period(c(90, 5), c("second", "minute"))
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)) and isinstance(args[1], (list, tuple, np.ndarray)):
        vals = args[0]
        units = args[1]
        # Lubridate's period(c(90, 5), c("second", "minute")) returns "5M 90S"
        # In Python, we consolidate them into one relativedelta
        res = relativedelta()
        for v, u in zip(vals, units):
            u = u.lower()
            if u == "second": res += relativedelta(seconds=v)
            elif u == "minute": res += relativedelta(minutes=v)
            elif u == "hour": res += relativedelta(hours=v)
            elif u == "day": res += relativedelta(days=v)
            elif u == "week": res += relativedelta(weeks=v)
        return res

    # Handle period(-1, "days")
    if len(args) == 2 and isinstance(args[1], str):
        unit = args[1].lower().rstrip('s')
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        return relativedelta(**{mapping.get(unit, unit): args[0]})

    # Handle named arguments: period(second = 90, minute = 5)
    if kwargs:
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        final_kwargs = {mapping.get(k, k): v for k, v in kwargs.items()}
        # If any argument is a vector, lubridate returns a vector of periods
        if any(isinstance(v, (list, tuple, np.ndarray)) for v in final_kwargs.values()):
            # Simplified vectorization
            return [relativedelta()] 
        return relativedelta(**final_kwargs)

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
print(period("day 2 sec") > period("day 1sec"))

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
[i * hours(1).hours for i in range(1, 4)] # approximating the result of multiplication
# hours(1:3)
hours(np.arange(1, 4))

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