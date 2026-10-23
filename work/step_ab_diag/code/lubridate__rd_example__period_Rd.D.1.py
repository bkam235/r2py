import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# Helper to mimic lubridate constructors
def days(n):
    return relativedelta(days=n) if not isinstance(n, (list, np.ndarray)) else [relativedelta(days=x) for x in n]

def hours(n):
    return relativedelta(hours=n) if not isinstance(n, (list, np.ndarray)) else [relativedelta(hours=x) for x in n]

def minutes(n):
    return relativedelta(minutes=n) if not isinstance(n, (list, np.ndarray)) else [relativedelta(minutes=x) for x in n]

def months(n):
    return relativedelta(months=n) if not isinstance(n, (list, np.ndarray)) else [relativedelta(months=x) for x in n]

def years(n):
    return relativedelta(years=n) if not isinstance(n, (list, np.ndarray)) else [relativedelta(years=x) for x in n]

def ddays(n):
    # ddays in lubridate is a duration (fixed 24h)
    return timedelta(days=n) if not isinstance(n, (list, np.ndarray)) else [timedelta(days=x) for x in n]

def is_period(obj):
    return isinstance(obj, relativedelta)

def period(*args, **kwargs):
    # Handle Lubridate style parsing and ISO 8601
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        res = relativedelta()
        # ISO 8601 basics
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
        
        # Lubridate style parsing (e.g., "2M 1sec", "day day")
        parts = re.findall(r'(\d*)\s*([a-zA-Z]+)', s)
        for val, unit in parts:
            v = int(val) if val else 1
            u = unit.lower()
            if u.startswith('year'): res += relativedelta(years=v)
            elif u.startswith('month'): res += relativedelta(months=v)
            elif u.startswith('day') or u == 'd': res += relativedelta(days=v)
            elif u.startswith('hour') or u == 'h': res += relativedelta(hours=v)
            elif u.startswith('min'): res += relativedelta(minutes=v)
            elif u.startswith('sec'): res += relativedelta(seconds=v)
        return res

    # Handle vectors: period(c(90, 5), c("second", "minute"))
    if len(args) == 2 and isinstance(args[0], (list, np.ndarray)) and isinstance(args[1], (list, np.ndarray)):
        vals = args[0]
        units = args[1]
        total = relativedelta()
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        for v, u in zip(vals, units):
            u_key = mapping.get(u.rstrip('s'), u)
            total += relativedelta(**{u_key: v})
        return total

    # Handle period(-1, "days")
    if len(args) == 2 and not isinstance(args[0], (list, np.ndarray)):
        val = args[0]
        unit = args[1].rstrip('s')
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        u_key = mapping.get(unit, unit)
        return relativedelta(**{u_key: val})

    # Handle named args: period(second=90, minute=5)
    if kwargs:
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        res = relativedelta()
        
        # Process positional vector args if present
        if len(args) == 2 and isinstance(args[0], (list, np.ndarray)):
            vals, units = args[0], args[1]
            for v, u in zip(vals, units):
                u_key = mapping.get(u.rstrip('s'), u)
                res += relativedelta(**{u_key: v})
        
        # Add named kwargs
        for k, v in kwargs.items():
            u_key = mapping.get(k, k)
            if isinstance(v, (list, np.ndarray)):
                res += relativedelta(**{u_key: v[0]}) # Simplified recycling
            else:
                res += relativedelta(**{u_key: v})
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
print("day 2 sec" > "day 1sec")

# x <- ymd("2009-08-03")
x = pd.to_datetime("2009-08-03")
# x + days(1) + hours(6) + minutes(30)
res_x1 = x + days(1) + hours(6) + minutes(30)
# x + days(100) - hours(8)
res_x2 = x + days(100) - hours(8)

# class(as.Date("2009-08-09") + days(1))
date_val = pd.to_datetime("2009-08-09").date()
res_date = date_val + timedelta(days=1)
print(type(res_date))

# as.Date("2009-08-09") + hours(12)
res_hours = pd.to_datetime("2009-08-09") + hours(12)
# class(as.Date("2009-08-09") + hours(12))
print(type(res_hours))

# years(1) - months(7)
res_ym = years(1) - months(7)
# c(1:3) * hours(1)
res_h1 = [relativedelta(hours=i * 1) for i in range(1, 4)]
# hours(1:3)
res_h2 = hours([1, 2, 3])

# y <- ymd(090101)
y = pd.to_datetime("2009-01-01")
# y + months(0:11)
res_y_seq = [y + relativedelta(months=i) for i in range(12)]

# boundary <- ymd_hms("2009-03-08 01:59:59", tz = "America/Chicago")
boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
# boundary + days(1)
res_b_days = boundary + days(1)
# boundary + ddays(1)
res_b_ddays = boundary + ddays(1)

# is.period(as.Date("2009-08-03"))
print(is_period(pd.to_datetime("2009-08-03").date()))
# is.period(period(months = 1, days = 15))
print(is_period(period(months=1, days=15)))