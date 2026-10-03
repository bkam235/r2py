import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
from datetime import date, timedelta

# jan31 <- ymd("2013-01-31")
# r2py:entity:jan31
jan31 = pd.to_datetime("2013-01-31").date()

# jan31 + months(0:11)
# r2py:entity:months
def r_months_add(start_date, month_counts):
    results = []
    for i in month_counts:
        try:
            year = start_date.year + (start_date.month + i - 1) // 12
            month = (start_date.month + i - 1) % 12 + 1
            # R's Period addition: if the day is not valid for the target month, result is NA
            res_date = pd.to_datetime(f"{year}-{month:02d}-{start_date.day:02d}").date()
            results.append(res_date)
        except ValueError:
            results.append(np.nan)
    return results

# Generate and print results for months
months_res = r_months_add(jan31, range(12))
print("[1] " + " ".join([f'"{d}"' if not pd.isna(d) else "NA" for d in months_res]))

# floor_date(jan31, "month") + months(0:11) + days(31)
# r2py:entity:days
floor_jan31 = jan31.replace(day=1)
res2 = []
for i in range(12):
    # 1. Add months (always valid since day is 1)
    year = floor_jan31.year + (floor_jan31.month + i - 1) // 12
    month = (floor_jan31.month + i - 1) % 12 + 1
    date_1st = date(year, month, 1)
    # 2. Add 31 days
    res2.append((pd.to_datetime(date_1st) + pd.Timedelta(days=31)).date())

print("[1] " + " ".join([f'"{d}"' for d in res2]))

# jan31 %m+% months(0:11)
# r2py:entity:months_2
res3 = []
for i in range(12):
    # %m+% in lubridate rolls back to the last valid day of the month
    res3.append((pd.to_datetime(jan31) + DateOffset(months=i)).date())

print("[1] " + " ".join([f'"{d}"' for d in res3]))