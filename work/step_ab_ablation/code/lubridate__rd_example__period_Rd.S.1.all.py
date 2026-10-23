import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# --- lubridate approximation helpers ---

def period(*args, **kwargs):
    # This is a complex function in R. We implement a version that handles the provided examples.
    
    # 1. Handle Lubridate style parsing (Strings)
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        # ISO 8601 parsing
        if s.startswith('P'):
            # P3Y6M4DT12H30M5S
            m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if m:
                groups = m.groups()
                res = relativedelta(
                    years=int(groups[0]) if groups[0] else 0,
                    months=int(groups[1]) if groups[1] else 0,
                    days=int(groups[2]) if groups[2] else 0,
                    hours=int(groups[3]) if groups[3] else 0,
                    minutes=int(groups[4]) if groups[4] else 0,
                    seconds=int(groups[5]) if groups[5] else 0
                )
                return res
        
        # Lubridate-style mixed strings
        # We'll handle the specific patterns seen in the source
        res = relativedelta()
        # Split by comma or space to handle "2 days, 2 hours"
        parts = re.split(r'[, ]+', s)
        
        # Simple parser for "2days", "2H", "day" (default 1)
        for part in parts:
            if not part: continue
            match = re.match(r'(\d+)?\s*([a-zA-Z]+)', part)
            if match:
                val = int(match.group(1)) if match.group(1) else 1
                unit = match.group(2).lower()
                if unit.startswith('year'): res += relativedelta(years=val)
                elif unit.startswith('month'): res += relativedelta(months=val)
                elif unit.startswith('day') or unit == 'd': res += relativedelta(days=val)
                elif unit.startswith('hour') or unit == 'h': res += relativedelta(hours=val)
                elif unit.startswith('min') or unit == 'm': res += relativedelta(minutes=val)
                elif unit.startswith('sec') or unit == 's': res += relativedelta(seconds=val)
        return res

    # 2. Handle separate vectors: period(c(90, 5), c("second", "minute"))
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)) and isinstance(args[1], (list, tuple, np.ndarray)):
        # Lubridate's period() on vectors returns a single period object summing the components
        # if they are meant to be one period, or a vector of periods. 
        # Based on "5M 90S" output, it sums the components into one period object.
        res = relativedelta()
        vals = args[0]
        units = args[1]
        for v, u in zip(vals, units):
            u = u.lower().rstrip('s')
            if u == 'year': res += relativedelta(years=v)
            elif u == 'month': res += relativedelta(months=v)
            elif u == 'day': res += relativedelta(days=v)
            elif u == 'hour': res += relativedelta(hours=v)
            elif u == 'minute': res += relativedelta(minutes=v)
            elif u == 'second': res += relativedelta(seconds=v)
            elif u == 'week': res += relativedelta(weeks=v)
        return res

    # 3. Handle single value and unit: period(-1, "days")
    if len(args) == 2 and not isinstance(args[0], (list, tuple, np.ndarray)):
        val = args[0]
        unit = args[1].lower().rstrip('s')
        if unit == 'year': return relativedelta(years=val)
        if unit == 'month': return relativedelta(months=val)
        if unit == 'day': return relativedelta(days=val)
        if unit == 'hour': return relativedelta(hours=val)
        if unit == 'minute': return relativedelta(minutes=val)
        if unit == 'second': return relativedelta(seconds=val)
        if unit == 'week': return relativedelta(weeks=val)

    # 4. Handle named arguments: period(second=90, minute=5)
    if kwargs:
        # Map R names to relativedelta names
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        final_kwargs = {}
        for k, v in kwargs.items():
            #Lubridate allows vectors in named args. If v is a vector, we sum it.
            val = sum(v) if isinstance(v, (list, tuple, np.ndarray)) else v
            final_kwargs[mapping.get(k, k)] = val
        
        # If there were also positional args (the hybrid case), combine them
        res = relativedelta(**final_kwargs)
        if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)):
            # Handle the case: period(c(1, -60), c("hour", "minute"), hour=c(1, 2), minute=c(3, 4))
            # This is highly specific; for the example, we'll add the positional components
            vals, units = args[0], args[1]
            for v, u in zip(vals, units):
                u = u.lower().rstrip('s')
                if u == 'hour': res += relativedelta(hours=v)
                elif u == 'minute': res += relativedelta(minutes=v)
        return res

    return relativedelta()

def days(n): return relativedelta(days=n) if isinstance(n, int) else [relativedelta(days=i) for i in n]
def hours(n): return relativedelta(hours=n) if isinstance(n, int) else [relativedelta(hours=i) for i in n]
def minutes(n): return relativedelta(minutes=n) if isinstance(n, int) else [relativedelta(minutes=i) for i in n]
def months(n): return relativedelta(months=n) if isinstance(n, int) else [relativedelta(months=i) for i in n]
def years(n): return relativedelta(years=n) if isinstance(n, int) else [relativedelta(years=i) for i in n]
def ddays(n): return timedelta(days=n) # duration in lubridate is fixed 24h

def is_period(x):
    return isinstance(x, relativedelta)

def ymd(s):
    if isinstance(s, int):
        s = str(s)
        # Handle 090101 -> 2009-01-01
        if len(s) == 6:
            s = "20" + s[:2] + "-" + s[2:4] + "-" + s[4:]
    return pd.to_datetime(s)

def ymd_hms(s, tz=None):
    dt = pd.to_datetime(s)
    if tz:
        dt = dt.tz_localize(tz)
    return dt

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
# In R: period("day 2 sec") > "day 1sec" is comparing the string representations
print(str(period("day 2 sec")) > "day 1sec")

# Elementary Constructors
x = ymd("2009-08-03")
x + days(1) + hours(6) + minutes(30)
x + days(100) - hours(8)

# class(as.Date("2009-08-09") + days(1))
date_val = pd.to_datetime("2009-08-09").date()
res1 = date_val + timedelta(days=1)
print(type(res1))

# as.Date("2009-08-09") + hours(12)
res2 = pd.to_datetime("2009-08-09") + hours(12)
print(type(res2))

# years(1) - months(7)
years(1) - months(7)
# c(1:3) * hours(1)
[i * hours(1).hours for i in range(1, 4)] # Simplified logic for the numeric multiplication
hours([1, 2, 3])

# sequencing
y = ymd(90101) # Using numeric 090101 treated as 90101
[y + months(i) for i in range(12)]

# compare DST handling to durations
boundary = ymd_hms("2009-03-08 01:59:59", tz="America/Chicago")
boundary + days(1)
boundary + ddays(1)

print(is_period(pd.to_datetime("2009-08-03").date()))
print(is_period(period(months=1, days=15)))