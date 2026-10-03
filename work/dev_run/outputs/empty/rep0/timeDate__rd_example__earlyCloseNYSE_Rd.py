import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def timeDate(charvec, format_val=None, zone="", FinCenter=""):
    if charvec is None:
        return pd.NaT
    if isinstance(charvec, (list, np.ndarray)):
        return np.array([_parse_timeDate(x) for x in charvec])
    return _parse_timeDate(charvec)

def _parse_timeDate(x):
    if pd.isna(x):
        return pd.NaT
    s = str(x)
    try:
        if len(s) == 8 and s.isdigit():
            return datetime.strptime(s, "%Y%m%d")
        if " " in s:
            return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return pd.NaT

def dayOfWeek(dt):
    if isinstance(dt, np.ndarray):
        return np.array([_day_of_week(x) for x in dt])
    return _day_of_week(dt)

def _day_of_week(dt):
    if pd.isna(dt):
        return np.nan
    return dt.strftime("%a")

def _nth_of_nday(year, month, weekday_r, n):
    # weekday_r: R uses 0=Sun, 1=Mon, ..., 6=Sat
    # Python weekday(): 0=Mon, ..., 6=Sun
    py_weekday = (weekday_r - 1) % 7
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    days_to_first = (py_weekday - first_weekday + 7) % 7
    target_date = first_day + timedelta(days=days_to_first + (n - 1) * 7)
    return target_date.strftime("%Y-%m-%d")

def USThanksgivingDay(year, value="timeDate"):
    ans = _nth_of_nday(year, 11, 4, 4) # 4th Thursday
    return timeDate(ans) if value == "timeDate" else ans

def USLaborDay(year, value="timeDate"):
    ans = _nth_of_nday(year, 9, 1, 1) # 1st Monday
    return timeDate(ans) if value == "timeDate" else ans

def USColumbusDay(year, value="timeDate"):
    ans = _nth_of_nday(year, 10, 1, 2) # 2nd Monday
    return timeDate(ans) if value == "timeDate" else ans

def USMLKingsBirthday(year, value="timeDate"):
    ans = _nth_of_nday(year, 1, 1, 3) # 3rd Monday
    return timeDate(ans) if value == "timeDate" else ans

def USPresidentsDay(year, value="timeDate"):
    ans = _nth_of_nday(year, 2, 1, 3) # 3rd Monday
    return timeDate(ans) if value == "timeDate" else ans

def USMemorialDay(year, value="timeDate"):
    # Last Monday of May
    last_day = datetime(year, 5, 31)
    days_back = (last_day.weekday() - 0 + 7) % 7
    ans = last_day - timedelta(days=days_back)
    ans_str = ans.strftime("%Y-%m-%d")
    return timeDate(ans_str) if value == "timeDate" else ans_str

def USGoodFriday(year, value="timeDate"):
    # Easter calculation
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
    good_friday = easter_sunday - timedelta(days=2)
    ans_str = good_friday.strftime("%Y-%m-%d")
    return timeDate(ans_str) if value == "timeDate" else ans_str

def ChristmasDay(year, value="timeDate"):
    ans = f"{year}-12-25"
    return timeDate(ans) if value == "timeDate" else ans

def ChristmasEve(year, value="timeDate"):
    ans = f"{year}-12-24"
    return timeDate(ans) if value == "timeDate" else ans

def USNewYearsDay(year, value="timeDate"):
    ans = f"{year}-01-01"
    return timeDate(ans) if value == "timeDate" else ans

def USIndependenceDay(year, value="timeDate"):
    ans = f"{year}-07-04"
    return timeDate(ans) if value == "timeDate" else ans

def USChristmasDay(year, value="timeDate"):
    ans = f"{year}-12-25"
    return timeDate(ans) if value == "timeDate" else ans

def USLincolnsBirthday(year, value="timeDate"):
    ans = f"{year}-02-12"
    return timeDate(ans) if value == "timeDate" else ans

def USVeteransDay(year, value="timeDate"):
    ans = f"{year}-11-11"
    return timeDate(ans) if value == "timeDate" else ans

def USJuneteenthNationalIndependenceDay(year, value="timeDate"):
    ans = f"{year}-06-19"
    return timeDate(ans) if value == "timeDate" else ans

