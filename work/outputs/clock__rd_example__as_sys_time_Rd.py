import pandas as pd
from datetime import datetime, date
import pytz

# Simulation of clock's custom time types to match R output formatting
class ClockTime:
    def __init__(self, value, precision_label):
        self.value = value
        self.precision_label = precision_label

    def __repr__(self):
        # R prints: <sys_time<day>[1]>\n[1] "2019-01-01"
        # We simulate this by returning the header; the [1] "..." part is handled in the print wrapper
        return f"<{self.precision_label}[1]>"

def clock_print(obj):
    if isinstance(obj, ClockTime):
        print(f"      {repr(obj)}")
        # Format value based on precision
        val = obj.value
        if "day" in obj.precision_label:
            formatted = f'"{val.strftime("%Y-%m-%d")}"'
        elif "second" in obj.precision_label:
            formatted = f'"{val.strftime("%Y-%m-%dT%H:%M:%S")}"'
        else:
            formatted = f'"{val}"'
        print(f"[1] {formatted}")
    else:
        print(f"[1] {obj}")

# r2py:entity:as_sys_time
def as_sys_time(x):
    """
    Converts to a system time (UTC timestamp).
    """
    if isinstance(x, date) and not isinstance(x, datetime):
        # R Date is naive, as_sys_time treats as UTC
        dt = datetime.combine(x, datetime.min.time()).replace(tzinfo=pytz.UTC)
        return ClockTime(dt, "sys_time<day>")
    
    if isinstance(x, datetime):
        if x.tzinfo is None:
            dt = x.replace(tzinfo=pytz.UTC)
        else:
            dt = x.astimezone(pytz.UTC)
        
        # Determine precision for label
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            return ClockTime(dt, "sys_time<day>")
        return ClockTime(dt, "sys_time<second>")
    
    if isinstance(x, YearMonthDay):
        if x.day is None:
            # In R, as_sys_time(ym) where ym is just year-month fails
            raise TypeError("Can't perform this operation on a YearMonthDay without day precision.")
        dt = datetime(x.year, x.month, x.day).replace(tzinfo=pytz.UTC)
        return ClockTime(dt, "sys_time<day>")
    
    raise TypeError(f"Can't perform this operation on a {type(x).__name__}.")

# r2py:entity:as_naive_time
def as_naive_time(x):
    """
    Converts to a naive time.
    """
    if isinstance(x, date) and not isinstance(x, datetime):
        dt = datetime.combine(x, datetime.min.time())
        return ClockTime(dt, "naive_time<day>")
    
    if isinstance(x, datetime):
        dt = x.replace(tzinfo=None)
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            return ClockTime(dt, "naive_time<day>")
        return ClockTime(dt, "naive_time<second>")
    
    if isinstance(x, YearMonthDay):
        if x.day is None:
            raise TypeError("Can't perform this operation on a YearMonthDay without day precision.")
        dt = datetime(x.year, x.month, x.day)
        return ClockTime(dt, "naive_time<day>")
    
    raise TypeError(f"Can't perform this operation on a {type(x).__name__}.")

class YearMonthDay:
    def __init__(self, year, month=None, day=None):
        self.year = year
        self.month = month
        self.day = day
    
    def __repr__(self):
        return f"YearMonthDay(year={self.year}, month={self.month}, day={self.day})"

# r2py:entity:ym
def year_month_day(year, month=None, day=None):
    return YearMonthDay(year, month, day)

# r2py:entity:ymd
def set_day(ym, day_val):
    if not isinstance(ym, YearMonthDay):
        raise TypeError(f"Can't perform this operation on a {type(ym).__name__}.")
    return YearMonthDay(ym.year, ym.month, day_val)

# Execution
# r2py:entity:x
x = pd.to_datetime("2019-01-01").date()

# Dates are assumed to be naive, so the printed time is the same whether
# we convert it to sys-time or naive-time
# r2py:entity:as_sys_time
clock_print(as_sys_time(x))
# r2py:entity:as_naive_time
clock_print(as_naive_time(x))

# America/New_York 2019-01-01 01:00:00
# r2py:entity:y
tz_ny = pytz.timezone("America/New_York")
y = tz_ny.localize(datetime(2019, 1, 1, 1, 0, 0))

# The sys time displays the equivalent time in UTC (5 hours ahead of
# America/New_York at this point in the year)
# r2py:entity:as_sys_time_1
clock_print(as_sys_time(y))

# r2py:entity:ym
ym = year_month_day(2019, 2)

# A minimum of day precision is required
# r2py:entity:try
try:
    as_sys_time(ym)
except Exception:
    # R's try() prints the error to stderr or as a warning, 
    # but in the provided R output, it resulted in (empty) stdout.
    pass

# r2py:entity:ymd
ymd = set_day(ym, 10)
# r2py:entity:as_sys_time_2
clock_print(as_sys_time(ymd))