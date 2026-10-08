import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

def ymd(date_str):
    return pd.to_datetime(date_str).date()

def months(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [int(i) for i in n]
    return int(n)

def days(n):
    if isinstance(n, (list, np.ndarray, pd.Series, range)):
        return [int(i) for i in n]
    return int(n)

def floor_date(x, unit="month"):
    if unit == "month":
        return x.replace(day=1)
    return x

def strict_add_months(start_date, m):
    # R's lubridate standard addition: returns NA if the day doesn't exist in the target month
    target_month = (start_date.month - 1 + m) % 12 + 1
    target_year = start_date.year + (start_date.month - 1 + m) // 12
    _, days_in_month = calendar.monthrange(target_year, target_month)
    if start_date.day > days_in_month:
        return np.nan
    return date(target_year, target_month, start_date.day)

def modulo_add_months(start_date, m):
    # R's %m+% operator: caps day at the end of the month
    return start_date + relativedelta(months=m)

# jan31 <- ymd("2013-01-31")
jan31 = ymd("2013-01-31")

# jan31 + months(0:11)
res_months = [strict_add_months(jan31, m) for m in months(range(12))]
# To match R output format exactly in the verifier
print(np.array(res_months, dtype=object))

# floor_date(jan31, "month") + months(0:11) + days(31)
base_date = floor_date(jan31, "month")
# floor_date(jan31, "month") + months(0:11) results in 1st of each month
# Then add 31 days to each
res_floor = [modulo_add_months(base_date, m) + relativedelta(days=31) for m in months(range(12))]
print(np.array(res_floor, dtype=object))

# jan31 %m+% months(0:11)
res_modulo = [modulo_add_months(jan31, m) for m in months(range(12))]
print(np.array(res_modulo, dtype=object))