# r2py:entity:earlyCloseNYSE
def earlyCloseNYSE(year):
    years = np.arange(year[0], year[-1] + 1) if isinstance(year, (list, np.ndarray, range)) else [year]
    all_results = []
    
    for y in years:
        # Thanksgiving Friday
        thanks = USThanksgivingDay(y)
        thanks_fri = thanks + timedelta(days=1)
        all_results.append(thanks_fri.replace(hour=13, minute=0))
        
        # July 3rd (if July 4th is not Sat/Sun, but NYSE often closes early on 3rd if 4th is weekend)
        # The R source says: indep_m1 <- timeDate(paste0(year, "-07-03", " ", "13:00:00"))
        # then filters dayOfWeek(indep_m1) %in% c("Sat", "Sun")
        indep_m1 = datetime(y, 7, 3, 13, 0, 0)
        if dayOfWeek(indep_m1) not in ["Sat", "Sun"]:
            all_results.append(indep_m1)
        
        # Christmas Eve
        xmas = ChristmasDay(y)
        eve = ChristmasEve(y)
        if dayOfWeek(xmas) not in ["Mon", "Sat", "Sun"]:
            all_results.append(eve.replace(hour=13, minute=0))
            
    # The 1990 output in R suggests there's a specific case for 12-24 that results in both 13:00 and 14:00?
    # Actually, the R output says [1990-12-24 13:00:00] and [1990-12-24 14:00:00].
    # We'll stick to the formula provided in the R function source which uses .reset_time(res, "13:00:00").
    # But since the output has 14:00, there might be a data table. Since we don't have it, 
    # we will just ensure the logic matches the function provided.
    
    if not all_results:
        return np.array([])
    
    res = sorted(all_results)
    return np.array(res)

# r2py:entity:holidayNYSE
def holidayNYSE(year, type_val=""):
    years = np.arange(year[0], year[-1] + 1) if isinstance(year, (list, np.ndarray, range)) else [year]
    holidays = []
    
    for y in years:
        h_year = []
        if y >= 1885:
            h_year.append(USNewYearsDay(y, value=""))
            h_year.append(USIndependenceDay(y, value=""))
            h_year.append(USThanksgivingDay(y, value=""))
            h_year.append(USChristmasDay(y, value=""))
        if y >= 1887:
            h_year.append(USLaborDay(y, value=""))
        if y not in [1898, 1906, 1907]:
            h_year.append(USGoodFriday(y, value=""))
        if 1896 <= y <= 1953:
            h_year.append(USLincolnsBirthday(y, value=""))
        if 1909 <= y <= 1953:
            h_year.append(USColumbusDay(y, value=""))
        if y in [1918, 1921] or (1934 <= y <= 1953):
            h_year.append(USVeteransDay(y, value=""))
        if y <= 1970:
            h_year.append(f"{y}-02-12")
            h_year.append(USMemorialDay(y, value=""))
        else:
            h_year.append(USPresidentsDay(y, value=""))
            h_year.append(USMemorialDay(y, value=""))
        if y >= 1998:
            h_year.append(USMLKingsBirthday(y, value=""))
        if y >= 2022:
            h_year.append(USJuneteenthNationalIndependenceDay(y, value=""))
            
        holidays.extend(h_year)

    res_dates = []
    for h in sorted(list(set(holidays))):
        dt = timeDate(h)
        # Observed holiday logic: if Sunday, move to Monday. If Saturday, move to Friday.
        if dayOfWeek(dt) == "Sun":
            dt += timedelta(days=1)
        elif dayOfWeek(dt) == "Sat":
            dt -= timedelta(days=1)
        res_dates.append(dt)
    
    # Final filter: Remove weekends
    res_dates = [d for d in res_dates if dayOfWeek(d) not in ["Sat", "Sun"]]
    return np.array(sorted(res_dates))

# Main execution
# r2py:entity:earlyCloseNYSE
print(earlyCloseNYSE(1990))
# r2py:entity:earlyCloseNYSE_1
print(earlyCloseNYSE(np.arange(2022, 2025)))
# r2py:entity:holidayNYSE
print(holidayNYSE(np.arange(2022, 2025)))
# r2py:entity:c
combined = np.concatenate([earlyCloseNYSE(np.arange(2022, 2025)), holidayNYSE(np.arange(2022, 2025))])
print(combined)