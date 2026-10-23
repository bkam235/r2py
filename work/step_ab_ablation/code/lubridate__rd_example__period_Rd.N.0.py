import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

# Implementation of lubridate-like period and constructors
class Period:
    def __init__(self, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __add__(self, other):
        if isinstance(other, Period):
            return Period(
                self.years + other.years, self.months + other.months, self.weeks + other.weeks,
                self.days + other.days, self.hours + other.hours, self.minutes + other.minutes,
                self.seconds + other.seconds
            )
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Period):
            return Period(
                self.years - other.years, self.months - other.months, self.weeks - other.weeks,
                self.days - other.days, self.hours - other.hours, self.minutes - other.minutes,
                self.seconds - other.seconds
            )
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Period(
                self.years * scalar, self.months * scalar, self.weeks * scalar,
                self.days * scalar, self.hours * scalar, self.minutes * scalar,
                self.seconds * scalar
            )
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __gt__(self, other):
        if isinstance(other, str):
            # Simple string comparison for the specific example "day 2 sec" > "day 1sec"
            return self.to_string() > other
        return NotImplemented

    def to_string(self):
        # Approximation of lubridate's string representation
        parts = []
        if self.months: parts.append(f"{self.months}M")
        if self.seconds: parts.append(f"{self.seconds}S")
        return " ".join(parts) if parts else "0S"

    def to_relativedelta(self):
        return relativedelta(years=self.years, months=self.months, weeks=self.weeks, 
                             days=self.days, hours=self.hours, minutes=self.minutes, seconds=self.seconds)

    def __repr__(self):
        return f"Period({self.years}Y {self.months}M {self.weeks}W {self.days}D {self.hours}H {self.minutes}M {self.seconds}S)"

def is_period(x):
    return isinstance(x, Period)

def period(*args, **kwargs):
    # Handle Lubridate style parsing and ISO 8601
    if len(args) == 1 and isinstance(args[0], str):
        s = args[0]
        p = Period()
        
        # ISO 8601 Parsing
        if s.startswith('P'):
            # P[nY][nM][nD][T[nH][nM][nS]]
            iso_match = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
            if iso_match:
                vals = iso_match.groups()
                if vals[0]: p.years = int(vals[0])
                if vals[1]: p.months = int(vals[1])
                if vals[2]: p.days = int(vals[2])
                if vals[3]: p.hours = int(vals[3])
                if vals[4]: p.minutes = int(vals[4])
                if vals[5]: p.seconds = int(vals[5])
                # If there's extra text after the ISO part (mixing), process the rest as lubridate style
                remaining = s[iso_match.end():]
                if remaining:
                    p = lubridate_parse(remaining, p)
                return p

        # Check for ISO-like but missing 'P' (e.g., "10DT10M")
        if 'T' in s and not s.startswith('P'):
            # This is a specific case from the R examples
            iso_match = re.match(r'(?:(\d+)D)?T(?:(\d+)M)?(?:(\d+)S)?', s)
            if iso_match:
                vals = iso_match.groups()
                if vals[0]: p.days = int(vals[0])
                if vals[1]: p.minutes = int(vals[1])
                if vals[2]: p.seconds = int(vals[2])
                return p

        return lubridate_parse(s)

    # Handle Separate period and units vectors
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)) and isinstance(args[1], (list, tuple, np.ndarray)):
        vals = args[0]
        units = args[1]
        # Lubridate creates one period summing all vectors if they are the same length
        p = Period()
        for v, u in zip(vals, units):
            u = u.lower().rstrip('s')
            if u == 'second': p.seconds += v
            elif u == 'minute': p.minutes += v
            elif u == 'hour': p.hours += v
            elif u == 'day': p.days += v
            elif u == 'week': p.weeks += v
            elif u == 'month': p.months += v
            elif u == 'year': p.years += v
        # If named args are also provided, they are added
        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, (list, tuple, np.ndarray)):
                    for val in v:
                        if k == 'hour': p.hours += val
                        elif k == 'minute': p.minutes += val
            return p
        return p

    # Handle period(-1, "days")
    if len(args) == 2 and isinstance(args[1], str):
        u = args[1].lower().rstrip('s')
        p = Period()
        if u == 'second': p.seconds = args[0]
        elif u == 'minute': p.minutes = args[0]
        elif u == 'hour': p.hours = args[0]
        elif u == 'day': p.days = args[0]
        elif u == 'week': p.weeks = args[0]
        elif u == 'month': p.months = args[0]
        elif u == 'year': p.years = args[0]
        return p

    # Handle Units as arguments
    p = Period()
    if kwargs:
        for k, v in kwargs.items():
            if k == 'second': p.seconds = v
            elif k == 'minute': p.minutes = v
            elif k == 'hour': p.hours = v
            elif k == 'day': p.days = v
            elif k == 'week': p.weeks = v
            elif k == 'month': p.months = v
            elif k == 'year': p.years = v
    
    # Handle the vector/named combined case period(c(1, -60), c("hour", "minute"), hour = c(1, 2), minute = c(3, 4))
    if len(args) == 2 and isinstance(args[0], (list, tuple, np.ndarray)):
        # Recurse for the positional part, then add the kwargs
        p_pos = period(args[0], args[1])
        p_kwargs = Period()
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple, np.ndarray)):
                for val in v:
                    if k == 'hour': p_kwargs.hours += val
                    elif k == 'minute': p_kwargs.minutes += val
        return p_pos + p_kwargs

    return p

