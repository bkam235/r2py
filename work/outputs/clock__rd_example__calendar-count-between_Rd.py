# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

# r2py:entity:x
def year_month_day(year, month=None, day=None):
    """
    Simplified implementation of clock::year_month_day.
    Handles scalars and sequences for the 'day' argument to match R's vectorization.
    """
    if month is None:
        # Precision is year
        return np.array([date(int(year), 1, 1)]) if isinstance(year, (list, np.ndarray)) else date(int(year), 1, 1)
    
    if day is None:
        # Precision is month
        return np.array([date(int(year), int(month), 1)]) if isinstance(year, (list, np.ndarray)) else date(int(year), int(month), 1)
    
    # Precision is day
    # Handle R-style sequence: 04:06 -> [4, 5, 6]
    if isinstance(day, (list, np.ndarray)):
        return np.array([date(int(year), int(month), int(d)) for d in day])
    else:
        return date(int(year), int(month), int(day))

# r2py:entity:calendar_count_between
def calendar_count_between(start, end, precision):
    """
    Mimics clock::calendar_count_between for 'year' precision.
    Calculates the number of whole units (years) between dates.
    """
    if precision != "year":
        raise NotImplementedError("Only 'year' precision is implemented for this translation.")

    # Convert start to list/array if scalar to handle vectorized 'end'
    starts = np.atleast_1d(start)
    ends = np.atleast_1d(end)
    
    # Ensure starts is broadcasted to match ends length
    if len(starts) == 1 and len(ends) > 1:
        starts = np.repeat(starts, len(ends))
    
    results = []
    for s, e in zip(starts, ends):
        # relativedelta calculates difference in years, months, days
        diff = relativedelta(e, s)
        results.append(diff.years)
    
    return np.array(results) if len(results) > 1 else results[0]

# Number of whole years between these dates
# r2py:entity:x
x = year_month_day(2000, 1, 5)
# R's 04:06 is a sequence [4, 5, 6]
# r2py:entity:y
y = year_month_day(2005, 1, [4, 5, 6])

# Note that `2000-01-05 -> 2005-01-04` is only 4 full years
# r2py:entity:calendar_count_between
result = calendar_count_between(x, y, "year")
print(result)