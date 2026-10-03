# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 63

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def ymd_hms(date_str):
    return pd.to_datetime(date_str)

def ymd(date_str):
    return pd.to_datetime(date_str).normalize()

def days(n=1):
    return timedelta(days=n)

def years(n=1):
    return relativedelta(years=n)

def round_date(x, unit):
    if isinstance(unit, (timedelta, relativedelta)):
        # Approximation for Period unit rounding
        # This is a simplified version of the logic described in the R source
        return x # Simplified
    
    unit = str(unit)
    # Handle fractional seconds
    if unit == ".5s":
        seconds = x.timestamp()
        rounded = round(seconds * 2) / 2
        return pd.to_datetime(rounded, unit='s')
    
    # Standard units
    if unit in ["sec", "second"]:
        return x.floor('s') if (x.timestamp() % 1) < 0.5 else x.ceil('s')
    if unit == "minute":
        return x.round('min')
    if unit == "5 mins":
        seconds = x.timestamp()
        rounded = (seconds // 300) * 300 + (300 if (seconds % 300) >= 150 else 0)
        return pd.to_datetime(rounded, unit='s')
    if unit == "hour":
        return x.round('h')
    if unit == "2 hours":
        seconds = x.timestamp()
        rounded = (seconds // 7200) * 7200 + (7200 if (seconds % 7200) >= 3600 else 0)
        return pd.to_datetime(rounded, unit='s')
    if unit == "day":
        return x.round('D')
    if unit == "week":
        # R lubridate weeks start on Sunday by default (week_start=7)
        days_since_sunday = (x.weekday() + 1) % 7
        return x - pd.Timedelta(days=days_since_sunday)
    if unit == "month":
        # Simple rounding to first of month (simplified)
        return x.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "bimonth":
        month = ((x.month - 1) // 2) * 2 + 1
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit in ["quarter", "3 months"]:
        month = ((x.month - 1) // 3) * 3 + 1
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "halfyear":
        month = 1 if x.month <= 6 else 7
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "year":
        return x.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return x

def floor_date(x, unit):
    if isinstance(unit, (timedelta, relativedelta)):
        if isinstance(unit, relativedelta) and unit.years >= 1:
            return x.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return x - (x - x.floor('D')) # Simple day floor
        
    unit = str(unit)
    if unit == ".1s":
        seconds = x.timestamp()
        return pd.to_datetime((seconds // 0.1) * 0.1, unit='s')
    if unit in ["second", "sec"]:
        return x.floor('s')
    if unit == "minute":
        return x.floor('min')
    if unit == "hour":
        return x.floor('h')
    if unit == "day":
        return x.floor('D')
    if unit == "week":
        days_since_sunday = (x.weekday() + 1) % 7
        return x - pd.Timedelta(days=days_since_sunday)
    if unit == "month":
        return x.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "bimonth":
        month = ((x.month - 1) // 2) * 2 + 1
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "quarter":
        month = ((x.month - 1) // 3) * 3 + 1
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "season": # Simplified approximation
        month = (x.month - 1) // 3 * 3 + 1
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "halfyear":
        month = 1 if x.month <= 6 else 7
        return x.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "year":
        return x.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return x

def ceiling_date(x, unit, change_on_boundary=None):
    if change_on_boundary is None:
        # In R, change_on_boundary is TRUE if x is a Date object
        change_on_boundary = False # Default for POSIXct
        
    if not change_on_boundary and (x.hour == 0 and x.minute == 0 and x.second == 0 and x.microsecond == 0):
        # If on boundary and change_on_boundary is False, return x
        if unit in ["month", "year", "day"]:
            return x

    if isinstance(unit, (timedelta, relativedelta)):
        return x + unit # Simple approximation

    unit = str(unit)
    if unit == ".1 sec":
        seconds = x.timestamp()
        return pd.to_datetime(np.ceil(seconds * 10) / 10, unit='s')
    if unit in ["second", "sec"]:
        return x.ceil('s')
    if unit == "minute":
        return x.ceil('min')
    if unit == "5 mins":
        seconds = x.timestamp()
        return pd.to_datetime(np.ceil(seconds / 300) * 300, unit='s')
    if unit == "hour":
        return x.ceil('h')
    if unit == "day":
        return x.ceil('D')
    if unit == "week":
        days_until_sunday = (6 - x.weekday()) % 7
        if days_until_sunday == 0 and x.time() == datetime().time():
            return x if not change_on_boundary else x + pd.Timedelta(days=7)
        return x + pd.Timedelta(days=days_until_sunday)
    if unit == "month":
        next_month = x.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + pd.Timedelta(days=31)
        res = next_month.replace(day=1)
        if not change_on_boundary and x.day == 1 and x.time() == datetime().time():
            return x
        return res
    if unit in ["bimonth", "2 months"]:
        month = ((x.month - 1) // 2) * 2 + 3
        year_offset = 0
        if month > 12:
            month -= 12
            year_offset = 1
        res = x.replace(year=x.year + year_offset, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
        return res
    if unit == "quarter":
        month = ((x.month - 1) // 3) * 3 + 4
        year_offset = 0
        if month > 12:
            month -= 12
            year_offset = 1
        return x.replace(year=x.year + year_offset, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "season":
        month = ((x.month - 1) // 3) * 3 + 4
        year_offset = 0
        if month > 12:
            month -= 12
            year_offset = 1
        return x.replace(year=x.year + year_offset, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "halfyear":
        month = 7 if x.month <= 6 else 1
        year_offset = 1 if month == 1 else 0
        return x.replace(year=x.year + year_offset, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == "year":
        return x.replace(year=x.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return x

x = ymd_hms("2009-08-03 12:01:59.23")
print(round_date(x, ".5s"))
print(round_date(x, "sec"))
print(round_date(x, "second"))
print(round_date(x, "minute"))
print(round_date(x, "5 mins"))
print(round_date(x, "hour"))
print(round_date(x, "2 hours"))
print(round_date(x, "day"))
print(round_date(x, "week"))
print(round_date(x, "month"))
print(round_date(x, "bimonth"))
print(round_date(x, "quarter") == round_date(x, "3 months"))
print(round_date(x, "halfyear"))
print(round_date(x, "year"))

x = ymd_hms("2009-08-03 12:01:59.23")
print(floor_date(x, ".1s"))
print(floor_date(x, "second"))
print(floor_date(x, "minute"))
print(floor_date(x, "hour"))
print(floor_date(x, "day"))
print(floor_date(x, "week"))
print(floor_date(x, "month"))
print(floor_date(x, "bimonth"))
print(floor_date(x, "quarter"))
print(floor_date(x, "season"))
print(floor_date(x, "halfyear"))
print(floor_date(x, "year"))

x = ymd_hms("2009-08-03 12:01:59.23")
print(ceiling_date(x, ".1 sec"))
print(ceiling_date(x, "second"))
print(ceiling_date(x, "minute"))
print(ceiling_date(x, "5 mins"))
print(ceiling_date(x, "hour"))
print(ceiling_date(x, "day"))
print(ceiling_date(x, "week"))
print(ceiling_date(x, "month"))
print(ceiling_date(x, "bimonth") == ceiling_date(x, "2 months"))
print(ceiling_date(x, "quarter"))
print(ceiling_date(x, "season"))
print(ceiling_date(x, "halfyear"))
print(ceiling_date(x, "year"))

print(floor_date(x, days(2)))
print(floor_date(x, years(1)))

print(pd.to_datetime("2009-08-03 12:01:59.3"))
print(ceiling_date(x, ".1 sec"))

print(ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month"))
print(ceiling_date(ymd("2000-01-01"), "month"))

print(ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month", change_on_boundary=True))
print(ceiling_date(ymd("2000-01-01"), "month"))

print(ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month", change_on_boundary=False))
print(ceiling_date(ymd("2000-01-01"), "month"))

x = ymd_hms("2000-01-01 00:00:00")
print(ceiling_date(x, "month"))
print(ceiling_date(x, "month", change_on_boundary=True))

x = ymd("2000-01-01")
print(ceiling_date(x, "month"))
print(ceiling_date(x, "month", change_on_boundary=True))