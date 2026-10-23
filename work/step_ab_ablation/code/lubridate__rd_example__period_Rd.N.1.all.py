import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# --- HELPERS TO MIMIC LUBRIDATE ---

def period(*args, **kwargs):
    """
    Approximates lubridate::period. 
    Handles:
    - Vectors of values and units: period(c(90, 5), c("second", "minute"))
    - Single value and unit: period(-1, "days")
    - Named arguments: period(second=90, minute=5)
    - Lubridate style strings: "2M 1sec"
    - ISO 8601 strings: "P10M23DT23H"
    """
    unit_map = {
        'second': 'seconds', 'seconds': 'seconds',
        'minute': 'minutes', 'minutes': 'minutes', 'min': 'minutes', 'mins': 'minutes',
        'hour': 'hours', 'hours': 'hours', 'hr': 'hours', 'hrs': 'hours',
        'day': 'days', 'days': 'days', 'd': 'days',
        'week': 'weeks', 'weeks': 'weeks', 'w': 'weeks',
        'month': 'months', 'months': 'months', 'M': 'months',
        'year': 'years', 'years': 'years', 'Y': 'years'
    }

    # Case: period("string")
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        res = relativedelta()
        
        # ISO 8601 Parsing
        if s.startswith('P'):
            # P[n]Y[n]M[n]DT[n]H[n]M[n]S
            # Note: M is months if before T, minutes if after T
            match = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if match:
                g = match.groups()
                if g[0]: res += relativedelta(years=int(g[0]))
                if g[1]: res += relativedelta(months=int(g[1]))
                if g[2]: res += relativedelta(days=int(g[2]))
                if g[3]: res += relativedelta(hours=int(g[3]))
                if g[4]: res += relativedelta(minutes=int(g[4]))
                if g[5]: res += relativedelta(seconds=int(g[5]))
                return res

        # Lubridate style parsing (simplified regex)
        # Matches numbers followed by unit labels
        pattern = r'(\d+)\s*([a-zA-Z]+)'
        matches = re.findall(pattern, s)
        if not matches:
            # Handle cases like "day day" where numerals are missing (default to 1)
            words = re.findall(r'[a-zA-Z]+', s)
            for word in words:
                if word.lower() in ['day', 'days', 'd']: res += relativedelta(days=1)
                elif word.lower() in ['hour', 'hours', 'h']: res += relativedelta(hours=1)
                elif word.lower() in ['minute', 'minutes', 'min', 'mins', 'm']: res += relativedelta(minutes=1)
                elif word.lower() in ['second', 'seconds', 'sec', 'secs', 's']: res += relativedelta(seconds=1)
                elif word.lower() in ['month', 'months']: res += relativedelta(months=1)
                elif word.lower() in ['year', 'years']: res += relativedelta(years=1)
        else:
            for val, unit in matches:
                # Determine correct unit key
                u_low = unit.lower()
                # Special case for 'M' which could be month or minute
                if unit == 'M':
                    # In lubridate strings not starting with P, 'M' usually means minutes
                    # unless explicitly months. This is a simplification.
                    key = 'minutes'
                elif u_low in ['m', 'min', 'mins', 'minute', 'minutes']:
                    key = 'minutes'
                elif u_low in ['s', 'sec', 'secs', 'second', 'seconds']:
                    key = 'seconds'
                elif u_low in ['h', 'hour', 'hours']:
                    key = 'hours'
                elif u_low in ['d', 'day', 'days']:
                    key = 'days'
                elif u_low in ['w', 'week', 'weeks']:
                    key = 'weeks'
                elif u_low in ['month', 'months']:
                    key = 'months'
                elif u_low in ['year', 'years']:
                    key = 'years'
                else:
                    key = unit_map.get(unit, unit)
                res += relativedelta(**{key: int(val)})
        return res

    # Case: period(c(vals), c(units))
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)) and isinstance(args[1], (list, tuple, np.ndarray)):
        # lubridate combines these into one period
        res = relativedelta()
        for v, u in zip(args[0], args[1]):
            key = unit_map.get(u, u)
            res += relativedelta(**{key: v})
        return res

    # Case: period(-1, "days")
    if len(args) == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], str):
        key = unit_map.get(args[1], args[1])
        return relativedelta(**{key: args[0]})

    # Case: Named arguments
    if kwargs:
        res = relativedelta()
        for k, v in kwargs.items():
            key = unit_map.get(k, k)
            if isinstance(v, (list, tuple, np.ndarray)):
                # Handle vector named args by summing them
                for val in v:
                    res += relativedelta(**{key: val})
            else:
                res += relativedelta(**{key: v})
        # If positional args were also provided, add them (though R rarely does both)
        if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)):
             # This matches the weird example: period(c(1, -60), c("hour", "minute"), hour=c(1,2), minute=c(3,4))
             # We sum everything
             for v, u in zip(args[0], args[1]):
                 res += relativedelta(**{unit_map.get(u, u): v})
        return res

    return relativedelta()

