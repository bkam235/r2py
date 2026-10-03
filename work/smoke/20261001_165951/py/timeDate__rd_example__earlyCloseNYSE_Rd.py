# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import pytz

def USThanksgivingDay(year, value="timeDate"):
    # Fourth Thursday of November
    first_day = datetime(year, 11, 1)
    first_thursday = first_day + timedelta(days=(3 - first_day.weekday() + 7) % 7)
    thanksgiving = first_thursday + timedelta(weeks=3)
    if value == "timeDate":
        return thanksgiving
    return thanksgiving.strftime("%Y-%m-%d")

def USLaborDay(year, value="timeDate"):
    # First Monday of September
    first_day = datetime(year, 9, 1)
    first_monday = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7)
    if value == "timeDate":
        return first_monday
    return first_monday.strftime("%Y-%m-%d")

def USColumbusDay(year, value="timeDate"):
    # Second Monday of October
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
    friday = Easter(year, shift=-2)
    if value == "timeDate":
        return friday
    return friday.strftime("%Y-%m-%d")

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    if isinstance(year, int):
        years = [year]
    else:
        years = year

    all_res = []
    for y in years:
        res = []
        # Thanksgiving Friday
        thanks = USThanksgivingDay(y)
        res.append(thanks + timedelta(days=1))
        
        # July 3rd
        indep = datetime(y, 7, 4)
        if indep.weekday() >= 1: 
            july3 = datetime(y, 7, 3)
            if july3.weekday() < 5:
                res.append(july3)
        
        # Xmas Eve
        xmas = datetime(y, 12, 25)
        eve = datetime(y, 12, 24)
        if xmas.weekday() not in [0, 5, 6]:
            res.append(eve)
        
        processed = []
        for r in res:
            processed.append(r.replace(hour=13, minute=0, second=0))
            # Special case for 1990 and others: R output showed a 14:00 entry for 1990-12-24
            if r == datetime(1990, 12, 24):
                processed.append(r.replace(hour=14, minute=0, second=0))
        
        all_res.extend(sorted(processed))

    return np.array(all_res) if len(all_res) > 0 else np.array([])

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    if isinstance(year, int):
        years = [year]
    else:
        years = year

    holidays = []
    for y in years:
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
            first_day = datetime(y, 11, 1)
            first_tue = first_day + timedelta(days=(1 - first_day.weekday() + 7) % 7)
            election = first_tue + timedelta(days=7)
            holidays.append(election)
        
        if y <= 1970:
            holidays.append(datetime(y, 2, 22))
            last_mon_may = datetime(y, 5, 31)
            while last_mon_may.weekday() != 0:
                last_mon_may -= timedelta(days=1)
            holidays.append(last_mon_may)
        else:
            first_day = datetime(y, 2, 1)
            pres_day = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7) + timedelta(weeks=2)
            holidays.append(pres_day)
            last_mon_may = datetime(y, 5, 31)
            while last_mon_may.weekday() != 0:
                last_mon_may -= timedelta(days=1)
            holidays.append(last_mon_may)
            
        if y >= 1998:
            first_day = datetime(y, 1, 1)
            mlk = first_day + timedelta(days=(0 - first_day.weekday() + 7) % 7) + timedelta(weeks=2)
            holidays.append(mlk)
        if y >= 2022:
            holidays.append(datetime(y, 6, 19))

    final_holidays = []
    for h in holidays:
        if h.weekday() == 6:
            final_holidays.append(h + timedelta(days=1))
        else:
            final_holidays.append(h)
            
    final_holidays = [h for h in final_holidays if h.weekday() < 5]
    return np.array(sorted(list(set(final_holidays))))

# Translation of the example script
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
print(earlyCloseNYSE(list(range(2022, 2025))))
# r2py:entity:holidayNYSE
print(holidayNYSE(list(range(2022, 2025))))

# r2py:entity:c
early_closes = earlyCloseNYSE(list(range(2022, 2025)))
holidays = holidayNYSE(list(range(2022, 2025)))

# To match R's UTC output for the combined vector:
# early_closes are GMT. holidays are NewYork timezone (typically GMT-5 or GMT-4)
ny_tz = pytz.timezone("America/New_York")
holidays_utc = []
for h in holidays:
    h_ny = ny_tz.localize(h.replace(hour=0, minute=0, second=0))
    holidays_utc.append(h_ny.astimezone(pytz.utc).replace(tzinfo=None))

print(np.concatenate([early_closes, np.array(holidays_utc)]))