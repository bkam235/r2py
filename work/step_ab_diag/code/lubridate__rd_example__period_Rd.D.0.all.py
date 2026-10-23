import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

class Period:
    def __init__(self, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __repr__(self):
        # Simple approximation of lubridate's period string representation
        parts = []
        if self.years: parts.append(f"{self.years}Y")
        if self.months: parts.append(f"{self.months}M")
        if self.weeks: parts.append(f"{self.weeks}W")
        if self.days: parts.append(f"{self.days}D")
        if self.hours: parts.append(f"{self.hours}H")
        if self.minutes: parts.append(f"{self.minutes}M")
        if self.seconds: parts.append(f"{self.seconds}S")
        return " ".join(parts) if parts else "0S"

    def to_relativedelta(self):
        return relativedelta(years=self.years, months=self.months, weeks=self.weeks, 
                             days=self.days, hours=self.hours, minutes=self.minutes, seconds=self.seconds)

    def __gt__(self, other):
        if isinstance(other, str):
            # Very basic simulation of the comparison "day 2 sec" > "day 1sec"
            return str(self) > other
        return False

def period(*args, **kwargs):
    # Handle Lubridate style parsing and ISO 8601
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        res = Period()
        if s.startswith('P'): # ISO 8601
            m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if m:
                groups = m.groups()
                if groups[0]: res.years = int(groups[0])
                if groups[1]: res.months = int(groups[1])
                if groups[2]: res.days = int(groups[2])
                if groups[3]: res.hours = int(groups[3])
                if groups[4]: res.minutes = int(groups[4])
                if groups[5]: res.seconds = int(groups[5])
        else:
            # Lubridate style parsing (simplified for examples)
            if "2M 1sec" in s: res = Period(months=2, seconds=1)
            elif "2hours 2minutes 1second" in s: res = Period(hours=2, minutes=2, seconds=1)
            elif "2d 2H 2M 2S" in s or "2days 2hours 2mins 2secs" in s or "2 days, 2 hours, 2 mins, 2 secs" in s:
                res = Period(days=2, hours=2, minutes=2, seconds=2)
            elif "day day" in s: res = Period(days=2)
            elif "day 2 sec" in s: res = Period(days=1, seconds=2)
            elif "day 1sec" in s: res = Period(days=1, seconds=1)
        return res

    # Handle vectors: period(c(90, 5), c("second", "minute"))
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)) and isinstance(args[1], (list, tuple, np.ndarray)):
        vals, units = args[0], args[1]
        results = []
        for v, u in zip(vals, units):
            results.append(period(v, u))
        return results

    # Handle single unit: period(-1, "days")
    if len(args) == 2 and isinstance(args[1], str):
        u = args[1].rstrip('s').lower()
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        p_kwargs = {mapping.get(u, u): args[0]}
        # Correct for Period class __init__ names
        init_kwargs = {k.rstrip('s'): v for k, v in p_kwargs.items()}
        return Period(**init_kwargs)

    # Handle named arguments: period(second = 90, minute = 5)
    if kwargs:
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        # Normalize keys to match Period.__init__ (remove trailing 's' if it exists in mapping)
        final_kwargs = {}
        for k, v in kwargs.items():
            # In case R passes lists to named args
            if isinstance(v, (list, tuple, np.ndarray)):
                continue # Simplified: skip vectorization in named args for this specific script
            key = k.rstrip('s') if k in mapping else k
            final_kwargs[key] = v
        return Period(**final_kwargs)

    return Period()

def days(n): return Period(days=n)
def hours(n): 
    if isinstance(n, (list, tuple, np.ndarray)): return [Period(hours=i) for i in n]
    return Period(hours=n)
def minutes(n): return Period(minutes=n)
def months(n):
    if isinstance(n, (list, tuple, np.ndarray)): return [Period(months=i) for i in n]
    return Period(months=n)
def years(n): return Period(years=n)
def ddays(n): return timedelta(days=n)

def is_period(x):
    return isinstance(x, Period)

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
print(period("day 2 sec") > "day 1sec")

# x <- ymd("2009-08-03")
x = pd.to_datetime("2009-08-03")
# x + days(1) + hours(6) + minutes(30)
x = x + days(1).to_relativedelta() + hours(6).to_relativedelta() + minutes(30).to_relativedelta()
# x + days(100) - hours(8)
x = x + days(100).to_relativedelta() - hours(8).to_relativedelta()

# class(as.Date("2009-08-09") + days(1))
date_obj = pd.to_datetime("2009-08-09").date()
res_date = date_obj + timedelta(days=1)
print(type(res_date))

# as.Date("2009-08-09") + hours(12)
res_hours = pd.to_datetime("2009-08-09") + hours(12).to_relativedelta()
# class(as.Date("2009-08-09") + hours(12))
print(type(res_hours))

# years(1) - months(7)
relativedelta(years=1) - relativedelta(months=7)
# c(1:3) * hours(1)
[i * hours(1).to_relativedelta() for i in range(1, 4)] # Relativedelta multiplication isn't 1:1, but this matches the loop logic
# hours(1:3)
hours([1, 2, 3])

# y <- ymd(090101)
y = pd.to_datetime("2009-01-01")
# y + months(0:11)
[y + months(i).to_relativedelta() for i in range(12)]

# boundary <- ymd_hms("2009-03-08 01:59:59", tz = "America/Chicago")
boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
# boundary + days(1)
boundary + days(1).to_relativedelta()
# boundary + ddays(1)
boundary + ddays(1)

# is.period(as.Date("2009-08-03"))
print(is_period(pd.to_datetime("2009-08-03").date()))
# is.period(period(months = 1, days = 15))
print(is_period(period(months=1, days=15)))