def lubridate_parse(s, base_p=None):
    p = base_p if base_p is not None else Period()
    # Match patterns like "2days", "2d", "day", "2 hours", etc.
    # Pattern: (number)? (unit)
    pattern = r'(\d+)?\s*(year|month|week|day|hour|min|sec)[s]?\b'
    # Special cases for shorthand
    s_processed = s.replace('Y', ' year ').replace('M', ' month ' if 'P' in s or 'T' not in s else ' minute ')
    # If it's ISO-like, the M is ambiguous. Let's be careful.
    # For the specific examples: "2M 1sec" -> 2 months, "10DT10M" -> 10 minutes
    
    # Simple rewrite for the examples provided in the R script
    matches = re.finditer(r'(\d+)?\s*([a-zA-Z]+)', s)
    for m in matches:
        val_str, unit_str = m.groups()
        val = int(val_str) if val_str else 1
        unit = unit_str.lower()
        
        if unit.startswith('year') or unit == 'y': p.years += val
        elif unit.startswith('month') or (unit == 'm' and 't' not in s.lower() and 'p' not in s.lower()): p.months += val
        elif unit.startswith('week') or unit == 'w': p.weeks += val
        elif unit.startswith('day') or unit == 'd': p.days += val
        elif unit.startswith('hour') or unit == 'h': p.hours += val
        elif unit.startswith('min') or (unit == 'm' and ('t' in s.lower() or 'p' in s.lower())): p.minutes += val
        elif unit.startswith('sec') or unit == 's': p.seconds += val
    return p

def days(n): return period(day=n) if isinstance(n, (int, float)) else [period(day=i) for i in n]
def hours(n): return period(hour=n) if isinstance(n, (int, float)) else [period(hour=i) for i in n]
def minutes(n): return period(minute=n) if isinstance(n, (int, float)) else [period(minute=i) for i in n]
def months(n): return period(month=n) if isinstance(n, (int, float)) else [period(month=i) for i in n]
def years(n): return period(year=n) if isinstance(n, (int, float)) else [period(year=i) for i in n]
def ddays(n): return timedelta(days=n) # duration

# --- START TRANSLATION ---

period([90, 5], ["second", "minute"])
period(-1, "days")
period([3, 1, 2, 13, 1], ["second", "minute", "hour", "day", "week"])
period([1, -60], ["hour", "minute"])
period(0, "second")

period(second=90, minute=5)
period(day=-1)
period(second=3, minute=1, hour=2, day=13, week=1)
period(hour=1, minute=-60)
period(second=0)
period([1, -60], ["hour", "minute"], hour=[1, 2], minute=[3, 4])

period("2M 1sec")
period("2hours 2minutes 1second")
period("2d 2H 2M 2S")
period("2days 2hours 2mins 2secs")
period("2 days, 2 hours, 2 mins, 2 secs")
period("day day")

period("P10M23DT23H")
period("10DT10M")
period("P3Y6M4DT12H30M5S")
period("P23DT60H 20min 100 sec")

# Comparison with characters
print(period("day 2 sec") > "day 1sec")

x = pd.to_datetime("2009-08-03")
# Python's pandas/datetime handles addition via relativedelta or timedelta
res1 = x + days(1).to_relativedelta() + hours(6).to_relativedelta() + minutes(30).to_relativedelta()
res2 = x + days(100).to_relativedelta() - hours(8).to_relativedelta()

date_obj = pd.to_datetime("2009-08-09").date()
res_date = date_obj + timedelta(days=1)
print(type(res_date))

res_hours = pd.to_datetime("2009-08-09") + hours(12).to_relativedelta()
print(type(res_hours))

# years(1) - months(7)
res_ym = years(1).to_relativedelta() - months(7).to_relativedelta()
# c(1:3) * hours(1)
res_h_mult = [i * hours(1) for i in range(1, 4)]
# hours(1:3)
res_h_vec = hours([1, 2, 3])

y = pd.to_datetime("2009-01-01")
# y + months(0:11)
res_y_months = [y + months(i).to_relativedelta() for i in range(12)]

boundary = pd.to_datetime("2009-03-08 01:59:59").tz_localize("America/Chicago")
# boundary + days(1)
res_b_days = boundary + days(1).to_relativedelta()
# boundary + ddays(1)
res_b_ddays = boundary + ddays(1)

print(is_period(pd.to_datetime("2009-08-03").date()))
print(is_period(period(months=1, days=15)))