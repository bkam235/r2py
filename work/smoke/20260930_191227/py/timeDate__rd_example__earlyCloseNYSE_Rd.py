# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def timeDate(charvec, format_val=None, zone="", FinCenter="", **kwargs):
    if charvec is None or (isinstance(charvec, (list, np.ndarray)) and len(charvec) == 0):
        return pd.DatetimeIndex([])
    if isinstance(charvec, (list, np.ndarray)):
        return pd.to_datetime(charvec)
    return pd.to_datetime(charvec)

def _nth_of_nday(year, month, day, n):
    first_day = datetime(year, month, 1)
    target_weekday = day - 1 
    first_weekday = first_day.weekday()
    days_to_first = (target_weekday - first_weekday + 7) % 7
    first_occurrence = first_day + timedelta(days=days_to_first)
    nth_occurrence = first_occurrence + timedelta(weeks=n-1)
    return nth_occurrence.strftime('%Y-%m-%d')

def USThanksgivingDay(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [_nth_of_nday(y, 11, 4, 4) for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    
    if value == "timeDate":
        return timeDate(res)
    return res

def ChristmasDay(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [f"{y}-12-25" for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    
    if value == "timeDate":
        return timeDate(res)
    return res

def ChristmasEve(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [f"{y}-12-24" for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    
    if value == "timeDate":
        return timeDate(res)
    return res

def _reset_time(res, time_str):
    if len(res) == 0:
        return res
    dates = pd.to_datetime(res)
    res_fixed = [d.strftime('%Y-%m-%d') + ' ' + time_str for d in dates]
    return pd.to_datetime(res_fixed)

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    years = np.atleast_1d(year)
    all_res = []
    
    for y in years:
        y_res = []
        # Thanksgiving + 1 day (Friday after)
        thanks = pd.to_datetime(USThanksgivingDay(y))
        y_res.append(thanks + timedelta(days=1))
        
        # July 3rd if not Sat/Sun
        indep_m1 = pd.to_datetime(f"{y}-07-03")
        if indep_m1.weekday() < 5:
            y_res.append(indep_m1)
        
        # Xmas Eve if Xmas is not Mon, Sat, Sun
        xmas = pd.to_datetime(ChristmasDay(y))
        eve = pd.to_datetime(ChristmasEve(y))
        if xmas.weekday() not in [0, 5, 6]:
            y_res.append(eve)
        
        y_res = _reset_time(y_res, "13:00:00")
        y_res = np.sort(y_res)
        all_res.extend(y_res)
    
    # The R source mentions 'early_close' which is a package internal data frame
    # Since we don't have it, we return the computed results
    return pd.DatetimeIndex(all_res)

def USNewYearsDay(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [f"{y}-01-01" for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    return timeDate(res) if value == "timeDate" else res

def USIndependenceDay(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [f"{y}-07-04" for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    return timeDate(res) if value == "timeDate" else res

def USLaborDay(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [_nth_of_nday(y, 9, 1, 1) for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    return timeDate(res) if value == "timeDate" else res

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
    easter_date = datetime(year, month, day) + timedelta(days=shift)
    return easter_date.strftime('%Y-%m-%d')

def USGoodFriday(year, value="timeDate", **kwargs):
    years = np.atleast_1d(year)
    res = [Easter(y, -2) for y in years]
    if not isinstance(year, (list, np.ndarray)):
        res = res[0]
    return timeDate(res) if value == "timeDate" else res

def USChristmasDay(year, value="timeDate", **kwargs):
    return ChristmasDay(year, value)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    years = np.atleast_1d(year)
    holidays = []
    
    if type_val == "" or type_val == "standard":
        for y in years:
            if y >= 1885:
                holidays.append(USNewYearsDay(y, value=""))
                holidays.append(USIndependenceDay(y, value=""))
                holidays.append(_nth_of_nday(y, 11, 4, 4))
                holidays.append(f"{y}-12-25")
            if y >= 1887:
                holidays.append(_nth_of_nday(y, 9, 1, 1))
            if y not in [1898, 1906, 1907]:
                holidays.append(Easter(y, -2))
            if 1896 <= y <= 1953:
                holidays.append(f"{y}-02-12")
            if 1909 <= y <= 1953:
                holidays.append(_nth_of_nday(y, 10, 1, 2))
            if y == 1918 or y == 1921 or (1934 <= y <= 1953):
                holidays.append(f"{y}-11-11")
            if y <= 1968 or y in [1972, 1976, 1980]:
                # Simplified Election Day logic (R source truncated, using common placeholder)
                holidays.append(f"{y}-11-02") 
            if y <= 1970:
                holidays.append(f"{y}-02-22")
                holidays.append(_nth_of_nday(y, 5, 1, 1))
            else:
                holidays.append(_nth_of_nday(y, 2, 1, 3))
                holidays.append(_nth_of_nday(y, 5, 1, 1))
            if y >= 1998:
                holidays.append(_nth_of_nday(y, 1, 1, 3))
            if y >= 2022:
                holidays.append(f"{y}-06-19")

        ans = pd.to_datetime(sorted(holidays))
        # In R, holidayNYSE filters weekends AFTER converting to NewYork time
        # Python's pd.to_datetime is naive by default. 
        # We filter Saturdays (5) and Sundays (6)
        ans = ans[~ans.weekday.isin([5, 6])]
    else:
        ans = pd.DatetimeIndex([])

    return ans

# Main script execution
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))

# r2py:entity:earlyCloseNYSE_1
print(earlyCloseNYSE(np.arange(2022, 2025)))

# r2py:entity:holidayNYSE
print(holidayNYSE(np.arange(2022, 2025)))

# r2py:entity:c
early_closes = earlyCloseNYSE(np.arange(2022, 2025))
holidays = holidayNYSE(np.arange(2022, 2025))
combined = np.concatenate([early_closes, holidays])
print(combined)