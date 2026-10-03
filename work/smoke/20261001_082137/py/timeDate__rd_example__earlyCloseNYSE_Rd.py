# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def get_nth_weekday(year, month, weekday, n):
    """ Helper to find the nth occurrence of a weekday in a month.
    weekday: 0=Mon, 6=Sun (Python convention)
    """
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    offset = (weekday - first_weekday) % 7
    day = 1 + offset + (n - 1) * 7
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
    years = np.atleast_1d(year)
    res_list = []
    
    for y in years:
        y_res = []
        if y >= 2012:
            # Thanksgiving Friday
            thanks_p1 = USThanksgivingDay(y) + timedelta(days=1)
            y_res.append(thanks_p1.replace(hour=13, minute=0, second=0))
            
            # July 3rd (if not Sat/Sun)
            indep_m1 = datetime(y, 7, 3, 13, 0, 0)
            if indep_m1.weekday() < 5:
                y_res.append(indep_m1)
            
            # Christmas Eve (if Xmas not Mon/Sat/Sun)
            xmas = datetime(y, 12, 25)
            eve = datetime(y, 12, 24, 13, 0, 0)
            if xmas.weekday() not in [0, 5, 6]:
                y_res.append(eve)
        
        res_list.extend(sorted(y_res))
    
    return np.array(res_list)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    years = np.atleast_1d(year)
    holidays = []
    
    for y in years:
        # New Year's
        if y >= 1885:
            holidays.append(datetime(y, 1, 1))
            holidays.append(datetime(y, 7, 4))
            holidays.append(USThanksgivingDay(y))
            holidays.append(datetime(y, 12, 25))
        if y >= 1887:
            holidays.append(USLaborDay(y))
        if y not in [1898, 1906, 1907]:
            holidays.append(Easter(y, shift=-2))
        if 1896 <= y <= 1953:
            holidays.append(datetime(y, 2, 12))
        if 1909 <= y <= 1953:
            holidays.append(USColumbusDay(y))
        if y == 1918 or y == 1921 or (1934 <= y <= 1953):
            holidays.append(datetime(y, 11, 11))
        if y <= 1968 or y in [1972, 1976, 1980]:
            # Simplified Election Day (First Tuesday after first Monday in Nov)
            first_mon = get_nth_weekday(y, 11, 0, 1)
            elect_day = first_mon + timedelta(days=1)
            holidays.append(elect_day)
            
        if y <= 1970:
            holidays.append(datetime(y, 2, 22)) # Washington's
            holidays.append(get_nth_weekday(y, 5, 0, 1)) # Memorial
        else:
            # Presidents Day (3rd Mon of Feb)
            holidays.append(get_nth_weekday(y, 2, 0, 3))
            holidays.append(get_nth_weekday(y, 5, 0, 1))
            
        if y >= 1998:
            holidays.append(get_nth_weekday(y, 1, 0, 3)) # MLK
        if y >= 2022:
            holidays.append(datetime(y, 6, 19)) # Juneteenth

    # Filter out weekends
    res = [h for h in holidays if h.weekday() < 5]
    return np.array(sorted(list(set(res))))

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

# Combined early closings & holidays
# r2py:entity:c
combined = np.concatenate([early_closings, holidays])
print(combined)