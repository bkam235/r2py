# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

def USThanksgivingDay(year):
    # Thanksgiving is the 4th Thursday of November
    # Start at Nov 1st, find first Thursday, add 3 weeks
    first_nov = datetime(year, 11, 1)
    # weekday(): Monday=0, Sunday=6. Thursday=3.
    first_thu = first_nov + timedelta(days=(3 - first_nov.weekday() + 7) % 7)
    return first_thu + timedelta(weeks=3)

def ChristmasDay(year):
    return datetime(year, 12, 25)

def ChristmasEve(year):
    return datetime(year, 12, 24)

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    # Handle scalar or iterable
    years = np.atleast_1d(year).astype(int)
    all_results = []

    for y in years:
        res = []
        # Logic for years >= 2012
        if y >= 2012:
            # Day after Thanksgiving
            thanks = USThanksgivingDay(y)
            res.append(thanks + timedelta(days=1))
            
            # July 3rd (if not Sat/Sun)
            indep_m1 = datetime(y, 7, 3)
            if indep_m1.weekday() < 5:
                res.append(indep_m1)
            
            # Christmas Eve (if Christmas is not Mon, Sat, Sun)
            xmas = ChristmasDay(y)
            eve = ChristmasEve(y)
            if xmas.weekday() not in [0, 5, 6]:
                res.append(eve)
        
        # Set time to 13:00:00 for early closings
        formatted_res = [datetime(d.year, d.month, d.day, 13, 0, 0) for d in res]
        all_results.extend(sorted(formatted_res))

    # In the original R code, 'early_close' is an internal database. 
    # Since we don't have the internal db, we return the calculated ones.
    return np.array(all_results) if len(all_results) > 0 else np.array([])

# r2py:entity:holidayNYSE
def holidayNYSE(year):
    years = np.atleast_1d(year).astype(int)
    cal = USFederalHolidayCalendar()
    holidays = []
    
    for y in years:
        # Use pandas Holiday calendar to get US Federal holidays
        start = pd.Timestamp(year=y, month=1, day=1)
        end = pd.Timestamp(year=y, month=12, day=31)
        holidays.extend(cal.holidays(start=start, end=end))
    
    # NYSE typically doesn't trade on weekends
    # The R code filters out Sat/Sun (posix3$wday == 0 | 6)
    valid_holidays = [h for h in holidays if h.weekday() < 5]
    
    # Convert to numpy array of datetimes for consistency
    return np.array(sorted(valid_holidays), dtype='datetime64[ns]')

# --- Example Execution ---

# earlyCloseNYSE(1990)
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# earlyCloseNYSE(2022:2024)
# r2py:entity:earlyCloseNYSE_1
print(earlyCloseNYSE(np.arange(2022, 2025)))

# holidayNYSE(2022:2024)
# r2py:entity:holidayNYSE
print(holidayNYSE(np.arange(2022, 2025)))

# early closings & holidays combined
# r2py:entity:c
early_closings = earlyCloseNYSE(np.arange(2022, 2025))
holidays = holidayNYSE(np.arange(2022, 2025))
# Convert both to a common format (datetime64) and concatenate
combined = np.concatenate([pd.to_datetime(early_closings), pd.to_datetime(holidays)])
print(np.sort(combined))