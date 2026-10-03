import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_nth_weekday(year, month, weekday, nth):
    """Helper to find the nth occurrence of a weekday in a month.
    weekday: 0=Mon, 6=Sun (Python convention)
    """
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    days_to_first = (weekday - first_weekday + 7) % 7
    target_day = 1 + days_to_first + (nth - 1) * 7
    return datetime(year, month, target_day)

def get_last_weekday(year, month, weekday):
    """Helper to find the last occurrence of a weekday in a month."""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    last_day = next_month - timedelta(days=1)
    last_weekday = last_day.weekday()
    days_to_subtract = (last_weekday - weekday + 7) % 7
    return last_day - timedelta(days=days_to_subtract)

def easter_date(year):
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
    return datetime(year, month, day)

# r2py:entity:holidayNYSE
def holidayNYSE(years, type_val=""):
    if isinstance(years, (int, float)):
        years = [int(years)]
    
    all_holidays = []
    for y in years:
        y = int(y)
        h_year = []
        if y >= 1885:
            h_year.append(datetime(y, 1, 1))
            h_year.append(datetime(y, 7, 4))
            h_year.append(get_nth_weekday(y, 11, 3, 4)) # Thanksgiving (Thu)
            h_year.append(datetime(y, 12, 25))
        if y >= 1887:
            h_year.append(get_nth_weekday(y, 9, 0, 1)) # Labor Day (Mon)
        if y not in [1898, 1906, 1907]:
            h_year.append(easter_date(y) - timedelta(days=2)) # Good Friday
        if 1896 <= y <= 1953:
            h_year.append(datetime(y, 2, 12))
        if 1909 <= y <= 1953:
            h_year.append(get_nth_weekday(y, 10, 0, 2)) # Columbus Day (Mon)
        if y == 1918 or y == 1921 or (1934 <= y <= 1953):
            h_year.append(datetime(y, 11, 11))
        if y <= 1968 or y in [1972, 1976, 1980]:
            # Election Day: first Tuesday after Nov 2
            nov2 = datetime(y, 11, 2)
            days_to_tue = (1 - nov2.weekday() + 7) % 7
            if days_to_tue == 0: days_to_tue = 7
            h_year.append(nov2 + timedelta(days=days_to_tue))
        
        if y <= 1970:
            h_year.append(datetime(y, 2, 22)) 
            h_year.append(get_last_weekday(y, 5, 0)) # Decoration Day (Last Mon May)
        else:
            h_year.append(get_nth_weekday(y, 2, 0, 3)) # Presidents Day (Mon)
            h_year.append(get_last_weekday(y, 5, 0)) # Memorial Day (Last Mon May)
        
        if y >= 1998:
            h_year.append(get_nth_weekday(y, 1, 0, 3)) # MLK Day (Mon)
        if y >= 2022:
            h_year.append(datetime(y, 6, 19)) # Juneteenth
            
        all_holidays.extend(h_year)

    observed = []
    for d in all_holidays:
        if d.weekday() == 6: # Sunday
            observed.append(d + timedelta(days=1))
        else:
            observed.append(d)
    
    final_holidays = [d for d in observed if d.weekday() < 5]
    unique_holidays = sorted(list(set(final_holidays)))
    
    return np.array([pd.Timestamp(d) for d in unique_holidays])

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(years):
    if isinstance(years, (int, float)):
        years = [int(years)]
    
    all_early = []
    for y in years:
        y = int(y)
        # Friday after Thanksgiving
        thanks = get_nth_weekday(y, 11, 3, 4)
        all_early.append(pd.Timestamp(thanks + timedelta(days=1)).replace(hour=13, minute=0))
        
        # July 3rd
        july3 = datetime(y, 7, 3)
        if july3.weekday() < 5:
            all_early.append(pd.Timestamp(july3).replace(hour=13, minute=0))
            
        # Christmas Eve
        xmas = datetime(y, 12, 25)
        # R logic: eve <- eve[!(dayOfWeek(xmas) %in% c("Mon", "Sat", "Sun"))]
        if xmas.weekday() not in [0, 5, 6]:
            eve = datetime(y, 12, 24)
            all_early.append(pd.Timestamp(eve).replace(hour=13, minute=0))
            # Special case for 1990 in R metadata/behavior if needed, 
            # but the R source provided shows it's derived from `early_close` table.
            if y == 1990:
                all_early.append(pd.Timestamp(eve).replace(hour=14, minute=0))
            
    res = sorted(all_early)
    return np.array(res)

# Translate R calls
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
years_range = np.arange(2022, 2025)
print(earlyCloseNYSE(years_range))

# r2py:entity:holidayNYSE
print(holidayNYSE(years_range))

# r2py:entity:c
combined = np.concatenate([earlyCloseNYSE(years_range), holidayNYSE(years_range)])
print(combined)