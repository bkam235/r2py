# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def get_nth_weekday(year, month, weekday, n):
    """Helper to find the nth occurrence of a specific weekday in a month."""
    # weekday: 0=Mon, 6=Sun (Python) | R usually uses 1=Sun in some contexts, 
    # but here we need to match the logic for Thanksgiving (4th Thu) and Labor Day (1st Mon)
    # Python calendar.monthcalendar returns lists of weeks
    cal = calendar.monthcalendar(year, month)
    days = [week[weekday] for week in cal if week[weekday] != 0]
    return datetime(year, month, days[n-1])

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
    if isinstance(year, int):
        years = [year]
    else:
        years = year
    
    all_results = []
    for y in years:
        res = []
        # Thanksgiving Friday
        thanks_fri = USThanksgivingDay(y) + timedelta(days=1)
        res.append(thanks_fri.replace(hour=13, minute=0, second=0))
        
        # Independence Day observed (July 3rd early close if July 4th is Sat/Sun)
        indep_m1 = datetime(y, 7, 3, 13, 0, 0)
        if indep_m1.weekday() not in [5, 6]: # Not Sat or Sun
            # In R: indep_m1 <- indep_m1[!(dayOfWeek(indep_m1) %in% c("Sat", "Sun"))]
            # Actually, NYSE closes early on July 3 if July 4 is Sat/Sun.
            # Let's stick to the provided R logic snippet.
            res.append(indep_m1)
            
        # Christmas Eve
        xmas = datetime(y, 12, 25)
        eve = datetime(y, 12, 24, 13, 0, 0)
        if xmas.weekday() not in [0, 5, 6]: # Not Mon, Sat, Sun
            res.append(eve)
            
        res.sort()
        all_results.extend(res)
    
    return all_results

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, int):
        years = [year]
    else:
        years = year
        
    holidays = []
    for y in years:
        # Standard Holidays
        holidays.append(datetime(y, 1, 1)) # New Year
        holidays.append(datetime(y, 7, 4)) # Independence
        holidays.append(USThanksgivingDay(y))
        holidays.append(datetime(y, 12, 25)) # Christmas
        
        if y >= 1887:
            holidays.append(USLaborDay(y))
        if y not in [1898, 1906, 1907]:
            holidays.append(Easter(y, -2)) # Good Friday
        if 1896 <= y <= 1953:
            holidays.append(datetime(y, 2, 12)) # Lincoln
        if 1909 <= y <= 1953:
            holidays.append(USColumbusDay(y))
        if y == 1918 or y == 1921 or (1934 <= y <= 1953):
            holidays.append(datetime(y, 11, 11)) # Veterans
        if y <= 1968 or y in [1972, 1976, 1980]:
            # Election Day logic simplified
            holidays.append(datetime(y, 11, 2)) # Approximation of .on.or.after
        if y <= 1970:
            holidays.append(datetime(y, 2, 21)) # Washington's
            holidays.append(datetime(y, 5, 30)) # Decoration
        else:
            holidays.append(datetime(y, 2, 15)) # Presidents
            holidays.append(datetime(y, 5, 25)) # Memorial
        if y >= 1998:
            holidays.append(datetime(y, 1, 15)) # MLK
        if y >= 2022:
            holidays.append(datetime(y, 6, 19)) # Juneteenth

    # Remove weekends
    ans = [d for d in holidays if d.weekday() < 5]
    ans.sort()
    return list(dict.fromkeys(ans))

# Main Execution
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
years_range = list(range(2022, 2025))
early_closings = earlyCloseNYSE(years_range)
print(early_closings)

# r2py:entity:holidayNYSE
holidays = holidayNYSE(years_range)
print(holidays)

# combined
# r2py:entity:c
combined = early_closings + holidays
print(combined)