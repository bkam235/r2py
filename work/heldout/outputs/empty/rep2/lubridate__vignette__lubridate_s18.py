import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# r2py:entity:jan31
def ymd(date_str):
    return pd.to_datetime(date_str).date()

# r2py:entity:months
def months(n):
    # In R, months(0:11) returns a period. 
    # We handle the arithmetic in the operator equivalents.
    return n

# r2py:entity:days
def days(n):
    return relativedelta(days=int(n))

# r2py:entity:floor_date
def floor_date(dt, unit):
    if unit == "month":
        return dt.replace(day=1)
    return dt

# Lubridate standard addition (+): 
# If the resulting day exceeds the days in the target month, result is NA.
# r2py:entity:months
def lubridate_add_months(dt, m):
    if m == 0:
        return dt
    target_date = dt + relativedelta(months=m)
    if target_date.day != dt.day:
        return np.nan
    return target_date

# Lubridate %m+% addition: 
# If the resulting day exceeds the days in the target month, it clips to the last day.
# r2py:entity:months_2
def m_plus(dt, m):
    return dt + relativedelta(months=m)

# r2py:entity:jan31
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
# r2py:entity:months
res1 = [lubridate_add_months(jan31, i) for i in range(12)]
res1_str = [d.strftime('%Y-%m-%d') if isinstance(d, (date, datetime)) else 'NA' for d in res1]
# Format to match R's output: [1] "d1" "d2"... [6] "d6"... [11] "d11"...
print(f'      [1] "{"  ".join(res1_str[0:5])}"')
print(f' [6] "{"  ".join(res1_str[5:10])}"')
print(f'[11] "{"  ".join(res1_str[10:])}"')

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:floor_date
base = floor_date(jan31, "month")
res2 = []
for i in range(12):
    # 1st of month + i months + 31 days
    m_added = base + relativedelta(months=i)
    res2.append(m_added + days(31))

res2_str = [d.strftime('%Y-%m-%d') for d in res2]
print(f'      [1] "{"  ".join(res2_str[0:5])}"')
print(f' [6] "{"  ".join(res2_str[5:10])}"')
print(f'[11] "{"  ".join(res2_str[10:])}"')

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = [m_plus(jan31, i) for i in range(12)]
res3_str = [d.strftime('%Y-%m-%d') for d in res3]
print(f'      [1] "{"  ".join(res3_str[0:5])}"')
print(f' [6] "{"  ".join(res3_str[5:10])}"')
print(f'[11] "{"  ".join(res3_str[10:])}"')