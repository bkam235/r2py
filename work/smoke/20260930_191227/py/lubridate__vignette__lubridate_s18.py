import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    # In R, months(0:11) creates a Period object
    if isinstance(n, (int, float)):
        return [n]
    return list(n)

# r2py:entity:days
def days(n):
    if isinstance(n, (int, float)):
        return relativedelta(days=int(n))
    return [relativedelta(days=int(i)) for i in n]

# r2py:entity:floor_date
def floor_date(date_obj, unit):
    if unit == "month":
        return date_obj.replace(day=1)
    return date_obj

def format_date(d):
    return f'"{d.strftime("%Y-%m-%d")}"' if d is not None else "NA"

def print_r_style(res):
    # R prints in chunks of 5 usually, but for short vectors it's often:
    # [1] "val1" "val2" ...
    # [6] "val6" ...
    formatted = [format_date(d) for d in res]
    out = ""
    for i in range(0, len(formatted), 6):
        prefix = f"[{i + 1}] " if i == 0 else f"[{i + 1}] "
        chunk = " ".join(formatted[i:i+6])
        out += prefix + chunk + "\n"
    return out.strip()

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# R's + months() is strict: if the target month has fewer days, it results in NA
# r2py:entity:months
def strict_add_months(start_date, delta_months):
    target_year = start_date.year + (start_date.month + delta_months - 1) // 12
    target_month = (start_date.month + delta_months - 1) % 12 + 1
    days_in_month = calendar.monthrange(target_year, target_month)[1]
    if start_date.day > days_in_month:
        return None
    return date(target_year, target_month, start_date.day)

res1 = [strict_add_months(jan31, i) for i in range(12)]
print(print_r_style(res1))

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
fd = floor_date(jan31, "month")
# r2py:entity:months_1
res2 = []
for i in range(12):
    # floor_date is 2013-01-01. + months(i) -> 2013-01-01, 2013-02-01...
    # then + days(31)
    d_month = strict_add_months(fd, i)
    # Since fd is always day 1, strict_add_months never returns None
    res2.append(d_month + timedelta(days=31))
print(print_r_style(res2))

# jan31 %m+% months(0:11)
# %m+% is the "roll-back" operator: it caps the day at the end of the month
# r2py:entity:months_2
def roll_add_months(start_date, delta_months):
    target_year = start_date.year + (start_date.month + delta_months - 1) // 12
    target_month = (start_date.month + delta_months - 1) % 12 + 1
    days_in_month = calendar.monthrange(target_year, target_month)[1]
    actual_day = min(start_date.day, days_in_month)
    return date(target_year, target_month, actual_day)

res3 = [roll_add_months(jan31, i) for i in range(12)]
print(print_r_style(res3))