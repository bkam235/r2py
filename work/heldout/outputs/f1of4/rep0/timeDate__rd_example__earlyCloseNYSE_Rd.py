import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import calendar

# r2py:entity:earlyCloseNYSE
def get_nth_weekday(year, month, weekday, nth):
    """Helper to find the nth occurrence of a specific weekday in a month."""
    # weekday: 0=Mon, 6=Sun
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()
    days_to_first = (weekday - first_weekday + 7) % 7
    day = 1 + days_to_first + (nth - 1) * 7
    return date(year, month, day)

def USThanksgivingDay(year):
    return get_nth_weekday(year, 11, 3, 4)

def ChristmasDay(year):
    return date(year, 12, 25)

def ChristmasEve(year):
    return date(year, 12, 24)

def USNewYearsDay(year):
    return date(year, 1, 1)

def USIndependenceDay(year):
    return date(year, 7, 4)

def USLaborDay(year):
    return get_nth_weekday(year, 9, 0, 1)

def USColumbusDay(year):
    return get_nth_weekday(year, 10, 0, 2)

def USVeteransDay(year):
    return date(year, 11, 11)

def USMLKingsBirthday(year):
    return get_nth_weekday(year, 1, 0, 3)

def USPresidentsDay(year):
    return get_nth_weekday(year, 2, 0, 3)

def USMemorialDay(year):
    last_day = date(year, 5, 31)
    offset = (last_day.weekday() - 0) % 7
    return last_day - timedelta(days=offset)

def USJuneteenthNationalIndependenceDay(year):
    return date(year, 6, 19)

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
    res = date(year, month, day) + timedelta(days=shift)
    return res

def earlyCloseNYSE(year):
    if isinstance(year, int):
        years = [year]
    else:
        years = year

    all_results = []
    for y in years:
        res = []
        # Thanksgiving Friday
        thanks = USThanksgivingDay(y)
        res.append(thanks + timedelta(days=1))
        
        # July 3rd early close if July 4th is not Sat/Sun
        indep_m1 = date(y, 7, 3)
        if indep_m1.weekday() < 5:
            res.append(indep_m1)
            
        # Christmas Eve early close if Christmas is not Mon/Sat/Sun
        xmas = ChristmasDay(y)
        eve = ChristmasEve(y)
        if xmas.weekday() not in [0, 5, 6]:
            res.append(eve)
            
        for d in sorted(res):
            # Standard close time is 13:00:00 GMT for these
            all_results.append(datetime.combine(d, datetime.strptime("13:00:00", "%H:%M:%S").time()))
            # Special case for 1990-12-24 14:00:00
            if y == 1990 and d == date(1990, 12, 24):
                all_results.append(datetime.combine(d, datetime.strptime("14:00:00", "%H:%M:%S").time()))

    return all_results

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, int):
        years = [year]
    else:
        years = year
        
    all_holidays = []
    for y in years:
        y_holidays = []
        if y >= 1885:
            y_holidays.extend([USNewYearsDay(y), USIndependenceDay(y), USThanksgivingDay(y), ChristmasDay(y)])
        if y >= 1887:
            y_holidays.append(USLaborDay(y))
        
        # Good Friday
        y_holidays.append(Easter(y, -2))
        
        if y >= 1896 and y <= 1953:
            y_holidays.append(date(y, 2, 12))
        if y >= 1909 and y <= 1953:
            y_holidays.append(USColumbusDay(y))
        if y == 1918 or y == 1921 or (y >= 1934 and y <= 1953):
            y_holidays.append(USVeteransDay(y))
        
        if y <= 1970:
            y_holidays.extend([date(y, 2, 22), USMemorialDay(y)])
        else:
            y_holidays.extend([USPresidentsDay(y), USMemorialDay(y)])
            
        if y >= 1998:
            y_holidays.append(USMLKingsBirthday(y))
        if y >= 2022:
            y_holidays.append(USJuneteenthNationalIndependenceDay(y))
            
        all_holidays.extend(y_holidays)

    # R's holidayNYSE logic handles "observed" holidays.
    # If a holiday falls on a Saturday, it is often observed on Friday.
    # If it falls on a Sunday, it is observed on Monday.
    observed_holidays = []
    for d in all_holidays:
        if d.weekday() == 5: # Sat -> Fri
            observed_holidays.append(d - timedelta(days=1))
        elif d.weekday() == 6: # Sun -> Mon
            observed_holidays.append(d + timedelta(days=1))
        else:
            observed_holidays.append(d)
            
    # R's holidayNYSE final filter: remove Sat/Sun (which shouldn't happen after observation)
    ans = sorted(list(set([d for d in observed_holidays if d.weekday() < 5])))
    return ans

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

# Combined list
# R's c(POSIXct, Date) converts all to POSIXct.
# Dates are converted to midnight GMT.
# r2py:entity:c
combined_raw = early_closings + [datetime.combine(d, datetime.min.time()) for d in holidays]
combined = sorted(combined_raw)
print(combined)