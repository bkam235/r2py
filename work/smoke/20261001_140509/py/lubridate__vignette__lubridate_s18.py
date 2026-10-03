# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

jan31 = ymd("2013-01-31")

# r2py:entity:months
def months(n):
    if isinstance(n, (int, float)):
        return [int(n)]
    return [int(x) for x in n]

# r2py:entity:days
def days(n):
    if isinstance(n, (int, float)):
        return [int(n)]
    return [int(x) for x in n]

# r2py:entity:floor_date
def floor_date(date_obj, unit):
    if unit == "month":
        return date_obj.replace(day=1)
    return date_obj

def add_months_lubridate(start_date, n):
    """Mimics lubridate's month addition: returns NA if day is not preserved."""
    target_month = (start_date.month + n - 1) % 12 + 1
    target_year = start_date.year + (start_date.month + n - 1) // 12
    last_day_of_target = calendar.monthrange(target_year, target_month)[1]
    if start_date.day > last_day_of_target:
        return None
    return date(target_year, target_month, start_date.day)

def add_months_clipped(start_date, n):
    """Mimics lubridate's %m+% operator: clips to end of month."""
    return start_date + relativedelta(months=n)

# r2py:entity:months_1
def add_periods(start_date, periods_vals):
    res = []
    for p in periods_vals:
        res.append(add_months_lubridate(start_date, p))
    return res

def format_r_vector(vec):
    """Helper to format Python lists to look like R date vectors."""
    formatted = []
    for val in vec:
        if val is None:
            formatted.append("NA")
        elif isinstance(val, (date, datetime)):
            formatted.append(val.strftime('%Y-%m-%d'))
        else:
            formatted.append(str(val))
    
    # R prints in chunks of 6-12 typically; here we just join with quotes
    quoted = ['"' + x + '"' if x != "NA" else "NA" for x in formatted]
    
    # Construct output string to mimic R's wrapping
    res = "      [1] " + " ".join(quoted[:6])
    if len(quoted) > 6:
        res += "\n [6] " + " ".join(quoted[6:])
    return res

# --- Main Script ---
# suppressPackageStartupMessages(library(lubridate))
# import_lubridate: lubridate

# jan31 <- ymd("2013-01-31")
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = add_periods(jan31, months(range(12)))
print(format_r_vector(res1))

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
base_date = floor_date(jan31, "month")
res2 = []
for m_val in range(12):
    d_m = add_months_lubridate(base_date, m_val)
    res2.append(d_m + timedelta(days=31))
# R produces 12 elements here based on range(12) but the source shows 12 results in stdout
# Let's ensure we calculate for the range
print(format_r_vector(res2))

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = []
for m_val in range(12):
    d = add_months_clipped(jan31, m_val)
    res3.append(d)
print(format_r_vector(res3))