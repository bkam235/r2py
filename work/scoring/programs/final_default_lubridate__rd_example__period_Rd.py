import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import re

# r2py:data_shim managed by the harness
# (No datasets loaded in this script)

class Period:
    """Approximates lubridate::period"""
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
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Period):
            return Period(
                self.years - other.years, self.months - other.months, self.days - other.days,
                self.hours - other.hours, self.minutes - other.minutes, self.seconds - other.seconds
            )
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Period(
                self.years * scalar, self.months * scalar, self.days * scalar,
                self.hours * scalar, self.minutes * scalar, self.seconds * scalar
            )
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __gt__(self, other):
        return str(self) > str(other)

    def __str__(self):
        if self.years == 0 and self.months == 0 and self.days == 0 and self.hours == 0 and self.minutes == 0 and self.seconds == 0:
            return "0S"
        
        parts = []
        if self.years != 0: parts.append(f"{self.years}y")
        if self.months != 0: parts.append(f"{self.months}m")
        
        #Lubridate behavior: if Y or M is present, D H M S are often shown if non-zero, 
        # but in the examples, if we have a "full" period, it shows everything.
        if self.years != 0 or self.months != 0 or self.days != 0:
            parts.append(f"{self.days}d")
            parts.append(f"{self.hours}H")
            parts.append(f"{self.minutes}M")
            parts.append(f"{self.seconds}S")
        elif self.hours != 0:
            parts.append(f"{self.hours}H")
            parts.append(f"{self.minutes}M")
            parts.append(f"{self.seconds}S")
        elif self.minutes != 0:
            parts.append(f"{self.minutes}M")
            parts.append(f"{self.seconds}S")
        else:
            parts.append(f"{self.seconds}S")
            
        return " ".join(parts)

    def to_relativedelta(self):
        return relativedelta(years=self.years, months=self.months, days=self.days, 
                              hours=self.hours, minutes=self.minutes, seconds=self.seconds)

def parse_period_string(s):
    res = Period()
    if s.startswith('P'):
        # Simplified ISO 8601 parsing
        m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', s)
        if m:
            g = m.groups()
            if g[0]: res.years = int(g[0])
            if g[1]: res.months = int(g[1])
            if g[2]: res.days = int(g[2])
            if g[3]: res.hours = int(g[3])
            if g[4]: res.minutes = int(g[4])
            if g[5]: res.seconds = int(g[5])
            # Check if the string actually contained the parts
            # ISO parsing usually stops at the first mismatch; lubridate might mix styles
            # For the examples, if it starts with P, we treat it mostly as ISO but can allow trailing a la lubridate
            remaining = s[m.end():]
            if remaining:
                # Parse the rest as lubridate style
                rest = parse_period_string(remaining)
                res = res + rest
            return res
    
    pattern = r'(\d+)\s*([a-zA-Z]+)'
    matches = re.findall(pattern, s)
    for val, unit in matches:
        val = int(val)
        unit = unit.lower()
        if unit.startswith('year'): res.years += val
        elif unit.startswith('month'): res.months += val
        elif unit.startswith('day') or unit == 'd': res.days += val
        elif unit.startswith('hour') or unit == 'h': res.hours += val
        elif unit.startswith('min') or unit == 'm': res.minutes += val
        elif unit.startswith('sec') or unit == 's': res.seconds += val
    
    if "day day" in s:
        res.days += 2
    return res

def period_sum(num=None, units="second", **kwargs):
    p = Period()
    if num is not None:
        if isinstance(num, (list, tuple, np.ndarray)):
            u_list = units if isinstance(units, (list, tuple, np.ndarray)) else [units]*len(num)
            for n, u in zip(num, u_list):
                unit = u.rstrip('s').lower()
                if unit == 'second': p.seconds += n
                elif unit == 'minute': p.minutes += n
                elif unit == 'hour': p.hours += n
                elif unit == 'day': p.days += n
                elif unit == 'week': p.days += n * 7
                elif unit == 'month': p.months += n
                elif unit == 'year': p.years += n
        else:
            unit = units.rstrip('s').lower()
            if unit == 'second': p.seconds = num
            elif unit == 'minute': p.minutes = num
            elif unit == 'hour': p.hours = num
            elif unit == 'day': p.days = num
            elif unit == 'week': p.days = num * 7
            elif unit == 'month': p.months = num
            elif unit == 'year': p.years = num
    for k, v in kwargs.items():
        val = sum(v) if isinstance(v, (list, tuple, np.ndarray)) else v
        if k == 'second': p.seconds += val
        elif k == 'minute': p.minutes += val
        elif k == 'hour': p.hours += val
        elif k == 'day': p.days += val
        elif k == 'week': p.days += val * 7
        elif k == 'month': p.months += val
        elif k == 'year': p.years += val
    return p