def days(n): return relativedelta(days=n) if isinstance(n, int) else [relativedelta(days=i) for i in n]
def hours(n): return relativedelta(hours=n) if isinstance(n, int) else [relativedelta(hours=i) for i in n]
def minutes(n): return relativedelta(minutes=n) if isinstance(n, int) else [relativedelta(minutes=i) for i in n]
def months(n): return relativedelta(months=n) if isinstance(n, int) else [relativedelta(months=i) for i in n]
def years(n): return relativedelta(years=n) if isinstance(n, int) else [relativedelta(years=i) for i in n]
def ddays(n): return timedelta(days=n) # Duration is absolute seconds

def is_period(x):
    return isinstance(x, relativedelta)

# --- START TRANSLATION ---

# Separate period and units vectors
period([90, 5], ["second", "minute"])
period(-1, "days")
period([3, 1, 2, 13, 1], ["second", "minute", "hour", "day", "week"])
period([1, -60], ["hour", "minute"])
period(0, "second")

# Units as arguments
period(second=90, minute=5)
period(day=-1)
period(second=3, minute=1, hour=2, day=13, week=1)
period(hour=1, minute=-60)
period(second=0)
period([1, -60], ["hour", "minute"], hour=[1, 2], minute=[3, 4])

# Lubridate style parsing
period("2M 1sec")
period("2hours 2minutes 1second")
period("2d 2H 2M 2S")
period("2days 2hours 2mins 2secs")
period("2 days, 2 hours, 2 mins, 2 secs")
period("day day")

# ISO 8601 parsing
period("P10M23DT23H")
period("10DT10M")
period("P3Y6M4DT12H30M5S")
period("P23DT60H 20min 100 sec")

# Comparison with characters
# In R: period("day 2 sec") > "day 1sec"
# This compares the internal representation or the string. In R, periods can be compared.
# Python doesn't have a direct equivalent for this specific R string-comparison logic,
# but we will perform the comparison as strings as in the original translation's fallback.
print("day 2 sec" > "day 1sec")

# Elementary Constructors
x = pd.to_datetime("2009-08-03")
res_x1 = x + days(1) + hours(6) + minutes(30) # Simplified addition
# Since relativedelta and timedelta can't be added together directly in some versions, 
# we'll wrap them.
x + relativedelta(days=1, hours=6, minutes=30)
x + relativedelta(days=100, hours=-8)

# class(as.Date("2009-08-09") + days(1))
date_val = pd.to_datetime("2009-08-09").date()
res_date = date_val + timedelta(days=1)
print(type(res_date))

# as.Date("2009-08-09") + hours(12)
# In R, adding hours to a Date converts it to POSIXct
res_hours = pd.to_datetime("2009-08-09") + relativedelta(hours=12)
print(type(res_hours))

# years(1) - months(7)
# relativedelta objects support subtraction
relativedelta(years=1) - relativedelta(months=7)
# c(1:3) * hours(1)
[relativedelta(hours=i) for i in range(1, 4)]
# hours(1:3)
hours([1, 2, 3])

# sequencing
y = pd.to_datetime("2009-01-01")
# y + months(0:11)
[y + relativedelta(months=i) for i in range(12)]

# compare DST handling to durations
boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
boundary + relativedelta(days=1)
boundary + timedelta(days=1)

# is.period
is_period(pd.to_datetime("2009-08-03").date())
is_period(period(months=1, days=15))