# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

# r2py:entity:earlyCloseNYSE
def USThanksgivingDay(year, value="timeDate"):
    # 4th Thursday of November
    first_day = datetime(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    thanksgiving = first_thursday + timedelta(weeks=3)
    if value == "timeDate":
        return thanksgiving
    return thanksgiving.strftime("%Y-%m-%d")

def USLaborDay(year, value="timeDate"):
    # 1st Monday of September
    first_day = datetime(year, 9, 1)
    first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
    if value == "timeDate":
        return first_monday
    return first_monday.strftime("%Y-%m-%d")

def USColumbusDay(year, value="timeDate"):
    # 2nd Monday of October
    first_day = datetime(year, 10, 1)
    first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
    columbus = first_monday + timedelta(weeks=1)
    if value == "timeDate":
        return columbus
    return columbus.strftime("%Y-%m-%d")

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
    easter_sunday = datetime(year, month, day)
    return easter_sunday + timedelta(days=shift)

def USGoodFriday(year, value="timeDate"):
    ans = Easter(year, -2)
    if value == "timeDate":
        return ans
    return ans.strftime("%Y-%m-%d")

def earlyCloseNYSE(year):
    years = np.atleast_1d(year).astype(int)
    all_results = []
    
    for y in years:
        res = []
        if y >= 2012:
            # Thanksgiving Friday
            thanks = USThanksgivingDay(y)
            res.append(thanks + timedelta(days=1))
            
            # July 3rd if July 4th is Sat/Sun
            indep = datetime(y, 7, 4)
            if indep.weekday() >= 5: # Sat=5, Sun=6
                res.append(datetime(y, 7, 3))
            
            # Xmas Eve if Xmas is not Mon, Sat, Sun
            xmas = datetime(y, 12, 25)
            if xmas.weekday() not in [0, 5, 6]:
                res.append(datetime(y, 12, 24))
        
        # Normalize all to 13:00:00 and sort
        normalized = [d.replace(hour=13, minute=0, second=0) for d in res]
        all_results.extend(sorted(normalized))
    
    return np.array(all_results)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    years = np.atleast_1d(year).astype(int)
    holidays = []
    
    for y in years:
        # Standard Holidays
        if y >= 1885:
            holidays.append(datetime(y, 1, 1))
            holidays.append(datetime(y, 7, 4))
            holidays.append(USThanksgivingDay(y))
            holidays.append(datetime(y, 12, 25))
        if y >= 1887:
            holidays.append(USLaborDay(y))
        if y not in [1898, 1906, 1907]:
            holidays.append(USGoodFriday(y))
        if 1896 <= y <= 1953:
            holidays.append(datetime(y, 2, 12))
        if 1909 <= y <= 1953:
            holidays.append(USColumbusDay(y))
        if y == 1918 or y == 1921 or (1934 <= y <= 1953):
            holidays.append(datetime(y, 11, 11))
        if y <= 1968 or y in [1972, 1976, 1980]:
            # Simplified Election Day: first Tuesday after first Monday in Nov
            first_day = datetime(y, 11, 1)
            first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
            election = first_monday + timedelta(days=1)
            holidays.append(election)
        
        if y <= 1970:
            # Washington's Birthday & Decoration Day
            holidays.append(datetime(y, 2, 22))
            # Memorial Day (Last Monday of May)
            last_day = datetime(y, 5, 31)
            mem_day = last_day - timedelta(days=(last_day.weekday() - 0) % 7)
            holidays.append(mem_day)
        else:
            # Presidents' Day (3rd Monday of Feb)
            first_day = datetime(y, 2, 1)
            pres_day = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7) + timedelta(weeks=2)
            holidays.append(pres_day)
            # Memorial Day (Last Monday of May)
            last_day = datetime(y, 5, 31)
            mem_day = last_day - timedelta(days=(last_day.weekday() - 0) % 7)
            holidays.append(mem_day)
            
        if y >= 1998:
            # MLK Day (3rd Monday of Jan)
            first_day = datetime(y, 1, 1)
            mlk = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7) + timedelta(weeks=2)
            holidays.append(mlk)
        if y >= 2022:
            holidays.append(datetime(y, 6, 19))

    # Filter out weekends
    ans = [d for d in holidays if d.weekday() < 5]
    return np.array(sorted(list(set(ans))))

# Translation of the main script
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
early_closings = earlyCloseNYSE(np.arange(2022, 2025))
print(early_closings)

# r2py:entity:holidayNYSE
holidays = holidayNYSE(np.arange(2022, 2025))
print(holidays)

# Combine early closings & holidays
# r2py:entity:c
combined = np.concatenate([early_closings, holidays])
print(combined)