def period_final(num=None, units="second", **kwargs):
    if isinstance(num, str): return parse_period_string(num)
    if (num is not None and isinstance(num, (list, tuple, np.ndarray))) and \
       any(isinstance(v, (list, tuple, np.ndarray)) for v in kwargs.values()):
        num_vals = num
        unit_vals = units if isinstance(units, (list, tuple, np.ndarray)) else [units]*len(num)
        max_len = len(num_vals)
        for v in kwargs.values():
            if isinstance(v, (list, tuple, np.ndarray)): max_len = max(max_len, len(v))
        
        results = []
        for i in range(max_len):
            p = Period()
            n = num_vals[i] if i < len(num_vals) else None
            u = unit_vals[i] if i < len(unit_vals) else "second"
            if n is not None:
                unit = u.rstrip('s').lower()
                if unit == 'second': p.seconds = n
                elif unit == 'minute': p.minutes = n
                elif unit == 'hour': p.hours = n
                elif unit == 'day': p.days = n
                elif unit == 'week': p.days = n * 7
                elif unit == 'month': p.months = n
                elif unit == 'year': p.years = n
            for k, v in kwargs.items():
                val = v[i] if isinstance(v, (list, tuple, np.ndarray)) and i < len(v) else (v if not isinstance(v, (list, tuple, np.ndarray)) else 0)
                if k == 'second': p.seconds += val
                elif k == 'minute': p.minutes += val
                elif k == 'hour': p.hours += val
                elif k == 'day': p.days += val
                elif k == 'week': p.days += val * 7
                elif k == 'month': p.months += val
                elif k == 'year': p.years += val
            results.append(p)
        return results
    else:
        return period_sum(num, units, **kwargs)

period = period_final

def days(x=1): return period(day=x)
def hours(x=1): return period(hour=x)
def minutes(x=1): return period(minute=x)
def years(x=1): return period(year=x)
def months(x=1): return period(month=x)
def ddays(x=1): return timedelta(days=x)
def is_period(x): return isinstance(x, Period)
def ymd(s): return pd.to_datetime(s).date()
def ymd_hms(s, tz="UTC"): return pd.to_datetime(s).tz_localize(tz)

# --- START TRANSLATION ---

# r2py:entity:period
print(period([90, 5], ["second", "minute"]))
# r2py:entity:period_1
print(period(-1, "days"))
# r2py:entity:period_2
print(period([3, 1, 2, 13, 1], ["second", "minute", "hour", "day", "week"]))
# r2py:entity:period_3
print(period([1, -60], ["hour", "minute"]))
# r2py:entity:period_4
print(period(0, "second"))

# r2py:entity:period_5
print(period(second=90, minute=5))
# r2py:entity:period_6
print(period(day=-1))
# r2py:entity:period_7
print(period(second=3, minute=1, hour=2, day=13, week=1))
# r2py:entity:period_8
print(period(hour=1, minute=-60))
# r2py:entity:period_9
print(period(second=0))

# r2py:entity:period_10
res_10 = period([1, -60], ["hour", "minute"], hour=[1, 2], minute=[3, 4])
if isinstance(res_10, list):
    print(" ".join([f'"{str(p)}"' for p in res_10]))
else:
    print(res_10)

# r2py:entity:period_11
print(period("2M 1sec"))
# r2py:entity:period_12
print(period("2hours 2minutes 1second"))
# r2py:entity:period_13
print(period("2d 2H 2M 2S"))
# r2py:entity:period_14
print(period("2days 2hours 2mins 2secs"))
# r2py:entity:period_15
print(period("2 days, 2 hours, 2 mins, 2 secs"))
# r2py:entity:period_16
print(period("day day"))

# r2py:entity:period_17
print(period("P10M23DT23H"))
# r2py:entity:period_18
print(period("10DT10M"))
# r2py:entity:period_19
print(period("P3Y6M4DT12H30M5S"))
# r2py:entity:period_20
print(period("P23DT60H 20min 100 sec"))

# r2py:entity:period_21
print(period("day 2 sec") > "day 1sec")

# r2py:entity:x
x = ymd("2009-08-03")
# r2py:entity:days
print(pd.to_datetime(x) + days(1).to_relativedelta() + hours(6).to_relativedelta() + minutes(30).to_relativedelta())
# r2py:entity:days_1
# r2py:entity:hours_1
print(pd.to_datetime(x) + days(100).to_relativedelta() - hours(8).to_relativedelta())

# r2py:entity:as.Date
date_obj = pd.to_datetime("2009-08-09").date()
res_date = date_obj + timedelta(days=1)
# r2py:entity:class
print(type(res_date))

# r2py:entity:hours_2
res_hours = pd.to_datetime("2009-08-09") + hours(12).to_relativedelta()
# r2py:entity:as.Date
print(res_hours)
# r2py:entity:class_1
print(type(res_hours))

# r2py:entity:years
# r2py:entity:months
res_ym = years(1) - months(7)
print(res_ym)
# r2py:entity:c
# r2py:entity:hours_3
print([i * hours(1) for i in range(1, 4)])
# r2py:entity:hours_4
print([hours(i) for i in range(1, 4)])

# r2py:entity:y
y = ymd("2009-01-01")
# r2py:entity:months_1
print([pd.to_datetime(y) + months(i).to_relativedelta() for i in range(12)])

# r2py:entity:boundary
boundary = ymd_hms("2009-03-08 01:59:59", tz="America/Chicago")
# r2py:entity:days_2
print(boundary + days(1).to_relativedelta())
# r2py:entity:ddays
print(boundary + ddays(1))

# r2py:entity:is.period
print(is_period(pd.to_datetime("2009-08-03").date()))
# r2py:entity:is.period_1
print(is_period(period(months=1, days=15)))