# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import pandas as pd
import numpy as np
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pytz

# r2py:entity:x_1
def add_years(x, n):
    """
    Adds n years to x. Handles both single dates/datetimes 
    and arrays/lists of dates/datetimes.
    """
    if isinstance(n, (list, np.ndarray, range)):
        # If n is a sequence, we produce a matrix-like result or list of lists
        # In R: add_years(date, 0:5) returns a vector of 6 dates.
        # If x is a single date, we return a list of dates.
        if not isinstance(x, (list, np.ndarray, pd.Series)):
            return [x + relativedelta(years=i) for i in n]
        else:
            # If x is also a sequence, this is usually outer-product behavior in R
            # But for this specific script, x is a single date being expanded.
            return [[val + relativedelta(years=i) for i in n] for val in x]
    else:
        return x + relativedelta(years=n)

# r2py:entity:date_leap_year
def date_leap_year(x):
    """
    Returns TRUE if the date is in a leap year, FALSE otherwise.
    """
    def is_leap(dt):
        year = dt.year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    if isinstance(x, (list, np.ndarray, pd.Series)):
        return np.array([is_leap(d) for d in x])
    else:
        return is_leap(x)

# Part 1: Date
# r2py:entity:x
x = pd.to_datetime("2019-01-01").date()
# r2py:entity:x_1
x_res = add_years(x, range(0, 6))
print(date_leap_year(x_res))

# Part 2: POSIXct (DateTime with timezone)
# r2py:entity:y
tz = pytz.timezone("America/New_York")
y = tz.localize(datetime(2019, 1, 1))
# r2py:entity:y_1
y_res = add_years(y, range(0, 6))
# r2py:entity:date_leap_year_1
print(date_leap_year(y_res))