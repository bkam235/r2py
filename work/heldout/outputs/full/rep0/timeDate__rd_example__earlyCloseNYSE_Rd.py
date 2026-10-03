# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

def get_nth_weekday(year, month, weekday, n):
    """Helper to find the nth occurrence of a weekday in a month (weekday: 0=Mon, 6=Sun)."""
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    day = 1 + (weekday - first_weekday + 7) % 7
    day += (n - 1) * 7
    return datetime(year, month, day)

def USThanksgivingDay(year):
    # 4th Thursday of November
    return get_nth_weekday(year, 11, 3, 4)

def USLaborDay(year):
    # 1st Monday of September
    return get_nth_weekday(year, 9, 0, 1)

def USColumbusDay(year):
    # 2nd Monday of October
    return get_nth_weekday(year, 10, 0, 2)

def Easter(year, shift=0):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day) + timedelta(days=shift)

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    if isinstance(year, (int, np.integer)):
        years = [year]
    else:
        years = year

    results = []
    for y in years:
        y_results = []
        # Thanksgiving Friday
        thanks_friday = USThanksgivingDay(y) + timedelta(days=1)
        y_results.append(thanks_friday.replace(hour=13, minute=0, second=0))
        
        # July 3rd early close if July 4th is Sat/Sun
        july_3 = datetime(y, 7, 3)
        july_4 = datetime(y, 7, 4)
        if july_4.weekday() >= 5: # Sat or Sun
            y_results.append(july_3.replace(hour=13, minute=0, second=0))
        
        # Christmas Eve early close if Christmas is not Mon, Sat, or Sun
        xmas = datetime(y, 12, 25)
        eve = datetime(y, 12, 24)
        if xmas.weekday() not in [0, 5, 6]:
            y_results.append(eve.replace(hour=13, minute=0, second=0))
            
        results.extend(sorted(y_results))
    
    return results if len(years) > 1 else (results[0] if results else None)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, (int, np.integer)):
        years = [year]
    else:
        years = year
        
    cal = USFederalHolidayCalendar()
    holidays = []
    
    for y in years:
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31)
        # Standard Federal Holidays
        fed_holidays = cal.holidays(start=start, end=end)
        holidays.extend(fed_holidays.tolist())
        
        # Good Friday
        good_friday = Easter(y, shift=-2)
        holidays.append(good_friday)
        
    # Filter weekends and sort
    final_holidays = [h for h in holidays if h.weekday() < 5]
    # Ensure unique and sorted
    final_holidays = sorted(list(set(final_holidays)))
    
    return final_holidays if len(years) > 1 else (final_holidays[0] if final_holidays else None)

# Execution
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
years_range = np.arange(2022, 2025)
early_closings = earlyCloseNYSE(years_range)
print(early_closings)

# r2py:entity:holidayNYSE
holidays = holidayNYSE(years_range)
print(holidays)

# Combine early closings and holidays
# r2py:entity:c
combined = early_closings + holidays
print(combined)