import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

# r2py:entity:x
def ymd(date_strings):
    return pd.to_datetime(date_strings)

# r2py:entity:quarter
def quarter(x, type_val="quarter", fiscal_start=1, with_year=None):
    if with_year is None:
        with_year = (type_val == "year.quarter")
    
    # R logic: fs <- (fiscal_start - 1) %% 12
    fs = (fiscal_start - 1) % 12
    # shifted <- seq(fs, 11 + fs) %% 12 + 1
    shifted = [(fs + i) % 12 + 1 for i in range(12)]
    
    months = x.month.values
    years = x.year.values
    
    # quarters <- rep(1:4, each = 3)
    quarters_map = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    
    # s <- match(m, shifted)
    # match finds the first index. shifted contains 1..12 in some order.
    q_vals = []
    for m in months:
        try:
            idx = shifted.index(m)
            q_vals.append(quarters_map[idx])
        except ValueError:
            q_vals.append(np.nan)
    q = np.array(q_vals)
    
    if with_year:
        type_val = "year.quarter"
        
    if type_val == "quarter":
        return q.astype(int)
# r2py:entity:quarter_1
    elif type_val == "year.quarter":
        # nxt_year_months <- if (fs != 0) (fs + 1):12
        if fs != 0:
            nxt_year_months = list(range(fs + 1, 13))
        else:
            nxt_year_months = []
            
        y = np.array([years[i] + (1 if months[i] in nxt_year_months else 0) for i in range(len(years))])
        out = y + (q / 10.0)
        return out
# r2py:entity:quarter_3
    elif type_val == "date_first":
        # starting_months <- shifted[seq(1, length(shifted), 3)]
        starting_months = [shifted[0], shifted[3], shifted[6], shifted[9]]
        
        first_dates = []
        for m, y, q_val in zip(months, years, q):
            start_m = starting_months[int(q_val) - 1]
            # final_years <- year(x) - (starting_months[q] > m)
            fy = y - (1 if start_m > m else 0)
            first_dates.append(date(int(fy), int(start_m), 1).isoformat())
        return np.array(first_dates)
# r2py:entity:quarter_4
    elif type_val == "date_last":
        # date_last uses date_first logic then adds 3 months and subtracts 1 day
        starting_months = [shifted[0], shifted[3], shifted[6], shifted[9]]
        last_dates = []
        for m, y, q_val in zip(months, years, q):
            start_m = starting_months[int(q_val) - 1]
            fy = y - (1 if start_m > m else 0)
            d_first = date(int(fy), int(start_m), 1)
            d_last = d_first + relativedelta(months=3) - relativedelta(days=1)
            last_dates.append(d_last.isoformat())
        return np.array(last_dates)
    else:
        raise ValueError(f"Unsupported type {type_val}")

# r2py:entity:semester
def semester(x, with_year=False):
    months = x.month.values
    years = x.year.values
    # semesters <- rep(1:2, each = 6)
    semesters_map = [1]*6 + [2]*6
    s = np.array([semesters_map[m-1] for m in months])
    
    if with_year:
        return years + (s / 10.0)
    else:
        return s.astype(int)

# r2py:entity:x
x = ymd(["2012-03-26", "2012-05-04", "2012-09-23", "2012-12-31"])

# r2py:entity:quarter
print(quarter(x))
# r2py:entity:quarter_1
print(quarter(x, type_val="year.quarter"))
# r2py:entity:quarter_2
print(quarter(x, type_val="year.quarter", fiscal_start=11))
# r2py:entity:quarter_3
print(quarter(x, type_val="date_first", fiscal_start=11))
# r2py:entity:quarter_4
print(quarter(x, type_val="date_last", fiscal_start=11))
# r2py:entity:semester
print(semester(x))
# r2py:entity:semester_1
print(semester(x, with_year=True))