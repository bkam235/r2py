import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# Mocking lubridate's period class for consistent representation and comparison
class Period:
    def __init__(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __add__(self, other):
        if isinstance(other, Period):
            return Period(
                self.years + other.years, self.months + other.months, self.days + other.days,
                self.hours + other.hours, self.minutes + other.minutes, self.seconds + other.seconds
            )
        return self

    def __sub__(self, other):
        if isinstance(other, Period):
            return Period(
                self.years - other.years, self.months - other.months, self.days - other.days,
                self.hours - other.hours, self.minutes - other.minutes, self.seconds - other.seconds
            )
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Period(
                self.years * other, self.months * other, self.days * other,
                self.hours * other, self.minutes * other, self.seconds * other
            )
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __gt__(self, other):
        # Lubridate period comparison with characters is alphabetical if not handled
        # but typically compares the string representation
        return str(self) > str(other)

    def __str__(self):
        # This is a simplified representation
        parts = []
        if self.years: parts.append(f"{self.years}Y")
        if self.months: parts.append(f"{self.months}M")
        if self.days: parts.append(f"{self.days}D")
        if self.hours: parts.append(f"{self.hours}H")
        if self.minutes: parts.append(f"{self.minutes}M")
        if self.seconds: parts.append(f"{self.seconds}S")
        return " ".join(parts) if parts else "0S"

    def to_relativedelta(self):
        return relativedelta(years=self.years, months=self.months, days=self.days, 
                             hours=self.hours, minutes=self.minutes, seconds=self.seconds)

def period(*args, **kwargs):
    # Handling named arguments: period(second=90, minute=5)
    # Handle vector named arguments like hour=c(1, 2)
    if kwargs:
        mapping = {'second': 'seconds', 'minute': 'minutes', 'hour': 'hours', 
                   'day': 'days', 'week': 'weeks', 'month': 'months', 'year': 'years'}
        
        # If any kwarg is a list/array, lubridate returns a vector of periods
        if any(isinstance(v, (list, tuple, np.ndarray)) for v in kwargs.values()):
            # Simplified: we just return a list of Periods
            return [Period()] 
        
        p = Period()
        for k, v in kwargs.items():
            attr = mapping.get(k, k)
            # Map 'week' to days since Period class uses days
            if k == 'week': p.days += v * 7
            elif hasattr(p, attr.rstrip('s')):
                setattr(p, attr.rstrip('s'), v)
        return p

    # Handling positional arguments
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        p = Period()
        # ISO 8601 Parsing
        if s.startswith('P'):
            # Simplified ISO regex
            m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if m:
                groups = m.groups()
                if groups[0]: p.years = int(groups[0])
                if groups[1]: p.months = int(groups[1])
                if groups[2]: p.days = int(groups[2])
                if groups[3]: p.hours = int(groups[3])
                if groups[4]: p.minutes = int(groups[4])
                if groups[5]: p.seconds = int(groups[5])
        else:
            # Lubridate style: "2M 1sec"
            # Extract numbers and units
            matches = re.findall(r'(\d+)\s*([a-zA-Z]+)', s)
            for val, unit in matches:
                val = int(val)
                u = unit.lower()
                if u.startswith('year'): p.years += val
                elif u.startswith('month'): p.months += val
                elif u.startswith('day'): p.days += val
                elif u.startswith('hour'): p.hours += val
                elif u.startswith('min'): p.minutes += val
                elif u.startswith('sec'): p.seconds += val
            # Special case: "day day"
            if not matches and "day" in s:
                p.days = s.count("day")
        return p

    if len(args) == 2:
        vals = args[0]
        units = args[1]
        if isinstance(vals, (list, tuple, np.ndarray)):
            # Lubridate combines these into one period if they are vectors of the same length
            p = Period()
            for v, u in zip(vals, units):
                u = u.lower().rstrip('s')
                if u == 'year': p.years += v
                elif u == 'month': p.months += v
                elif u == 'day': p.days += v
                elif u == 'hour': p.hours += v
                elif u == 'minute': p.minutes += v
                elif u == 'second': p.seconds += v
            return p
        else:
            # Single value, single unit
            u = units.lower().rstrip('s')
            p = Period()
            if u == 'year': p.years = vals
            elif u == 'month': p.months = vals
            elif u == 'day': p.days = vals
            elif u == 'hour': p.hours = vals
            elif u == 'minute': p.minutes = vals
            elif u == 'second': p.seconds = vals
            return p

    return Period()

def days(n): return Period(days=n) if np.isscalar(n) else [Period(days=i) for i in n]
def hours(n): return Period(hours=n) if np.isscalar(n) else [Period(hours=i) for i in n]
def minutes(n): return Period(minutes=n) if np.isscalar(n) else [Period(minutes=i) for i in n]
def months(n): return Period(months=n) if np.isscalar(n) else [Period(months=i) for i in n]
def years(n): return Period(years=n) if np.isscalar(n) else [Period(years=i) for i in n]
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
p_sum = days(1) + hours(6) + minutes(30)
res_x1 = x + p_sum.to_relativedelta()
# x + days(100) - hours(8)
p_diff = days(100) - hours(8)
res_x2 = x + p_diff.to_relativedelta()

# class(as.Date("2009-08-09") + days(1))
date_obj = pd.to_datetime("2009-08-09").date()
res_date = date_obj + timedelta(days=1)
print(type(res_date))

# as.Date("2009-08-09") + hours(12)
res_hours = pd.to_datetime("2009-08-09") + hours(12).to_relativedelta()
# class(as.Date("2009-08-09") + hours(12))
print(type(res_hours))

# years(1) - months(7)
res_ym = years(1) - months(7)
# c(1:3) * hours(1)
res_h_mult = [i * hours(1) for i in range(1, 4)]
# hours(1:3)
res_h_vec = hours([1, 2, 3])

# y <- ymd(090101)
y = pd.to_datetime("2009-01-01")
# y + months(0:11)
res_y_seq = [y + months(i).to_relativedelta() for i in range(12)]

# boundary <- ymd_hms("2009-03-08 01:59:59", tz = "America/Chicago")
boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
# boundary + days(1)
res_b1 = boundary + days(1).to_relativedelta()
# boundary + ddays(1)
res_b2 = boundary + ddays(1)

# is.period(as.Date("2009-08-03"))
print(is_period(pd.to_datetime("2009-08-03").date()))
# is.period(period(months = 1, days = 15))
print(is_period(period(months=1, days=15)))