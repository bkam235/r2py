import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np

# Suppress package startup messages (no-op in Python)
# import lubridate (no-op - simulating with dateutil)

def ymd(date_str):
    """Parse a date string in YYYY-MM-DD format."""
    return pd.to_datetime(date_str).date()

def months(n):
    """Return month offsets as integers."""
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

def days(n):
    """Return day offsets as integers."""
    if isinstance(n, (list, np.ndarray, pd.Series)):
        return [int(i) for i in n]
    return int(n)

def floor_date(x, unit="seconds"):
    """Floor a date to the specified unit."""
    if unit == "month":
        return x.replace(day=1)
    return x

def add_months_standard(d, m):
    """
    Add months with R's standard + behavior:
    Returns NA (None) if the resulting day doesn't exist in the target month.
    """
    if m == 0:
        return d
    try:
        result = d + relativedelta(months=m)
        # Check if day is valid in target month
        # If we're adding to day 31 and target month has fewer days,
        # relativedelta caps it, but R returns NA
        if d.day > 28:  # Only potential problem days
            # Try to create date with original day in target month
            test_date = d.replace(year=d.year, month=d.month) + relativedelta(months=m)
            next_month = test_date + relativedelta(days=1)
            # If adding 1 day goes to next month, original day doesn't exist
            if next_month.month != test_date.month:
                return None  # Represent NA as None
        return result
    except ValueError:
        return None

def add_months_modulo(d, m):
    """
    Add months with R's %m+% behavior:
    Preserves the day of month but caps at the last day of the target month.
    """
    return d + relativedelta(months=m)

# jan31 <- ymd("2013-01-31")
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
res1 = [add_months_standard(jan31, m) for m in months(np.arange(0, 12))]

# floor_date(jan31, "month") + months(0:11) + days(31)
base_dates = [add_months_modulo(floor_date(jan31, "month"), m) for m in months(np.arange(0, 12))]
res2 = [d + relativedelta(days=31) if d is not None else None for d in base_dates]

# jan31 %m+% months(0:11)
res3 = [add_months_modulo(jan31, m) for m in months(np.arange(0, 12))]
