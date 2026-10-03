# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar, AbstractHolidayCalendar, Holiday, nearest_workday, MO

def get_nth_weekday(year, month, weekday, nth):
    """Helper to get the nth specific weekday of a month."""
    first_day = datetime(year, month, 1)
    # weekday() in python: 0=Mon, 6=Sun. In R's .nth.of.nday logic, it varies.
    # For US Thanksgiving (4th Thu), Labor Day (1st Mon), Columbus (2nd Mon).
    # we map: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    weekday_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    target_wd = weekday_map[weekday]
    
    first_weekday = first_day.weekday()
    days_to_first = (target_wd - first_weekday + 7) % 7
    target_date = first_day + timedelta(days=days_to_first + (nth - 1) * 7)
    return target_date

def USThanksgivingDay(year):
    # 4th Thursday of November
    return get_nth_weekday(year, 11, 'Thu', 4)

def USLaborDay(year):
    # 1st Monday of September
    return get_nth_weekday(year, 9, 'Mon', 1)

def USColumbusDay(year):
    # 2nd Monday of October
    return get_nth_weekday(year, 10, 'Mon', 2)

def ChristmasDay(year):
    return datetime(year, 12, 25)

def ChristmasEve(year):
    return datetime(year, 12, 24)

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    if isinstance(year, (int, np.integer)):
        years = [int(year)]
    else:
        years = [int(y) for y in year]
    
    results = []
    for y in years:
        # logic for early closes
        # Thanksgiving Friday
        thanks = USThanksgivingDay(y)
        thanks_p1 = thanks + timedelta(days=1)
        
        # July 3rd if July 4th is not Sat/Sun
        indep_day = datetime(y, 7, 4)
        if indep_day.weekday() not in [5, 6]: # Not Sat or Sun
            indep_m1 = datetime(y, 7, 3)
            # July 3rd is early close unless it's a weekend
            if indep_m1.weekday() not in [5, 6]:
                results.append(indep_m1.replace(hour=13, minute=0))
        
        results.append(thanks_p1.replace(hour=13, minute=0))
        
        # Christmas Eve
        xmas = ChristmasDay(y)
        eve = ChristmasEve(y)
        if xmas.weekday() not in [0, 5, 6]: # Not Mon, Sat, Sun
            if eve.weekday() not in [5, 6]:
                results.append(eve.replace(hour=13, minute=0))
                
    # Return as sorted unique list or array to match R output
    res = sorted(list(set(results)))
    if isinstance(year, (int, np.integer)):
        return res[0] if res else None
    return res

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, (int, np.integer)):
        years = [int(year)]
    else:
        years = [int(y) for y in year]
        
    cal = USFederalHolidayCalendar()
    all_holidays = []
    
    for y in years:
        # Standard US Federal Holidays
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31)
        holidays = cal.holidays(start=start, end=end)
        all_holidays.extend(holidays.tolist())
        
        # Good Friday (not in Federal Calendar)
        # Approximation of Easter logic
        a = y % 19
        b = y // 100
        c = y % 100
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
        easter_sunday = datetime(y, month, day)
        good_friday = easter_sunday - timedelta(days=2)
        all_holidays.append(good_friday)

    # NYSE specific rule: If holiday falls on Sunday, Monday is holiday.
    # If holiday falls on Saturday, Friday is often observed.
    # Pandas USFederalHolidayCalendar generally handles observed days.
    
    # Filter out weekends for the final list as per the R logic (posix3$wday == 0 | 6)
    final_holidays = [d for d in all_holidays if d.weekday() not in [5, 6]]
    res = sorted(list(set(final_holidays)))
    
    if isinstance(year, (int, np.integer)):
        return res
    return res

# --- Main execution ---
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# early closings
# r2py:entity:earlyCloseNYSE_1
early_closes = earlyCloseNYSE(range(2022, 2025))
print(early_closes)

# holidays
# r2py:entity:holidayNYSE
holidays = holidayNYSE(range(2022, 2025))
print(holidays)

# early closings & holidays combined
# r2py:entity:c
combined = sorted(list(set(early_closes + holidays)))
print(combined)