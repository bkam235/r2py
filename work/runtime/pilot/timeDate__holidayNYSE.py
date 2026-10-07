import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import calendar
from dateutil.easter import easter

# Mock for the special closings dataset used by timeDate
NYSE_SPECIAL_CLOSINGS = [
    "1987-10-19", "2001-09-11", "2001-09-12", "2020-03-13"
]

def get_n_th_weekday(year, month, n, weekday):
    """n-th occurrence of weekday (0=Mon, 6=Sun) in year/month."""
    try:
        first_day = date(year, month, 1).weekday()
    except ValueError:
        return None
    first_occurrence = (weekday - first_day) % 7 + 1
    day = first_occurrence + (n - 1) * 7
    if day > calendar.monthrange(year, month)[1]:
        return None
    return date(year, month, day)

def USNewYearsDay(y): return date(y, 1, 1)
def USIndependenceDay(y): return date(y, 7, 4)
def USChristmasDay(y): return date(y, 12, 25)
def USThanksgivingDay(y): return get_n_th_weekday(y, 11, 4, 3)
def USLaborDay(y): return get_n_th_weekday(y, 9, 1, 0)
def USGoodFriday(y): return easter(y) - timedelta(days=2)
def USLincolnsBirthday(y): return date(y, 2, 12)
def USColumbusDay(y): return get_n_th_weekday(y, 10, 2, 0)
def USVeteransDay(y): return date(y, 11, 11)
def USElectionDay(y): 
    first_mon = get_n_th_weekday(y, 11, 1, 0)
    return first_mon + timedelta(days=1) if first_mon else None
def USWashingtonsBirthday(y): return date(y, 2, 22)
def USDecorationMemorialDay(y):
    last_day = calendar.monthrange(y, 5)[1]
    d = date(y, 5, last_day)
    return d - timedelta(days=(d.weekday() - 0) % 7)
def USPresidentsDay(y): return get_n_th_weekday(y, 2, 3, 0)
def USMemorialDay(y): return USDecorationMemorialDay(y)
def USMLKingsBirthday(y): return get_n_th_weekday(y, 1, 3, 0)
def USJuneteenthNationalIndependenceDay(y): return date(y, 6, 19)

def r_holidayNYSE(year=None, type=None, *args, **kwargs):
    if year is None:
        # In a real scenario, getRmetricsOptions("currentYear") would be used.
        year = np.array([datetime.now().year])
    
    year_arr = np.atleast_1d(year)
    if type is None:
        type = ""
    
    ans_dates = []
    
    if type == "" or type == "standard":
        for y in year_arr:
            try:
                y_int = int(y)
                if y_int < 1: continue 
                
                current_holidays = []
                if y_int >= 1885:
                    current_holidays.extend([USNewYearsDay(y_int), USIndependenceDay(y_int), USThanksgivingDay(y_int), USChristmasDay(y_int)])
                if y_int >= 1887:
                    current_holidays.append(USLaborDay(y_int))
                if y_int not in [1898, 1906, 1907]:
                    current_holidays.append(USGoodFriday(y_int))
                if 1896 <= y_int <= 1953:
                    current_holidays.append(USLincolnsBirthday(y_int))
                if 1909 <= y_int <= 1953:
                    current_holidays.append(USColumbusDay(y_int))
                if y_int == 1918 or y_int == 1921 or (1934 <= y_int <= 1953):
                    current_holidays.append(USVeteransDay(y_int))
                if y_int <= 1968 or y_int in [1972, 1976, 1980]:
                    current_holidays.append(USElectionDay(y_int))
                
                if y_int <= 1970:
                    current_holidays.extend([USWashingtonsBirthday(y_int), USDecorationMemorialDay(y_int)])
                else:
                    current_holidays.extend([USPresidentsDay(y_int), USMemorialDay(y_int)])
                
                if y_int >= 1998:
                    current_holidays.append(USMLKingsBirthday(y_int))
                if y_int >= 2022:
                    current_holidays.append(USJuneteenthNationalIndependenceDay(y_int))
                
                ans_dates.extend([d for d in current_holidays if d is not None])
            except (ValueError, OverflowError):
                continue

        unique_dates = sorted(list(set([d if isinstance(d, date) else d.date() for d in ans_dates])))
        
        processed_dates = []
        for d in unique_dates:
            dt = d
            if dt.weekday() == 6: # Sunday
                dt += timedelta(days=1)
            processed_dates.append(dt)
        
        final_dates = []
        for dt in processed_dates:
            if dt.weekday() == 5 and dt >= date(1959, 7, 3):
                dt -= timedelta(days=1)
            final_dates.append(dt)
        
        ans_dates = final_dates

    if type == "" or type == "special":
        sp_dates = []
        for s in NYSE_SPECIAL_CLOSINGS:
            sd = datetime.strptime(s, "%Y-%m-%d").date()
            if any(int(y) == sd.year for y in year_arr if np.isscalar(y) and not np.isnan(y) or (not np.isscalar(y) and not np.isnan(y).any())):
                sp_dates.append(sd)
        
        if not ans_dates:
            ans_dates = sp_dates
        else:
            ans_dates.extend(sp_dates)

    unique_ans = sorted(list(set([d if isinstance(d, date) else d.date() for d in ans_dates])))
    final_filtered = [d for d in unique_ans if d.weekday() != 5 and d.weekday() != 6]
    
    if not final_filtered:
        if type == "special" and not any(int(y) < 0 for y in year_arr if np.isscalar(y) and not np.isnan(y)):
            return {"Data": [], "format": "%Y-%m-%d", "FinCenter": "NewYork"}
        return {"Data": None, "format": "", "FinCenter": "NewYork"}

    res_data = []
    for d in final_filtered:
        # Accurate NYC DST: transitions usually early March and early November.
        # 2024 example: Nov 28 is after DST ends (Nov 3), so should be T05.
        # The R results show that Thanksgiving (Nov) is T05:00:00.
        # DST usually ends first Sunday of Nov.
        
        # Heuristic for NYSE T04 (DST) vs T05 (STD):
        # DST starts 2nd Sunday March, ends 1st Sunday November.
        # Calculate dates for current year's DST transition:
        march_dst = get_n_th_weekday(d.year, 3, 2, 6)
        nov_dst = get_n_th_weekday(d.year, 11, 1, 6)
        
        if march_dst <= d < nov_dst:
            res_data.append(d.strftime("%Y-%m-%dT04:00:00"))
        else:
            res_data.append(d.strftime("%Y-%m-%dT05:00:00"))

    return {"Data": res_data, "format": "%Y-%m-%d", "FinCenter": "NewYork"}
