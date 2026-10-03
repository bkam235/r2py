# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

# r2py:entity:earlyCloseNYSE
def USThanksgivingDay(year):
    # 4th Thursday of November
    first_day = datetime(year, 11, 1)
    first_thu = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    return first_thu + timedelta(weeks=3)

def ChristmasDay(year):
    return datetime(year, 12, 25)

def ChristmasEve(year):
    return datetime(year, 12, 24)

def earlyCloseNYSE(year):
    if isinstance(year, (int, np.integer)):
        years = [year]
    else:
        years = year

    all_results = []
    for y in years:
        res = []
        # Thanksgiving + 1 day (Friday after Thanksgiving)
        thanks = USThanksgivingDay(y)
        thanks_p1 = thanks + timedelta(days=1)
        res.append(thanks_p1.replace(hour=13, minute=0, second=0))

        # July 3rd if July 4th is not Sat/Sun
        indep_m1 = datetime(y, 7, 3, 13, 0, 0)
        july_4 = datetime(y, 7, 4)
        if july_4.weekday() < 5: # Not Sat/Sun
            res.append(indep_m1)

        # Christmas Eve if Christmas is not Mon, Sat, Sun
        xmas = ChristmasDay(y)
        if xmas.weekday() not in [0, 5, 6]: # 0=Mon, 5=Sat, 6=Sun
            eve = ChristmasEve(y).replace(hour=13, minute=0, second=0)
            res.append(eve)
        
        all_results.extend(sorted(res))
    
    return np.array(all_results)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, (int, np.integer)):
        years = [year]
    else:
        years = year

    cal = USFederalHolidayCalendar()
    holidays = []
    
    for y in years:
        # Using pandas USFederalHolidayCalendar as a close approximation for standard NYSE holidays
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31)
        hols = cal.holidays(start=start, end=end)
        holidays.extend(hols.tolist())

    # Filter for NYSE specific logic (removing weekends)
    # In R, holidayNYSE returns dates that are not Sat/Sun
    final_hols = [h for h in holidays if h.weekday() < 5]
    return np.array(sorted(final_hols))

# --- Main Script ---

# earlyCloseNYSE(1990)
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# earlyCloseNYSE(2022:2024)
# r2py:entity:earlyCloseNYSE_1
years_range = np.arange(2022, 2025)
print(earlyCloseNYSE(years_range))

# holidayNYSE(2022:2024)
# r2py:entity:holidayNYSE
print(holidayNYSE(years_range))

# Combined early closings & holidays
# r2py:entity:c
combined = np.concatenate([earlyCloseNYSE(years_range), holidayNYSE(years_range)])
print(combined)