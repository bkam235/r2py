import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    if isinstance(n, (int, float)):
        return [n]
    return list(n)

# r2py:entity:days
def days(n):
    return relativedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(x, unit="seconds"):
    if unit == "month":
        return x.replace(day=1)
    return x

# r2py:entity:months
def lubridate_add_months(start_date, n_months):
    """
    Implements R lubridate's default + months() behavior:
    Returns NA if the day of the month is not valid for the target month.
    """
    target_date = start_date + relativedelta(months=n_months)
    if target_date.day != start_date.day:
        return np.nan
    return target_date

# r2py:entity:months_2
def lubridate_mplus_months(start_date, n_months):
    """
    Implements R lubridate's %m+% behavior:
    Clamps the date to the last day of the month if it would overflow.
    """
    return start_date + relativedelta(months=n_months)

def format_r_dates(dates):
    """Helper to format output similar to R's print.prDate"""
    formatted = []
    for d in dates:
        if pd.isna(d):
            formatted.append("NA")
        else:
            formatted.append(f'"{d.strftime("%Y-%m-%d")}"')
    
    output = []
    for i in range(0, len(formatted), 6):
        chunk = formatted[i:i+6]
        prefix = f" [1] " if i == 0 else f"[{i+1}] "
        output.append(prefix + " ".join(chunk))
    return "\n".join(output)

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = [lubridate_add_months(jan31, m) for m in months(range(12))]
print(format_r_dates(res1))

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
floor_jan = floor_date(jan31, "month")
# r2py:entity:months_1
res2 = []
for m in range(12):
    # In R, floor_date(jan31, "month") is 2013-01-01
    # 2013-01-01 + months(m) + days(31)
    step1 = floor_jan + relativedelta(months=m)
# r2py:entity:days
    step2 = step1 + days(31)
    res2.append(step2)
print(format_r_dates(res2))

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = [lubridate_mplus_months(jan31, m) for m in months(range(12))]
print(format_r_dates(res3))